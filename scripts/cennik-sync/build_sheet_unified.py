#!/usr/bin/env python3
"""Buduje JEDEN, zunifikowany arkusz ze wszystkimi zabiegami (Faza 1 + 2 + 3),
zastępując poprzedni podział na osobne zakładki "Faza 1"/"Faza 2"."""
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import gspread
from google.oauth2.service_account import Credentials

from baseline import load_baseline_rows
from baseline_phase2 import load_phase2_baseline_rows
from baseline_phase3 import load_phase3_baseline_rows

BASE = Path(__file__).parent
CREDS_PATH = BASE.parent.parent / ".secrets" / "google-service-account.json"
SHEET_ID = "1XNXfThupDPVX6UVDJ6JCsfsSa9_JTEHa2OkhSEuhNzo"
TAB_NAME = "Cennik — wszystkie zabiegi"
OLD_TABS_TO_REMOVE = ["Faza 1 — Zabiegi", "Faza 2 — Zabiegi złożone"]

HEADERS = [
    "Zabieg", "Podgrupa", "Wariant", "Czas trwania",
    "Cena na stronie", "Cena Fresha", "Zgodność",
    "offerItemId", "packageId", "Promo", "URL podstrony",
]


def formula_for_row(i):
    return (
        f'=IF(AND(H{i}="";I{i}="");"— brak w Fresha";'
        f'IF(TRIM(REGEXREPLACE(E{i};"[^0-9]";""))=TRIM(REGEXREPLACE(F{i};"[^0-9]";""))'
        f';"✅ zgodne";"⚠️ rozjazd"))'
    )


def collect_all_rows():
    rows = []
    for r in load_baseline_rows():  # Faza 1
        rows.append({
            "zabieg": r["zabieg"], "podgrupa": "Zabieg", "wariant": r["wariant"],
            "czas": r["czas"], "cena": r["cena"], "offerItemId": r["offerItemId"],
            "packageId": "", "promo": "", "url": r["url"],
        })
    for r in load_phase2_baseline_rows():  # Faza 2
        rows.append({
            "zabieg": r["zabieg"], "podgrupa": r["podgrupa"], "wariant": r["wariant"],
            "czas": r["czas"], "cena": r["cena"], "offerItemId": r["offerItemId"],
            "packageId": r["packageId"], "promo": r.get("promo", ""), "url": r["url"],
        })
    for r in load_phase3_baseline_rows():  # Faza 3
        rows.append({
            "zabieg": r["zabieg"], "podgrupa": r["podgrupa"], "wariant": r["wariant"],
            "czas": r["czas"], "cena": r["cena"], "offerItemId": r["offerItemId"],
            "packageId": r["packageId"], "promo": r.get("promo", ""), "url": r["url"],
        })
    return rows


def main():
    rows = collect_all_rows()
    body = [
        [r["zabieg"], r["podgrupa"], r["wariant"], r["czas"], r["cena"], r["cena"],
         r["offerItemId"], r["packageId"], r["promo"], r["url"]]
        for r in rows
    ]
    print(f"Przygotowano {len(body)} wierszy łącznie (Faza 1+2+3).")

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)

    try:
        ws = sh.worksheet(TAB_NAME)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=TAB_NAME, rows=300, cols=10)

    ws.clear()
    ws.update("A1", [HEADERS])

    last_row = len(body) + 1
    left_cols = [r[:6] for r in body]
    right_cols = [r[6:] for r in body]
    ws.update(f"A2:F{last_row}", left_cols, value_input_option="RAW")
    ws.update(f"H2:K{last_row}", right_cols, value_input_option="RAW")

    formulas = [[formula_for_row(i)] for i in range(2, last_row + 1)]
    ws.update(f"G2:G{last_row}", formulas, value_input_option="USER_ENTERED")

    ws.freeze(rows=1, cols=2)
    ws.format("A1:K1", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}})
    ws.format(f"A2:B{last_row}", {"textFormat": {"bold": True}})

    widths = {"A": 280, "B": 200, "C": 280, "D": 220, "E": 110, "F": 110, "G": 130, "H": 100, "I": 220, "J": 140, "K": 260}
    requests = []
    sheet_id = ws.id
    col_map = {c: i for i, c in enumerate("ABCDEFGHIJK")}
    for col, width in widths.items():
        idx = col_map[col]
        requests.append({"updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": idx, "endIndex": idx + 1},
            "properties": {"pixelSize": width}, "fields": "pixelSize"}})
    sh.batch_update({"requests": requests})

    # przenieś nową zakładkę na pierwsze miejsce
    sh.reorder_worksheets([ws] + [w for w in sh.worksheets() if w.id != ws.id])

    # usuń stare, rozdzielone zakładki
    for name in OLD_TABS_TO_REMOVE:
        try:
            old = sh.worksheet(name)
            sh.del_worksheet(old)
            print(f"Usunięto starą zakładkę: {name}")
        except gspread.WorksheetNotFound:
            pass

    print(f"Zapisano {len(body)} wierszy do zakładki '{TAB_NAME}'.")


if __name__ == "__main__":
    main()
