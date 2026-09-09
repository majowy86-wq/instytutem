#!/usr/bin/env python3
"""Czyta AKTUALNY stan zunifikowanego arkusza Google — to jest PRAWDZIWE źródło danych
dla synchronizacji (w przeciwieństwie do baseline*.py, które tylko budują arkusz z plików
za pierwszym razem). Każda kolejna synchronizacja MUSI iść przez ten moduł."""
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import gspread
from google.oauth2.service_account import Credentials

BASE = Path(__file__).parent
CREDS_PATH = BASE.parent.parent / ".secrets" / "google-service-account.json"
SHEET_ID = "1XNXfThupDPVX6UVDJ6JCsfsSa9_JTEHa2OkhSEuhNzo"
TAB_NAME = "Cennik — wszystkie zabiegi"


def get_worksheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    return sh.worksheet(TAB_NAME)


def read_all_rows():
    """Zwraca listę dictów: zabieg, podgrupa, wariant, czas, cena, cena_fresha, zgodnosc,
    offerItemId, packageId, promo, url — dokładnie to, co jest AKTUALNIE w arkuszu."""
    ws = get_worksheet()
    values = ws.get_all_values()
    rows = []
    for row in values[1:]:  # pomiń nagłówek
        row = row + [""] * (11 - len(row))  # dopełnij, gdyby wiersz był krótszy
        zabieg = row[0].strip()
        if not zabieg:
            continue  # pusty wiersz — pomiń
        rows.append({
            "zabieg": zabieg,
            "podgrupa": row[1].strip(),
            "wariant": row[2].strip(),
            "czas": row[3].strip(),
            "cena": row[4].strip(),
            "cena_fresha": row[5].strip(),
            "zgodnosc": row[6].strip(),
            "offerItemId": row[7].strip(),
            "packageId": row[8].strip(),
            "promo": row[9].strip(),
            "url": row[10].strip(),
        })
    return rows


if __name__ == "__main__":
    rows = read_all_rows()
    print(f"Odczytano {len(rows)} wierszy z arkusza.")
    mismatches = [r for r in rows if r["zgodnosc"].startswith("⚠️")]
    print(f"Rozjazdów cena-na-stronie vs Fresha: {len(mismatches)}")
    for r in mismatches:
        print(" ", r["zabieg"], "|", r["wariant"], "|", r["cena"], "vs Fresha:", r["cena_fresha"])
