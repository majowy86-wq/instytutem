#!/usr/bin/env python3
"""Test walidacyjny: generuje bloki cennikowe z aktualnych danych arkusza (identycznych
dziś z tym, co jest na stronie) i porównuje bit w bit z tym, co faktycznie jest w plikach.
Jeśli się zgadza — silnik jest bezpieczny do użycia. Nic tu NIE zapisuje do plików."""
import json
import urllib.parse
from pathlib import Path

from html_engine import find_price_tier_rows_block, find_price_tier_badge
from row_generator import generate_rows_block, compute_badge_price

ROOT = Path("/Users/krzysztofmajchrzak/INSTYTUTem")
EXCLUDED = {"LUMIVEX® - laser tulowy (erbowo-szklany)"}  # stara struktura, poza zakresem Fazy 1


def load_groups():
    data = json.loads((Path(__file__).parent / "cennik_extracted.json").read_text(encoding="utf-8"))
    groups = []
    for s in data:
        for g in s["groups"]:
            if g["subpageUrl"] and not g["nestedTiers"] and g["tierName"] not in EXCLUDED:
                groups.append(g)
    return groups


def rows_for_engine(group_rows, zabieg_name):
    return [
        {
            "zabieg": zabieg_name,
            "wariant": r["name"],
            "czas": r["duration"],
            "cena": r["price"],
            "offerItemId": r["offerItemId"],
        }
        for r in group_rows
    ]


def test_cennik(groups):
    html = (ROOT / "cennik" / "index.html").read_text(encoding="utf-8")
    ok, fail = 0, 0
    for g in groups:
        name = g["tierName"]
        rows = rows_for_engine(g["rows"], name)
        try:
            start, end, content_start = find_price_tier_rows_block(html, name)
            current_inner = html[content_start:end - len("</div>")]
            generated_inner = generate_rows_block(rows, row_indent=16, closing_indent=16)
            b_start, b_end, current_badge = find_price_tier_badge(html, name)
            generated_badge = compute_badge_price(rows)
        except Exception as e:
            print(f"  BŁĄD lokalizacji [{name}]: {e}")
            fail += 1
            continue

        rows_match = current_inner == generated_inner
        badge_match = current_badge.strip() == generated_badge.strip()
        if rows_match and badge_match:
            ok += 1
        else:
            fail += 1
            print(f"  NIEZGODNE [{name}]:")
            if not rows_match:
                print(f"    wiersze: oczekiwano identyczne, różnią się")
                print(f"    OBECNE : {current_inner[:200]!r}")
                print(f"    NOWE   : {generated_inner[:200]!r}")
            if not badge_match:
                print(f"    badge: obecny={current_badge!r} vs wygenerowany={generated_badge!r}")
    print(f"cennik/index.html: {ok} OK, {fail} niezgodnych (z {len(groups)})")
    return fail == 0


def test_subpages(groups):
    ok, fail = 0, 0
    for g in groups:
        name = g["tierName"]
        rel = urllib.parse.unquote(g["subpageUrl"].replace("../", "", 1))
        path = ROOT / rel / "index.html"
        html = path.read_text(encoding="utf-8")
        rows = rows_for_engine(g["rows"], name)
        try:
            start, end, content_start = find_price_tier_rows_block(html, "Zabieg")
            current_inner = html[content_start:end - len("</div>")]
            generated_inner = generate_rows_block(rows, row_indent=14, closing_indent=12)
            b_start, b_end, current_badge = find_price_tier_badge(html, "Zabieg")
            generated_badge = compute_badge_price(rows)
        except Exception as e:
            print(f"  BŁĄD lokalizacji [{name}] ({rel}): {e}")
            fail += 1
            continue

        rows_match = current_inner == generated_inner
        badge_match = current_badge.strip() == generated_badge.strip()
        if rows_match and badge_match:
            ok += 1
        else:
            fail += 1
            print(f"  NIEZGODNE [{name}] ({rel}):")
            if not rows_match:
                print(f"    OBECNE : {current_inner[:200]!r}")
                print(f"    NOWE   : {generated_inner[:200]!r}")
            if not badge_match:
                print(f"    badge: obecny={current_badge!r} vs wygenerowany={generated_badge!r}")
    print(f"podstrony zabiegów: {ok} OK, {fail} niezgodnych (z {len(groups)})")
    return fail == 0


def main():
    groups = load_groups()
    print(f"Testowanych zabiegów: {len(groups)} (wykluczono: {EXCLUDED})\n")
    ok1 = test_cennik(groups)
    print()
    ok2 = test_subpages(groups)
    print()
    print("WYNIK:", "✅ WSZYSTKO ZGODNE" if (ok1 and ok2) else "❌ SĄ NIEZGODNOŚCI — silnik wymaga poprawek")


if __name__ == "__main__":
    main()
