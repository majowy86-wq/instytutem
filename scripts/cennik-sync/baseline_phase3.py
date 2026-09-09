#!/usr/bin/env python3
"""Faza 3: pozycje istniejące WYŁĄCZNIE w /cennik — bez własnej podstrony zabiegu.
Synchronizacja dotyczy tylko /cennik (jedno miejsce), źródłem prawdy jest samo /cennik
(nie ma z czym go konfrontować). Mikrodermabrazja i Plasma™ świadomie POMINIĘTE:
Mikrodermabrazja — zero dopasowania w Fresha, zablokowana (patrz PLAN.md);
Plasma™ — miała realną podstronę, naprawiona i przeniesiona do bazy Fazy 1."""
import json
from pathlib import Path

EXTRACTED_PATH = Path(__file__).parent / "cennik_extracted.json"
EXCLUDED = {"Mikrodermabrazja"}  # brak jakichkolwiek danych — zablokowane, patrz PLAN.md

TREATMENTS = [
    "Egzosomy i PDRN",
    "Tropokolagen – Atelokolagenowa odbudowa skóry",
    "Rytuały Neuro-Kosmetyczne",
    "Masaż endomodelujący twarzy",
    "Karboksyterapia bezigłowa CO2",
]


def load_phase3_baseline_rows():
    data = json.loads(EXTRACTED_PATH.read_text(encoding="utf-8"))
    rows = []
    for s in data:
        for g in s["groups"]:
            if g["tierName"] not in TREATMENTS:
                continue
            if g["tierName"] in EXCLUDED:
                continue

            # podgrupa bazowa = nazwa zabiegu (odpowiednik "Zabieg" z Fazy 1/2),
            # dla płaskich pozycji bez zagnieżdżeń
            for r in g["rows"]:
                rows.append({
                    "zabieg": g["tierName"], "podgrupa": "Zabieg",
                    "wariant": r["name"], "czas": r["duration"], "cena": r["price"],
                    "offerItemId": r["offerItemId"], "packageId": "", "promo": r["promo"],
                    "url": "",
                })
            for nt in g["nestedTiers"]:
                for r in nt["rows"]:
                    rows.append({
                        "zabieg": g["tierName"], "podgrupa": nt["tierName"],
                        "wariant": r["name"], "czas": r["duration"], "cena": r["price"],
                        "offerItemId": r["offerItemId"], "packageId": "", "promo": r["promo"],
                        "url": "",
                    })
    return rows


if __name__ == "__main__":
    rows = load_phase3_baseline_rows()
    print(f"Łącznie wierszy Fazy 3: {len(rows)}")
    for r in rows:
        print(" ", r["zabieg"][:35], "|", r["podgrupa"], "|", r["wariant"][:40], "|", r["cena"])
