#!/usr/bin/env python3
"""Buduje bazowe wiersze Fazy 2 (6 zabiegów ze złożoną strukturą, w tym pakiety)
na podstawie phase2_extracted.json + jawnej mapy podgrup (phase2_mapping.py).

Zasada tożsama z Fazą 1: tekst (nazwa/czas) z PODSTRONY wygrywa dla podgrup obecnych
w obu miejscach; podgrupy istniejące tylko w jednym miejscu trafiają też do drugiego.
"""
import json
from pathlib import Path

from phase2_mapping import TREATMENTS, CENNIK_NAME_OVERRIDE

EXTRACTED_PATH = Path(__file__).parent / "phase2_extracted.json"


def load_phase2_baseline_rows():
    """Zwraca listę dictów: zabieg, podgrupa, wariant, czas, cena, offerItemId,
    packageId, promo, url — jedna na wariant/pakiet."""
    data = json.loads(EXTRACTED_PATH.read_text(encoding="utf-8"))
    rows = []

    for zabieg, config in TREATMENTS.items():
        url = "/" + config["subpageRel"]
        extracted = data[zabieg]
        subpage_by_name = {g["name"]: g for g in extracted["subpage_groups"]}
        cennik_by_name = {g["name"]: g for g in extracted["cennik_subgroups"]}

        for canonical_name, source in config["subgroups"]:
            cennik_name = CENNIK_NAME_OVERRIDE.get((zabieg, canonical_name), canonical_name)

            if source == "both":
                sub_rows = subpage_by_name[canonical_name]["rows"]
                cen_rows = cennik_by_name[cennik_name]["rows"]
                n = min(len(sub_rows), len(cen_rows))
                for i in range(n):
                    sp = sub_rows[i]
                    rows.append({
                        "zabieg": zabieg, "podgrupa": canonical_name,
                        "wariant": sp["name"], "czas": sp["duration"], "cena": sp["price"],
                        "offerItemId": sp["offerItemId"] or cen_rows[i]["offerItemId"],
                        "packageId": sp["packageId"] or cen_rows[i]["packageId"],
                        "promo": sp["promo"] or cen_rows[i]["promo"],
                        "url": url,
                    })
                # nadmiarowe wiersze istniejące tylko w /cennik w obrębie tej samej podgrupy
                for extra in cen_rows[n:]:
                    rows.append({
                        "zabieg": zabieg, "podgrupa": canonical_name,
                        "wariant": extra["name"], "czas": extra["duration"], "cena": extra["price"],
                        "offerItemId": extra["offerItemId"], "packageId": extra["packageId"],
                        "promo": extra["promo"], "url": url,
                    })

            elif source == "cennik_only":
                for r in cennik_by_name[cennik_name]["rows"]:
                    rows.append({
                        "zabieg": zabieg, "podgrupa": canonical_name,
                        "wariant": r["name"], "czas": r["duration"], "cena": r["price"],
                        "offerItemId": r["offerItemId"], "packageId": r["packageId"],
                        "promo": r["promo"], "url": url,
                    })

            elif source == "subpage_only":
                for r in subpage_by_name[canonical_name]["rows"]:
                    rows.append({
                        "zabieg": zabieg, "podgrupa": canonical_name,
                        "wariant": r["name"], "czas": r["duration"], "cena": r["price"],
                        "offerItemId": r["offerItemId"], "packageId": r["packageId"],
                        "promo": r["promo"], "url": url,
                    })

    return rows


if __name__ == "__main__":
    rows = load_phase2_baseline_rows()
    print(f"Łącznie wierszy Fazy 2: {len(rows)}")
    for r in rows:
        print(" ", r["zabieg"][:25], "|", r["podgrupa"], "|", r["wariant"], "|", r["czas"][:30], "|", r["cena"], "|", "pkg" if r["packageId"] else ("oid" if r["offerItemId"] else "-"))
