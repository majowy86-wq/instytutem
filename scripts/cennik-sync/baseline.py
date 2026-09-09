#!/usr/bin/env python3
"""Buduje POPRAWIONĄ bazową listę wierszy dla Fazy 1.

Zasada (ustalona z użytkownikiem): tekst (nazwa/czas trwania) z PODSTRONY zabiegu jest
zawsze kanoniczny — /cennik bywa napisane inną stylistyką (nawiasy zamiast myślnika,
skrócone/wydłużone opisy) dla dokładnie tej samej pozycji. Wiersze istniejące TYLKO
w /cennik (nigdy nie dodane do podstrony) są dołączane na końcu listy danego zabiegu —
przy synchronizacji trafią też na podstronę.

Dopasowanie podstrona<->cennik jest POZYCYJNE w obrębie grupy (nie po offerItemId,
bo jeden offerItemId bywa dzielony przez kilka różnych, nazwanych wierszy — potwierdzone
na Dermalux/RF/Bloomea/Lenisna itd.) — zweryfikowane, że kolejność wierszy jest zawsze
identyczna tam, gdzie oba źródła mają tę samą liczbę pozycji.
"""
import json
import re
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")
EXTRACTED_PATH = Path(__file__).parent / "cennik_extracted.json"
EXCLUDED = set()  # LUMIVEX® - laser tulowy: struktura naprawiona, dołączony do Fazy 1


def _parse_subpage_row(row_div):
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


def _get_subpage_rows(subpage_url: str):
    # subpage_url to oryginalny href z /cennik (np. "../zabiegi/modeling-skory-bloomea")
    rel = urllib.parse.unquote(subpage_url.replace("../", "", 1))
    html = (ROOT / rel / "index.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    cennik = soup.find("section", id="cennik")
    h3s = cennik.find_all("h3", class_="treatment-accordion-q")
    zabieg_h3 = next(h for h in h3s if h.get_text(strip=True) == "Zabieg")
    details = zabieg_h3.find_parent("details", class_="price-tier")
    rows_div = details.find("div", class_="price-tier-rows")
    return [_parse_subpage_row(d) for d in rows_div.find_all("div", class_="price-row", recursive=False)]


def load_baseline_rows():
    """Zwraca listę dictów: zabieg, wariant, czas, cena, offerItemId, url."""
    data = json.loads(EXTRACTED_PATH.read_text(encoding="utf-8"))
    rows = []
    for s in data:
        for g in s["groups"]:
            if not (g["subpageUrl"] and not g["nestedTiers"] and g["tierName"] not in EXCLUDED):
                continue

            zabieg = g["tierName"]
            url = g["subpageUrl"].replace("../", "/")
            cennik_rows = g["rows"]
            subpage_rows = _get_subpage_rows(g["subpageUrl"])

            # prefiks: tekst z podstrony (kanoniczny), cena też z podstrony —
            # obie strony BUDOWAŁEM z tych samych danych Fresha, więc cena powinna się zgadzać;
            # jeśli mimo to się różni, to prawdziwy rozjazd do wykrycia przy następnym sprawdzeniu Fresha
            n = min(len(subpage_rows), len(cennik_rows))
            for i in range(n):
                sp = subpage_rows[i]
                rows.append({
                    "zabieg": zabieg,
                    "wariant": sp["name"],
                    "czas": sp["duration"],
                    "cena": sp["price"],
                    "offerItemId": sp["offerItemId"] or cennik_rows[i]["offerItemId"],
                    "url": url,
                })

            # nadmiarowe wiersze istniejące TYLKO w /cennik — dołączane z danymi cennika
            for extra in cennik_rows[n:]:
                rows.append({
                    "zabieg": zabieg,
                    "wariant": extra["name"],
                    "czas": extra["duration"],
                    "cena": extra["price"],
                    "offerItemId": extra["offerItemId"],
                    "url": url,
                })

    return rows


if __name__ == "__main__":
    rows = load_baseline_rows()
    print(f"Łącznie wierszy bazowych: {len(rows)}")
