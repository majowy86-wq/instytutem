#!/usr/bin/env python3
"""Silnik do precyzyjnej podmiany bloków cennikowych w surowym HTML-u.

Celowo NIE parsuje i nie serializuje całego dokumentu na nowo (to zmienia
kolejność atrybutów i zaśmieca diffy) — zamiast tego lokalizuje dokładne
fragmenty przez wyszukiwanie znaczników tekstowych i liczenie zagnieżdżeń
<div>, a podmienia tylko wybrany fragment, zostawiając resztę pliku bit
w bit taką samą.
"""
import re


def find_matching_close_tag(html: str, open_tag_end: int, tag_name: str = "div") -> int:
    """Zwraca pozycję TUŻ PO domykającym tagu (np. </div> lub </details>) dla elementu,
    którego tag otwierający kończy się na open_tag_end (pozycja znaku '>')."""
    depth = 1
    pos = open_tag_end + 1
    tag_re = re.compile(rf"<(/?){tag_name}\b")
    while depth > 0:
        m = tag_re.search(html, pos)
        if not m:
            raise ValueError(f"Nie znaleziono domykającego </{tag_name}> — uszkodzona struktura HTML")
        if m.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos = m.end()
    close_gt = html.index(">", pos)
    return close_gt + 1


def find_matching_close_div(html: str, open_tag_end: int) -> int:
    return find_matching_close_tag(html, open_tag_end, "div")


def find_outer_treatment_block(html: str, treatment_name: str, search_from: int = 0):
    """Znajduje OUTER <details class="price-tier price-tier--group">...</details> zabiegu
    w /cennik (identyfikowany po h3 z accordion-info-link, bo nested-podgrupy powtarzają
    tę samą nazwę bez linku). Zwraca (start, end) — end TUŻ PO zamykającym </details>."""
    marker = f'<h3 class="treatment-accordion-q">{treatment_name}<a class="accordion-info-link"'
    h3_pos = html.find(marker, search_from)
    if h3_pos == -1:
        raise ValueError(f"Nie znaleziono nagłówka zabiegu (z linkiem): {treatment_name!r}")

    # cofnij się do otwierającego <details ...> poprzedzającego ten h3
    details_start = html.rfind("<details", 0, h3_pos)
    if details_start == -1:
        raise ValueError(f"Nie znaleziono otwierającego <details> dla {treatment_name!r}")
    open_tag_end = html.index(">", details_start)
    end = find_matching_close_tag(html, open_tag_end, "details")

    # start zakresu TUŻ PO własnym </summary> zabiegu — inaczej wyszukiwanie podgrupy
    # o identycznej nazwie jak zabieg (częste, np. "Kriolipoliza cooltech®" x2) łapie
    # własny nagłówek zamiast pierwszej zagnieżdżonej podgrupy
    own_summary_end = html.index("</summary>", h3_pos) + len("</summary>")
    return own_summary_end, end


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


def find_loose_rows_block(html: str):
    """Dla przypadków typu Mezoterapia bezigłowa w /cennik: podgrupa BEZ własnego
    <details>/badge — luźne <div class="price-row"> leżą wprost w kontenerze
    price-tier-rows--nested, przed pierwszą zagnieżdżoną <details>.
    Zwraca (start, end, content_start) analogicznie do find_price_tier_rows_block."""
    # klasa bywa "price-tier-rows price-tier-rows--nested" (dwie klasy) — szukaj tekstu
    # gdziekolwiek w atrybucie, potem cofnij się do początku samego tagu <div
    marker_pos = html.find("price-tier-rows--nested")
    if marker_pos == -1:
        raise ValueError("Nie znaleziono price-tier-rows--nested")
    c_pos = html.rfind("<div", 0, marker_pos)
    if c_pos == -1:
        raise ValueError("Nie znaleziono otwierającego <div> dla price-tier-rows--nested")
    open_tag_end = html.index(">", c_pos)
    content_start = open_tag_end + 1

    # koniec luźnych wierszy = pozycja pierwszego <details wewnątrz kontenera
    details_pos = html.find("<details", content_start)
    if details_pos == -1:
        raise ValueError("Nie znaleziono zagnieżdżonej <details> po luźnych wierszach")

    return c_pos, details_pos, content_start


def replace_span(html: str, start: int, end: int, new_text: str) -> str:
    return html[:start] + new_text + html[end:]


def replace_block(html: str, start: int, end: int, new_html: str) -> str:
    return html[:start] + new_html + html[end:]
