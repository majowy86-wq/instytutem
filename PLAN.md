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

## Checklista sekcji — stan po rundzie weryfikacji z 2026-08-26

| Sekcja | Zbudowane | Zgodne z archon.au | Uwagi |
|---|---|---|---|
| Nav (sticky, mega-menu Skin) | ✅ | ✅ | Poprawiono: kolejność przycisków (Book Online → Gift Vouchers), padding loga (konflikt CSS `.nav-row`/`.container`) |
| Hero | ✅ | ✅ | Poprawiono: `max-width` nagłówka (680px→720px), `line-height` (1.08→1.2), `letter-spacing` (-0.05em→-0.04em) — teraz łamie się identycznie w 2 linie |
| Marquee (pasek korzyści) | ✅ | ✅ | **Przeniesiony** — nie jest po hero, tylko między bannerem rezerwacji a newsletterem (błędne założenie na starcie). Tło zmienione cream→(było olive), kolor tekstu → `--a-gray` |
| Filozofia marki | ✅ | ✅ | Przebudowana z 1-kolumnowego bloku na: linia-separator + eyebrow, potem siatka 1:2 (nagłówek / akapity) — dokładnie jak oryginał |
| Rząd zabiegów (kadr „łuk”) | ✅ | ✅ | Przebudowany z „pigułek” tekstowych na poziomo przewijany rząd 11 kart w kadrze-łuku ze zdjęciem + podpisem — to jest właściwe miejsce sygnaturowego kształtu, nie pojedyncze zdjęcie obok tekstu |
| RX Facials (zima) | ✅ | ✅ | Ten sam wzorzec linia+siatka 1:2 co Filozofia. 3 karty zabiegów bez zmian strukturalnych |
| Opinie klientów (karuzela) | ✅ | ✅ | Licznik „Slide X of 7”, przyciski prev/next, klawiatura — działa |
| Kontakt | ✅ | ✅ | Bez linii-separatora (oryginał też jej tu nie ma) |
| Vouchery | ✅ | ✅ | Poprawiono: tło cream→**black-olive**, przycisk outline→**white**, wydzielono osobny fine-print pod przyciskiem, nagłówek podzielony na H2 (był częścią akapitu) |
| Banner rezerwacji | ✅ | ✅ | Dodano warstwę zdjęcia-placeholderu (oryginał ma zdjęcie wnętrza, nie płaskie tło) |
| Newsletter | ✅ | ✅ | Bez zmian względem pierwszej wersji |
| Stopka | ✅ | ✅ | Bez zmian względem pierwszej wersji |
| Responsywność (mobile/desktop) | ✅ | ✅ | Hamburger, drawer, siatki 1-kolumnowe poniżej 900px |
| Dostępność (klawiatura) | ✅ | ✅ | Skip-link, focus-visible, mega-menu/hamburger/karuzela obsługiwane klawiaturą |

---

## Otwarte TODO (pełna lista i szczegóły → [DOKUMENTACJA.md](DOKUMENTACJA.md))

- [ ] 6 placeholderów zdjęć do podmiany (hero, kadr-łuk ×11 w rzędzie zabiegów, 3× RX Facials, banner rezerwacji)
- [ ] Prawdziwy adres e-mail kontaktowy
- [ ] Link do platformy rezerwacyjnej
- [ ] Link do platformy voucherów
- [ ] Podstrony `skin.html`, `laser.html`, `men.html`, `women.html`, `about.html`
- [ ] Podłączenie formularza newslettera pod realny ESP (Mailchimp/Klaviyo/Formspree)

---

## Znane ograniczenie narzędziowe (nie dotyczy strony)

Podczas tej rundy weryfikacji panel przeglądarki miał powtarzającą się usterkę: zrzuty ekranu czasem pokazywały puste/nieaktualne klatki mimo poprawnie wyrenderowanej strony (zweryfikowane niezależnie przez `getBoundingClientRect`/`getComputedStyle`/`elementFromPoint` — wartości zawsze poprawne). Otwarcie świeżej karty zwykle to rozwiązywało. Odnotowane na wypadek powtórki w przyszłości — to nie jest błąd w kodzie strony.
