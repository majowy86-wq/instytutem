# Dokumentacja projektu — archon.au (wersja własna)

> Ten plik to żywy dziennik dokumentacji technicznej projektu. Uzupełniany na bieżąco w trakcie pracy — po każdej istotnej decyzji, dodanej zależności lub sprawdzonej dokumentacji zewnętrznej biblioteki.
>
> Design system marki: patrz [archon.md](archon.md) — obowiązuje bez wyjątków przy każdej zmianie wizualnej.
>
> Postęp i checklisty: patrz [PLAN.md](PLAN.md) — zawiera stały proces weryfikacji wizualnej wobec archon.au, obowiązujący przy każdej zmianie kodu.

---

## Zasady współpracy (obowiązują zawsze, priorytet ekstra wysoki)

Ustalone przez użytkownika 2026-08-26 — mają pierwszeństwo przed domyślnymi nawykami:

1. **Kontekst użytkownika** (rola, stos, poziom wiedzy) jest zawsze respektowany w odpowiedziach.
2. **Źródło prawdy**: dla wyglądu — [archon.md](archon.md) (design system); dla postępu/procesu — [PLAN.md](PLAN.md). Jeśli w projekcie pojawi się PRD, schemat bazy danych lub endpointy API, to one staną się źródłem prawdy dla warstwy backendowej i muszą zostać z nimi spójne — obecnie projekt jest statyczną stroną bez backendu, więc ten punkt czeka na przyszły rozwój.
3. Nowe/aktualne zadania trafiają do checklisty w [PLAN.md](PLAN.md), gdy tylko się pojawią — nie tylko na koniec większego etapu.
4. **Przypominanie o commitach do GitHuba** — regularnie, nie tylko na wyraźną prośbę. (Repo git nie jest jeszcze zainicjowane w tym projekcie — patrz przypomnienie niżej.)
5. **KISS + DRY** w każdym rozwiązaniu — najprostszy działający kod, bez duplikacji.
6. **Jasność ponad sprytem** — przy niejasnościach pytać przed pisaniem kodu, nie zgadywać.
7. **Minimalne, działające przykłady kodu** zamiast abstrakcyjnej teorii.

---

## Zasady prowadzenia dokumentacji

1. **Context7** (`context7@claude-plugins-official`) jest używany do pobierania aktualnej, wersjonowanej dokumentacji bibliotek/frameworków przed ich użyciem — zamiast polegać na wiedzy pamięciowej, która może być nieaktualna.
2. Każdy wpis w sekcji „Log decyzji" zawiera: datę, co zostało sprawdzone/zdecydowane, i dlaczego.
3. Każda nowo dodana zależność (biblioteka, framework, narzędzie) trafia do sekcji „Stos technologiczny" wraz z wersją i krótkim uzasadnieniem wyboru.
4. Dokumentacja jest pisana na bieżąco, nie retrospektywnie na koniec projektu.

---

## Stos technologiczny

| Technologia | Wersja | Status | Uzasadnienie |
|---|---|---|---|
| HTML5 / CSS3 / JavaScript (vanilla, ES6) | — | Aktywny | Strona marketingowa jednostronicowa (na razie) — brak potrzeby frameworka czy build-stepu. Najprostszy sposób na wierne, kontrolowane odtworzenie 1:1 designu z archon.md. Łatwy hosting gdziekolwiek (statyczne pliki). |
| Google Fonts (Tenor Sans, Inter) | CDN | Aktywny | Kroje wymagane przez design system (archon.md §3), ładowane przez `<link>` w `<head>`. |

---

## Log decyzji i konsultacji dokumentacji

| Data | Temat | Źródło (Context7 / inne) | Notatka |
|---|---|---|---|
| 2026-08-26 | Instalacja narzędzi | `claude plugin install superpowers@claude-plugins-official`, `claude plugin install context7@claude-plugins-official` | Oba pluginy zainstalowane w zakresie użytkownika (dostępne we wszystkich projektach na tej maszynie). Superpowers dostarcza metodykę pracy (TDD, debugging, planowanie). Context7 dostarcza aktualną dokumentację bibliotek na żądanie. |
| 2026-08-26 | Stos technologiczny strony głównej | Plan wdrożenia (agent planujący) | Wybrano czysty HTML/CSS/JS bez frameworka i bez build-stepu — zgodnie z prośbą „zrób tak samo jak na archon.au”, priorytet: wierność designowi, prostota, łatwy hosting. Node/npm/git dostępne w środowisku, ale świadomie nieużywane na tym etapie. |
| 2026-08-26 | Zbudowano stronę główną (index.html) | — | Pełny zakres z archon.au: nav + mega-menu, hero, marquee korzyści, filozofia marki, RX Facials (3 karty), karuzela 7 opinii, kontakt (3 kolumny), vouchery, banner rezerwacji, newsletter, stopka. Zweryfikowano wizualnie (desktop + mobile) i funkcjonalnie (mega-menu, hamburger, karuzela, formularz) w przeglądarce. |
| 2026-08-26 | Kadr „łuk” — miejsce na stronie głównej | Plan wdrożenia | Jedyne wystąpienie na tej stronie: zdjęcie towarzyszące tekstowi w sekcji „Filozofia marki” (brak sekcji zespołu w treści, więc to jedyne naturalne miejsce zgodne z archon.md §5). |
| 2026-08-26 | Formularz newslettera — brak backendu | Plan wdrożenia | Zamiast udawać sukces, JS przechwytuje submit i pokazuje uczciwy komunikat: „Sign-ups aren't connected yet — needs an email service…”. Docelowo do podłączenia pod Mailchimp/Klaviyo/Formspree lub inny ESP. |
| 2026-08-26 | Tryb ciemny systemu | Plan wdrożenia | Świadomie **nie** wdrożono `prefers-color-scheme` — to strona firmowa, ma wyglądać identycznie niezależnie od motywu systemu odwiedzającego (inaczej niż artefakt-dokumentacja design systemu, który się dostosowuje). |
| 2026-08-26 | Instalacja `chrome-devtools-mcp@claude-plugins-official` | `claude plugin install chrome-devtools-mcp@claude-plugins-official` | Zainstalowany w zakresie użytkownika. Prawdziwy serwer MCP (Puppeteer/Chrome DevTools Protocol) + skille do debugowania a11y, wydajności (LCP), wycieków pamięci. Uzupełnia dotychczasowy podgląd w przeglądarce o głębszą diagnostykę (trace'y wydajności, network, źródłowe stack trace'y w konsoli). Wymaga restartu sesji, żeby narzędzia się załadowały. |
| 2026-08-26 | Wprowadzono stały proces weryfikacji wizualnej | Porównanie bezpośrednie z żywą archon.au | Od teraz każda zmiana kodu przechodzi przez porównanie zrzut-do-zrzutu z archon.au (patrz [PLAN.md](PLAN.md)). Pierwsza runda ujawniła i naprawiła: (1) konflikt CSS `padding` w `.nav-row`/`.section-pad` łamiący padding `.container`; (2) złe łamanie nagłówka hero (max-width 680→720px, line-height 1.08→1.2); (3) błędną kolejność przycisków w nav; (4) całkowicie błędną strukturę sekcji „Filozofia marki” — oryginał używa siatki 1:2 (nagłówek/akapity) z linią-separatorem nad eyebrow, nie pojedynczego bloku tekstu; (5) błędne miejsce sygnaturowego kadru-łuk — to cały poziomo przewijany rząd 11 kart zabiegów, nie jedno zdjęcie obok tekstu; (6) błędne tło sekcji Vouchers (miało być cream, jest black-olive) i zły wariant przycisku (outline→white); (7) marquee było źle umieszczone zaraz po hero — w oryginale jest między bannerem rezerwacji a newsletterem, na tle cream (nie olive). |

---

## Struktura projektu

```
INSTYTUTem/
├── archon.md              — design system marki (obowiązujący, patrz plik)
├── DOKUMENTACJA.md         — ten plik
├── PLAN.md                 — checklisty postępu + stały proces weryfikacji wizualnej
├── index.html              — strona główna
├── css/
│   └── styles.css          — wszystkie style, tokeny z archon.md w :root
├── js/
│   └── main.js              — nav sticky, mega-menu, hamburger, karuzela opinii, formularz newslettera
└── assets/
    └── images/              — puste, patrz „Lista placeholderów zdjęć” niżej
```

---

## Lista placeholderów zdjęć — do podmiany na prawdziwe zdjęcia

Miejsca oznaczone w kodzie komentarzem/atrybutem `TODO` lub `aria-label` zaczynającym się od „TODO”. Obecnie wypełnione gradientem CSS w klimacie marki (ciemne, organiczne, ciepłe akcenty).

1. **Tło hero** (`index.html`, sekcja `.hero-bg`) — pełnoekranowe zdjęcie botaniczne/makro w ciemnym klimacie + overlay.
2. **Zdjęcie w kadrze „łuk”** w sekcji „Filozofia marki” (`.philosophy-photo`).
3. Zdjęcie karty **RX Benefactor Facial**.
4. Zdjęcie karty **RX Illuminate Facial**.
5. Zdjęcie karty **RX Detox Facial**.
6. **Favicon / logo mark** — brak jeszcze pliku.

## Inne otwarte TODO w kodzie (do potwierdzenia/uzupełnienia)

- Prawdziwy adres e-mail kontaktowy (obecnie placeholder `info@archon.au`).
- Docelowy link do platformy rezerwacyjnej (obecnie `#book`).
- Docelowy link do platformy voucherów prezentowych (obecnie `#`).
- Strony `skin.html`, `laser.html`, `men.html`, `women.html`, `about.html` — linkowane z nawigacji/stopki, ale jeszcze nie zbudowane (będą 404 do czasu ich stworzenia).

## Następny krok (niewykonany automatycznie)

`git init` + pierwszy commit — wymaga wyraźnej zgody w czacie przed wykonaniem.
