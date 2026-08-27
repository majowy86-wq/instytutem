# PLAN — INSTYTUTem.pl (redesign wizualnie wzorowany na archon.au)

> Ten plik jest checklistą postępu, widoczną „jak na dłoni” obok [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) (design system) i [DOKUMENTACJA.md](DOKUMENTACJA.md) (log decyzji). Aktualizowany po każdej rundzie weryfikacji.

---

## Stały proces weryfikacji (obowiązuje przy KAŻDEJ zmianie kodu)

Pełny, obowiązujący proces (pomiar DOM → kod → ponowna weryfikacja) opisany jest raz, w [CLAUDE.md](CLAUDE.md#zweryfikowany-proces-na-przyszłość) — nie duplikować go tutaj. Wynik każdej rundy trafia do tabeli niżej (stan bieżący) i do [DOKUMENTACJA.md](DOKUMENTACJA.md) (pełny log decyzji).

---

## Checklista sekcji — stan bieżący

Kolumna „Uwagi” to skrót stanu bieżącego, nie historia zmian — pełny, chronologiczny opis każdej rundy (co, dlaczego, jak zweryfikowane) jest w [DOKUMENTACJA.md](DOKUMENTACJA.md#log-decyzji-i-konsultacji-dokumentacji).

| Sekcja | Zbudowane | Zgodne z archon.au | Stan bieżący |
|---|---|---|---|
| Nav (sticky) | ✅ | 🟡 świadome odejście w treści, 1:1 w stylu | **Runda 9+10 (2026-08-27)**, patrz DOKUMENTACJA.md. Menu: **Konsultacje / Problem / Zabiegi / Cennik / O nas / Kontakt** + przyciski „Rezerwuj online"/„Kup Voucher" (`rezerwuj.instytutem.pl`, prawdziwy). Mega-panele wielokolumnowe (kolumna = kategoria) — treść dużo obszerniejsza niż archon.au, świadome odejście strukturalne. **Styl teraz 1:1 z archon.au** (Runda 10): panel zaczyna się dokładnie na dole headera (przycisk `height:80px`, nie samo `top:100%` na wyśrodkowanym flexem elemencie), hover linku = kolor rdzawy `--a-rust` (nie podkreślenie), otwarta pozycja menu = cienka oliwkowa linia u dołu (`box-shadow inset`), padding panelu `20px 48px 25px`. Szerokie panele pozycjonowane dynamicznie w JS, żeby zawsze mieściły się w viewport. Logo prawdziwe (instytutem.pl), wysokość stała 80px, menu+CTA jedna grupa wyrównana do prawej — bez zmian. |
| Hero | ✅ | ✅ | Treść rozciągnięta na pełną szerokość (nie kurczy się), hover na przyciskach jak w oryginale |
| Filozofia marki | ✅ | ✅ | Nagłówek (`.h-section`) i akapit (`.lede`) naprawione na realne, zmierzone wartości (Runda 28): `30px/waga 500/36px/-1px` (było błędnie `~48px`, nigdy niezmierzone) i `16px/27.2px` — sitewide, patrz niżej. **Runda 29**: naprawiono też wyrównanie akapitu do nagłówka (`margin:0`, znosi domyślny margines `<p>`) i jego szerokość (`max-width:none` zamiast zgadniętego `60ch`) — teraz `diff:0` i pełna szerokość kolumny `2fr` (`732px` przy 1280px okna), zgodnie z archon.au |
| Rząd zabiegów (kadr „łuk”) | ✅ | 🟢 **ZAMKNIĘTE (Runda 29)** | **Wszystkie 24 zabiegi z menu „Zabiegi", w tej samej kolejności** (Runda 26+27 — patrz [DOKUMENTACJA.md](DOKUMENTACJA.md#lista-zabiegów-oferta-—-źródło-prawdy) dla pełnej, aktualnej listy nazwa→URL→zdjęcie) — 11 z realnym zdjęciem z CDN archon.au, 13 jako placeholder-gradient (`.ph-gradient`, ta sama konwencja co karty RX Facials) do czasu prawdziwych fotografii. Karta `width:22%` (responsywnie 38%/60%) **ograniczone `min-width:173px`/`max-width:315px`, zmierzone na archon.au** (Runda 26). Przewijanie: drag-to-scroll myszką + natywne, pasek scrolla ukryty, margines po lewej tylko w widoku początkowym, po prawej zawsze `0` (edge-to-edge, wyrównane z nagłówkiem nawet >1440px). Pozioma paralaksa zdjęć 1:1 z archon.au (tylko na prawdziwych zdjęciach). Hover: łuk się odwraca + przyciemnienie zdjęcia — **bez unoszenia karty** (świadome odejście od 1:1 z archon.au na wyraźną prośbę). Podpisy zweryfikowane pod kątem przepełnienia na wąskich widokach (naprawiony `overflow-wrap` dla nazw z „/"). **Ważne**: „Lista zabiegów" w DOKUMENTACJA.md jest teraz jedynym źródłem prawdy dla tej galerii i dla nav/drawer/stopki — aktualizować ją przy każdej zmianie oferty (zasada dodana w Rundzie 27 po tym, jak te dwa miejsca się rozjechały). **Sekcja zamknięta**: cały cykl przebudowy (Rundy 7, 20–29 — zdjęcia, drag-to-scroll, ukryty scrollbar, margines edge-to-edge, paralaksa, hover bez liftu, min/max-width, komplet 24 pozycji, podpisy) jest zakończony i zweryfikowany pomiarem DOM zgodnie z procesem z CLAUDE.md; dalsze zmiany w tej sekcji to już nie poprawki wizualne/interakcyjne, tylko czysto treściowe zadania, śledzone osobno niżej w „Otwarte TODO" (13 kart bez zdjęcia, niejednoznaczność „LPG® Ergolift") |
| RX Facials (zima) | ✅ | ✅ | Nagłówek dzieli tę samą naprawioną `.h-section` (Runda 28) — `30px/500/36px/-1px`, zgodne z archon.au. Akapit `.lede` wyrównany do nagłówka i pełna szerokość kolumny (Runda 29) |
| Opinie klientów (karuzela) | ✅ | ✅ | Cytat Inter 16px/27.2px, nagłówek stały 30px (od Rundy 6; scoped override usunięty w Rundzie 28, bo bazowa `.h-section` teraz daje ten sam wynik), gwiazdki SVG, strzałki po bokach boksu 800px, przejście `translateX` z animowaną wysokością |
| Kontakt | ✅ | 🟡 do zweryfikowania | Tło black-olive, kolumny jako obramowane boxy z przyciskami `.abtn.gray`. **Nagłówek „Bądźmy w kontakcie" używa tej samej `.h-section` (30px), ale na archon.au odpowiednik („Get in touch") to inna, większa klasa `.heading.hero` — realnie 60px/500/-2px** (Runda 28, zauważone, nie naprawione — patrz „Otwarte TODO") |
| Vouchery | ✅ | ✅ | Nagłówek dzieli tę samą naprawioną `.h-section` (Runda 28). Akapit `.lede` wyrównany do nagłówka i pełna szerokość kolumny (Runda 29) |
| Banner rezerwacji | ✅ | ✅ | Bez otwartych rozbieżności |
| Newsletter | ✅ | 🟡 do zweryfikowania | **Cytat „Zrób sobie chwilę poza codziennością" używa `.h-section` (30px), ale odpowiednik na archon.au to `.heading.display` — realnie 60px/500/-1px, line-height 94px** (Runda 28, zauważone, nie naprawione — patrz „Otwarte TODO") |
| Stopka | ✅ | ✅ | Ikony Facebook + Instagram z prawdziwymi linkami |
| Responsywność (mobile/desktop) | ✅ | ✅ | Bez otwartych rozbieżności |
| Dostępność (klawiatura) | ✅ | ✅ | Kropki karuzeli klikalne, z `aria-label` |

---

## Otwarte TODO

To jest **jedyne, aktualne** miejsce śledzenia zadań i placeholderów — nie duplikować w DOKUMENTACJA.md ani gdzie indziej. Pełny opis decyzji stojących za poszczególnymi punktami → [DOKUMENTACJA.md](DOKUMENTACJA.md#log-decyzji-i-konsultacji-dokumentacji).

- [x] ~~Stopka niespójna z nowym menu głównym~~ — naprawione (2026-08-27, Runda 11): stopka przebudowana na te same 5 kategorii i te same linki co menu w nagłówku (Konsultacje/Problem/Zabiegi/O nas + Cennik/Kontakt), z podpisami podkategorii jak w drawerze mobilnym. Dane kontaktowe w stopce podmienione na realne z instytutem.pl.
- [ ] **Potwierdzić z użytkownikiem treść kategorii „O INSTYTUTem."** (dropdown „O nas") — dostarczona treść była identyczna z „Dla Klientów" (najpewniej błąd kopiuj-wklej), tymczasowo jeden link zastępczy `/o-nas`. Oznaczone `TODO` w kodzie (desktop + mobile).
- [ ] **Zbudować realne podstrony dla nowego menu** (Runda 9) — ok. 50 pozycji pod Konsultacje/Problem/Zabiegi/O nas prowadzi na razie donikąd (404), w tym: 14 linków do już realnych, zaindeksowanych URL-i z listy SEO (do zachowania 1:1 przy budowie), reszta to nowe adresy własnego autorstwa (kebab-case, `/problem/...`, `/konsultacje/...`, nowe pozycje w `/zabiegi/...`) — **do potwierdzenia z użytkownikiem przed zbudowaniem treści**, żeby nie inwestować w złą strukturę URL. Pełna lista decyzji URL→URL w DOKUMENTACJA.md (Runda 9).
- [ ] Cała pozostała treść `index.html` (hero, oferta, adres, kontakt) — podmienić z archon.au (Australia) na prawdziwą treść instytutem.pl, zachowując zebraną listę URL 1:1 (patrz DOKUMENTACJA.md, sekcja SEO)
- [ ] Podłączenie formularza newslettera pod realny ESP (Mailchimp/Klaviyo/Formspree)
- [ ] **Nagłówek sekcji Kontakt i cytat Newslettera używają za małego stylu** (Runda 28) — obecnie dzielą `.h-section` (30px, poprawne dla większości sekcji), ale ich odpowiedniki na archon.au to inna, większa klasa `.heading.hero`/`.heading.display`: realnie **60px/waga 500**, letter-spacing -1px do -2px (dokładne wartości i różnice line-height w DESIGN-SYSTEM.md). Wymaga nowej klasy (np. `.h-hero-alt`) i przypięcia jej do tych 2 miejsc — nie zrobione, bo wykracza poza zakres prośby o weryfikację.
- [ ] **Baner „Archon Rewards — Dołącz za Darmo" prawdopodobnie używa złego stylu** (Runda 28) — u nas duży nagłówek sekcji (`.h-section`), ale odpowiednik na archon.au to mała etykieta wielkimi literami (`h4.uppercase`, 12px/600/uppercase — bardzo bliska naszej `.eyebrow`), nie duży nagłówek. Niezweryfikowane dokładnie, tylko zauważone przy okazji.
- [x] ~~Przebudować mega-menu „Mężczyźni"/„Kobiety" (podział wg płci 1:1 z archon.au)~~ — nieaktualne (2026-08-27, Runda 9): całe menu Skóra/Laser/Mężczyźni/Kobiety/O nas zastąpione nową strukturą instytutem.pl (Konsultacje/Problem/Zabiegi/Cennik/O nas/Kontakt), patrz wiersz „Nav" wyżej i DOKUMENTACJA.md.
- [x] ~~Podstrony `skin.html`, `laser.html`, `men.html`, `women.html`, `about.html`~~ — nieaktualne jako cel menu głównego (Runda 9, zastąpione nową strukturą); nadal linkowane ze stopki, patrz punkt o stopce wyżej.
- [x] ~~Nav: logo ściska się (traci proporcje) przy szerokości okna ok. 900–1000px~~ — naprawione (2026-08-27): dodano `flex-shrink:0` do `.logo`. Zweryfikowane pomiarem DOM przy 990px (proporcja 2.201, bez zniekształcenia). Efekt uboczny zaakceptowany: w tym samym wąskim zakresie etykieta „O nas" może się zawinąć do dwóch linii (nav-links ma domyślny `flex-shrink:1`, więc to on teraz ustępuje miejsca zamiast logo) — mniejsze zło niż zniekształcona marka.
- [x] ~~Prawdziwy adres e-mail kontaktowy~~ — znalezione i wstawione (2026-08-27): `hello@archonspas.com.au` (kontakt), `hello@archon.au` (stopka)
- [x] ~~Link do platformy rezerwacyjnej~~ — znalezione i wstawione (2026-08-27): `bookings.gettimely.com/archonspas/book`
- [x] ~~Link do platformy voucherów~~ — znalezione i wstawione (2026-08-27): `bookings.gettimely.com/archonspas/purchase`
- [x] ~~Mega-menu Laser/Men/Women/About~~ — zbudowane (2026-08-27): realna treść i struktura pobrane bezpośrednio z żywej archon.au (grupy kategorii + podkreślenie, wąska 1-kolumnowa, dokładnie jak Skin). JS uogólniony do obsługi wszystkich 5 przycisków. Dodano też odpowiedniki w mobilnym `<details>`.

### Placeholdery zdjęć do podmiany na prawdziwe fotografie instytutem.pl

Miejsca oznaczone w kodzie komentarzem/atrybutem `TODO` lub `aria-label` zaczynającym się od „TODO” (poza rzędem zabiegów, już wypełnionym — patrz niżej). Obecnie wypełnione gradientem CSS w klimacie marki.

- [ ] **Tło hero** (`index.html`, sekcja `.hero-bg`) — pełnoekranowe zdjęcie botaniczne/makro w ciemnym klimacie + overlay.
- [x] ~~11 zdjęć w kadrze „łuk” w rzędzie zabiegów~~ (`.trick-card`) — wypełnione (Runda 7, 2026-08-27) prawdziwymi zdjęciami z CDN archon.au (`assets/images/treatments/`), wizualnie gotowe. **Nadal treściowo AU** (zdjęcia stockowe klientów Archon) — do podmiany na prawdziwe fotografie zabiegów instytutem.pl przed publikacją.
- [ ] **13 dalszych kart w rzędzie zabiegów bez żadnego zdjęcia** (Runda 26+27, po rozszerzeniu rzędu do pełnych 24 pozycji z menu „Zabiegi" — pełna lista z URL-ami w DOKUMENTACJA.md) — obecnie placeholder-gradient (`.ph-gradient`): Laser Tulowy Erbowo-Szklany, LPG® Ergolift, Fototerapia LED Dermalux®, Plasma™, Autologiczne wypełniacze ATR, Kwas polimlekowy PLLA, Mezoterapia igłowa, Nici liftingujące PDO/PLLA, Fibryna i osocze bogatopłytkowe, Stymulatory tkankowe, Mezoterapia mikroigłowa, Mezoterapia bezigłowa, Peelingi Medyczne.
- [ ] **Do potwierdzenia: „LPG® Ergolift" vs realny URL `/zabiegi/endermologia-twarzy-plock-lpg-endermolift`** — mogą być tym samym zabiegiem pod różnymi nazwami (patrz DOKUMENTACJA.md, sekcja „Lista zabiegów"). Nie zmieniane bez potwierdzenia — użytkownik już raz odrzucił podobną pozycję jako duplikat (Runda 13).
- [ ] Zdjęcie karty **RX Benefactor Facial**.
- [ ] Zdjęcie karty **RX Illuminate Facial**.
- [ ] Zdjęcie karty **RX Detox Facial**.
- [ ] Zdjęcie tła **bannera rezerwacji** (`.banner-photo-bg`) — wnętrze salonu.
- [ ] **Favicon** — logo mark już mamy (`instytutem-logo.svg`), ale favicon (16×16/32×32) jeszcze nie wygenerowany.
