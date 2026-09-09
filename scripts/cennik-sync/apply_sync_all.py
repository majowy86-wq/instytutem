#!/usr/bin/env python3
"""JEDYNY skrypt do uruchamiania od teraz przy „zsynchronizuj ceny" — czyta AKTUALNY
stan zunifikowanego arkusza Google (read_sheet.py) i aplikuje go do wszystkich plików
(cennik/index.html + podstrony zabiegów, gdzie istnieją).

Klasyfikacja zabiegu (prosta/zagnieżdżona) wynika WPROST z danych arkusza: więcej niż
jedna wartość w kolumnie "Podgrupa" dla danego zabiegu = struktura zagnieżdżona w /cennik
(analogicznie do Fazy 2) i wymaga zawężenia wyszukiwania (find_outer_treatment_block).

Użycie:
  python3 apply_sync_all.py            # podgląd (dry-run)
  python3 apply_sync_all.py --write    # zapis
"""
import argparse
import difflib
import json
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path

from read_sheet import read_all_rows

STATE_PATH = Path(__file__).parent / "last_synced_state.json"
from html_engine import (
    find_price_tier_rows_block, find_price_tier_badge, replace_span, replace_block,
    find_outer_treatment_block, find_loose_rows_block,
)
from row_generator import generate_rows_block, compute_badge_price

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")

# nazwa zabiegu użyta w /cennik, gdy różni się od nazwy podgrupy "Zabieg" na arkuszu
# (przypadki, gdzie /cennik i podstrona historycznie nazwały główną podgrupę inaczej)
CENNIK_NAME_OVERRIDE = {
    ("Epilacja laserowa LightSheer®", "(S) Mała partia ciała"): "(S) mała partia ciała",
    ("Epilacja laserowa LightSheer®", "(M) Standardowa partia ciała"): "(M) standardowa partia ciała",
    ("Epilacja laserowa LightSheer®", "(L) Duża partia ciała"): "(L) duża partia ciała",
    ("Endermologia LPG® Alliance", "Sesje zabiegowe"): "Endermologia LPG® Alliance",
    ("Kriolipoliza cooltech®", "Zabieg"): "Kriolipoliza cooltech®",
    ("Mezoterapia bezigłowa", "Zabieg"): "Mezoterapia bezigłowa",
    ("Karboksyterapia bezigłowa CO2", "Zabieg"): "Karboksyterapia bezigłowa CO2",
}

# podgrupy, których reprezentacja w /cennik to LUŹNE wiersze bez własnego <details>/badge
LOOSE_CENNIK_SUBGROUPS = {
    ("Mezoterapia bezigłowa", "Zabieg"),
    ("Karboksyterapia bezigłowa CO2", "Zabieg"),
}


def to_row_dict(r, zabieg):
    return {
        "zabieg": zabieg, "wariant": r["wariant"], "czas": r["czas"], "cena": r["cena"],
        "offerItemId": r["offerItemId"], "packageId": r["packageId"], "promo": r["promo"],
    }


def _extract_trailing_notes(inner_html: str) -> str:
    """Zwraca surowy HTML wszystkich <p class="price-row-note">...</p> occurring PO
    ostatnim <div class="price-row">...</div> w bloku — treści niezwiązane z żadnym
    wierszem (np. informacyjne dopiski), które inaczej zostałyby bezpowrotnie skasowane
    przy regeneracji z arkusza. Zweryfikowane na "Strój zabiegowy" (Endermologia LPG®)."""
    last_row_end = inner_html.rfind("</div>")
    if last_row_end == -1:
        return ""
    tail = inner_html[last_row_end + len("</div>"):]
    notes = re.findall(r'<p class="price-row-note">.*?</p>', tail, flags=re.DOTALL)
    return "".join(notes)


def _splice_notes(new_inner: str, notes: str, row_indent: int) -> str:
    if not notes:
        return new_inner
    # new_inner kończy się na "\n" + (spacje zamykające) — wstaw notatki tuż przed tym
    idx = new_inner.rstrip(" ").rfind("\n")
    closing_ws = new_inner[idx + 1:]
    return new_inner[:idx + 1] + (" " * row_indent) + notes + "\n" + closing_ws


def _apply_unscoped(html, h3_prefix, rows, row_indent, closing_indent):
    changed = False
    b_start, b_end, current_badge = find_price_tier_badge(html, h3_prefix)
    new_badge = compute_badge_price(rows)
    if current_badge != new_badge:
        html = replace_span(html, b_start, b_end, new_badge)
        changed = True
    start, end, content_start = find_price_tier_rows_block(html, h3_prefix)
    current_inner = html[content_start:end - len("</div>")]
    notes = _extract_trailing_notes(current_inner)
    new_inner = generate_rows_block(rows, row_indent=row_indent, closing_indent=closing_indent)
    new_inner = _splice_notes(new_inner, notes, row_indent)
    if current_inner != new_inner:
        html = replace_block(html, content_start, end - len("</div>"), new_inner)
        changed = True
    return html, changed


def _apply_loose_unscoped(html, rows, row_indent, closing_indent):
    start, end, content_start = find_loose_rows_block(html)
    current_inner = html[content_start:end]
    notes = _extract_trailing_notes(current_inner)
    new_inner = generate_rows_block(rows, row_indent=row_indent, closing_indent=closing_indent)
    new_inner = _splice_notes(new_inner, notes, row_indent)
    if current_inner == new_inner:
        return html, False
    return html[:content_start] + new_inner + html[end:], True


def apply_group(html, h3_prefix, rows, row_indent, closing_indent, scope=None, loose=False):
    if scope:
        s_start, s_end = scope
        sub = html[s_start:s_end]
        if loose:
            new_sub, changed = _apply_loose_unscoped(sub, rows, row_indent, closing_indent)
        else:
            new_sub, changed = _apply_unscoped(sub, h3_prefix, rows, row_indent, closing_indent)
        if not changed:
            return html, False
        return html[:s_start] + new_sub + html[s_end:], True
    return _apply_unscoped(html, h3_prefix, rows, row_indent, closing_indent)


def show_diff(label, old, new):
    if old == new:
        return False
    diff = list(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                      fromfile=f"{label} (przed)", tofile=f"{label} (po)"))
    print(f"\n{'='*70}\n{label}\n{'='*70}")
    print("".join(diff))
    return True


def check_deletions(sheet_rows):
    """Porównuje bieżące (zabieg,podgrupa,wariant) z ostatnim znanym stanem arkusza.
    Zwraca listę usuniętych kluczy (obecnych wcześniej, nieobecnych teraz)."""
    if not STATE_PATH.exists():
        return []
    last_state = {tuple(x) for x in json.loads(STATE_PATH.read_text(encoding="utf-8"))}
    current_state = {(r["zabieg"], r["podgrupa"], r["wariant"]) for r in sheet_rows}
    return sorted(last_state - current_state)


def save_synced_state(sheet_rows):
    snapshot = sorted({(r["zabieg"], r["podgrupa"], r["wariant"]) for r in sheet_rows})
    STATE_PATH.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--confirm-deletions", action="store_true",
                         help="potwierdź, że wykryte usunięcia wierszy są zamierzone")
    args = parser.parse_args()

    sheet_rows = read_all_rows()

    # walidacja PRZED czymkolwiek: rozjazdy cena-na-stronie vs Fresha
    mismatches = [r for r in sheet_rows if r["zgodnosc"].startswith("⚠️")]
    if mismatches:
        print("⚠️  WYKRYTO ROZJAZDY CEN — zatrzymuję się przed zapisem:")
        for r in mismatches:
            print(f"   {r['zabieg']} | {r['wariant']} | strona={r['cena']!r} vs Fresha={r['cena_fresha']!r}")
        print("\nPopraw w arkuszu (cenę na stronie albo cenę w Fresha), zanim uruchomisz ponownie.")
        return

    deletions = check_deletions(sheet_rows)
    if deletions and not args.confirm_deletions:
        print("⚠️  WYKRYTO USUNIĘTE WIERSZE (były w arkuszu, teraz ich nie ma) — zatrzymuję się:")
        for zabieg, podgrupa, wariant in deletions:
            print(f"   {zabieg} | {podgrupa} | {wariant}")
        print("\nJeśli to zamierzone, uruchom ponownie z flagą --confirm-deletions (razem z --write, jeśli chcesz też zapisać).")
        return

    by_zabieg = defaultdict(list)
    for r in sheet_rows:
        by_zabieg[r["zabieg"]].append(r)

    any_changes = False
    cennik_path = ROOT / "cennik" / "index.html"
    cennik_html = cennik_path.read_text(encoding="utf-8")
    original_cennik_html = cennik_html

    subpage_cache = {}

    for zabieg, rows in by_zabieg.items():
        podgrupy = sorted(set(r["podgrupa"] for r in rows))
        is_nested = len(podgrupy) > 1
        url = rows[0]["url"]

        if url and url not in subpage_cache:
            rel = urllib.parse.unquote(url.lstrip("/"))
            subpage_cache[url] = (rel, (ROOT / rel / "index.html").read_text(encoding="utf-8"))

        cennik_scope = None
        if is_nested:
            try:
                cennik_scope = find_outer_treatment_block(cennik_html, zabieg)
            except ValueError as e:
                print(f"UWAGA: {e}")
                continue

        for podgrupa in podgrupy:
            group_rows = [to_row_dict(r, zabieg) for r in rows if r["podgrupa"] == podgrupa]

            if url:
                rel, subpage_html = subpage_cache[url]
                subpage_html, _ = apply_group(subpage_html, podgrupa, group_rows, row_indent=14, closing_indent=12)
                subpage_cache[url] = (rel, subpage_html)

            cennik_name = CENNIK_NAME_OVERRIDE.get((zabieg, podgrupa), podgrupa if is_nested else zabieg)
            is_loose = (zabieg, podgrupa) in LOOSE_CENNIK_SUBGROUPS
            if is_nested:
                indent = 16 if is_loose else 32
                if cennik_scope:
                    cennik_html, changed2 = apply_group(cennik_html, cennik_name, group_rows, row_indent=indent, closing_indent=indent, scope=cennik_scope, loose=is_loose)
                    if changed2:
                        cennik_scope = find_outer_treatment_block(cennik_html, zabieg)
            else:
                cennik_html, _ = apply_group(cennik_html, cennik_name, group_rows, row_indent=16, closing_indent=16)

    if show_diff("cennik/index.html", original_cennik_html, cennik_html):
        any_changes = True
        if args.write:
            cennik_path.write_text(cennik_html, encoding="utf-8")

    for url, (rel, html) in subpage_cache.items():
        original = (ROOT / rel / "index.html").read_text(encoding="utf-8")
        if show_diff(f"{rel}/index.html", original, html):
            any_changes = True
            if args.write:
                (ROOT / rel / "index.html").write_text(html, encoding="utf-8")

    if args.write:
        save_synced_state(sheet_rows)

    print(f"\n\n{'WYNIK: zapisano zmiany.' if (any_changes and args.write) else ('WYNIK: znaleziono zmiany (tryb podglądu).' if any_changes else 'WYNIK: brak zmian, wszystko już zgodne.')}")


if __name__ == "__main__":
    main()
