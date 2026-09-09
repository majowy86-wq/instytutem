#!/usr/bin/env python3
"""Poprawiony raport różnic cennik-vs-podstrona: dopasowuje wiersze pozycyjnie w obrębie
tej samej grupy (zamiast po samym offerItemId, który bywa dzielony przez wiele wierszy)."""
import json
import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")
EXCLUDED = {"LUMIVEX® - laser tulowy (erbowo-szklany)"}


def parse_row(row_div):
    p_tags = row_div.find_all("p", recursive=False)
    name_p = p_tags[0] if p_tags else None
    name, duration = "", ""
    if name_p:
        span = name_p.find("span")
        duration = span.get_text(strip=True).lstrip("·").strip() if span else ""
        name = name_p.get_text(strip=True)
        if span:
            name = name.replace(span.get_text(strip=True), "").strip()
    buy = row_div.find("span", class_="price-row-buy")
    price = buy.find("p").get_text(strip=True) if buy else (p_tags[1].get_text(strip=True) if len(p_tags) > 1 else "")
    offer_id = ""
    if buy:
        a = buy.find("a")
        if a and a.get("href"):
            m = re.search(r"offerItemId=([^&]+)", a["href"])
            if m:
                offer_id = m.group(1).replace("%3A", ":")
    return {"name": name, "duration": duration, "price": price, "offerItemId": offer_id}


def get_subpage_zabieg_rows(html):
    soup = BeautifulSoup(html, "html.parser")
    cennik = soup.find("section", id="cennik")
    h3s = cennik.find_all("h3", class_="treatment-accordion-q")
    zabieg_h3 = next(h for h in h3s if h.get_text(strip=True) == "Zabieg")
    details = zabieg_h3.find_parent("details", class_="price-tier")
    rows_div = details.find("div", class_="price-tier-rows")
    return [parse_row(d) for d in rows_div.find_all("div", class_="price-row", recursive=False)]


def main():
    data = json.loads((Path(__file__).parent / "cennik_extracted.json").read_text(encoding="utf-8"))
    groups = [g for s in data for g in s["groups"] if g["subpageUrl"] and not g["nestedTiers"] and g["tierName"] not in EXCLUDED]

    total_diffs = 0
    for g in groups:
        name = g["tierName"]
        rel = urllib.parse.unquote(g["subpageUrl"].replace("../", "", 1))
        path = ROOT / rel / "index.html"
        html = path.read_text(encoding="utf-8")
        subpage_rows = get_subpage_zabieg_rows(html)
        cennik_rows = [{"name": r["name"], "duration": r["duration"], "price": r["price"], "offerItemId": r["offerItemId"]} for r in g["rows"]]

        printed_header = False

        def header():
            nonlocal printed_header
            if not printed_header:
                print(f"\n### {name}  ({rel})")
                printed_header = True

        # dopasowanie POZYCYJNE w obrębie grupy (kolejność wierszy jest identyczna, gdy nic nie brakuje)
        max_len = max(len(subpage_rows), len(cennik_rows))
        if len(subpage_rows) != len(cennik_rows):
            header()
            total_diffs += 1
            print(f"  LICZBA WIERSZY RÓŻNA: podstrona={len(subpage_rows)}, cennik={len(cennik_rows)}")
            print(f"    podstrona: {[r['name'] for r in subpage_rows]}")
            print(f"    cennik:    {[r['name'] for r in cennik_rows]}")
            continue  # dalsze pozycyjne porównanie nie ma sensu, gdy liczby się różnią

        for i in range(max_len):
            s_row = subpage_rows[i]
            c_row = cennik_rows[i]
            diffs = []
            if s_row["name"] != c_row["name"]:
                diffs.append(f"nazwa: podstrona={s_row['name']!r} | cennik={c_row['name']!r}")
            if s_row["duration"] != c_row["duration"]:
                diffs.append(f"czas: podstrona={s_row['duration']!r} | cennik={c_row['duration']!r}")
            if s_row["price"] != c_row["price"]:
                diffs.append(f"cena: podstrona={s_row['price']!r} | cennik={c_row['price']!r}")
            if s_row["offerItemId"] != c_row["offerItemId"]:
                diffs.append(f"offerItemId: podstrona={s_row['offerItemId']!r} | cennik={c_row['offerItemId']!r}")
            if diffs:
                header()
                total_diffs += 1
                print(f"  wiersz #{i+1}:")
                for d in diffs:
                    print(f"    {d}")

    print(f"\n\nŁĄCZNIE rozbieżnych wierszy: {total_diffs}")


if __name__ == "__main__":
    main()
