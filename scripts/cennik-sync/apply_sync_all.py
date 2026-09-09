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
    find_full_outer_block, find_full_subpage_block, find_price_strip_giant,
    find_nested_container_bounds, rename_h3_heading,
)
from row_generator import generate_rows_block, compute_badge_price, _extract_number
from subgroup_generator import (
    generate_subgroup_block, SUBPAGE_INDENTS, CENNIK_FLAT_INDENTS, CENNIK_NESTED_INDENTS,
    ACCORDION_INFO_LINK_ICON,
)

ROOT = Path(__file__).resolve().parent.parent.parent

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
        "opis": r.get("opis", ""), "link_reczny": r.get("link_reczny", ""),
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


def _load_state() -> dict:
    """{"<id>": {"zabieg":..., "podgrupa":..., "wariant":...}} — stan ostatniej synchronizacji,
    kluczowany po stałym ID wiersza (kolumna "ID" w arkuszu, dodana 2026-09-09), NIE po tekście.
    Dzięki temu zmiana samej nazwy zabiegu/podgrupy/wariantu dla ISTNIEJĄCEGO wiersza to
    rename (patrz detect_group_renames), nie usunięcie+dodanie — patrz DOKUMENTACJA.md,
    incydent Endermolift 2026-09-09."""
    if not STATE_PATH.exists():
        return {}
    raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return {}  # stary format (lista trójek, bez ID) — brak ID, nie da się zmigrować 1:1
    return raw


def _state_triples(state: dict, exclude_zabiegi=frozenset()):
    """Lista (nie set!) — zachowuje kolejność wpisów w last_synced_state.json, od której
    zależy porządek podgrup w find_flatten_candidates/find_new_subgroup_candidates."""
    return [(v["zabieg"], v["podgrupa"], v["wariant"]) for v in state.values()
            if v["zabieg"] not in exclude_zabiegi]


def check_deletions(sheet_rows, exclude_zabiegi=frozenset()):
    """ID-based: prawdziwe usunięcie wiersza = jego ID było zapisane w last_synced_state.json,
    a teraz go nie ma wśród ID w arkuszu. Zmiana samej nazwy (zabieg/podgrupa/wariant) dla
    ISTNIEJĄCEGO ID to rename (detect_group_renames), NIE usunięcie — to jest różnica względem
    starej wersji tej funkcji (dopasowanie po tekście), która fałszywie łapała np. zmianę
    interpunkcji w nazwie wariantu jako "usunięcie" (Endermolift, 2026-09-09). Zabiegi z
    exclude_zabiegi (spłaszczane) są pomijane — ich stare nazwy podgrup naturalnie znikają
    przy spłaszczeniu, to nie jest prawdziwe usunięcie."""
    state = _load_state()
    if not state:
        return []
    current_ids = {r["id"] for r in sheet_rows if r["id"] and r["zabieg"] not in exclude_zabiegi}
    deleted = []
    for id_, info in state.items():
        if info["zabieg"] in exclude_zabiegi:
            continue
        if id_ not in current_ids:
            deleted.append((info["zabieg"], info["podgrupa"], info["wariant"]))
    return sorted(deleted)


def detect_group_renames(sheet_rows, exclude_zabiegi=frozenset()):
    """Wykrywa zmianę nazwy zabiegu i/lub podgrupy dla ISTNIEJĄCEGO id (wiersz był w ostatnim
    stanie I wciąż jest w arkuszu, ale pod inną nazwą zabiegu/podgrupy) — odróżnione od
    usunięcia właśnie dzięki ID. Zwraca listę unikalnych par
    (old_zabieg, old_podgrupa, new_zabieg, new_podgrupa), po jednej per faktycznie zmieniona
    grupa (deduplikowane — wiele wierszy tej samej grupy dają tę samą parę)."""
    state = _load_state()
    if not state:
        return []
    seen = set()
    renames = []
    for r in sheet_rows:
        id_ = r["id"]
        if not id_ or r["zabieg"] in exclude_zabiegi:
            continue
        old = state.get(id_)
        if not old:
            continue  # nowy wiersz (nowe ID) — to nie rename
        if old["zabieg"] != r["zabieg"] or old["podgrupa"] != r["podgrupa"]:
            key = (old["zabieg"], old["podgrupa"], r["zabieg"], r["podgrupa"])
            if key not in seen:
                seen.add(key)
                renames.append(key)
    return renames


def save_synced_state(sheet_rows, skip_zabiegi=frozenset()):
    """Zapisuje bieżący stan arkusza (kluczowany po ID) jako 'ostatnio zsynchronizowany' —
    ale dla zabiegów pominiętych w tym przebiegu (skip_zabiegi: czekają na --confirm-*)
    zachowuje ich STARY zapisany stan, żeby przy kolejnym uruchomieniu nadal były wykrywane
    jako wymagające potwierdzenia, a nie wyglądały na już zsynchronizowane."""
    old_state = _load_state()
    snapshot = {}
    if skip_zabiegi:
        snapshot.update({id_: v for id_, v in old_state.items() if v["zabieg"] in skip_zabiegi})
    for r in sheet_rows:
        if not r["id"] or r["zabieg"] in skip_zabiegi:
            continue
        snapshot[r["id"]] = {"zabieg": r["zabieg"], "podgrupa": r["podgrupa"], "wariant": r["wariant"]}
    # UWAGA: bez sort_keys — kolejność wpisów (insertion order słownika Pythona) musi
    # odpowiadać kolejności wierszy w arkuszu, bo od niej zależy porządek podgrup
    # w find_flatten_candidates/find_new_subgroup_candidates (patrz _state_triples).
    STATE_PATH.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_blank_podgrupa(sheet_rows):
    """Zabieg, którego WSZYSTKIE wiersze mają puste Podgrupa (użytkownik wyczyścił
    kolumnę), jest odtąd traktowany jak zwykły płaski zabieg — ujednolica się jego
    Podgrupa do konwencjonalnego "Zabieg" (tak jak każdy inny płaski zabieg w arkuszu),
    żeby dalsza logika (is_nested, dopasowanie h3 na podstronie) działała bez wyjątków."""
    by_zabieg = defaultdict(list)
    for r in sheet_rows:
        by_zabieg[r["zabieg"]].append(r)
    for zabieg, rows in by_zabieg.items():
        if all(r["podgrupa"] == "" for r in rows):
            for r in rows:
                r["podgrupa"] = "Zabieg"


def find_flatten_candidates(sheet_rows):
    """Wykrywa zabiegi, których kolumna Podgrupa została WYCZYSZCZONA (wszystkie wiersze
    puste) dla zabiegu, który wcześniej (wg last_synced_state.json) miał więcej niż jedną
    podgrupę — czyli miał zagnieżdżoną strukturę w /cennik. Zwraca listę
    (zabieg, [stare_nazwy_podgrup_w_kolejności_z_ostatniego_stanu])."""
    last_state = _state_triples(_load_state())
    if not last_state:
        return []
    prev_podgrupy_by_zabieg = defaultdict(list)
    for zabieg, podgrupa, _wariant in last_state:
        if podgrupa not in prev_podgrupy_by_zabieg[zabieg]:
            prev_podgrupy_by_zabieg[zabieg].append(podgrupa)

    raw_by_zabieg = defaultdict(list)
    for r in sheet_rows:
        raw_by_zabieg[r["zabieg"]].append(r["podgrupa"])

    candidates = []
    for zabieg, raw_podgrupy in raw_by_zabieg.items():
        if set(raw_podgrupy) != {""}:
            continue
        prev_podgrupy = prev_podgrupy_by_zabieg.get(zabieg, [])
        if len(prev_podgrupy) > 1:
            candidates.append((zabieg, prev_podgrupy))
    return candidates


def extract_accordion_info_link(block: str):
    m = re.search(r'<a class="accordion-info-link" href="([^"]*)" aria-label="([^"]*)">', block)
    if not m:
        return None
    return (m.group(1), m.group(2))


def flatten_cennik_group(html: str, zabieg: str, rows: list[dict]) -> str:
    """Zastępuje CAŁY zagnieżdżony outer blok zabiegu w /cennik jednym płaskim
    <details class="price-tier">, zachowując accordion-info-link (jeśli istniał)."""
    full_start, full_end = find_full_outer_block(html, zabieg)
    info_link = extract_accordion_info_link(html[full_start:full_end])
    new_block = generate_subgroup_block(zabieg, rows, CENNIK_FLAT_INDENTS, info_link=info_link)
    return html[:full_start] + new_block + html[full_end:]


def flatten_subpage_sections(html: str, old_podgrupa_names: list[str], rows: list[dict]) -> str:
    """Scala kilka sąsiadujących <details class="price-tier"> (dawne podgrupy) na
    podstronie zabiegu w JEDEN blok o konwencjonalnej nazwie "Zabieg", zachowując
    ewentualne dopiski (price-row-note) ze wszystkich scalanych bloków."""
    spans = []
    for name in old_podgrupa_names:
        try:
            spans.append(find_full_subpage_block(html, name))
        except ValueError:
            continue
    if not spans:
        raise ValueError("Nie znaleziono żadnej z dawnych podgrup do scalenia na podstronie")
    spans.sort()

    notes = "".join(_extract_trailing_notes(html[s:e]) for s, e in spans)
    new_block = generate_subgroup_block("Zabieg", rows, SUBPAGE_INDENTS)
    if notes:
        row_indent = SUBPAGE_INDENTS[10]
        idx = new_block.rstrip(" ").rfind("\n")
        closing_ws = new_block[idx + 1:]
        new_block = new_block[:idx + 1] + (" " * row_indent) + notes + "\n" + closing_ws

    insert_pos = spans[0][0]
    result = html
    for s, e in reversed(spans):
        if s == insert_pos:
            result = result[:s] + new_block + result[e:]
        else:
            rm_end = e + 1 if result[e:e + 1] == "\n" else e
            result = result[:s] + result[rm_end:]
    return result


def find_new_subgroup_candidates(sheet_rows, exclude_zabiegi=frozenset()):
    """Wykrywa zabiegi, dla których w arkuszu pojawiła się CAŁKIEM NOWA nazwa podgrupy
    (nieobecna w last_synced_state.json), podczas gdy sam zabieg już wcześniej istniał —
    wywoływać PO normalize_blank_podgrupa. Zwraca listę
    (zabieg, poprzednie_podgrupy: set, nowe_podgrupy: set)."""
    last_state = _state_triples(_load_state())
    if not last_state:
        return []
    prev_podgrupy_by_zabieg = defaultdict(set)
    for zabieg, podgrupa, _w in last_state:
        prev_podgrupy_by_zabieg[zabieg].add(podgrupa)

    current_by_zabieg = defaultdict(set)
    for r in sheet_rows:
        current_by_zabieg[r["zabieg"]].add(r["podgrupa"])

    candidates = []
    for zabieg, current_podgrupy in current_by_zabieg.items():
        if zabieg in exclude_zabiegi:
            continue
        prev_podgrupy = prev_podgrupy_by_zabieg.get(zabieg)
        if not prev_podgrupy:
            continue  # zabieg jeszcze nie istniał na stronie — nieobsługiwane tutaj
        new_names = current_podgrupy - prev_podgrupy
        if new_names:
            candidates.append((zabieg, prev_podgrupy, new_names))
    return candidates


def insert_cennik_subgroup(html: str, zabieg: str, name: str, rows: list[dict]) -> str:
    """Dopisuje nową podgrupę na końcu już istniejącej zagnieżdżonej struktury zabiegu
    w /cennik (zabieg musi już mieć co najmniej jedną podgrupę we własnym <details>)."""
    content_start, content_end = find_nested_container_bounds(html, zabieg)
    content = html[content_start:content_end]
    last_details_end = content.rfind("</details>")
    if last_details_end == -1:
        raise ValueError(f"Brak istniejących podgrup w kontenerze zagnieżdżonym {zabieg!r}")
    last_details_end += len("</details>")
    cennik_name = CENNIK_NAME_OVERRIDE.get((zabieg, name), name)
    new_block = generate_subgroup_block(cennik_name, rows, CENNIK_NESTED_INDENTS)
    new_content = content[:last_details_end] + "\n" + new_block + content[last_details_end:]
    return html[:content_start] + new_content + html[content_end:]


def insert_subpage_subgroup(html: str, after_h3_name: str, name: str, rows: list[dict]) -> str:
    """Dopisuje nową podgrupę jako kolejną sekcję na podstronie zabiegu, zaraz po
    sekcji after_h3_name."""
    _s, after_end = find_full_subpage_block(html, after_h3_name)
    new_block = generate_subgroup_block(name, rows, SUBPAGE_INDENTS)
    return html[:after_end] + "\n" + new_block + html[after_end:]


def unflatten_cennik_group(html: str, zabieg: str, rows_by_podgrupa: dict) -> str:
    """Przekształca dziś PŁASKI blok zabiegu w /cennik w nowo zagnieżdżoną strukturę —
    odwrotność flatten_cennik_group. rows_by_podgrupa: {podgrupa: [wiersze]} w kolejności
    z arkusza — pierwsza podgrupa to dotychczasowa zawartość dawnego płaskiego bloku."""
    full_start, full_end = find_full_outer_block(html, zabieg)
    info_link = extract_accordion_info_link(html[full_start:full_end])

    first_rows = next(iter(rows_by_podgrupa.values()))
    outer_badge = compute_badge_price(first_rows)

    inner_blocks = []
    for podgrupa, rows in rows_by_podgrupa.items():
        cennik_name = CENNIK_NAME_OVERRIDE.get((zabieg, podgrupa), zabieg if podgrupa == "Zabieg" else podgrupa)
        inner_blocks.append(generate_subgroup_block(cennik_name, rows, CENNIK_NESTED_INDENTS))
    inner_html = "\n".join(inner_blocks)

    h3_content = zabieg
    if info_link:
        href, aria_label = info_link
        h3_content += (f'<a class="accordion-info-link" href="{href}" aria-label="{aria_label}">'
                        f'{ACCORDION_INFO_LINK_ICON}</a>')

    caret_svg = ('<svg class="caret" viewBox="0 0 10 6" fill="none" aria-hidden="true">'
                 '<path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.4" '
                 'stroke-linecap="round" stroke-linejoin="round"/></svg>')

    new_block = "\n".join([
        " " * 12 + '<details class="price-tier price-tier--group">',
        " " * 14 + '<summary>',
        " " * 16 + '<span class="price-tier-label">',
        " " * 18 + f'<h3 class="treatment-accordion-q">{h3_content}</h3>',
        " " * 18 + f'<span class="price-tier-badge">{outer_badge}</span>',
        " " * 16 + '</span>',
        " " * 16 + caret_svg,
        " " * 14 + '</summary>',
        " " * 14 + '<div class="treatment-accordion-body">',
        " " * 16 + '<div class="price-tier-rows price-tier-rows--nested">',
        inner_html,
        " " * 16 + '</div>',
        " " * 14 + '</div>',
        " " * 12 + '</details>',
    ])
    return html[:full_start] + new_block + html[full_end:]


def apply_renames(cennik_html, subpage_cache, renames, url_by_zabieg):
    """Aplikuje zmiany nazwy zabiegu/podgrupy (wykryte przez detect_group_renames) na
    /cennik i — jeśli zabieg ma podstronę — na niej też, PRZED głównym przebiegiem
    synchronizacji (który dalej lokalizuje grupy PO NOWEJ nazwie). Bez tego kroku główny
    przebieg dostałby ValueError "nie znaleziono nagłówka", bo HTML wciąż ma starą nazwę.

    Zasięg zmian jest ograniczony do tego, czym ten skrypt już i tak zarządza (nagłówki
    <h3 class="treatment-accordion-q"> w cenniku/na podstronie zabiegu) — NIE dotyka
    <title>, meta description, JSON-LD, H1 czy sekcji opisowych strony zabiegu. Zmiana
    nazwy zabiegu w arkuszu więc odświeży cennik, ale nie całą resztę strony — to świadome
    ograniczenie zakresu (2026-09-09), nie przeoczenie."""
    state = _load_state()
    prev_podgrupy_by_old_zabieg = defaultdict(set)
    for v in state.values():
        prev_podgrupy_by_old_zabieg[v["zabieg"]].add(v["podgrupa"])

    for old_zabieg, old_podgrupa, new_zabieg, new_podgrupa in renames:
        was_nested = len(prev_podgrupy_by_old_zabieg.get(old_zabieg, set())) > 1
        zabieg_changed = old_zabieg != new_zabieg
        podgrupa_changed = old_podgrupa != new_podgrupa

        if zabieg_changed:
            try:
                cennik_html = rename_h3_heading(cennik_html, old_zabieg, new_zabieg)
            except ValueError as e:
                print(f"UWAGA: zmiana nazwy zabiegu w /cennik — {e} (pomijam tę zmianę nazwy w tym przebiegu)")
                continue

        if was_nested and podgrupa_changed and (old_zabieg, old_podgrupa) not in LOOSE_CENNIK_SUBGROUPS:
            old_display = CENNIK_NAME_OVERRIDE.get((old_zabieg, old_podgrupa), old_podgrupa)
            new_display = CENNIK_NAME_OVERRIDE.get((new_zabieg, new_podgrupa), new_podgrupa)
            try:
                scope_start, _scope_end = find_outer_treatment_block(cennik_html, new_zabieg)
                cennik_html = rename_h3_heading(cennik_html, old_display, new_display, search_from=scope_start)
            except ValueError as e:
                print(f"UWAGA: zmiana nazwy podgrupy w /cennik — {e} (pomijam tę zmianę nazwy w tym przebiegu)")

        url = url_by_zabieg.get(new_zabieg) or url_by_zabieg.get(old_zabieg)
        if url and podgrupa_changed and url in subpage_cache:
            rel, subpage_html = subpage_cache[url]
            try:
                subpage_html = rename_h3_heading(subpage_html, old_podgrupa, new_podgrupa)
                subpage_cache[url] = (rel, subpage_html)
            except ValueError as e:
                print(f"UWAGA: zmiana nazwy podgrupy na podstronie {rel} — {e} (pomijam tę zmianę nazwy w tym przebiegu)")

    return cennik_html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--confirm-deletions", action="store_true",
                         help="potwierdź, że wykryte usunięcia wierszy są zamierzone")
    parser.add_argument("--confirm-flatten", action="store_true",
                         help="potwierdź spłaszczenie zabiegu(-ów) do jednego poziomu (wykryte "
                              "po wyczyszczeniu kolumny Podgrupa)")
    parser.add_argument("--confirm-grow", action="store_true",
                         help="potwierdź dodanie nowej podgrupy zabiegu (wykrytej jako nowa "
                              "nazwa w kolumnie Podgrupa dla już istniejącego zabiegu)")
    parser.add_argument("--report-to-sheet", action="store_true",
                         help="zapisz krótkie podsumowanie przebiegu do zakładki Status w arkuszu "
                              "(używane przez przycisk/automatyzację, nie potrzebne z terminala)")
    args = parser.parse_args()

    sheet_rows = read_all_rows()
    status_lines = []

    # rozjazdy cena-na-stronie vs Fresha są TYLKO informacyjne — widać je jako ⚠️ w kolumnie
    # Zgodność w samym arkuszu, więc nie blokują zapisu; cena na stronie to zawsze to, co jest
    # wpisane w kolumnie "Cena na stronie", niezależnie od tego, co pokazuje Fresha
    mismatches = [r for r in sheet_rows if r["zgodnosc"].startswith("⚠️")]
    if mismatches:
        print("ℹ️  Rozjazdy cena-na-stronie vs Fresha (informacyjnie, nie blokują zapisu):")
        for r in mismatches:
            print(f"   {r['zabieg']} | {r['wariant']} | strona={r['cena']!r} vs Fresha={r['cena_fresha']!r}")
        status_lines.append(f"ℹ️ {len(mismatches)} rozjazd(ów) cena-Fresha — patrz kolumna Zgodność")

    # wykrywanie PRZED normalizacją Podgrupa — potrzebne surowe (puste) wartości
    flatten_candidates = find_flatten_candidates(sheet_rows)
    flatten_zabiegi = {z for z, _ in flatten_candidates}
    flatten_pending = set() if args.confirm_flatten else flatten_zabiegi
    if flatten_pending:
        print("⚠️  WYKRYTO SPŁASZCZENIE PODGRUP (kolumna Podgrupa wyczyszczona) — pomijam te zabiegi:")
        for zabieg, old_podgrupy in flatten_candidates:
            print(f"   {zabieg}: {', '.join(old_podgrupy)} → jeden poziom ('Zabieg')")
        print("Uruchom z flagą --confirm-flatten (razem z --write), żeby to zastosować.")
        status_lines.append(f"⚠️ Do potwierdzenia (spłaszczenie): {', '.join(sorted(flatten_pending))}")

    normalize_blank_podgrupa(sheet_rows)

    deletions = check_deletions(sheet_rows, exclude_zabiegi=flatten_zabiegi)
    deletion_zabiegi = {z for z, _p, _w in deletions}
    deletions_pending = set() if args.confirm_deletions else deletion_zabiegi
    if deletions_pending:
        print("⚠️  WYKRYTO USUNIĘTE WIERSZE (były w arkuszu, teraz ich nie ma) — pomijam te zabiegi:")
        for zabieg, podgrupa, wariant in deletions:
            print(f"   {zabieg} | {podgrupa} | {wariant}")
        print("Uruchom z flagą --confirm-deletions (razem z --write), żeby to zastosować.")
        status_lines.append(f"⚠️ Do potwierdzenia (usunięcia): {', '.join(sorted(deletions_pending))}")

    grow_candidates = find_new_subgroup_candidates(sheet_rows, exclude_zabiegi=flatten_zabiegi)
    grow_zabiegi = {z for z, _prev, _new in grow_candidates}
    grow_pending = set() if args.confirm_grow else grow_zabiegi
    if grow_pending:
        print("⚠️  WYKRYTO NOWĄ PODGRUPĘ ZABIEGU — pomijam te zabiegi:")
        for zabieg, prev_podgrupy, new_names in grow_candidates:
            print(f"   {zabieg}: nowa podgrupa {', '.join(sorted(new_names))} "
                  f"(dotychczas: {', '.join(sorted(prev_podgrupy))})")
        print("Uruchom z flagą --confirm-grow (razem z --write), żeby dodać nową sekcję na stronie.")
        status_lines.append(f"⚠️ Do potwierdzenia (nowa podgrupa): {', '.join(sorted(grow_pending))}")

    skip_zabiegi = flatten_pending | deletions_pending | grow_pending

    by_zabieg = defaultdict(list)
    for r in sheet_rows:
        if r["zabieg"] in skip_zabiegi:
            continue
        by_zabieg[r["zabieg"]].append(r)

    any_changes = False
    cennik_path = ROOT / "cennik" / "index.html"
    cennik_html = cennik_path.read_text(encoding="utf-8")
    original_cennik_html = cennik_html

    subpage_cache = {}

    # zmiana nazwy zabiegu/podgrupy dla ISTNIEJĄCEGO id (patrz detect_group_renames) — NIE
    # wymaga --confirm-*, w przeciwieństwie do flatten/deletions/grow, bo dzięki ID wiemy
    # na pewno że to nie usunięcie+dodanie, tylko ten sam wiersz pod inną nazwą
    renames = detect_group_renames(sheet_rows, exclude_zabiegi=flatten_zabiegi | deletion_zabiegi | grow_zabiegi)
    if renames:
        print("ℹ️  Wykryto zmianę nazwy zabiegu/podgrupy (stosowane automatycznie, bez potwierdzenia):")
        for old_z, old_p, new_z, new_p in renames:
            print(f"   {old_z} | {old_p}  →  {new_z} | {new_p}")
        status_lines.append(f"ℹ️ {len(renames)} zmiana(y) nazwy zabiegu/podgrupy zastosowana(e) automatycznie")

        url_by_zabieg = {r["zabieg"]: r["url"] for r in sheet_rows if r["url"]}
        for old_z, _old_p, new_z, _new_p in renames:
            url = url_by_zabieg.get(new_z) or url_by_zabieg.get(old_z)
            if url and url not in subpage_cache:
                rel = urllib.parse.unquote(url.lstrip("/"))
                subpage_cache[url] = (rel, (ROOT / rel / "index.html").read_text(encoding="utf-8"))
        cennik_html = apply_renames(cennik_html, subpage_cache, renames, url_by_zabieg)

    for zabieg, old_podgrupy in flatten_candidates:
        if zabieg in skip_zabiegi:
            continue
        rows = by_zabieg[zabieg]
        group_rows = [to_row_dict(r, zabieg) for r in rows]
        cennik_html = flatten_cennik_group(cennik_html, zabieg, group_rows)

        url = rows[0]["url"]
        if url:
            rel = urllib.parse.unquote(url.lstrip("/"))
            if url not in subpage_cache:
                subpage_cache[url] = (rel, (ROOT / rel / "index.html").read_text(encoding="utf-8"))
            rel, subpage_html = subpage_cache[url]
            subpage_html = flatten_subpage_sections(subpage_html, old_podgrupy, group_rows)
            subpage_cache[url] = (rel, subpage_html)

    for zabieg, prev_podgrupy, new_names in grow_candidates:
        if zabieg in skip_zabiegi:
            continue
        rows = by_zabieg[zabieg]
        was_nested = len(prev_podgrupy) > 1

        rows_by_podgrupa = defaultdict(list)
        for r in rows:
            rows_by_podgrupa[r["podgrupa"]].append(to_row_dict(r, zabieg))

        url = rows[0]["url"]
        if url and url not in subpage_cache:
            rel = urllib.parse.unquote(url.lstrip("/"))
            subpage_cache[url] = (rel, (ROOT / rel / "index.html").read_text(encoding="utf-8"))

        if was_nested:
            for name in sorted(new_names):
                cennik_html = insert_cennik_subgroup(cennik_html, zabieg, name, rows_by_podgrupa[name])
            if url:
                rel, subpage_html = subpage_cache[url]
                sheet_order = list(dict.fromkeys(r["podgrupa"] for r in rows))
                existing_order = [p for p in sheet_order if p not in new_names]
                after_name = existing_order[-1] if existing_order else None
                for name in sorted(new_names):
                    if after_name:
                        subpage_html = insert_subpage_subgroup(subpage_html, after_name, name, rows_by_podgrupa[name])
                    after_name = name
                subpage_cache[url] = (rel, subpage_html)
        else:
            # było płaskie ("Zabieg") -> teraz zagnieżdżone (odwrotność spłaszczania)
            sheet_order = list(dict.fromkeys(r["podgrupa"] for r in rows))
            rows_by_podgrupa_ordered = {p: rows_by_podgrupa[p] for p in sheet_order}
            cennik_html = unflatten_cennik_group(cennik_html, zabieg, rows_by_podgrupa_ordered)
            if url:
                rel, subpage_html = subpage_cache[url]
                after_name = "Zabieg" if "Zabieg" in sheet_order else sheet_order[0]
                for name in sheet_order:
                    if name in new_names:
                        subpage_html = insert_subpage_subgroup(subpage_html, after_name, name, rows_by_podgrupa[name])
                        after_name = name
                subpage_cache[url] = (rel, subpage_html)

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
                try:
                    subpage_html, _ = apply_group(subpage_html, podgrupa, group_rows, row_indent=14, closing_indent=12)
                    subpage_cache[url] = (rel, subpage_html)
                except ValueError as e:
                    print(f"UWAGA: podstrona {rel} — {e} (pomijam tę pozycję; to nie jest "
                          f"nowy wariant istniejącej pozycji, tylko zupełnie nowa nazwa "
                          f"podgrupy — trzeba najpierw ręcznie dodać dla niej sekcję na stronie)")

            cennik_name = CENNIK_NAME_OVERRIDE.get((zabieg, podgrupa), podgrupa if is_nested else zabieg)
            is_loose = (zabieg, podgrupa) in LOOSE_CENNIK_SUBGROUPS
            try:
                if is_nested:
                    indent = 16 if is_loose else 32
                    if cennik_scope:
                        cennik_html, changed2 = apply_group(cennik_html, cennik_name, group_rows, row_indent=indent, closing_indent=indent, scope=cennik_scope, loose=is_loose)
                        if changed2:
                            cennik_scope = find_outer_treatment_block(cennik_html, zabieg)
                else:
                    cennik_html, _ = apply_group(cennik_html, cennik_name, group_rows, row_indent=16, closing_indent=16)
            except ValueError as e:
                print(f"UWAGA: /cennik — {e} (pomijam tę pozycję; to nie jest nowy wariant "
                      f"istniejącej pozycji, tylko zupełnie nowa nazwa podgrupy — trzeba "
                      f"najpierw ręcznie dodać dla niej sekcję na stronie)")

    # czarny pasek cenowy na górze podstrony ("Cena już od: X zł") — pokazuje minimum
    # z PIERWSZEJ grupy w arkuszu dla danego zabiegu (główna usługa), pomijając celowo
    # akcesoria/pakiety/dodatki dodane w arkuszu po niej
    for zabieg, rows in by_zabieg.items():
        url = rows[0]["url"]
        if not url or url not in subpage_cache:
            continue
        first_podgrupa = rows[0]["podgrupa"]
        first_group_rows = [r for r in rows if r["podgrupa"] == first_podgrupa]
        min_price = min(_extract_number(r["cena"]) for r in first_group_rows)
        rel, subpage_html = subpage_cache[url]
        try:
            p_start, p_end, current = find_price_strip_giant(subpage_html)
        except ValueError:
            continue
        new_value = str(min_price)
        if current != new_value:
            subpage_cache[url] = (rel, replace_span(subpage_html, p_start, p_end, new_value))

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
        save_synced_state(sheet_rows, skip_zabiegi=skip_zabiegi)

    result_line = ('WYNIK: zapisano zmiany.' if (any_changes and args.write)
                    else ('WYNIK: znaleziono zmiany (tryb podglądu).' if any_changes
                          else 'WYNIK: brak zmian, wszystko już zgodne.'))
    print(f"\n\n{result_line}")

    if args.report_to_sheet:
        from read_sheet import write_status
        if not status_lines:
            status_lines.append("✅ Wszystko zsynchronizowane, bez zastrzeżeń.")
        write_status(result_line, status_lines)


if __name__ == "__main__":
    main()
