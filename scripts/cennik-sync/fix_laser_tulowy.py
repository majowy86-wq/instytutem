#!/usr/bin/env python3
"""Naprawia strukturę /laser-tulowy-plock — jedyną podstronę w projekcie, na której
7 wierszy cennika leżało luzem bez własnego <details class="price-tier"> (najstarszy
szablon w projekcie, sprzed ustalenia się standardowego wzorca). Opakowuje je w
dokładnie taki sam blok, jaki mają wszystkie pozostałe 26 podstron zabiegów."""
import argparse
import difflib
from pathlib import Path

from subgroup_generator import generate_subgroup_block, SUBPAGE_INDENTS

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")
PATH = ROOT / "laser-tulowy-plock" / "index.html"

ROWS = [
    {"zabieg": "Zabieg", "wariant": "Zabieg punktowy", "czas": "20 min", "cena": "od 299 zł", "offerItemId": "s:24468530", "packageId": "", "promo": ""},
    {"zabieg": "Zabieg", "wariant": "Dłonie", "czas": "45 min", "cena": "599 zł", "offerItemId": "s:24468530", "packageId": "", "promo": ""},
    {"zabieg": "Zabieg", "wariant": "Okolica oczu", "czas": "45 min", "cena": "799 zł", "offerItemId": "s:24468530", "packageId": "", "promo": ""},
    {"zabieg": "Zabieg", "wariant": "Szyja lub dekolt", "czas": "45 min", "cena": "899 zł", "offerItemId": "s:24468530", "packageId": "", "promo": ""},
    {"zabieg": "Zabieg", "wariant": "Twarz", "czas": "1 godz. i 5 min", "cena": "1199 zł", "offerItemId": "s:24468530", "packageId": "", "promo": ""},
    {"zabieg": "Zabieg", "wariant": "Twarz + szyja", "czas": "1 godz. i 20 min", "cena": "1499 zł", "offerItemId": "s:24468530", "packageId": "", "promo": ""},
    {"zabieg": "Zabieg", "wariant": "Twarz + szyja + dekolt", "czas": "1 godz. i 35 min", "cena": "1799 zł", "offerItemId": "s:24468530", "packageId": "", "promo": ""},
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    html = PATH.read_text(encoding="utf-8")
    cennik_start = html.find('id="cennik"')

    start = html.find('<div class="price-row"><p>Zabieg punktowy', cennik_start)
    if start == -1:
        raise SystemExit("Nie znaleziono luźnych wierszy — może już naprawione?")
    line_start = html.rfind("\n", 0, start) + 1

    end_marker = '<div class="price-row"><p>Twarz + szyja + dekolt'
    end_row_start = html.find(end_marker, cennik_start)
    end_row_end = html.find("</div>", end_row_start) + len("</div>")
    # koniec zamiany = zaraz po ostatnim wierszu (przed jego własnym \n)
    old_block = html[line_start:end_row_end]

    new_block = generate_subgroup_block("Zabieg", ROWS, SUBPAGE_INDENTS)
    new_html = html[:line_start] + new_block + html[end_row_end:]

    diff = list(difflib.unified_diff(
        html.splitlines(keepends=True), new_html.splitlines(keepends=True),
        fromfile="laser-tulowy-plock (przed)", tofile="laser-tulowy-plock (po)",
    ))
    print("".join(diff))

    if args.write:
        PATH.write_text(new_html, encoding="utf-8")
        print("\nZapisano.")
    else:
        print("\nTryb podglądu — nic nie zapisano.")


if __name__ == "__main__":
    main()
