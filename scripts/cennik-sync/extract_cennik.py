#!/usr/bin/env python3
"""Wyciąga pełną strukturę cennika z /cennik/index.html do JSON — krok 1 budowy arkusza."""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

CENNIK_PATH = Path(__file__).parent.parent.parent / "cennik" / "index.html"
OUT_PATH = Path(__file__).parent / "cennik_extracted.json"


def parse_price_row(row_div):
    """Zwraca dict dla jednego <div class="price-row">."""
    p_tags = row_div.find_all("p", recursive=False)
    name_p = p_tags[0] if p_tags else None
    name = ""
    duration = ""
    if name_p:
        span = name_p.find("span")
        duration_text = span.get_text(strip=True) if span else ""
        duration = duration_text.lstrip("·").strip()
        # nazwa = tekst przed <span>, bez tekstu spana
        name = name_p.get_text(strip=True)
        if duration_text:
            name = name.replace(duration_text, "").strip()

    price_text = ""
    offer_item_id = ""
    buy = row_div.find("span", class_="price-row-buy")
    if buy:
        price_p = buy.find("p")
        if price_p:
            price_text = price_p.get_text(strip=True)
        a = buy.find("a", class_="treatment-card-cta")
        if a and a.get("href"):
            m = re.search(r"offerItemId=([^&]+)", a["href"])
            if m:
                offer_item_id = m.group(1).replace("%3A", ":")
    else:
        # brak CTA — druga <p> to cena
        if len(p_tags) > 1:
            price_text = p_tags[1].get_text(strip=True)

    promo_badge = row_div.find("span", class_="promo-badge")
    promo = promo_badge.get_text(strip=True) if promo_badge else ""

    return {
        "name": name,
        "duration": duration,
        "price": price_text,
        "offerItemId": offer_item_id,
        "promo": promo,
    }


def parse_price_tier(details_tag):
    h3 = details_tag.find("h3", class_="treatment-accordion-q")
    tier_name = h3.contents[0].strip() if h3 and h3.contents else (h3.get_text(strip=True) if h3 else "")
    link = h3.find("a", class_="accordion-info-link") if h3 else None
    subpage_url = link["href"] if link and link.get("href") else ""
    badge = details_tag.find("span", class_="price-tier-badge")
    badge_price = badge.get_text(strip=True) if badge else ""

    rows = []
    nested_tiers = []
    rows_container = details_tag.find("div", class_="price-tier-rows")
    if rows_container:
        for child in rows_container.find_all(recursive=False):
            if child.name == "div" and "price-row" in child.get("class", []):
                rows.append(parse_price_row(child))
            elif child.name == "details" and "price-tier" in child.get("class", []):
                nested_tiers.append(parse_price_tier(child))

    return {
        "tierName": tier_name,
        "subpageUrl": subpage_url,
        "badgePrice": badge_price,
        "rows": rows,
        "nestedTiers": nested_tiers,
    }


def main():
    html = CENNIK_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")

    sections = []
    main_el = soup.find("main")

    for section in main_el.find_all("section", recursive=False):
        h2 = section.find("h2")
        section_title = h2.get_text(strip=True) if h2 else ""
        price_list = section.find("div", class_="price-list")
        if not price_list:
            continue

        groups = []
        current_subheading = ""
        for child in price_list.find_all(recursive=False):
            if child.name == "p" and "price-list-subheading" in child.get("class", []):
                current_subheading = child.get_text(strip=True)
            elif child.name == "details" and "price-tier" in child.get("class", []):
                tier = parse_price_tier(child)
                tier["subheading"] = current_subheading
                groups.append(tier)

        if groups:
            sections.append({
                "sectionTitle": section_title,
                "sectionId": section.get("id", ""),
                "groups": groups,
            })

    OUT_PATH.write_text(json.dumps(sections, ensure_ascii=False, indent=2), encoding="utf-8")

    total_rows = sum(
        len(g["rows"]) + sum(len(nt["rows"]) for nt in g["nestedTiers"])
        for s in sections for g in s["groups"]
    )
    total_groups = sum(len(s["groups"]) for s in sections)
    print(f"Sekcje: {len(sections)}")
    print(f"Grupy (pozycje cennikowe): {total_groups}")
    print(f"Łączna liczba wierszy (wariantów): {total_rows}")
    print(f"Zapisano do: {OUT_PATH}")


if __name__ == "__main__":
    main()
