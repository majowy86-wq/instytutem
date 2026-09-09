#!/usr/bin/env python3
"""Generuje CAŁY nowy blok <details class="price-tier">...</details> dla podgrupy,
która jeszcze nie istnieje w danym miejscu (Faza 2: wstawianie brakujących podgrup).

Wcięcia zmierzone bezpośrednio w plikach (nie zgadywane) — podstrony używają regularnego
wzorca +2 na poziom, /cennik ma na poziomie zagnieżdżonym nieregularne, "ciężkie" wcięcia
odziedziczone z wcześniejszych rund budowy (zweryfikowane wprost w cennik/index.html)."""
from row_generator import generate_price_row, compute_badge_price

# (details, summary, label, h3/badge, closespan, svg, closesummary, body, rows_wrapper,
#  row_content, close_rows, close_body, close_details)
SUBPAGE_INDENTS = (8, 10, 12, 14, 14, 12, 12, 10, 10, 12, 14, 12, 10, 8)
CENNIK_NESTED_INDENTS = (16, 30, 32, 34, 34, 32, 32, 30, 30, 32, 32, 32, 30, 28)
# płaski wzorzec /cennik (jeden poziom rozwijania) — zmierzone bezpośrednio w pliku (np. blok
# "Lipoliza iniekcyjna")
CENNIK_FLAT_INDENTS = (12, 14, 16, 18, 18, 16, 16, 14, 14, 16, 16, 16, 14, 12)

ACCORDION_INFO_LINK_ICON = (
    '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" '
    'stroke="currentColor" stroke-width="1.3"/><line x1="8" y1="7.1" x2="8" y2="11.3" '
    'stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>'
    '<circle cx="8" cy="4.7" r="0.95" fill="currentColor"/></svg>'
    '<span class="accordion-info-link-label">Informacje o zabiegu</span>'
)


def generate_subgroup_block(name: str, rows: list[dict], indents: tuple, promo_badges_wrapper: str = "",
                             info_link=None) -> str:
    d, summ, lbl, h3b, badgeb, cspan, svg, csumm, body, rowsw, rowc, crows, cbody, cdet = indents
    badge = compute_badge_price(rows)
    row_lines = "\n".join(
        " " * rowc + generate_price_row(r["zabieg"], r["wariant"], r["czas"], r["cena"],
                                         r["offerItemId"], r.get("packageId", ""), r.get("promo", ""))
        for r in rows
    )
    caret_svg = ('<svg class="caret" viewBox="0 0 10 6" fill="none" aria-hidden="true">'
                 '<path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.4" '
                 'stroke-linecap="round" stroke-linejoin="round"/></svg>')

    h3_content = name
    if info_link:
        href, aria_label = info_link
        h3_content += (f'<a class="accordion-info-link" href="{href}" aria-label="{aria_label}">'
                        f'{ACCORDION_INFO_LINK_ICON}</a>')

    lines = [
        " " * d + '<details class="price-tier">',
        " " * summ + '<summary>',
        " " * lbl + '<span class="price-tier-label">',
        " " * h3b + f'<h3 class="treatment-accordion-q">{h3_content}</h3>',
        " " * badgeb + f'<span class="price-tier-badge">{badge}</span>',
        " " * cspan + '</span>',
        " " * svg + caret_svg,
        " " * csumm + '</summary>',
        " " * body + '<div class="treatment-accordion-body">',
        " " * rowsw + '<div class="price-tier-rows">',
        row_lines,
        " " * crows + '</div>',
        " " * cbody + '</div>',
        " " * cdet + '</details>',
    ]
    return "\n".join(lines)
