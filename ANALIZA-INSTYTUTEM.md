# Analiza instytutem.pl i Fresha

> Analiza struktury treściowej strony www.instytutem.pl (docelowe źródło treści, patrz [CLAUDE.md](CLAUDE.md)) oraz platformy rezerwacyjnej Fresha — referencja do migracji treści, nie plik statusu/checklisty (to [PLAN.md](PLAN.md)) ani design system (to [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md)).

---

## 📊 Strona instytutem.pl — Struktura sekcji

### 1. **Header (Sticky)**
- **Top bar**: Email (recepcja@instytutem.pl) + Telefon (+48 737 836 092) + Social (Instagram, Facebook)
- **Logo** → link do strony głównej
- **Mega-menu nawigacji** (patrz poniżej)
- **CTA "REZERWUJ WIZYTĘ"** (link: rezerwuj.instytutem.pl)

### 2. **Nawigacja główna (Mega-menu)**
```
├── ZABIEGI (18 podstron) ↓
│   ├── Depilacja Laserowa
│   ├── Laser Tulowy Erbowo-Szklany
│   ├── Endermologia
│   ├── Kriolipoliza
│   ├── RF Radiofrekwencja Mikroigłowa
│   ├── Fototerapia LED Dermalux
│   ├── Fibryna i Osocze Bogatopłytkowe
│   ├── Lipoliza Iniekcyjna
│   ├── Karboksyterapia
│   ├── Mikronakłuwanie
│   ├── Wypełnianie Kwasem Hialuronowym
│   ├── Peelingi Medyczne
│   ├── Trychologia
│   ├── Nici Liftingujące PDO
│   ├── Mikrodermabrazja
│   ├── Mezoterapia Igłowa
│   ├── Plasma
│   ├── Endermologia Twarzy
│   └── Oczyszczanie Wodorowe
├── PROMOCJE (3 podstrony) ↓
│   ├── Pakiet Powitalny
│   ├── Poleć Nas
│   └── Pakiety Depilacji Laserowej
├── BLOG
├── CENNIK (link do Fresha)
├── NA RATY
├── KONTAKT
└── WIĘCEJ
```

### 3. **Hero Section**
- **Tło**: Zdjęcie kosmetolog Eweliny z pacjentką (dermokonsultacja)
- **Overlay text**: "PIERWSZA WIZYTA?" (nagłówek)
- **Subtext**: "ODBIERZ PAKIET POWITALNY" + opis korzyści
- **CTA**: "ZAREJESTRUJ SIĘ" (link: /pakiet-powitalny-dla-nowych-klientow)

### 4. **Główna sekcja („O nas" + 3 Taby)**
- **Nagłówek**: „INSTYTUTem.™ to nowoczesny salon depilacji laserowej i zabiegów kosmetologicznych w Płocku..."
- **3 Taby z zawartością:**
  1. **Depilacja Laserowa w Płocku**
     - Tekst opisu zabiegu
     - Zdjęcie (zabieg na nogach)
     - Link: "Dowiedz się więcej o zabiegu"
  2. **Zabiegi na Twarz**
     - Tekst opisu (oczyszczanie, peelingi, kwas hialuronowy, mezoterapia)
     - Zdjęcie (mezoterapia igłowa)
     - Link: "Dowiedz się więcej o zabiegach"
  3. **Modelowanie Ciała**
     - Tekst opisu (endermologia, kriolipoliza)
     - Zdjęcie (kriolipoliza ud)
     - Link: "Dowiedz się więcej o zabiegach"
- **CTA pod tabami**: "ZOBACZ WSZYSTKIE ZABIEGI" (link: /zabiegi)

### 5. **Sekcja z cytatem właścicielki**
- **Portret**: Ewelina Majchrzak (kosmetolog, właścicielka, szkoleniowiec)
- **Cytat**: „Nasze ciało jest jedynym miejscem w którym jesteśmy zmuszeni przebywać, dlatego tak ważne jest abyś czuła się w nim komfortowo."
- **Attribution**: „- Ewelina Majchrzak"

### 6. **Sekcja opinii (Testimonials)**
- **Nagłówek**: „Dziękujemy Wam za zaufanie! 5/5 ★★★★★"
- **Karuzelę opinii** — pokazuje 3-5 opinii naraz, przesuwalne:
  - Magdalena Górska: „Szeroki wybór zabiegów, zabiegi dostosowane..."
  - Karolina Piotrowska: „Super obsługa, miła, dbająca o komfort..."
  - Katarzyna Mazuchowska: „Wspaniała atmosfera. Przesympatyczne panie..."
  - (+ więcej...)
- **CTA #1**: "WIĘCEJ OPINII" (link do Google Reviews)
- **CTA #2**: "ZOSTAW OPINIĘ" (link do dodania opinii na Google)

### 7. **Footer (Stopka)**
- **Kolumna 1 — Kontakt i Social:**
  - Logo
  - Telefon: +48 737 836 092 (link `tel:`)
  - Email: recepcja@instytutem.pl (link `mailto:`)
  - Adres: ul. 1 Maja 6, 09-402 Płock + Google Maps
  - Godziny: pon-pt 08:00-21:00, sob 08:00-16:00, niedziela zamknięta
  - IBAN: PL52 1140 2004 0000 3802 7602 0101
  - Social: Instagram, Facebook

- **Kolumna 2 — Sekcje:**
  - PROMOCJE
  - ZABIEGI
  - SZKOLENIA
  - REGULAMINY
  - O NAS

- **Kolumna 3 — Szybkie linki:**
  - POLEĆ NAS
  - PAKIETY DEPILACJI LASEROWEJ
  - PROMOCJA DLA NOWYCH KLIENTÓW
  - OFERTA ZABIEGOWA
  - CENNIK
  - VOUCHER PODARUNKOWY
  - NA RATY
  - PROGRAM LOJALNOŚCIOWY

- **Kolumna 4 — Regulaminy & Info:**
  - POLITYKA PRYWATNOŚCI I COOKIES
  - REGULAMIN SPRZEDAŻY I ŚWIADCZENIA USŁUG
  - REGULAMIN PAKIETÓW

- **Copyright:**
  - WSZELKIE PRAWA ZASTRZEŻONE © 2023 INSTYTUTem™
  - Z DUMĄ STWORZONE PRZEZ [MAJCHRZAK.STUDIO](https://majchrzak.studio/)

---

## 🌟 Platforma Fresha — Struktura profilu

### Profile Navigation (Taby)
1. **Zdjęcia** — galeria salonów/zabiegów
2. **Usługi** — lista wszystkich usług (148 dostępnych)
3. **Zespół** — lista terapeutul (Ewelina, Julia, Nikola)
4. **Oceny** — recenzje (5.0/5, 33 głosy)
5. **Informacje** — opis, godziny, adres, parking

### Kategoryzacja usług (problem-based)
- Konsultacje i diagnostyka
- Nadmierne owłosienie (epilacja laserowa)
- Zmarszczki, lifting i opadający owal (dla twarzy)
- Suchość, naczynka, głęboka regeneracja (dla twarzy)
- Trądzik, przebarwienia i oczyszczanie (dla twarzy i ciała)
- Blizny, rozstępy i przebudowa skóry (dla twarzy i ciała)
- Cellulit, wiotka skóra i obrzęki (dla ciała)
- Nadmiar tkanki tłuszczowej i modelowanie sylwetki (dla ciała)

### CTA i produkty
- **Zarezerwuj teraz** (główny CTA)
- **Kup karnet** — pakiety usług (oszczędności)
- **Kup kartę podarunkową** — voucher prezentowy

### Recenzje (Reviews)
- **Statystyka:** 5.0/5, 33 recenzje
- **Przykład recenzji:**
  > „W Instytutem™ klienci cenią sobie szczególnie profesjonalne konsultacje... epilacja laserowa LightSheer® oraz endermologia LPG® Alliance..."
  > — JS BM (5★)
- **Każda recenzja zawiera:** imię, ocenę, tekst, datę, terapeuta (Ewelina/Julia/Nikola)

---

## 🔄 Porównanie: Instytutem.pl vs Archon (bieżący projekt)

| Element | Instytutem.pl | Archon (obecny) | Rekomendacja |
|---------|---------------|-----------------|----------------|
| **Top bar** | Email + Tel zawsze | Nie ma | ✅ Dodać |
| **Hero section** | Zdjęcie + "Pierwsza wizyta?" CTA | Tekst + 2 przyciski | ✅ Zmienić na model instytutem.pl |
| **Taby kategorii** | 3 taby (Laser, Twarz, Ciało) | Brak | ✅ Dodać |
| **Sekcja promocji** | Dedykowana (Pakiet powitalny) | Brak | ✅ Dodać |
| **Cytat właścicielki** | Jest (Ewelina) | Brak | ✅ Dodać |
| **Opinie** | Karuzelę, dynamiczne | Statyczne, 7 opinii | ✅ Zmienić na slider |
| **Mega-menu** | Bogata, 18 zabiegów | Taka sama logika | ✔️ OK |
| **Footer** | Rozbudowany, IBAN, regulaminy | Podstawowy | ✅ Powiększyć |
| **Blog, Cennik, Na raty** | Są | Nie ma (zaplanowane) | ⏳ Na przyszłość |

---

## 💡 Top 8 zmian do wdrożenia (prioritet)

### 🥇 Priorytet 1: Hero + 3 Taby (Quickwin)
Zmienić hero section na model instytutem.pl:
- Zdjęcie kosmetologa/pacjentki + overlay text
- 3 taby poniżej (Zabiegi na Twarz, Laser, Modelowanie Ciała)
- Każdy tab: opis + zdjęcie + CTA "Więcej informacji"
- CTA pod tabami: "ZOBACZ WSZYSTKIE ZABIEGI"

**Zysk:** Lepszy visual hierarchy, bardziej atrakcyjnie, szybka orientacja user'a.

### 🥈 Priorytet 2: Top bar + Sticky header
Dodać na górze:
- Email (kontakt@...) + Telefon
- Social icons (Instagram, Facebook)
- Zawsze widoczny, nawet na mobilu

**Zysk:** Zwiększenie konwersji (direct contact easier).

### 🥉 Priorytet 3: Karuzelę opinii
Zmienić z 7 statycznych opinii na slider/karuzela (3-5 opinii widoczne):
- Przesuwalne (next/prev buttons lub auto-scroll)
- Dodać "WIĘCEJ OPINII" + "ZOSTAW OPINIĘ" linki

**Zysk:** Bardziej nowoczesny wygląd, lepszy engagement.

### 4️⃣ Cytat właścicielki
Dodać sekcję między tabasmi a opiniami:
- Portret (selfie/profesjonalne zdjęcie)
- Cytat (1-2 zdania o misji salonu)
- Imię + rola

**Zysk:** Personal touch, budowanie zaufania, brand identity.

### 5️⃣ Rozbudowany footer
Dodać:
- Kolumny: Sekcje, Szybkie linki, Regulaminy, Social
- Godziny otwarcia
- IBAN (dla przelewów)
- Copyright + Created by link

**Zysk:** SEO, anchor links, profesjonalny wygląd.

### 6️⃣ Sekcja promocji (Welcome package)
Dodać dedykowaną sekcję PROMOCJE:
- Pakiet powitalny (dla nowych klientów)
- Karty podarunkowe
- Pakiety zabiegów

**Zysk:** Zwiększenie konwersji, jasna propozycja dla nowych klientów.

### 7️⃣ Kategorie problemu (problem-based tagging)
Reorganizować mega-menu zamiast alphabet:
- Zmarszczki & Lifting
- Trądzik & Oczyszczanie
- Cellulit & Modelowanie
- itd.

**Zysk:** Lepsze UX, user od razu widzi co potrzebuje.

### 8️⃣ Blog + Cennik + Na raty (Nice to have)
Dodać strony/sekcje:
- Blog (artykuły edukacyjne)
- Cennik (pełna lista cen)
- Na raty (opcje finansowania)

**Zysk:** SEO, edukacja, accessibility, zmniejszenie barier konwersji.

---

## 🎨 Design notes

### Paleta instytutem.pl (dla porównania — nie używana)
- **Primary green:** ~#2a7f62 (dark green)
- **Accent gold/beige:** ~#d4a574
- **Text:** #333 / #555
- **Background:** white, #f9f9f9, cream

**Rekomendacja:** Zachować paletę Archon bez zmian — pełna specyfikacja w [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) §2, nie duplikować jej tutaj.

---

## 📁 Pliki do modyfikacji

1. **index.html** — zmiana hero section, dodanie tabów, sekcji promocji, cytatu, footer
2. **css/styles.css** — nowe style dla tabów, karuzel opinii, hero, top bar
3. **js/main.js** — logika tabów, karuzel opinii, smooth scrolling

### Nowe sekcje do dodania
- [ ] Top bar (kontakt zawsze widoczny)
- [ ] 3 Taby zamiast jednego hero
- [ ] Sekcja promocji (welcome package)
- [ ] Cytat właścicielki
- [ ] Karuzelę opinii
- [ ] Rozbudowany footer

---

## ✅ Proces implementacji

Standardowy proces z [CLAUDE.md](CLAUDE.md#zweryfikowany-proces-na-przyszłość) (pomiar → kod → weryfikacja) plus zadania w [PLAN.md](PLAN.md) — nie osobny proces dla tych zmian.

---

**Mapa interaktywna:** https://claude.ai/code/artifact/e8e52708-9be0-4424-8e08-07d37ababd8c
