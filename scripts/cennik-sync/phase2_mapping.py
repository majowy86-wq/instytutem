#!/usr/bin/env python3
"""Faza 2: jawna mapa podgrup dla 6 zabiegów ze złożoną strukturą.

Każdy wpis: (nazwa_kanoniczna, źródło) gdzie źródło to:
  "both"         — istnieje w obu miejscach, nazwa z podstrony wygrywa (jeśli różna od cennika)
  "cennik_only"  — istnieje tylko w /cennik, ma trafić też na podstronę
  "subpage_only" — istnieje tylko na podstronie, ma trafić też do /cennik

Kolejność w liście = docelowa kolejność wyświetlania (ustalona na podstawie pozycji
w /cennik, gdzie brakujące podgrupy naturalnie wskazują, gdzie powinny się wstawić).
"Konsultacje" świadomie pominięte — poza zakresem (wspólne, edytowane osobno).
"""

TREATMENTS = {
    "Epilacja laserowa LightSheer®": {
        "subpageRel": "zabiegi/depilacja-laserowa-plock-lightsheer",
        "subgroups": [
            ("(S) Mała partia ciała", "both"),
            ("(M) Standardowa partia ciała", "both"),
            ("(L) Duża partia ciała", "both"),
            ("Pakiety Elastyczne", "cennik_only"),
            ("Przygotowanie do zabiegu", "both"),
        ],
    },
    "Endermologia LPG® Alliance": {
        "subpageRel": "zabiegi/endermologia-plock-lpg-alliance",
        "subgroups": [
            ("Sesje zabiegowe", "both"),
            ("Strój zabiegowy", "subpage_only"),
            ("Pakiety", "both"),
        ],
    },
    "Endermologia Twarzy LPG® Endermolift™": {
        "subpageRel": "zabiegi/endermologia-twarzy-plock-lpg-endermolift",
        "subgroups": [
            ("Zabieg", "both"),
            ("Pakiety", "both"),
            ("Pakiety łączone", "both"),
        ],
    },
    "Kriolipoliza cooltech®": {
        "subpageRel": "zabiegi/kriolipoliza-plock-cooltech",
        "subgroups": [
            ("Zabieg", "both"),
            ("Pakiety", "both"),
        ],
    },
    "Fibryna i osocze bogatopłytkowe": {
        "subpageRel": "fibryna-i-osocze-bogatoplytkowe",
        "subgroups": [
            ("Osocze bogatopłytkowe PRP", "both"),
            ("Fibryna bogatopłytkowa PRF", "both"),
        ],
    },
    "Mezoterapia bezigłowa": {
        "subpageRel": "zabiegi/mezoterapia-bezigłowa",
        "subgroups": [
            ("Zabieg", "both"),
            ("Pakiety łączone", "both"),
        ],
    },
}

# nazwa kanoniczna (z powyższej mapy) -> nazwa użyta w /cennik, gdy różni się od kanonicznej
CENNIK_NAME_OVERRIDE = {
    ("Epilacja laserowa LightSheer®", "(S) Mała partia ciała"): "(S) mała partia ciała",
    ("Epilacja laserowa LightSheer®", "(M) Standardowa partia ciała"): "(M) standardowa partia ciała",
    ("Epilacja laserowa LightSheer®", "(L) Duża partia ciała"): "(L) duża partia ciała",
    ("Endermologia LPG® Alliance", "Sesje zabiegowe"): "Endermologia LPG® Alliance",
    ("Kriolipoliza cooltech®", "Zabieg"): "Kriolipoliza cooltech®",
    ("Mezoterapia bezigłowa", "Zabieg"): "Mezoterapia bezigłowa",
}
