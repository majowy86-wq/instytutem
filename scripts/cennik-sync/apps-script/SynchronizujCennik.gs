/**
 * Kod do wklejenia w Edytor rozszerzeń (Extensions → Apps Script) arkusza z cennikiem.
 * Dodaje w menu arkusza przycisk "Cennik → Synchronizuj cennik", który zdalnie odpala
 * workflow GitHub Actions (.github/workflows/sync-cennik.yml) synchronizujący ceny.
 *
 * Jednorazowa konfiguracja (patrz instrukcja w rozmowie z Claude):
 *   1. W GitHub: wygeneruj Personal Access Token (fine-grained, uprawnienie
 *      "Contents: Read and write" na repo instytutem) i sekret repo
 *      GOOGLE_SERVICE_ACCOUNT_JSON (zawartość pliku .secrets/google-service-account.json).
 *   2. Tutaj: Project Settings (ikona zębatki) → Script Properties → dodaj GITHUB_TOKEN
 *      z wartością tego tokenu.
 */

const GITHUB_OWNER = "majowy86-wq";
const GITHUB_REPO = "instytutem";

/**
 * Kolumna L ("ID") to stały identyfikator wiersza (dodany 2026-09-09) — synchronizacja
 * dopasowuje wiersze po NIM, nie po tekście (Zabieg/Podgrupa/Wariant), więc zmiana samej
 * nazwy nie wygląda już jak "usunięto stare + dodano nowe". Ten trigger sam wypełnia ID
 * dla każdego nowego wiersza (ma wypełnioną kolumnę A "Zabieg", ale puste ID) — użytkownik
 * nie musi o tym pamiętać przy dodawaniu nowej pozycji w arkuszu.
 */
const CENNIK_TAB_NAME = "Cennik — wszystkie zabiegi";
const COL_ZABIEG = 1;  // A
const COL_ID = 12;     // L

function onEdit(e) {
  try {
    const sheet = e.range.getSheet();
    if (sheet.getName() !== CENNIK_TAB_NAME) return;
    if (e.range.getRow() === 1) return; // nagłówek

    const startRow = e.range.getRow();
    const numRows = e.range.getNumRows();
    for (let r = startRow; r < startRow + numRows; r++) {
      const zabieg = sheet.getRange(r, COL_ZABIEG).getValue();
      const idCell = sheet.getRange(r, COL_ID);
      if (zabieg && !idCell.getValue()) {
        idCell.setValue(nextCennikId(sheet));
      }
    }
  } catch (err) {
    console.error(err); // proste triggery nie mogą pokazać ui.alert
  }
}

function nextCennikId(sheet) {
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return 1;
  const ids = sheet.getRange(2, COL_ID, lastRow - 1, 1).getValues().flat()
    .map(function (v) { return parseInt(v, 10); })
    .filter(function (n) { return !isNaN(n); });
  const max = ids.length ? Math.max.apply(null, ids) : 0;
  return max + 1;
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("Cennik")
    .addItem("🔄 Synchronizuj cennik", "synchronizujCennik")
    .addToUi();
}

function synchronizujCennik() {
  const ui = SpreadsheetApp.getUi();
  const token = PropertiesService.getScriptProperties().getProperty("GITHUB_TOKEN");
  if (!token) {
    ui.alert("Brak skonfigurowanego GITHUB_TOKEN w Script Properties — patrz instrukcja na górze pliku SynchronizujCennik.gs.");
    return;
  }

  const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/dispatches`;
  const response = UrlFetchApp.fetch(url, {
    method: "post",
    contentType: "application/json",
    headers: {
      Authorization: `token ${token}`,
      Accept: "application/vnd.github+json",
    },
    payload: JSON.stringify({ event_type: "sync-cennik" }),
    muteHttpExceptions: true,
  });

  const code = response.getResponseCode();
  if (code === 204) {
    ui.alert("Synchronizacja uruchomiona ✅\n\nPotrwa ok. 1 minutę. Wynik pojawi się w zakładce \"Status\" w tym arkuszu.");
  } else {
    ui.alert(`Coś poszło nie tak (kod ${code}):\n${response.getContentText()}`);
  }
}
