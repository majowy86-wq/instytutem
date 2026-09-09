#!/usr/bin/env python3
"""Wstawia 2 całkiem nowe podgrupy, których brakowało w jednym z dwóch miejsc:
  - LightSheer: "Pakiety Elastyczne" -> dodane na podstronę (przed "Przygotowanie do zabiegu")
  - Endermologia LPG® Alliance: "Strój zabiegowy" -> dodane do /cennik (po "Sesje zabiegowe", przed "Pakiety")

Użycie:
  python3 insert_missing_subgroups.py            # podgląd
  python3 insert_missing_subgroups.py --write    # zapis
"""
import argparse
import difflib
from pathlib import Path

from baseline_phase2 import load_phase2_baseline_rows
from subgroup_generator import generate_subgroup_block, SUBPAGE_INDENTS, CENNIK_NESTED_INDENTS

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")


def insert_before_marker(html: str, marker: str, new_block: str) -> str:
    """Wstawia new_block PRZED elementem <details> który ZAWIERA marker (nie przed samym
    markerem — inaczej ląduje wewnątrz już otwartego summary/label, korumpując strukturę)."""
    pos = html.find(marker)
    if pos == -1:
        raise ValueError(f"Nie znaleziono miejsca wstawienia: {marker!r}")
    details_start = html.rfind("<details", 0, pos)
    if details_start == -1:
        raise ValueError(f"Nie znaleziono otaczającego <details> dla {marker!r}")
    line_start = html.rfind("\n", 0, details_start) + 1
    return html[:line_start] + new_block + "\n" + html[line_start:]


def show_diff(label, old, new):
    if old == new:
        return False
    diff = list(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                      fromfile=f"{label} (przed)", tofile=f"{label} (po)"))
    print(f"\n{'='*70}\n{label}\n{'='*70}")
    print("".join(diff))
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    rows = load_phase2_baseline_rows()

    # --- 1. LightSheer: "Pakiety Elastyczne" -> podstrona ---
    pakiety_elastyczne = [r for r in rows if r["zabieg"] == "Epilacja laserowa LightSheer®" and r["podgrupa"] == "Pakiety Elastyczne"]
    subpage_path = ROOT / "zabiegi/depilacja-laserowa-plock-lightsheer/index.html"
    subpage_html = subpage_path.read_text(encoding="utf-8")
    new_block = generate_subgroup_block("Pakiety Elastyczne", pakiety_elastyczne, SUBPAGE_INDENTS)
    new_subpage_html = insert_before_marker(subpage_html, '<h3 class="treatment-accordion-q">Przygotowanie do zabiegu</h3>', new_block)
    changed1 = show_diff("zabiegi/depilacja-laserowa-plock-lightsheer/index.html", subpage_html, new_subpage_html)

    # --- 2. Endermologia LPG® Alliance: "Strój zabiegowy" -> /cennik ---
    stroj = [r for r in rows if r["zabieg"] == "Endermologia LPG® Alliance" and r["podgrupa"] == "Strój zabiegowy"]
    cennik_path = ROOT / "cennik/index.html"
    cennik_html = cennik_path.read_text(encoding="utf-8")
    new_block2 = generate_subgroup_block("Strój zabiegowy", stroj, CENNIK_NESTED_INDENTS)
    # marker: druga zagnieżdżona <details> w obrębie Endermologia LPG Alliance to "Pakiety"
    end_start = cennik_html.find("Endermologia LPG® Alliance<a")
    pakiety_marker_pos = cennik_html.find('<h3 class="treatment-accordion-q">Pakiety</h3>', end_start)
    marker = cennik_html[pakiety_marker_pos:pakiety_marker_pos + 10]  # unikalny fragment lokalny
    # bezpieczniej: wstaw bezpośrednio po pozycji, nie po fragmencie tekstu (by uniknąć kolizji nazw "Pakiety" gdzie indziej)
    line_start = cennik_html.rfind("\n", 0, cennik_html.rfind("<details", end_start, pakiety_marker_pos)) + 1
    new_cennik_html = cennik_html[:line_start] + new_block2 + "\n" + cennik_html[line_start:]
    changed2 = show_diff("cennik/index.html", cennik_html, new_cennik_html)

    if args.write:
        if changed1:
            subpage_path.write_text(new_subpage_html, encoding="utf-8")
        if changed2:
            cennik_path.write_text(new_cennik_html, encoding="utf-8")
        print("\nWYNIK: zapisano.")
    else:
        print("\nWYNIK: podgląd — nic nie zapisano.")


if __name__ == "__main__":
    main()
