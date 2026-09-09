#!/usr/bin/env python3
"""Główny skrypt synchronizujący: regeneruje sekcje cennikowe w /cennik i na podstronach
zabiegów na podstawie bieżących danych arkusza (lub baseline.py przy pierwszym uruchomieniu).

Użycie:
  python3 apply_sync.py            # tryb podglądu (dry-run) — pokazuje diff, NIC nie zapisuje
  python3 apply_sync.py --write    # zapisuje zmiany do plików
"""
import argparse
import difflib
import urllib.parse
from collections import defaultdict
from pathlib import Path

from baseline import load_baseline_rows
from html_engine import find_price_tier_rows_block, find_price_tier_badge, replace_span, replace_block
from row_generator import generate_rows_block, compute_badge_price

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")


def group_rows_by_zabieg(rows):
    grouped = defaultdict(list)
    for r in rows:
        grouped[r["zabieg"]].append(r)
    return grouped


def apply_group_to_html(html: str, h3_prefix: str, rows: list[dict], row_indent: int, closing_indent: int):
    """Zwraca (nowy_html, zmieniono: bool)."""
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
    parser.add_argument("--write", action="store_true", help="zapisz zmiany do plików (domyślnie: tylko podgląd)")
    args = parser.parse_args()

    rows = load_baseline_rows()
    grouped = group_rows_by_zabieg(rows)

    any_changes = False

    # --- cennik/index.html ---
    cennik_path = ROOT / "cennik" / "index.html"
    cennik_html = cennik_path.read_text(encoding="utf-8")
    original_cennik_html = cennik_html
    for zabieg, zabieg_rows in grouped.items():
        cennik_html, changed = apply_group_to_html(cennik_html, zabieg, zabieg_rows, row_indent=16, closing_indent=16)

    if show_diff("cennik/index.html", original_cennik_html, cennik_html):
        any_changes = True
        if args.write:
            cennik_path.write_text(cennik_html, encoding="utf-8")

    # --- podstrony zabiegów ---
    urls_by_zabieg = {r["zabieg"]: r["url"] for r in rows}
    for zabieg, zabieg_rows in grouped.items():
        url = urls_by_zabieg[zabieg]
        rel = urllib.parse.unquote(url.lstrip("/"))
        path = ROOT / rel / "index.html"
        html = path.read_text(encoding="utf-8")
        original_html = html
        html, changed = apply_group_to_html(html, "Zabieg", zabieg_rows, row_indent=14, closing_indent=12)

        if show_diff(f"{rel}/index.html", original_html, html):
            any_changes = True
            if args.write:
                path.write_text(html, encoding="utf-8")

    print(f"\n\n{'WYNIK: zapisano zmiany.' if (any_changes and args.write) else ('WYNIK: znaleziono zmiany (tryb podglądu — nic nie zapisano).' if any_changes else 'WYNIK: brak zmian, wszystko już zgodne.')}")


if __name__ == "__main__":
    main()
