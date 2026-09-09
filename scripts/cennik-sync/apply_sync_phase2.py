#!/usr/bin/env python3
"""Faza 2: synchronizacja 6 zabiegów ze złożoną strukturą (podgrupy, pakiety).

Na tym etapie obsługuje TYLKO podgrupy typu "both" (istniejące w obu miejscach) —
aktualizacja treści/cen. Podgrupy "cennik_only"/"subpage_only" (dodanie całkiem nowej
podgrupy) są w kolejnym kroku, bo wymagają WSTAWIANIA nowego bloku <details>, nie
tylko podmiany istniejącej zawartości.

Użycie:
  python3 apply_sync_phase2.py            # podgląd (dry-run)
  python3 apply_sync_phase2.py --write    # zapis
"""
import argparse
import difflib
from collections import defaultdict
from pathlib import Path

from baseline_phase2 import load_phase2_baseline_rows
from phase2_mapping import TREATMENTS, CENNIK_NAME_OVERRIDE
from html_engine import find_price_tier_rows_block, find_price_tier_badge, replace_span, replace_block, find_outer_treatment_block, find_loose_rows_block

# podgrupy, których reprezentacja w /cennik to LUŹNE wiersze bez własnego <details>/badge
# (np. Mezoterapia bezigłowa: bazowy wiersz zabiegu leży wprost w kontenerze zagnieżdżonym)
LOOSE_CENNIK_SUBGROUPS = {("Mezoterapia bezigłowa", "Zabieg")}
from row_generator import generate_rows_block, compute_badge_price

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")


def apply_group_to_html(html: str, h3_prefix: str, rows: list[dict], row_indent: int, closing_indent: int, scope=None, loose=False):
    """scope: opcjonalny (start, end) ograniczający wyszukiwanie do fragmentu html.
    loose: True -> podgrupa bez własnego <details>/badge (patrz LOOSE_CENNIK_SUBGROUPS).
    Zwraca (nowy_html, zmieniono: bool)."""
    if scope:
        s_start, s_end = scope
        sub = html[s_start:s_end]
        if loose:
            new_sub, changed = _apply_loose_rows_unscoped(sub, rows, row_indent, closing_indent)
        else:
            new_sub, changed = _apply_group_to_html_unscoped(sub, h3_prefix, rows, row_indent, closing_indent)
        if not changed:
            return html, False
        return html[:s_start] + new_sub + html[s_end:], True
    return _apply_group_to_html_unscoped(html, h3_prefix, rows, row_indent, closing_indent)


def _apply_loose_rows_unscoped(html: str, rows: list[dict], row_indent: int, closing_indent: int):
    start, end, content_start = find_loose_rows_block(html)
    current_inner = html[content_start:end]
    new_inner = generate_rows_block(rows, row_indent=row_indent, closing_indent=closing_indent)
    if current_inner == new_inner:
        return html, False
    return html[:content_start] + new_inner + html[end:], True


def _apply_group_to_html_unscoped(html: str, h3_prefix: str, rows: list[dict], row_indent: int, closing_indent: int):
    changed = False
    b_start, b_end, current_badge = find_price_tier_badge(html, h3_prefix)
    new_badge = compute_badge_price(rows)
    if current_badge != new_badge:
        html = replace_span(html, b_start, b_end, new_badge)
        changed = True

    start, end, content_start = find_price_tier_rows_block(html, h3_prefix)
    current_inner = html[content_start:end - len("</div>")]
    new_inner = generate_rows_block(rows, row_indent=row_indent, closing_indent=closing_indent)
    if current_inner != new_inner:
        html = replace_block(html, content_start, end - len("</div>"), new_inner)
        changed = True

    return html, changed


def show_diff(label: str, old: str, new: str):
    if old == new:
        return False
    diff = list(difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile=f"{label} (przed)", tofile=f"{label} (po)",
    ))
    if diff:
        print(f"\n{'='*70}\n{label}\n{'='*70}")
        print("".join(diff))
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    rows = load_phase2_baseline_rows()
    by_zabieg_podgrupa = defaultdict(list)
    for r in rows:
        by_zabieg_podgrupa[(r["zabieg"], r["podgrupa"])].append(r)

    any_changes = False
    cennik_path = ROOT / "cennik" / "index.html"
    cennik_html = cennik_path.read_text(encoding="utf-8")
    original_cennik_html = cennik_html

    subpage_cache = {}  # rel -> html (do modyfikacji w pamięci przed zapisem)

    for zabieg, config in TREATMENTS.items():
        rel = config["subpageRel"]
        if rel not in subpage_cache:
            subpage_cache[rel] = (ROOT / rel / "index.html").read_text(encoding="utf-8")
        subpage_html = subpage_cache[rel]

        # scope w /cennik — wyszukaj RAZ na iterację zabiegu (podgrupy współdzielą scope)
        try:
            cennik_scope = find_outer_treatment_block(cennik_html, zabieg)
        except ValueError as e:
            print(f"UWAGA: {e}")
            cennik_scope = None

        for canonical_name, source in config["subgroups"]:
            if source != "both":
                continue  # insercja nowych podgrup — osobny krok
            group_rows = by_zabieg_podgrupa[(zabieg, canonical_name)]

            # --- podstrona (bez scope — nazwy unikalne w obrębie pliku) ---
            subpage_html, changed = apply_group_to_html(subpage_html, canonical_name, group_rows, row_indent=14, closing_indent=12)

            # --- cennik (w obrębie scope tego zabiegu) ---
            cennik_name = CENNIK_NAME_OVERRIDE.get((zabieg, canonical_name), canonical_name)
            is_loose = (zabieg, canonical_name) in LOOSE_CENNIK_SUBGROUPS
            # podgrupy ZAGNIEŻDŻONE w /cennik mają głębsze wcięcie (32) niż płaskie grupy
            # z Fazy 1 (16); luźne wiersze (bez własnej <details>) zostają na 16, bo leżą
            # bezpośrednio w kontenerze nadrzędnym — zweryfikowane w pliku, nie zgadywane
            cennik_indent = 16 if is_loose else 32
            if cennik_scope:
                cennik_html, changed2 = apply_group_to_html(cennik_html, cennik_name, group_rows, row_indent=cennik_indent, closing_indent=cennik_indent, scope=cennik_scope, loose=is_loose)
                # scope mógł się przesunąć po edycji — przelicz
                if changed2:
                    cennik_scope = find_outer_treatment_block(cennik_html, zabieg)

        subpage_cache[rel] = subpage_html

    if show_diff("cennik/index.html", original_cennik_html, cennik_html):
        any_changes = True
        if args.write:
            cennik_path.write_text(cennik_html, encoding="utf-8")

    for rel, html in subpage_cache.items():
        original = (ROOT / rel / "index.html").read_text(encoding="utf-8")
        if show_diff(f"{rel}/index.html", original, html):
            any_changes = True
            if args.write:
                (ROOT / rel / "index.html").write_text(html, encoding="utf-8")

    print(f"\n\n{'WYNIK: zapisano zmiany.' if (any_changes and args.write) else ('WYNIK: znaleziono zmiany (tryb podglądu).' if any_changes else 'WYNIK: brak zmian, wszystko już zgodne.')}")


if __name__ == "__main__":
    main()
