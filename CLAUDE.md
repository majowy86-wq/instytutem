# CLAUDE.md — indeks projektu INSTYTUTem

> Ten plik jest wczytywany automatycznie na start każdej sesji Claude Code w tym katalogu. To jest **indeks** — trzyma tylko zasady obowiązujące co sesję i odnośniki dalej, nie historię/szczegóły. Design system: [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md). Log decyzji, wnioski techniczne, błędy z przeszłości i zweryfikowane procesy: [DOKUMENTACJA.md](DOKUMENTACJA.md). Checklisty/TODO: [PLAN.md](PLAN.md).

---

## 🗣️ Język komunikacji

Zawsze odpowiadaj użytkownikowi po polsku — cały tekst kierowany do użytkownika (wyjaśnienia, pytania, podsumowania), niezależnie od języka treści w kodzie czy commitach. Nie dotyczy to samego kodu/treści strony (np. `lang="pl"` w HTML to osobna sprawa — patrz reszta tego pliku).

---

## 🌐 Podgląd lokalny — otwierać w zewnętrznej domyślnej przeglądarce

Po każdej zmianie w kodzie (HTML/CSS/JS) otwórz aktualną wersję strony w **zewnętrznej, domyślnej przeglądarce systemowej** (nie w panelu przeglądarki wbudowanym w Claude Code) — komendą `open` (macOS), np.:

```bash
open http://localhost:8090
```

Adres lokalny ma być **zawsze ten sam**: `http://localhost:8090` — stały port ustawiony w `.claude/launch.json` (`archon-local`). Jeśli lokalny serwer (`python3 -m http.server 8090`) nie działa, uruchom go najpierw w tle.

---

## 🤝 Zasady współpracy (obowiązują zawsze, priorytet ekstra wysoki)

Ustalone przez użytkownika 2026-08-26 — mają pierwszeństwo przed domyślnymi nawykami:

1. **Kontekst użytkownika** (rola, stos, poziom wiedzy) jest zawsze respektowany w odpowiedziach.
2. **Źródło prawdy**: dla wyglądu — [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md); dla postępu/procesu — [PLAN.md](PLAN.md). Jeśli w projekcie pojawi się PRD, schemat bazy danych lub endpointy API, to one staną się źródłem prawdy dla warstwy backendowej — obecnie projekt jest statyczną stroną bez backendu, więc ten punkt czeka na przyszły rozwój.
3. Nowe/aktualne zadania trafiają do checklisty w [PLAN.md](PLAN.md), gdy tylko się pojawią — nie tylko na koniec większego etapu.
4. **Przypominanie o commitach do GitHuba** — regularnie, nie tylko na wyraźną prośbę.
5. **KISS + DRY** w każdym rozwiązaniu — najprostszy działający kod, bez duplikacji.
6. **Jasność ponad sprytem** — przy niejasnościach pytać przed pisaniem kodu, nie zgadywać.
7. **Minimalne, działające przykłady kodu** zamiast abstrakcyjnej teorii.
8. **Odtwarzając cokolwiek z archon.au — NIGDY nie zgaduj wartości, zawsze mierz precyzyjnie.** Dotyczy rozmiaru czcionki, line-height, letter-spacing, paddingu, marginesu, koloru — każdej wartości liczbowej. Pomiar = `getComputedStyle()`/`getBoundingClientRect()` na żywej stronie archon.au, nie "na oko" ze zrzutu ekranu ani z pamięci z wcześniejszej rundy. Ustalone 2026-08-27 po tym, jak zgadnięty `font-size:.78rem` dla przycisków CTA w menu mobilnym okazał się błędny (realna wartość na archon.au to 14px) — patrz też pkt 1 w "Błędy, które popełniliśmy" i "Zweryfikowany proces na przyszłość" niżej.
9. **Nazwy własne sprzętu/laserów/technologii zawsze z symbolem znaku towarowego na końcu, przy KAŻDYM wystąpieniu w widocznej treści** (nagłówki, akapity, `alt`, meta description, JSON-LD) — nie tylko przy pierwszym wystąpieniu na stronie. Który symbol (® zastrzeżony vs ™ niezastrzeżony) zależy od konkretnej marki — sprawdzić już ustalone, poprawne przykłady w kodzie zamiast zgadywać: **LightSheer®, LPG®, Dermalux®, SkinPen®, Bloomea®, cooltech®** (rejestrowane), **Plasma™, DUET™** (niezastrzeżone). Uwaga: w „LPG® Ergolift" symbol siedzi tylko po „LPG", nie po „Ergolift" — to nazwa linii produktowej pod marką LPG, nie osobno zastrzeżona nazwa. Nie dotyczy adresów URL/`href`/nazw plików/klas CSS/komentarzy w kodzie — tylko realnej, widocznej treści strony. Ustalone 2026-09-02.

---

## 🎯 Koncepcja projektu (fundament — czytać przed wszystkim innym)

Ustalone z użytkownikiem 2026-08-27.

**Wizualnie: archon.au. Treściowo: www.instytutem.pl.**

To jest definicja tego, co budujemy:
- **Design, layout, komponenty, typografia, animacje, styl** — wzorowane na archon.au (design system: [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md)), zweryfikowane pomiarem DOM zgodnie z procesem opisanym niżej.
- **Treść, oferta zabiegów, ceny, dane kontaktowe, zespół, opinie, struktura podstron/URL** — realne dane z www.instytutem.pl (salon kosmetologiczny w Płocku, właścicielka Ewelina Majchrzak), nie z Australii.

Innymi słowy: archon.au dał nam **jak to ma wyglądać**, instytutem.pl daje **co ma tam być**. Efekt końcowy zastępuje żywą stronę www.instytutem.pl (patrz sekcja SEO niżej) — więc żadna treść z Australii (Archon, Teneriffe/Brisbane, ceny w AUD) nie może trafić do wersji produkcyjnej, nawet jeśli jest już przetłumaczona na polski w obecnym `index.html`.

**Przy każdej decyzji projektowej pytanie brzmi:** "czy to pytanie o wygląd (→ patrz archon.au) czy o treść/dane biznesowe (→ patrz instytutem.pl)?"

---

## 🚨 KRYTYCZNE: ta strona zastąpi żywą www.instytutem.pl — zero utraty SEO

Ustalone z użytkownikiem 2026-08-27. Ta reguła ma priorytet nad wszystkimi innymi przy każdej decyzji dotyczącej struktury URL, treści czy meta danych.

**Kontekst:** ten projekt (zbudowany na bazie designu archon.au) docelowo **podmieni obecną, żywą stronę www.instytutem.pl** — prawdziwy, działający biznes z ugruntowanymi pozycjami w Google. To nie jest strona od zera; to migracja/redesign istniejącej strony z ruchem i rankingami do stracenia.

**Twarda zasada:** każdy adres URL, który jest dziś zaindeksowany na www.instytutem.pl, **musi zostać zachowany 1:1** (dokładnie ten sam path) w nowej wersji, chyba że użytkownik świadomie zdecyduje inaczej — a wtedy wymagane jest przekierowanie **301** (nigdy 302). Pełna lista adresów do zachowania i checklista SEO: patrz [DOKUMENTACJA.md](DOKUMENTACJA.md#zasada-nadrzędna-zachowanie-seo-przy-migracji-na-wwwinstytutempl).

**Konsekwencje praktyczne dla kodu:**
- Nie "porządkować" niespójnej dziś struktury URL (część zabiegów pod `/zabiegi/...`, część luzem w root) — to osobny projekt na później, nie coś do naprawienia przy okazji redesignu.
- Nie skracać/zmieniać treści na stronach zabiegów bez wyraźnej potrzeby — Google ocenia stronę też po głębi treści.
- Obecny `index.html` w tym repo ma wciąż **treść z Australii** (Archon, Teneriffe/Brisbane, adres, telefon) przetłumaczoną na polski — to placeholder do podmiany na prawdziwą treść instytutem.pl (usługi, adres Płock, dane kontaktowe), nie do publikacji w obecnym stanie.
- Przed właściwym wdrożeniem: pobrać pełną listę zaindeksowanych URL z Google Search Console / sitemap.xml na instytutem.pl (lista w DOKUMENTACJA.md pochodzi z menu nawigacji i może nie być kompletna, np. wpisy blogowe).
- Nowa wersja idzie na **staging z `noindex`**, testy przekierowań przed startem, **jednorazowa publikacja całości** (nie mieszanka starych/nowych stron), monitoring Google Search Console (Coverage) przez 2–4 tygodnie po starcie.

---

## Historia, wnioski i zweryfikowane procesy → DOKUMENTACJA.md

Cała treść, która kiedyś tu była (jak doszliśmy do obecnego procesu, 13 błędów które popełniliśmy, 17 technicznych odkryć, proces zdjęć AI, 10-punktowa checklista "zmierz przed każdą poprawką") — przeniesiona do jednej sekcji w [DOKUMENTACJA.md § Wnioski i błędy z budowy strony](DOKUMENTACJA.md#wnioski-i-błędy-z-budowy-strony-przeniesione-z-claudemd-2026-08-30). Nic nie zostało utracone, tylko zebrane w jednym miejscu razem z resztą logu decyzji — CLAUDE.md ma zostać krótki i czytać się w całości na starcie sesji.

**Skrót najważniejszej reguły stamtąd, żeby nie trzeba było klikać linku:** zmierz `getComputedStyle`/`getBoundingClientRect` na żywym elemencie, zanim napiszesz jakąkolwiek wartość liczbową — nigdy z pamięci, nigdy ze zrzutu ekranu. Reszta szczegółów i uzasadnień → link wyżej.
