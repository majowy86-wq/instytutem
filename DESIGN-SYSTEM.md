# Archon — Design System

> Ten dokument jest jedynym źródłem prawdy dla wyglądu strony. Wszystkie decyzje projektowe (kolory, typografia, komponenty, odstępy, ton głosu) muszą być zgodne z tym, co tu zapisano. Wartości zostały zmierzone bezpośrednio na żywej stronie archon.au (computed styles, sierpień 2026) i tam, gdzie było to potrzebne dla spójności wdrożeniowej, zaokrąglone do czytelnej skali.

---

## 1. Filozofia marki

Archon to unisex klinika skóry, laseroterapii i urody (Teneriffe, Brisbane, AU). Pozycjonowanie: **jakość zamiast ilości**, uproszczone menu zabiegów, brak nachalnej sprzedaży.

Zasady, które mają wpływać na każdą decyzję treściową i wizualną:

- **Inkluzywność przede wszystkim** — "unisex", "male + female therapists", "everyone welcome". Nigdy nie projektować pod jedną płeć/estetykę.
- **Zaproszenie, nie sprzedaż** — CTA brzmią jak "book a free consult", nie jak twarde domknięcie transakcji.
- **Jakość nad ilością** — unikać przytłaczania użytkownika liczbą opcji; prosty, wyselekcjonowany wybór.
- **Dowód społeczny z twarzą** — opinie klientów podpisane imieniem + inicjałem nazwiska, nigdy anonimowo.
- **Znak „+” jako łącznik marki** — powtarzający się motyw graficzno-językowy: „skin + body”, „Aesthetics + Beauty + Grooming”, „Male + Female”. Używać go świadomie jako spójnika łączącego usługi/grupy, nie jako ozdobnika.

Reprezentatywne cytaty (oryginalne, EN — ton do naśladowania):

- „Just effective treatments for skin + body”
- „If it matters to you, it matters to us.”
- „Not sure where to begin? Just book in a free consult and we'll help guide you in the right direction.”
- „Fall in love with your skin and body”
- „Take a moment outside your usual.”

---

## 2. Kolory

Paleta jest wąska i zdyscyplinowana. Kremowe tło i niemal czarna oliwkowa zieleń niosą 90% interfejsu; limonkowy akcent jest **rzadki i celowy**.

| Token | Nazwa | HEX | RGB | Zastosowanie |
|---|---|---|---|---|
| `--a-cream` | Cream | `#F1EDE7` | 241, 237, 231 | Główne tło jasnych sekcji, nawigacja, stopka |
| `--a-olive-black` | Black Olive | `#161810` | 22, 24, 16 | Tło ciemnych sekcji; kolor nagłówków na jasnym tle |
| `--a-olive` | Olive | `#3A412A` | 58, 65, 42 | Główny przycisk CTA („Book Online”) |
| `--a-olive-deep` | Deep Olive | `#232715` | 35, 39, 21 | Obwódki przycisków typu outline |
| `--a-ink-warm` | Warm Ink | `#3F3D3B` | 63, 61, 59 | Tekst podstawowy na jasnym tle |
| `--a-border-gray` | Border Gray | `#696969` | 105, 105, 105 | Cienkie obwódki, przycisk „Call Us” |
| `--a-gray` | Muted Gray | `#7A7772` | 122, 119, 114 | Przycisk z numerem telefonu |
| `--a-taupe` | Taupe | `#D6D0C5` | 214, 208, 197 | Separatory, subtelne tła w kartach |
| `--a-lime` | Lime | `#BFF751` | 191, 247, 81 | Rzadki akcent — jedna specjalna sekcja, cena w kartach zabiegów |
| `--a-white` | White | `#FFFFFF` | 255, 255, 255 | Przycisk kontrastowy na ciemnym tle |
| `--a-rust` | Rust | `#C7642D` | 199, 100, 45 | **Kolor hover dla wszystkich klikalnych linków tekstowych** (patrz sekcja 8, „Linki i stany hover”) |

**Zasady użycia:**
- Lime (`#BFF751`) nigdy jako kolor tła dużej powierzchni tekstu ani jako kolor tekstu — tylko jako akcent punktowy (tło jednej wyróżnionej sekcji, cena, mały highlight).
- Rust (`#C7642D`) tylko jako stan `:hover` na klikalnych linkach tekstowych — nigdy jako domyślny kolor tekstu ani jako tło. Nie dotyczy przycisków (`.abtn`) ani ikon (social media, strzałki karuzeli) — te mają własny, osobny język interakcji (podniesienie + cień / zmiana koloru ikony).
- Sekcje strony naprzemiennie przełączają tło między `cream` i `black-olive` — to jedyny mechanizm rytmu wizualnego strony (patrz sekcja 7).
- Tekst na `cream` = `--a-ink-warm` lub `--a-olive-black`. Tekst na `black-olive` = `--a-cream` lub `--a-white`. Nigdy ciemny tekst na ciemnym tle ani jasny na jasnym.

---

## 3. Typografia

Dwa kroje na całą markę, ładowane z Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=Tenor+Sans&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

- **Tenor Sans** (waga 400, jedyna dostępna) — wąski, geometryczny szeryf-sans. Niesie wszystkie nagłówki. Znak charakterystyczny: **ujemny tracking** na dużych rozmiarach (do -3,2px), który ściska litery i nadaje elegancję zamiast krzykliwości.
- **Inter** (400/500/600/700) — obsługuje wszystko funkcjonalne: treść, nawigację, etykiety, przyciski, dane.

### Skala typograficzna

| Rola | Krój / waga | Rozmiar / line-height | Tracking | Transform |
|---|---|---|---|---|
| Nagłówek hero / H1–H2 | Tenor Sans 400 | 64px / 76,8px (desktop) | -3,2px | none |
| Nagłówek sekcji | Tenor Sans **500** | **30px / 36px, płaskie na każdej szerokości ekranu — bez skalowania** | **-1px** | none |
| Etykieta duża (eyebrow) | Inter 700 | 15px / 21px | normal | capitalize |
| Etykieta mała (label) | Inter 600 | 10–12px | +1px | UPPERCASE |
| Nagłówek karty (H4) | Inter 500 | 16px / 24px | normal | capitalize |
| Tekst podstawowy | Inter 400 | 16px / 27,2px | normal | none |
| Nawigacja | Inter 500 | 12px / 20,4px | normal | none |

**Zasada:** etykiety (eyebrow/label) idą w przeciwną stronę niż nagłówki — dodatni tracking i wersaliki budują dyscyplinę informacyjną, kontrastującą z miękkością dużych nagłówków Tenor Sans. Nie mieszać tych dwóch charakterów w jednym elemencie.

**Korekta 2026-08-27:** wiersz „Nagłówek sekcji" wcześniej podawał `~48px / -2,5px` — wartość nigdy nie zmierzoną bezpośrednio, tylko przybliżoną. Zweryfikowano bezpośrednio na żywej archon.au (`.heading.h2`, klasa dzieląca się między sekcją filozofii marki, RX Facials i opiniami klientów): realna wartość to **płaskie 30px/500/-1px/line-height 36px, bez żadnego skalowania względem szerokości okna** (brak media query zmieniającego `font-size` dla tej klasy). **Wyjątki, które NIE używają tego stylu** (zweryfikowane, że to inny, większy poziom nagłówka na oryginale — nie kopiować do nich wartości 30px):
- Sekcja Kontakt („Get in touch") i cytat w Bannerze Rezerwacji („Take a moment outside your usual." — **uwaga, korekta z Rundy 39**: wcześniej ta notatka błędnie umiejscawiała ten cytat w sekcji Newsletter/programu lojalnościowego; w naszym kodzie od zawsze należał do osobnej sekcji `#book`, Newsletter to inne, niepowiązane miejsce) — na archon.au to dwie różne klasy, obie zmierzone precyzyjnie bezpośrednio (Runda 34 i 39, `document.styleSheets`, łącznie z media queries):
  - `.heading.hero` (Kontakt): flat **60px / waga 500 / line-height:1 (=60px) / letter-spacing -2px**, `margin-bottom:35px`, breakpoint `≤479px → 42px`. U nas: klasa `.h-hero`.
  - `.heading.display` (Banner Rezerwacji): **60px / waga 500 / letter-spacing -1px / line-height 94px** powyżej 991px, ale responsywnie **rośnie** do `72px/71px` między 480–991px, i dopiero **spada** do `51px/52px` poniżej 479px — realny, zmierzony w źródłowym CSS quirk archon.au (nie literówka), `margin-bottom:52px`, kolor czysto biały (`#FFFFFF`, nie `--a-cream`) na tle zdjęcia. U nas: klasa `.h-quote`.
  Obie zweryfikowane i wdrożone na naszej stronie.
- Baner „Archon Rewards" — na archon.au to w ogóle nie nagłówek sekcji, tylko mała etykieta wielkimi literami (`h4.uppercase`, 12px/600/uppercase/+0.5px) — bardzo bliska już istniejącej klasie `.eyebrow` w tym dokumencie. Nasza strona obecnie prawdopodobnie błędnie używa tam dużego nagłówka sekcji zamiast małej etykiety — niezweryfikowane w tej rundzie, do sprawdzenia osobno.

---

## 4. Przyciski

Zero pigułkowatych kształtów. **Ostry, minimalny promień 2–3px** to kluczowy, rozpoznawalny detal marki — kontrastuje z organiczną fotografią w tle. Stała wysokość **44px**, poziomy padding **23–27px**, krój Inter 500 14px.

| Wariant | Tło | Tekst | Obwódka | Promień | Użycie |
|---|---|---|---|---|---|
| Primary — czarny | `#161810` | `#FFFFFF` | brak | 2px | Główne CTA w hero, kartach |
| Primary — oliwka | `#3A412A` | `#F1EDE7` | brak | 3px | „Book Online” w nawigacji |
| Outline — ciemny | przezroczyste | `#232715` | 1px solid `#232715` | 3px | Drugorzędne CTA na jasnym tle |
| Outline — jasny | przezroczyste | `#FFFFFF` | 1px solid `#F1EDE7` | 2px | CTA na zdjęciu w hero |
| White | `#FFFFFF` | `#161810` | brak | 2px | CTA na ciemnych sekcjach |
| Gray | `#7A7772` | `#FFFFFF` | brak | 2px | Numer telefonu / kontakt |
| Outline — szary | przezroczyste | `#3F3D3B` | 1px solid `#696969` | 2px | „Call Us” |

**Zasada:** nigdy nie stosować `border-radius` większego niż 3px na przyciskach — to złamałoby sygnaturowy, architektoniczny charakter marki.

---

## 5. Kształty i cienie

### Skala promieni (border-radius)

| Wartość | Zastosowanie |
|---|---|
| 1px | Cienkie obwódki |
| 2px | Przycisk (primary-black, white, gray) |
| 3px | Przycisk (primary-olive, outline) |
| 8px | Panel (np. mega-menu dropdown) |
| 10px | Karta zabiegu |
| 50% | Ikony okrągłe |

### Kadr „łuk” — sygnaturowy kształt marki

```css
border-radius: 150px 150px 20px 20px;
```

Górne rogi zdjęcia w pełni zaokrąglone (150px), dolne ledwie muśnięte (20px) — dosłowne, architektoniczne nawiązanie do nazwy „Archon”. Stosowany **wyłącznie** na zdjęciach zabiegów i portretach zespołu — nie jest ogólnym stylem kart i nie należy go nadużywać gdzie indziej.

### Cień

Jeden, konsekwentnie powtarzany cień dla unoszących się paneli (np. rozwijane menu):

```css
box-shadow: 24px 0px 64px 0px rgba(112, 108, 105, 0.1);
```

Duży, miękki, ciepło-szary (nie czarny) przy 10% krycia — panel „unosi się” bez twardej krawędzi.

---

## 6. Siatka i odstępy

- Maksymalna szerokość kontenera treści: **1440px**
- Skala odstępów (zaokrąglona z obserwowanych ~78,5px / ~39,25px do spójnej skali 8-punktowej):

| Token | Wartość | Użycie |
|---|---|---|
| micro | 8px | Odstępy wewnątrz elementu |
| element | 16px | Między powiązanymi elementami |
| group | 24px | Między grupami elementów |
| gutter | 40px | Margines boczny kontenera (mobile/tablet) |
| block | 64px | Odstęp między blokami treści |
| section-y | 80px | Padding pionowy sekcji (desktop) |
| section-gap | 120px | Odstęp między głównymi sekcjami |

---

## 7. Rytm sekcji

Cała strona przełącza się naprzemiennie między tłem `cream` i `black-olive`. To **jedyny** mechanizm rytmu wizualnego — brak pośrednich kolorowych bloków. Każde przejście ma działać jak oddech.

Referencyjny układ strony głównej:

1. Hero — zdjęcie pełnoekranowe + ciemny overlay
2. Filozofia marki — `cream`
3. Zabiegi / oferta — `black-olive`
4. Opinie klientów (karuzela) — `black-olive`
5. Kontakt (3 kolumny: telefon / adres / e-mail) — `cream`
6. Newsletter / program lojalnościowy — `cream`
7. Stopka — `cream`

**Zasada:** nowa sekcja nie powinna powtarzać tła bezpośredniego poprzednika częściej niż dwa razy z rzędu — inaczej rytm się gubi.

---

## 8. Komponenty

### Nawigacja
Pasek **sticky**, tło `cream`, logotyp „ARCHON” (Tenor Sans, wersaliki, mały superscript „TM”) po lewej, linki nawigacyjne na środku/prawo (Inter 500 12px), dwa CTA po prawej krawędzi (outline + solid olive).

### Mega-menu
Rozwijany panel na tle `#FFFFFF`, cień z sekcji 5, kolumny grupujące linki. Każda kolumna ma małą, wersalikową etykietę kategorii (Inter 700, ~10px, +1px tracking) podkreśloną cienką linią-separatorem (`--a-taupe`), a pod nią listę zwykłych linków (Inter 400/500, ~13–14px).

### Linki i stany hover
**Reguła obowiązująca w całym serwisie**: każdy klikalny link tekstowy (nawigacja, linki w mega-menu, stopka, linki w treści) zmienia kolor na `--a-rust` (`#C7642D`) na `:hover`, z płynnym przejściem `transition:color .2s`. Bez podkreślenia — sama zmiana koloru wystarcza jako sygnał interaktywności. Wzorzec ustalony pierwotnie w mega-menu, rozszerzony na całą stronę.

**Wyjątki** (własny, odrębny język interakcji, nie rust):
- Przyciski `.abtn` — hover to uniesienie (`translateY(-8px)`) + cień, bez zmiany koloru tekstu.
- Ikony social media (stopka) — zmiana na `--a-olive`.
- Strzałki karuzeli opinii — zmiana na `--a-taupe`.
- Karty zabiegów („kadr łuk”) — własny hover (odwrócenie zaokrąglenia + uniesienie + przyciemnienie zdjęcia), nie kolor tekstu.

### Karty zabiegów
Tło `black-olive` lub `#1f2117`, zdjęcie zabiegu u góry (bez zaokrąglenia typu „łuk” — tu zwykłe 10px), nazwa zabiegu (Inter 500), cena w kolorze `--a-lime`, link „Book Just This” jako **ghost-link** (podkreślenie, nie pełny przycisk) — mniej szumu przy wielu kartach obok siebie.

### Testimoniale
Karuzela na tle `black-olive`, cytat + imię i inicjał nazwiska + gwiazdki + dopisek źródła („Google Review - 5 Stars” na archon.au; u nas „Opinia Google/Fresha - 5 Gwiazdek”, dopasowany do faktycznego źródła każdej opinii), nagłówek sekcji wyśrodkowany (`text-align:center`, jedyna różnica względem bazowej `.h-section`). Nagłówek dzieli bazową `.h-section` (30px/500/36px/-1px). Licznik slajdów w stylu „Slide 2 of 7” na archon.au — u nas kropki nawigacyjne zamiast licznika tekstowego (ustalone we wcześniejszej rundzie).

**Świadome odejście od archon.au (na wyraźną prośbę użytkownika, Runda 33, 2026-08-27)**: cytat ma `line-height:30px` i `margin-bottom:36px` zamiast sitewide `16px/27,2px` (patrz sekcja 3) — nasza najdłuższa opinia (406 znaków) jest dłuższa niż najdłuższa na archon.au (384 znaków) i przy standardowym odstępie wyglądała na zbyt gęstą. Dotyczy wyłącznie tego komponentu, nie zmienia tokenu sitewide.

### Kontakt
3 kolumny (Telefon / Adres / E-mail), każda z krótkim opisem i linkiem akcji.

### Stopka
Tło `cream`, kolumny linków pogrupowane tematycznie (zabiegi skórne, laserowe, zasoby), dane kontaktowe, linki prawne, nota o wykonawcy strony.

---

## 9. Fotografia

| Element | Wytyczna |
|---|---|
| Nastrój | Ciemny, stonowany, redukcyjny — nigdy jasny i „kliniczny” |
| Motywy | Botanika (liście, gałązki), tekstury wody, owoce/cytrusy w makro |
| Overlay | Gradient do czerni pod tekstem w hero, ~40–60% krycia |
| Kadrowanie produktowe | Kadr „łuk” (sekcja 5), bardziej nasycone, ciepłe światło niż tło hero |

---

## 10. Zasady twarde (nie łamać)

1. Border-radius przycisków nigdy > 3px.
2. Kadr „łuk” (`150px 150px 20px 20px`) tylko na zdjęciach zabiegów/portretach — nie jako ogólny styl kart.
3. Lime (`#BFF751`) tylko jako rzadki akcent punktowy, nigdy jako dominujące tło lub kolor tekstu.
4. Nagłówki zawsze Tenor Sans 400 z ujemnym trackingiem; nigdy pogrubione, nigdy wersaliki.
5. Etykiety (eyebrow/label) zawsze Inter, zawsze z dodatnim trackingiem, zawsze wersaliki lub capitalize — nigdy Tenor Sans.
6. Sekcje przełączają się między `cream` i `black-olive` — bez wprowadzania nowych kolorów tła.
7. Ton głosu: zapraszający, inkluzywny („everyone welcome”), nigdy nachalnie sprzedażowy.

---

*Źródło: analiza computed styles żywej strony archon.au, sierpień 2026. Pełna wersja wizualna (próbki kolorów, żywe specimeny typografii, komponenty) dostępna jako artefakt: „Archon Design System”.*
