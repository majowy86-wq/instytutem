# CLAUDE.md — wnioski z budowy strony Archon

> Ten plik jest wczytywany automatycznie na start każdej sesji Claude Code w tym katalogu. Zawiera wnioski z dotychczasowej pracy nad odtworzeniem archon.au — żeby nie powtarzać tych samych błędów. Design system: [DESIGN-SYSTEM.md](DESIGN-SYSTEM.md). Log decyzji: [DOKUMENTACJA.md](DOKUMENTACJA.md). Checklisty: [PLAN.md](PLAN.md).

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

## Jak do tego doszło (skrót)

Zadanie brzmiało: odtwórz archon.au 1:1. Pierwsza wersja strony powstała głównie na podstawie **oglądania zrzutów ekranu** i jednorazowego researchu na starcie. Efekt: strona wyglądała "podobnie", ale użytkownik dwukrotnie wrócił z „to nadal nie wygląda jak oryginał" — i za każdym razem miał rację. Dopiero bezpośrednie pomiary DOM (`getBoundingClientRect`, `getComputedStyle`) i realna interakcja (klik/hover przez Chrome DevTools MCP) na żywej stronie ujawniły prawdziwe różnice.

**Główny wniosek: zrzut ekranu pokazuje ROBIONE wrażenie, nie fakty. Pomiar DOM pokazuje fakty.**

---

## Błędy, które popełniliśmy (i dlaczego)

1. **Zgadywanie zamiast mierzenia.** Marginesy kontenera (40px zamiast realnych ~72px/5%), rozmiary czcionek (`.8rem`/`.6rem` zamiast realnych 14px/12px), rozmiary kart (243×600 zamiast 282×450) — wszystko to były wartości "na oko" z pierwszego researchu, nigdy nie zweryfikowane liczbowo. Każda z nich okazała się zauważalnie inna od oryginału.
2. **Wnioskowanie o strukturze z jednego zrzutu ekranu.** Mega-menu wyglądało na 3 kolumny na screenshocie → zbudowaliśmy siatkę 3 kolumn. W rzeczywistości to jedna wąska kolumna (300px) z kategoriami ułożonymi pionowo — błąd wykryty dopiero po **kliknięciu** prawdziwego menu, nie po jego obejrzeniu.
3. **Zakładanie układu bez sprawdzenia sąsiednich elementów.** Sekcja kontaktu "wyglądała jasno" na fragmencie zrzutu → założyliśmy tło cream. Było black-olive. Nav "wyglądał na 3 rozstawione grupy" → było `space-between` na 3 elementach zamiast prawdziwej struktury logo + (menu+CTA jako jedna grupa wyrównana do prawej).
4. **Dodawanie funkcji, o które nikt nie prosił, bez potwierdzenia w oryginale.** Dwa razy: animacja scroll-reveal (opacity:0 + IntersectionObserver) i efekt kurczenia się nagłówka przy scrollu. Obie były "ładnymi dodatkami" wymyślonymi przez nas, żadnej nie ma w oryginale, i **obie realnie psuły stronę** — reveal potrafił zostawiać całe sekcje niewidocznymi, shrink-on-scroll psuł stałą wysokość headera. Zasada KISS z „Zasad współpracy” istnieje właśnie po to, żeby to wyłapać: nie dodawaj czegoś, czego nie ma w źródle prawdy, choćby wyglądało dobrze.
5. **Błędne przypisanie winy narzędziu.** Przez dużą część sesji zrzuty ekranu pokazujące puste sekcje uznawaliśmy za usterkę panelu przeglądarki ("tool flakiness"). Część z nich faktycznie nią była, ale **przynajmniej jeden przypadek to był realny błąd w naszym kodzie** (pkt 4, scroll-reveal). Kiedy coś wygląda dziwnie wielokrotnie, sprawdź kod, zanim uznasz to za usterkę środowiska.
6. **Ufanie CSS bez sprawdzenia, czy faktycznie się stosuje.** `.hero{display:flex}` w połączeniu z `.container{margin:0 auto}` sprawiało, że `.hero-content` kurczył się do szerokości nagłówka i centrował, zamiast rozciągać się na całą szerokość — klasyczna pułapka flexboksa (element-dziecko bez `width:100%` w kontenerze `display:flex` domyślnie się kurczy). Wyglądało poprawnie w kodzie, było błędne w renderze.
7. **Podstawowa higiena CSS pominięta.** Nigdy nie zresetowaliśmy domyślnych stylów `<button>` (`border`, `background`) — stąd tajemniczy „obramowanie" wokół przycisku „Skin", które nie było zamierzonym stylem, tylko domyślnym wyglądem przeglądarki.
8. **Kompensacja centrowania umieszczona na złym elemencie.** Przy rzędzie zabiegów margines wyśrodkowujący (formuła zależna od szerokości okna) trafił na `.trick-wrap` (kontener, który się NIE przewija) zamiast na `.trick-row` (element, który faktycznie ma `overflow-x`/`scrollLeft`). W spoczynku wyglądało to identycznie, ale margines nigdy nie „znikał" podczas przewijania, bo siedział na elemencie, który nie scrolluje. **Wniosek**: właściwość, która ma zniknąć/przesunąć się razem z przewijaną treścią, musi być ustawiona na TYM SAMYM elemencie, który realnie scrolluje — nie na jego rodzicu, nawet jeśli wizualny efekt w spoczynku jest identyczny.
9. **Budowanie powielonej treści z „zapamiętanej" listy zamiast z aktualnego stanu DOM.** Galeria kart zabiegów (`#treatments`) została zbudowana na bazie listy zabiegów sprzed rundy, w której równoległa sesja dodała 2 nowe pozycje do mega-menu — galeria nigdy nie została z nim zsynchronizowana, więc 2 zabiegi „zniknęły" z galerii, mimo że były w nav/drawer/stopce. **Wniosek**: gdy ta sama treść (np. lista zabiegów) powiela się w kilku miejscach kodu, porównywać ją programowo z AKTUALNYM stanem DOM w innym miejscu (np. `querySelectorAll` na obu i porównanie długości/kolejności), nie z pamięcią wcześniejszej rundy — stąd nowa zasada w DOKUMENTACJA.md: jedna „Lista zabiegów" jako jedyne źródło prawdy.
10. **Ten sam typ błędu co pkt 7, inny element.** `.lede` (akapit sekcji) dostawał niechciany domyślny margines przeglądarki (`margin:1em` górą), bo nigdy nie zresetowano marginesu `<p>` sitewide — psuło to wyrównanie do nagłówka w układzie grid. Wniosek ten sam co w pkt 7, tylko potwierdzony drugi raz: przy każdym nowym typie elementu HTML (nie tylko `<button>`) warto od razu sprawdzić, czy przeglądarka nie dokłada własnego marginesu/paddingu/obramowania.
11. **Uogólnienie jednej obserwacji stylu na regułę dla wszystkich promptów AI**, bez sprawdzenia więcej niż jednego przykładu. Pierwsze wygenerowane zdjęcie zabiegu miało trzymaną gałązkę eukaliptusa jako rekwizyt → założono, że to stały motyw marki, i dodawano go do kolejnych promptów. Dopiero pytanie użytkownika i sprawdzenie 3 dodatkowych realnych zdjęć archon.au ujawniło, że to był jednorazowy wybór, nie reguła. **Wniosek**: jedna próbka nie wystarcza do uogólnienia stylu — sprawdzić kilka przykładów, zanim coś trafi do stałych wytycznych.
12. **Zastosowanie reguły „pokaż realną cechę, nie idealny efekt" (ustalonej dla zabiegów redukujących tkankę tłuszczową) uniwersalnie do wszystkich kategorii zabiegów**, bez wyjątku. Zadziałało dobrze dla kriolipolizy (naturalne ciało z wałeczkami), ale dało nieapetyczny, odpychający rezultat dla epilacji laserowej (pokazane owłosienie zamiast gładkiej skóry) — trzeba było cofnąć i ustalić wyjątek. **Wniosek**: przy niepewności, czy wytyczna faktycznie zadziała wizualnie, zweryfikować na realnie wygenerowanym obrazie, nie zakładać z góry, że jedna zasada uogólnia się na wszystkie przypadki tej samej rodziny zabiegów.
13. **Prompt AI ze sformułowaniem negatywnym zamiast wprost opisanego stroju.** Fraza „no clothing visible in frame" (w intencji: bez zwykłych ubrań typu spodnie w kadrze) wygenerowała pełną nagość zamiast po prostu braku nieedytorialnej odzieży. **Wniosek**: modele generujące obrazy trzeba instruować pozytywnie i wprost, co ma być w kadrze (np. „wearing plain fitted underwear"), nie liczyć na to, że sam brak wzmianki o ubraniu da bezpieczny rezultat.

---

## Ważne odkrycia (techniczne)

1. **Synthetic events (`el.click()`, `dispatchEvent(new MouseEvent(...))`) nie uruchamiają skompilowanego JS Webflow (IX2).** Żeby zobaczyć prawdziwy stan dropdownu/mega-menu, trzeba użyć realnej symulacji inputu na poziomie CDP — w Chrome DevTools MCP to narzędzia `click`/`hover` (nie `evaluate_script` z `.click()`).
2. **`fullPage` screenshot jest zawodny na stronach ze scroll-reveal.** Dotyczy to też samego archon.au — ich własne animacje Webflow też nie odpalają się przy jednorazowym renderze pełnej wysokości strony. Do porównań używać normalnego przewijania + zrzutów widoku (viewport), nie zrzutu całej strony naraz.
3. **Prawdziwe logo to plik SVG z CDN Webflow, nie tekst w foncie.** Warto od razu sprawdzić `<img>`/`background-image` w miejscach, które "wyglądają jak tekst" — mogą być gotowym assetem graficznym.
4. **Odstępy kontenera bywają procentowe (np. `padding: 0 5%`), nie stałe w px**, z górnym ograniczeniem przez `max-width`. Mierzenie na jednym viewporcie i zapisanie wyniku jako stały px to błąd, jeśli oryginał używa wartości względnej.
5. **Snapshot drzewa dostępności (`take_snapshot` / a11y tree) to szybki sposób na wyciągnięcie prawdziwych `href`/`mailto:` bez zgadywania** — tak znaleźliśmy realne linki do rezerwacji (Timely), voucherów i adresy e-mail.
6. **Pomiar DOM (`getBoundingClientRect` + `getComputedStyle`) jest szybszy i bardziej wiarygodny niż seria zrzutów ekranu** przy dopasowywaniu pikselowej zgodności — powinien być domyślną metodą, zrzut ekranu tylko jako końcowa kontrola wzrokowa.
7. **`overflow-x:auto` bez jawnego `overflow-y` wymusza `overflow-y:auto`** na drugiej osi — nie da się mieć czysto CSS-owo „scrolluj poziomo, nigdy nie przycinaj pionowo" przy natywnym scrollu. Realny efekt: element podnoszony na hover (`translateY`) wewnątrz takiego kontenera bywa ucinany u góry, jeśli nie ma zapasowego `padding-top`.
8. **Natywny gest przeglądarki „przeciągnij ten obrazek/link" przechwytuje input przed własnym JS drag-to-scroll.** Bez jawnego wyłączenia (`-webkit-user-drag:none` na obrazkach/linkach + `dragstart → preventDefault()` w JS jako zabezpieczenie dla Firefoksa) przeciąganie działa tylko w „szczelinach" między elementami, nie na samych zdjęciach — wygląda jak bug w logice JS, a jest to konflikt z domyślnym zachowaniem przeglądarki.
9. **Biblioteki JS z własnym cache layoutu (np. karuzela Flickity na archon.au) nie zawsze przeliczają się po samym resize viewportu** bez pełnego przeładowania strony — pierwszy pomiar po samym `resize` może zwrócić ewidentnie nieaktualną wartość z poprzedniej szerokości okna. Przy pomiarach porównawczych na wielu szerokościach: zawsze pełny `location.reload()` przed KAŻDYM pomiarem, nie tylko raz na początku.
10. **Flex-item domyślnie ma `min-width:auto`**, co po cichu ignoruje `max-width`/`overflow-wrap` ustawione na tym elemencie, dopóki nie zresetuje się jawnie `min-width:0` — inaczej długi, nierozdzielny tekst (np. z ukośnikiem `/`) wychodzi poza szerokość rodzica mimo pozornie poprawnego CSS.
11. **Animacja scroll-reveal sterowana `IntersectionObserver` na archon.au nie uruchamia się przez `scrollIntoView()` ani scroll ustawiany programowo** (`window.scrollTo`/`scrollBy`) — tylko przez realny input (kółko myszy/dotyk). Element mierzony w trakcie niewywołanej animacji ma fałszywe, tymczasowe wartości (`opacity:0`, przesunięty `transform`). Żeby zmierzyć stan SPOCZYNKOWY bez czekania na realny scroll, można punktowo wymusić przez JS `opacity:1;transform:none!important` wyłącznie na czas pomiaru (nie jako trwała zmiana) — to ujawnia docelowe wartości do porównania.
12. **Narzędzie Browser MCP (panel przeglądarki) ma powtarzalne, znane usterki**, które nie oznaczają błędu w kodzie: zrzut ekranu bywa błędny (pusta/ucięta strona) przy nie-zerowej pozycji scrolla — obejście: mierzyć przez DOM zamiast ufać zrzutowi, albo powiększyć wysokość viewportu (`resize_window`) i oglądać sekcję przy `scrollY:0` zamiast scrollować; gest scrolla kółkiem (`computer` action `scroll`) potrafi się timeoutować z komunikatem „Browser pane is currently hidden"; odczyt `window.innerWidth`/podobnych przez `javascript_tool` sporadycznie zwraca `0` mimo poprawnego stanu strony — obejście: opakować odczyt w `JSON.stringify({...})` i spróbować ponownie na świeżej karcie.
13. **Obrazy wklejone bezpośrednio na czacie nie trafiają na dysk dostępny narzędziom plikowym sesji.** Sprawdzone: `/tmp`, `~/.claude`, `~/Library/Application Support/Claude/*`, `/var/folders` — nigdzie nic. Trzeba poprosić użytkownika o ręczne zapisanie pliku (np. do `assets/images/`), dopiero wtedy `ls -lat`/`find` go znajdzie.
14. **Cache-bust dotyczy też pojedynczych obrazków, nie tylko CSS/JS.** Nadpisanie pliku pod tą samą nazwą (np. druga wersja tego samego zdjęcia zabiegu) wymaga dopisania `?v=2` do atrybutu `src` w HTML, inaczej przeglądarka nadal pokazuje starą wersję z własnego cache obrazków — ten sam mechanizm co przy `styles.css?v=N`, ale trzeba go pilnować osobno przy każdym pliku graficznym.
15. **`window.scrollTo()` wywoływane programowo z poziomu narzędzia automatyzacji przeglądarki nie zawsze wywołuje realne zdarzenie `scroll`** — potwierdzone: nawet własny, niezależny listener testowy nic nie logował po `scrollTo()`, a zadziałał dopiero po prawdziwym geście scrolla kółkiem myszy (`computer` action `scroll`). To nowy przypadek tego samego wzorca co pkt 11 (syntetyczne eventy nie zawsze uruchamiają prawdziwą logikę) — dotyczy nie tylko scroll-reveal na archon.au, ale ogólnie testowania własnego kodu scroll-linked w tym narzędziu.
16. **Element z „nieskończonym" przewijaniem (marquee) ze sztywno zdublowaną raz treścią nie jest odporny na szerokie ekrany.** Jeśli kontener bywa szerszy niż zdublowana treść, przewijanie w pewnym momencie ujawnia pustą przestrzeń — sztywne „zdubluj raz" nie skaluje się z szerokością ekranu. Rozwiązanie: dynamicznie doklonować tyle kopii treści („kafelków"), ile potrzeba, żeby pokryć szerokość kontenera z zapasem, przeliczane też przy `resize` — zwłaszcza gdy rozmiar czcionki (a więc i kafelka) sam zależy od viewportu.

---

## Proces: zdjęcia zabiegów generowane AI (Nano Banana / Gemini)

Ustalony w Rundach 40–68 (2026-08-28) przy uzupełnianiu zdjęć w galerii `#treatments` i tła bannera rezerwacji. Zasady doboru **treści** promptu (rdzeń stylu, model, tło, „realna cecha", kadr z kotwicą) są w [DESIGN-SYSTEM.md §9](DESIGN-SYSTEM.md) — nie duplikować ich tutaj. Poniżej tylko techniczny przebieg pracy z plikiem:

1. Obraz wklejony na czacie nie trafia na dysk (patrz pkt 13 w „Ważne odkrycia") — poproś użytkownika o zapisanie pliku do `assets/images/` (lub `assets/images/treatments/`), dopiero wtedy `ls -lat`/`find` go znajdzie.
2. Obejrzyj plik (`Read`) i oceń, czy pasuje do promptu i stylu marki, zanim go przetworzysz.
3. Zoptymalizuj `sips` (natywne macOS): `sips -Z 1000 --setProperty formatOptions 82 <plik> --out assets/images/treatments/<nazwa-kebab-case>.jpg` — cel to ok. 100–250KB przy 1000×1000, dopasowane do istniejących zdjęć w tym folderze.
4. Nadaj czystą nazwę kebab-case bez polskich znaków specjalnych (np. `mezoterapia-beziglowa.jpg`, nie dosłowna transliteracja z ogonkami) i usuń oryginalny plik `Gemini_Generated_Image_....jpeg` po przetworzeniu.
5. Podepnij w `index.html`: zamień `<div class="trick-img ph-gradient">` na `<img class="trick-img" src="..." alt="...">` (`alt` opisuje treść zdjęcia, nie nazwę zabiegu). Jeśli to podmiana pliku pod TĄ SAMĄ nazwą (nadpisanie), dopisz `?v=2` do `src` (patrz pkt 14 w „Ważne odkrycia").
6. Jeśli podmieniasz stare zdjęcie z CDN archon.au, usuń stary plik dopiero po `grep`, że nie jest używany gdzie indziej.
7. Zweryfikuj `fetch()` nowego URL-a na lokalnym serwerze (status 200).
8. Zaktualizuj „Listę zabiegów" w DOKUMENTACJA.md (jedyne źródło prawdy per-pozycja) i jednolinijkowy status w PLAN.md — historia decyzji zostaje w DOKUMENTACJA.md, nie w PLAN.md.

**Przed wymyśleniem koncepcji zdjęcia dla zabiegu**: sprawdź, co ten zabieg faktycznie leczy/robi — żywą podstronę instytutem.pl (jeśli URL jest realny, nie wymyślony w Rundzie 9) albo `WebSearch`, nigdy z samej nazwy. Sprawdź też, czy to nie duplikat innej już obsłużonej pozycji w menu pod inną nazwą (marka urządzenia vs nazwa generyczna techniki — tak jak potwierdzony duplikat „LPG® Ergolift"/„Endermologia Twarzy" czy podejrzewany „SkinPen"/„Mezoterapia mikroigłowa", oba w PLAN.md) — w razie wątpliwości zapytaj użytkownika, nie zgaduj i nie rozstrzygaj samodzielnie.

---

## Zweryfikowany proces na przyszłość

Przy KAŻDEJ kolejnej poprawce wizualnej, w tej kolejności:

1. **Zmierz najpierw, buduj potem — NIGDY nie zgaduj.** Otwórz element na żywej archon.au i pobierz `getBoundingClientRect()` + `getComputedStyle()` dla niego i jego rodzica/rodzeństwa. Nie zgaduj wartości z samego wyglądu, ze zrzutu ekranu ani "z pamięci" tego, co wydawało się słuszne we wcześniejszej rundzie — każda liczba (rozmiar czcionki, line-height, letter-spacing, padding, kolor) musi pochodzić z realnego pomiaru DOM. Po zmianie zweryfikuj też, że zmierzona wartość faktycznie się renderuje na naszej stronie (patrz pkt 5) — zagnieżdżony element z własną, konkurencyjną regułą (np. wewnętrzny `<span>` z innym `font-size`) potrafi po cichu nadpisać poprawnie ustawioną wartość na rodzicu.
2. **Jeśli element jest interaktywny (dropdown, hover, karuzela) — kliknij/najedź naprawdę** (`click`/`hover` w Chrome DevTools MCP), nie symuluj eventów przez JS.
3. **Sprawdź nie tylko sam element, ale jego bezpośrednich rodziców** — źle założona struktura (np. "3 równe kolumny" zamiast "logo + jedna grupa po prawej") jest częstszym błędem niż zła wartość pojedynczej właściwości.
4. **Nie dodawaj niczego, czego nie potwierdziłeś w oryginale** — żadnych animacji, efektów, "ulepszeń", nawet jeśli wydają się nieszkodliwe. Jeśli oryginał czegoś nie robi, strona też nie powinna.
5. **Po poprawce — zweryfikuj przez ponowny pomiar, nie tylko zrzut ekranu.** Zrzut ekranu na końcu jako potwierdzenie wizualne, nie jako jedyne źródło prawdy.
6. Zapisz wynik w [PLAN.md](PLAN.md) (checklista) i [DOKUMENTACJA.md](DOKUMENTACJA.md) (log decyzji) — zgodnie z już ustalonym stałym procesem weryfikacji.
7. **Właściwość, która ma zniknąć/przesunąć się razem z przewijaną treścią, musi być na tym samym elemencie, który realnie scrolluje** (ma `overflow`/`scrollLeft`) — nie na jego rodzicu, nawet jeśli w spoczynku wygląda identycznie.
8. **Gdy ta sama treść powiela się w kilku miejscach kodu** (np. lista zabiegów w nav/drawer/stopce/galerii), porównuj ją programowo z aktualnym stanem DOM w innym miejscu (liczba i kolejność elementów), nie z pamięcią wcześniejszej rundy.
9. **Przy każdym nowym typie elementu HTML sprawdź domyślny margines/padding/obramowanie przeglądarki** (nie tylko `<button>`, patrz też `<p>`) — źródło pozornie niewytłumaczalnych przesunięć.
10. **Jeśli zrzut ekranu z Browser MCP wygląda ewidentnie błędnie (pusta/ucięta strona) przy przewiniętej pozycji, nie traktuj tego jako dowodu błędu w kodzie** — najpierw zmierz przez `getBoundingClientRect`/`getComputedStyle`, dopiero potwierdzony błąd pomiaru = realny błąd w CSS/JS.
