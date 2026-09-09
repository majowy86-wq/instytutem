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
