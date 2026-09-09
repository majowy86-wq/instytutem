#!/usr/bin/env python3
"""Faza 1: zapisuje poprawioną bazę (baseline.py) do arkusza Google."""
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import gspread
from google.oauth2.service_account import Credentials

from baseline import load_baseline_rows

BASE = Path(__file__).parent
CREDS_PATH = BASE.parent.parent / ".secrets" / "google-service-account.json"
SHEET_ID = "1XNXfThupDPVX6UVDJ6JCsfsSa9_JTEHa2OkhSEuhNzo"

HEADERS = [
    "Zabieg",
    "Wariant",
    "Czas trwania",
    "Cena na stronie",
    "Cena Fresha",
    "Zgodność",
    "offerItemId",
    "URL podstrony",
]


def formula_for_row(i):
    # locale pl_PL => Google Sheets wymaga średników zamiast przecinków jako separatorów argumentów
    # G{i} = offerItemId — puste, gdy zabieg nie ma odpowiednika w Fresha (np. Kwas Hialuronowy)
    return (
        f'=IF(G{i}="";"— brak w Fresha";'
        f'IF(TRIM(REGEXREPLACE(D{i};"[^0-9]";""))=TRIM(REGEXREPLACE(E{i};"[^0-9]";""))'
        f';"✅ zgodne";"⚠️ rozjazd"))'
    )


def main():
    baseline_rows = load_baseline_rows()
    rows = [
        [r["zabieg"], r["wariant"], r["czas"], r["cena"], r["cena"], r["offerItemId"], r["url"]]
        for r in baseline_rows
    ]
    print(f"Przygotowano {len(rows)} wierszy do zapisu.")

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.sheet1
    ws.update_title("Faza 1 — Zabiegi")

    ws.clear()
    ws.update("A1", [HEADERS])

    last_row = len(rows) + 1

    # A-E i G-H jako RAW — inaczej pl_PL locale "poprawia" tekst typu "599 zł" (zjada spację)
    left_cols = [r[:5] for r in rows]      # Zabieg, Wariant, Czas, Cena strona, Cena Fresha
    right_cols = [r[5:] for r in rows]     # offerItemId, URL
    ws.update(f"A2:E{last_row}", left_cols, value_input_option="RAW")
    ws.update(f"G2:H{last_row}", right_cols, value_input_option="RAW")

    # F jako prawdziwa formuła (USER_ENTERED), osobno — wymaga interpretacji "="
    formulas = [[formula_for_row(i)] for i in range(2, last_row + 1)]
    ws.update(f"F2:F{last_row}", formulas, value_input_option="USER_ENTERED")

    # formatowanie: zamrożony nagłówek + pogrubienie
    ws.freeze(rows=1)
    ws.format("A1:H1", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}})
    ws.format("A2:A1000", {"textFormat": {"bold": True}})

    print(f"Zapisano {len(rows)} wierszy do arkusza '{ws.title}'.")


if __name__ == "__main__":
    main()
