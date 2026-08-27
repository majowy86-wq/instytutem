# PLAN — Archon (strona własna)

> Ten plik jest checklistą postępu, widoczną „jak na dłoni” obok [archon.md](archon.md) (design system) i [DOKUMENTACJA.md](DOKUMENTACJA.md) (log decyzji). Aktualizowany po każdej rundzie weryfikacji.

---

## Stały proces weryfikacji (obowiązuje przy KAŻDEJ zmianie kodu)

Przy każdej zmianie w `index.html` / `css/styles.css` / `js/main.js`:

1. **Zrzut ekranu** zmienionej sekcji z lokalnej wersji (przeglądarka, desktop + mobile).
2. **Zrzut ekranu** tej samej sekcji z żywej **archon.au** — obok siebie.
3. **Porównanie**: układ, kolory, typografia, odstępy, zachowanie interakcji. Gdy zrzut ekranu zawiedzie technicznie, porównanie przez bezpośredni odczyt DOM (`getBoundingClientRect`, `getComputedStyle`) jako metoda równoważna.
4. **Różnice** → poprawka kodu → ponowne porównanie, aż będzie zgodnie. Jedyny akceptowalny wyjątek: brak prawdziwych zdjęć (placeholdery CSS udokumentowane w [DOKUMENTACJA.md](DOKUMENTACJA.md)).
5. Gdy `chrome-devtools-mcp` będzie załadowany w sesji — dołączenie sprawdzenia konsoli/sieci/wydajności do tej samej pętli.

---

## Checklista sekcji — stan po rundzie weryfikacji z 2026-08-27 (Chrome DevTools MCP)

| Sekcja | Zbudowane | Zgodne z archon.au | Uwagi |
|---|---|---|---|
| Nav (sticky, mega-menu Skin) | ✅ | ✅ | **Prawdziwe logo SVG** (nie tekst) pobrane z CDN archon.au. Dodano strzałki dropdown na Laser/Men/Women/About. Poprawiony margines kontenera (40px→72px/5%). **Runda 2**: usunięto domyślne obramowanie przycisku „Skin” (globalny reset `button{border:0;background:none}`), powiększono i ujednolicono strzałki (SVG chevron zamiast małego unikodu), **całkowicie przebudowano mega-menu „Skin”** z 3-kolumnowej siatki na jedną wąską kolumnę (300px, lewo-wyrównaną pod przyciskiem) — dokładnie jak oryginał, zweryfikowane przez realne kliknięcie na żywej stronie |
| Hero | ✅ | ✅ | **Runda 2 — poprawiony realny błąd**: `.hero{display:flex}` powodowało, że `.hero-content` kurczyło się do szerokości nagłówka i centrowało przez `margin:auto`, zamiast rozciągać się na całą szerokość — stąd treść była "przyklejona" nie do tej samej krawędzi co nawigacja. Naprawione przez `position:absolute;inset:0` + wewnętrzny wrapper `width:100%`. Dodano animację hover na przyciskach (`translateY(-8px)` + cień, dokładnie jak oryginał) |
| Filozofia marki | ✅ | ✅ | Poprawiony `letter-spacing` eyebrow (.14em→0.5px), margines kontenera |
| Rząd zabiegów (kadr „łuk”) | ✅ | ✅ | Poprawiony rozmiar kart na desktop (243×600px → **282×450px**, gap 1.25rem→1rem) na podstawie realnego pomiaru na żywej stronie |
| RX Facials (zima) | ✅ | ✅ | Bez dodatkowych zmian w tej rundzie |
| Opinie klientów (karuzela) | ✅ | ✅ | **Przebudowana struktura**: wyśrodkowany układ (był lewostronny), dodano gwiazdki ★★★★★ i imię/nazwisko jako osobne linie, licznik tekstowy „Slide X of 7” zamieniony na **kropki paginacji** (7 kropek, klikalne) — dokładnie jak oryginał |
| Kontakt | ✅ | ✅ | **Błędne wcześniej tło** — poprawione z cream na **black-olive**. Każda kolumna to teraz obramowany box (`border:1px solid var(--a-gray)`), wartości (telefon/adres/e-mail) jako pełnoszerokie przyciski `.abtn.gray` zamiast podkreślonych linków — dokładnie jak oryginał |
| Vouchery | ✅ | ✅ | Bez dodatkowych zmian w tej rundzie |
| Banner rezerwacji | ✅ | ✅ | Bez dodatkowych zmian w tej rundzie |
| Newsletter | ✅ | ✅ | Bez zmian |
| Stopka | ✅ | ✅ | Dodano ikony Facebook + Instagram (prawdziwe linki: facebook.com/archonaustralia, instagram.com/archon.australia) |
| Responsywność (mobile/desktop) | ✅ | ✅ | Bez zmian w tej rundzie |
| Dostępność (klawiatura) | ✅ | ✅ | Kropki karuzeli też klikalne i z `aria-label` |

### Krytyczna poprawka: usunięto animację scroll-reveal

Animacja pojawiania się sekcji przy scrollu (JS + IntersectionObserver, ustawiająca `opacity:0` na starcie) **nie zawsze się uruchamiała poprawnie i zostawiała całe sekcje niewidocznymi**. To był prawdziwy błąd w kodzie, nie usterka narzędzia — wykryty dzięki zrzutowi pełnej strony w Chrome DevTools MCP, gdzie widać było puste bloki tam, gdzie powinna być treść. Bardzo prawdopodobne, że to główny powód wcześniejszych odczuć „strona nie wygląda jak oryginał”. Usunięto całą funkcję (zgodnie z zasadą KISS — to była tylko dekoracja, niewarta ryzyka niewidocznej treści).

**Poprawka procesu weryfikacji na przyszłość**: zrzut *pełnej strony* (`fullPage`) jest zawodny na stronach z animacjami scroll-reveal (dotyczy też samego archon.au — ich Webflow-owe animacje też nie odpalają się przy jednorazowym renderze pełnej wysokości). Weryfikacja powinna polegać na przewijaniu normalnym + zrzutach widoku (viewport), tak jak robi to prawdziwy użytkownik — nie na jednorazowym renderze całej strony.

---

## Otwarte TODO (pełna lista i szczegóły → [DOKUMENTACJA.md](DOKUMENTACJA.md))

- [ ] 6 placeholderów zdjęć do podmiany (hero, kadr-łuk ×11 w rzędzie zabiegów, 3× RX Facials, banner rezerwacji)
- [x] ~~Prawdziwy adres e-mail kontaktowy~~ — znalezione i wstawione (2026-08-27): `hello@archonspas.com.au` (kontakt), `hello@archon.au` (stopka)
- [x] ~~Link do platformy rezerwacyjnej~~ — znalezione i wstawione (2026-08-27): `bookings.gettimely.com/archonspas/book`
- [x] ~~Link do platformy voucherów~~ — znalezione i wstawione (2026-08-27): `bookings.gettimely.com/archonspas/purchase`
- [ ] Podstrony `skin.html`, `laser.html`, `men.html`, `women.html`, `about.html` — w tym pełne mega-menu dla Laser/Men/Women/About (obecnie same strzałki bez treści; wiemy już, że to wąskie 1-kolumnowe dropdowny jak Skin, nie duże mega-menu — brakuje tylko realnej treści linków)
- [ ] Podłączenie formularza newslettera pod realny ESP (Mailchimp/Klaviyo/Formspree)
