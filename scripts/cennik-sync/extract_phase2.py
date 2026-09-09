#!/usr/bin/env python3
"""Faza 2: wyciąga PEŁNĄ strukturę (podgrupy + wiersze, w tym pakiety) dla 6 zabiegów
ze złożoną strukturą, zarówno z /cennik jak i z każdej podstrony osobno — do analizy
przed zaprojektowaniem finalnego mapowania podgrup."""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")

TREATMENTS = {
    "Epilacja laserowa LightSheer®": "zabiegi/depilacja-laserowa-plock-lightsheer",
    "Endermologia LPG® Alliance": "zabiegi/endermologia-plock-lpg-alliance",
    "Endermologia Twarzy LPG® Endermolift™": "zabiegi/endermologia-twarzy-plock-lpg-endermolift",
    "Kriolipoliza cooltech®": "zabiegi/kriolipoliza-plock-cooltech",
    "Fibryna i osocze bogatopłytkowe": "fibryna-i-osocze-bogatoplytkowe",
    "Mezoterapia bezigłowa": "zabiegi/mezoterapia-bezigłowa",
}


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
    offer_id, package_id, cta_label = "", "", ""
    if buy:
        a = buy.find("a")
        if a and a.get("href"):
            href = a["href"]
            m = re.search(r"offerItemId=([^&]+)", href)
            if m:
                offer_id = m.group(1).replace("%3A", ":")
            m2 = re.search(r"packages\?id=([^&]+)", href)
            if m2:
                package_id = m2.group(1)
        title = a.find("span", class_="treatment-card-cta-title-wrap") if a else None
        cta_label = title.find("span").get_text(strip=True) if title else ""
    promo_badge = row_div.find("span", class_="promo-badge")
    promo = promo_badge.get_text(strip=True) if promo_badge else ""
    return {
        "name": name, "duration": duration, "price": price,
        "offerItemId": offer_id, "packageId": package_id, "ctaLabel": cta_label, "promo": promo,
    }


def parse_subpage_groups(html):
    """Zwraca listę {name, badge, rows} dla WSZYSTKICH top-level <details class="price-tier">
    w sekcji #cennik (płaska lista, bez zagnieżdżeń — tak jak podstrony to organizują)."""
    soup = BeautifulSoup(html, "html.parser")
    cennik = soup.find("section", id="cennik")
    groups = []
    for details in cennik.find_all("details", class_="price-tier"):
        h3 = details.find("h3", class_="treatment-accordion-q")
        badge = details.find("span", class_="price-tier-badge")
        rows_div = details.find("div", class_="price-tier-rows")
        rows = [parse_row(d) for d in rows_div.find_all("div", class_="price-row", recursive=False)] if rows_div else []
        groups.append({
            "name": h3.get_text(strip=True) if h3 else "",
            "badge": badge.get_text(strip=True) if badge else "",
            "rows": rows,
        })
    return groups


def parse_cennik_nested_group(cennik_html, treatment_name):
    """Parsuje bezpośrednio z surowego HTML /cennik (nie z cennik_extracted.json, żeby
    mieć packageId) — zwraca listę podgrup {name, badge, rows} dla danego zabiegu."""
    soup = BeautifulSoup(cennik_html, "html.parser")
    # znajdź OUTER <details> którego h3 zaczyna się od treatment_name
    outer = None
    for details in soup.find_all("details", class_="price-tier"):
        h3 = details.find("h3", class_="treatment-accordion-q", recursive=True)
        if h3 and h3.get_text(strip=True).startswith(treatment_name) and "accordion-info-link" in str(h3):
            outer = details
            break
    if outer is None:
        raise ValueError(f"Nie znaleziono grupy w /cennik: {treatment_name}")

    nested_container = outer.find("div", class_="price-tier-rows--nested")
    if nested_container is None:
        # brak zagnieżdżenia — traktuj jak płaską listę jednej "podgrupy" o nazwie zabiegu
        rows_div = outer.find("div", class_="price-tier-rows")
        rows = [parse_row(d) for d in rows_div.find_all("div", class_="price-row", recursive=False)]
        badge = outer.find("span", class_="price-tier-badge")
        return [{"name": treatment_name, "badge": badge.get_text(strip=True) if badge else "", "rows": rows}]

    subgroups = []
    # UWAGA: kontener zagnieżdżony bywa MIESZANY — luźne <div class="price-row"> (baza
    # zabiegu, bez własnej podgrupy) obok właściwych <details> podgrup (potwierdzone na
    # Mezoterapii bezigłowej: 1 luźny wiersz + 1 zagnieżdżona podgrupa "Pakiety łączone").
    loose_rows = [parse_row(d) for d in nested_container.find_all("div", class_="price-row", recursive=False)]
    if loose_rows:
        badge = outer.find("span", class_="price-tier-badge")
        subgroups.append({"name": treatment_name, "badge": badge.get_text(strip=True) if badge else "", "rows": loose_rows})

    for sub_details in nested_container.find_all("details", class_="price-tier", recursive=False):
        h3 = sub_details.find("h3", class_="treatment-accordion-q")
        badge = sub_details.find("span", class_="price-tier-badge")
        rows_div = sub_details.find("div", class_="price-tier-rows")
        rows = [parse_row(d) for d in rows_div.find_all("div", class_="price-row", recursive=False)] if rows_div else []
        subgroups.append({
            "name": h3.get_text(strip=True) if h3 else "",
            "badge": badge.get_text(strip=True) if badge else "",
            "rows": rows,
        })
    return subgroups


def main():
    cennik_html = (ROOT / "cennik" / "index.html").read_text(encoding="utf-8")

    output = {}
    for name, rel in TREATMENTS.items():
        html = (ROOT / rel / "index.html").read_text(encoding="utf-8")
        subpage_groups = parse_subpage_groups(html)
        cennik_subgroups = parse_cennik_nested_group(cennik_html, name)

        output[name] = {
            "subpageRel": rel,
            "subpage_groups": subpage_groups,
            "cennik_subgroups": cennik_subgroups,
        }

    out_path = Path(__file__).parent / "phase2_extracted.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Zapisano: {out_path}")

    for name, d in output.items():
        print(f"\n=== {name} ===")
        print("  PODSTRONA:", [(g["name"], len(g["rows"])) for g in d["subpage_groups"]])
        print("  CENNIK:   ", [(g["name"], len(g["rows"])) for g in d["cennik_subgroups"]])


if __name__ == "__main__":
    main()
