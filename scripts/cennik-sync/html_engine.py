#!/usr/bin/env python3
"""Silnik do precyzyjnej podmiany bloków cennikowych w surowym HTML-u.

Celowo NIE parsuje i nie serializuje całego dokumentu na nowo (to zmienia
kolejność atrybutów i zaśmieca diffy) — zamiast tego lokalizuje dokładne
fragmenty przez wyszukiwanie znaczników tekstowych i liczenie zagnieżdżeń
<div>, a podmienia tylko wybrany fragment, zostawiając resztę pliku bit
w bit taką samą.
"""
import re


def find_matching_close_div(html: str, open_tag_end: int) -> int:
    """Zwraca pozycję TUŻ PO domykającym </div> dla diva, którego tag otwierający
    kończy się na open_tag_end (pozycja znaku '>' otwierającego tagu)."""
    depth = 1
    pos = open_tag_end + 1
    tag_re = re.compile(r"<(/?)div\b")
    while depth > 0:
        m = tag_re.search(html, pos)
        if not m:
            raise ValueError("Nie znaleziono domykającego </div> — uszkodzona struktura HTML")
        if m.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos = m.end()
    # pos jest zaraz za "</div" tego wpisu który domknął depth==0 -> doszukaj ">"
    close_gt = html.index(">", pos)
    return close_gt + 1


def find_price_tier_rows_block(html: str, h3_prefix: str):
    """Znajduje blok <div class="price-tier-rows">...</div> należący do grupy
    zaczynającej się od <h3 class="treatment-accordion-q">{h3_prefix}.
    Zwraca (start, end) — end to pozycja TUŻ PO zamykającym </div>."""
    marker = f'<h3 class="treatment-accordion-q">{h3_prefix}'
    h3_pos = html.find(marker)
    if h3_pos == -1:
        raise ValueError(f"Nie znaleziono nagłówka: {marker!r}")

    rows_marker = '<div class="price-tier-rows'
    rows_start = html.find(rows_marker, h3_pos)
    if rows_start == -1:
        raise ValueError(f"Nie znaleziono price-tier-rows po nagłówku {h3_prefix!r}")

    open_tag_end = html.index(">", rows_start)
    end = find_matching_close_div(html, open_tag_end)
    return rows_start, end, open_tag_end + 1


def find_price_tier_badge(html: str, h3_prefix: str):
    """Znajduje <span class="price-tier-badge">TEKST</span> powiązany z danym h3.
    Zwraca (start_tekstu, end_tekstu, obecny_tekst)."""
    marker = f'<h3 class="treatment-accordion-q">{h3_prefix}'
    h3_pos = html.find(marker)
    if h3_pos == -1:
        raise ValueError(f"Nie znaleziono nagłówka: {marker!r}")

    summary_end = html.find("</summary>", h3_pos)
    if summary_end == -1:
        raise ValueError(f"Nie znaleziono </summary> po nagłówku {h3_prefix!r}")

    badge_open = '<span class="price-tier-badge">'
    badge_start = html.find(badge_open, h3_pos)
    if badge_start == -1 or badge_start > summary_end:
        raise ValueError(f"Nie znaleziono price-tier-badge w obrębie <summary> dla {h3_prefix!r}")

    text_start = badge_start + len(badge_open)
    text_end = html.index("</span>", text_start)
    return text_start, text_end, html[text_start:text_end]


def replace_span(html: str, start: int, end: int, new_text: str) -> str:
    return html[:start] + new_text + html[end:]


def replace_block(html: str, start: int, end: int, new_html: str) -> str:
    return html[:start] + new_html + html[end:]
