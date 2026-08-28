# PLAN — INSTYTUTem.pl (redesign wizualnie wzorowany na archon.au)

> Ten plik jest checklistą postępu, widoczną „jak na dłoni” obok [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md) (design system) i [DOKUMENTACJA.md](DOKUMENTACJA.md) (log decyzji). Aktualizowany po każdej rundzie weryfikacji.

---

## Stały proces weryfikacji (obowiązuje przy KAŻDEJ zmianie kodu)

Pełny, obowiązujący proces (pomiar DOM → kod → ponowna weryfikacja) opisany jest raz, w [CLAUDE.md](CLAUDE.md#zweryfikowany-proces-na-przyszłość) — nie duplikować go tutaj. Proces dla zdjęć AI zabiegów: [CLAUDE.md](CLAUDE.md#proces-zdjęcia-zabiegów-generowane-ai-nano-banana--gemini). Wynik każdej rundy trafia do tabeli niżej (stan bieżący, jedno zdanie) i do [DOKUMENTACJA.md](DOKUMENTACJA.md) (pełny log decyzji, historia).

---

## Checklista sekcji — stan bieżący

Kolumna „Uwagi” to **skrót stanu bieżącego, jedno-dwa zdania, nie historia zmian** — pełny, chronologiczny opis każdej rundy (co, dlaczego, jak zweryfikowane) jest wyłącznie w [DOKUMENTACJA.md](DOKUMENTACJA.md#log-decyzji-i-konsultacji-dokumentacji). Nie kopiować stamtąd akapitów tutaj.

| Sekcja | Zbudowane | Zgodne z archon.au | Stan bieżący |
|---|---|---|---|
| Nav (sticky) | ✅ | 🟡 świadome odejście w treści, 1:1 w stylu | Menu: Konsultacje/Problem/Zabiegi/Cennik/O nas/Kontakt + CTA „Rezerwuj online”/„Kup Kartę Podarunkową” (linki Fresha). Mega-panele stylowo 1:1 z archon.au (pozycja pod headerem, hover rdzawy, dynamiczne pozycjonowanie JS), treść własna — szersza niż archon.au. Historia: DOKUMENTACJA.md Rundy 9–10, 36–38. |
| Hero | ✅ | ✅ | Treść pełnej szerokości, hover przycisków 1:1 z oryginałem. |
| Filozofia marki | ✅ | ✅ | Nagłówek/akapit na zmierzonych wartościach archon.au (`.h-section` 30px/500/36px/-1px, `.lede` 16px/27.2px), wyrównanie i szerokość kolumny naprawione. |
| Rząd zabiegów (kadr „łuk”) | ✅ | 🟢 zamknięte (layout), treść w toku | Wszystkie 24 zabiegi z menu „Zabiegi”, w tej kolejności. Layout/interakcje (min/max-width, drag-to-scroll, paralaksa, hover) zamknięte i zweryfikowane. Status zdjęcia per pozycja: [Lista zabiegów, DOKUMENTACJA.md](DOKUMENTACJA.md#lista-zabiegów-oferta-—-źródło-prawdy) — jedyne źródło prawdy, nie duplikować tu. |
| RX Facials (zima) | ✅ | 🟡 do zweryfikowania | Nagłówek/akapit dzielą naprawioną `.h-section`/`.lede`. 3× link „Zarezerwuj Tylko To” na realnym Fresha, ale ogólny, nie deep-link per zabieg (patrz TODO). |
| Opinie klientów (karuzela) | ✅ | ✅ | 7 prawdziwych opinii (3 instytutem.pl + 4 Fresha), dopisek źródła 1:1 z archon.au, nagłówek wyśrodkowany + większy odstęp cytatu (świadome odejście, opisane w DESIGN-SYSTEM.md). |
| Kontakt | ✅ | 🟢 zamknięte | Nagłówek `.h-hero.center` (60px, zmierzony), realne dane instytutem.pl (telefon/adres/e-mail — te same co w stopce). |
| Karty podarunkowe (dawniej „Vouchery”) | ✅ | 🟢 1:1 | Odstępy/kolory zmierzone z archon.au, nazewnictwo ujednolicone na „karta podarunkowa” w całym projekcie, link zakupu Fresha we wszystkich 6 miejscach. |
| Banner rezerwacji | ✅ | 🟢 1:1 | Klasa `.h-quote` (60px, responsywny quirk 72px/51px), stała wysokość 600px, przycisk `.abtn.primary-black`, prawdziwe zdjęcie tła AI. Świadome, udokumentowane odejścia (bez magnetic-hover, bez wymuszonej szerokości przycisku) — DOKUMENTACJA.md. |
| Pasek korzyści (marquee) | ✅ | 🟢 1:1 | Kropka `#FFC8AA` (nie rdzawa), typografia responsywna, mechanizm scroll-linked JS (nie samoczynna pętla) z dynamicznym doklonowaniem kafelków dla dowolnej szerokości ekranu. |
| Newsletter | ✅ | 🟡 do zweryfikowania | Nagłówek „Archon Rewards” prawdopodobnie za duży styl (powinna być mała etykieta jak `.eyebrow`) — niezweryfikowane dokładnie, patrz TODO. |
| Stopka | ✅ | ✅ | Ikony Facebook + Instagram z prawdziwymi linkami. |
| Responsywność (mobile/desktop) | ✅ | ✅ | Bez otwartych rozbieżności. |
| Dostępność (klawiatura) | ✅ | ✅ | Kropki karuzeli klikalne, z `aria-label`. |

---

## Zdjęcia zabiegów (galeria `#treatments`)

Pełny status per zabieg (24 pozycji, plik/AI/CDN archon.au/placeholder) → **wyłącznie** [Lista zabiegów, DOKUMENTACJA.md](DOKUMENTACJA.md#lista-zabiegów-oferta-—-źródło-prawdy). Podsumowanie na dziś:

- **23 z 24** kart ma zdjęcie — jedyna bez to **Mezoterapia mikroigłowa**, celowo wstrzymana, patrz TODO niżej (możliwy duplikat SkinPen).
- **Wszystkie 11 oryginalnych zdjęć CDN archon.au podmienione na AI** — galeria `#treatments` jest teraz wolna od treści z Australii.
- Poza galerią: hero, RX Facials (×3), banner rezerwacji — patrz „Otwarte TODO”.

---

## Otwarte TODO

To jest **jedyne, aktualne** miejsce śledzenia zadań — nie duplikować w DOKUMENTACJA.md ani gdzie indziej, i nie trzymać tu ukończonych zadań (te mają swoją historię w DOKUMENTACJA.md, tutaj usuwane po zamknięciu). Pełny opis decyzji stojących za poszczególnymi punktami → [DOKUMENTACJA.md](DOKUMENTACJA.md#log-decyzji-i-konsultacji-dokumentacji).

- [ ] **Potwierdzić treść kategorii „O INSTYTUTem.”** (dropdown „O nas”) — dostarczona treść była identyczna z „Dla Klientów” (błąd kopiuj-wklej), tymczasowo jeden link zastępczy `/o-nas`.
- [ ] **Potwierdzić, czy „Mezoterapia mikroigłowa” i „Mikronakłuwanie SkinPen®” to zdublowana usługa** (Runda 68) — SkinPen to marka urządzenia do mezoterapii mikroigłowej, mogą to być dwie nazwy tego samego zabiegu (analogicznie do potwierdzonego duplikatu niżej). Użytkownik musi dopytać w salonie. Do odpowiedzi karta zostaje bez zdjęcia.
- [ ] **Potwierdzić, czy „LPG® Ergolift” i realny URL `/zabiegi/endermologia-twarzy-plock-lpg-endermolift` to ten sam zabieg** — użytkownik w innej rundzie już raz odrzucił podobną pozycję jako duplikat, więc nie zmieniać bez ponownego potwierdzenia.
- [ ] **Zbudować realne podstrony dla nowego menu** (~50 pozycji pod Konsultacje/Problem/Zabiegi/O nas, dziś 404) — 14 z nich to już realne, zaindeksowane URL-e z listy SEO (zachować 1:1), reszta to nowe adresy własnego autorstwa do potwierdzenia przed budową treści.
- [ ] Cała pozostała treść `index.html` poza tym, co już podmienione (hero, dane wizytówki poza Kontaktem/stopką) — zachować listę URL 1:1 (sekcja SEO w DOKUMENTACJA.md).
- [ ] Podłączenie formularza newslettera pod realny ESP (Mailchimp/Klaviyo/Formspree).
- [ ] 3 linki „Zarezerwuj Tylko To” w RX Facials prowadzą na ogólny link Fresha, nie deep-link per zabieg — podmienić, jeśli Fresha udostępni linki per-usługa.
- [ ] Odstęp nagłówek→siatka w sekcji Kontakt: archon.au ma 150px, u nas 40px — do decyzji, czy dociągnąć czy zostawić jako świadome odejście.
- [ ] Nagłówek „Archon Rewards — Dołącz za Darmo” prawdopodobnie zły styl (powinna być mała etykieta `.eyebrow`-podobna, nie duży `.h-section`) — niezweryfikowane dokładnie.
- [ ] Zdjęcia kart **RX Benefactor / RX Illuminate / RX Detox Facial** (3 placeholdery poza galerią `#treatments`).
- [ ] **Tło hero** (`.hero-bg`) — pełnoekranowe zdjęcie botaniczne/makro w ciemnym klimacie + overlay, wciąż placeholder.
- [ ] **Favicon** — logo mark już mamy (`instytutem-logo.svg`), favicon (16×16/32×32) jeszcze nie wygenerowany.
