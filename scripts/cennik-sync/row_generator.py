#!/usr/bin/env python3
"""Generuje HTML pojedynczego wiersza cennikowego (price-row) oraz przelicza
cenę-badge ("od X zł") na podstawie wierszy arkusza — dokładnie w formacie
używanym we wszystkich podstronach zabiegów tego projektu."""
import re

CTA_ARROW_SVG = (
    '<svg viewBox="0 0 16 12" aria-hidden="true">'
    '<path d="M15,6H1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M10,11l5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M10,1l5,5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)


def offer_item_id_to_url_param(offer_item_id: str) -> str:
    # "s:24481347" -> "s%3A24481347"
    return offer_item_id.replace(":", "%3A")


PACKAGES_BASE_URL = "https://www.fresha.com/book-now/testem-xh2mr620/packages"


def generate_price_row(zabieg: str, wariant: str, czas: str, cena: str, offer_item_id: str,
                        package_id: str = "", promo: str = "") -> str:
    """Buduje jeden <div class="price-row">...</div>. Obsługuje 3 warianty przycisku:
    offerItemId -> "Zarezerwuj" (booking), packageId -> "Kup pakiet" (packages), brak obu -> płaska cena."""
    name_html = wariant
    duration_html = f' <span>· {czas}</span>' if czas else ''
    label = f'<p>{name_html}{duration_html}</p>'
    promo_html = f'<span class="promo-badge">{promo}</span>' if promo else ''

    if offer_item_id:
        href = (
            "https://www.fresha.com/pl/a/instytutem-tm-plock-1-maja-6-jrr27hgf/booking"
            f"?offerItemId={offer_item_id_to_url_param(offer_item_id)}"
        )
        cta_label = "Zarezerwuj"
    elif package_id:
        href = f"{PACKAGES_BASE_URL}?id={package_id}&share=true&pId=602910"
        cta_label = "Kup pakiet"
    else:
        href = None
        cta_label = None

    if href:
        buy = (
            f'<span class="price-row-buy"><p>{cena}</p>'
            f'<a class="treatment-card-cta" href="{href}" target="_blank" rel="noopener">'
            f'<span class="treatment-card-cta-title-wrap"><span>{cta_label}</span>'
            f'<span class="treatment-card-cta-arrow">{CTA_ARROW_SVG}</span></span>'
            f'<span class="treatment-card-cta-underline"></span></a></span>'
        )
    else:
        buy = f'<p>{cena}</p>'

    return f'<div class="price-row">{promo_html}{label}{buy}</div>'


def generate_rows_block(rows: list[dict], row_indent: int, closing_indent: int) -> str:
    """rows: lista dictów z kluczami zabieg/wariant/czas/cena/offerItemId.
    Zwraca zawartość <div class="price-tier-rows"> (bez samego wrappera),
    z takim samym wcięciem jak reszta pliku. W /cennik: row_indent=16, closing_indent=16.
    Na podstronach: row_indent=14, closing_indent=12 (zweryfikowane bezpośrednio w plikach)."""
    pad = " " * row_indent
    parts = [
        pad + generate_price_row(
            r["zabieg"], r["wariant"], r["czas"], r["cena"], r["offerItemId"],
            r.get("packageId", ""), r.get("promo", ""),
        )
        for r in rows
    ]
    return "\n" + "\n".join(parts) + "\n" + (" " * closing_indent)


def _extract_number(price_text: str) -> int:
    digits = re.sub(r"[^0-9]", "", price_text)
    return int(digits) if digits else 0


def compute_badge_price(rows: list[dict]) -> str:
    """Zwraca 'X zł' jeśli wszystkie ceny identyczne, inaczej 'od MIN zł'.
    Wyjątek: jeden wiersz z ceną typu 'od X zł' (widełki nawet dla jednego
    wariantu) — badge przejmuje ten tekst dosłownie, bez ucinania 'od'."""
    if not rows:
        return "---"
    if len(rows) == 1:
        return rows[0]["cena"]
    numbers = [_extract_number(r["cena"]) for r in rows]
    if len(set(numbers)) == 1:
        return f"{numbers[0]} zł"
    return f"od {min(numbers)} zł"
