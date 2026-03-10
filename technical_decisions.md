# Technical Decisions: crypto-market-data-analysis

## 1. Erster Vorschlag

Diese Datei definiert die zentralen technischen und methodischen Entscheidungen fuer das Projekt `crypto-market-data-analysis`.

### Ausgangsvorschlag
- Datenquelle: `yfinance`
- Frequenz: taegliche Daten
- Assets im MVP: BTC, ETH, SOL
- Zeitraum: letzte 5 Jahre
- Preisbasis: `Adj Close`, falls sinnvoll, sonst `Close`
- Returns: simple returns und log returns
- Statistik basiert primaer auf log returns
- Annualisierung mit 365 Tagen
- Sharpe Ratio im MVP mit risikofreiem Zins = 0
- Kernanalysen: Jarque-Bera, ACF returns, ACF squared returns, Rolling Volatility, Drawdown
- Output: gespeicherte Plots und automatischer Markdown-Report
- AI-Rolle: nur kommentierend, nicht rechnend

Dieser Vorschlag ist bereits solide, aber an mehreren Stellen noch zu offen. Damit Codex spaeter nicht falsche Annahmen trifft, werden im naechsten Abschnitt gezielte Verbesserungen eingebaut.

---

## 2. Meine Verbesserungsvorschlaege und direkte Implementierung

### Verbesserung 1: Preisbasis explizit dokumentieren
Nur `Adj Close, falls sinnvoll` zu schreiben ist zu ungenau. Gerade bei Krypto sind `Adj Close` und `Close` oft identisch oder `Adj Close` nicht sinnvoll unterschiedlich. Deshalb muss die Preisbasis im Code geprueft und im Report explizit dokumentiert werden.

**Implementierung:**
- zuerst auf `Adj Close` pruefen
- wenn nicht vorhanden oder nicht sinnvoll abweichend, `Close` verwenden
- im Report festhalten, welche Preisbasis pro Asset verwendet wurde

### Verbesserung 2: Return-Logik methodisch trennen
Viele Projekte mischen Return-Arten unsauber. Deshalb wird klar getrennt:
- simple returns werden mitberechnet
- log returns sind die Hauptbasis fuer Verteilungs- und Autokorrelationsanalysen
- Drawdown und Preisentwicklung werden auf Preis- bzw. Vermoegenskurvenlogik berechnet

### Verbesserung 3: Annualisierung fuer Krypto sauber festlegen
Krypto wird 7 Tage pro Woche gehandelt. Deshalb ist `365` fuer dieses Projekt die fachlich passendere Annahme als `252`.

**Implementierung:**
- annualisierte Volatilitaet = daily std * sqrt(365)
- annualisierte Sharpe Ratio = daily Sharpe * sqrt(365)
- diese Regel muss in Code und Report sichtbar dokumentiert sein

### Verbesserung 4: Sharpe Ratio bewusst einfach halten
Statt sofort externe risikofreie Zinsen einzubauen, wird fuer den MVP eine dokumentierte Annahme gesetzt.

**Implementierung:**
- `risk_free_rate = 0.0` als Default in der Konfiguration
- spaetere Erweiterung moeglich
- im Report klar vermerken, dass die Sharpe Ratio im MVP mit 0 risikofreiem Zins berechnet wurde

### Verbesserung 5: Fehlende Werte konservativ behandeln
Es soll nichts blind interpoliert oder aufgefuellt werden.

**Implementierung:**
- Zeitreihe sortieren
- ungueltige Zeilen entfernen
- keine aggressive Imputation
- erste NaN nach Return-Berechnung entfernen
- Datenbereinigung kurz im Report nennen

### Verbesserung 6: MVP bewusst klein halten
Damit der erste Stand stabil laeuft, bleiben komplexere Tests und Modelle draussen.

**Implementierung:**
Im MVP enthalten:
- Jarque-Bera
- ACF log returns
- ACF squared log returns
- Rolling Volatility
- Drawdown

Nicht im MVP:
- GARCH
- ARIMA
- Hurst Exponent
- Ljung-Box als Pflichtbestandteil
- Intraday-Analyse

---

## 3. Finaler Output

Diese Datei definiert verbindlich die technischen und methodischen Entscheidungen fuer das Projekt `crypto-market-data-analysis`.

### 3.1 Datenquelle
- Es wird `yfinance` als erste Datenquelle verwendet.
- Begruendung:
  - kostenlos
  - einfach in Python integrierbar
  - ausreichend fuer ein erstes Quant-Research-MVP
- Hinweis:
  - fuer Lern- und Forschungszwecke geeignet, aber kein institutioneller Premium-Datenfeed

### 3.2 Datenfrequenz
- Verwendet werden **taegliche Daten**.
- Begruendung:
  - stabiler und sauberer als Intraday-Daten
  - weniger Datenprobleme
  - leichter nachvollziehbar
  - passend fuer ein erstes Statistikprojekt

### 3.3 Assets im MVP
- BTC-USD
- ETH-USD
- SOL-USD

Optionale spaetere Erweiterung:
- ADA-USD
- LINK-USD
- AVAX-USD

### 3.4 Analysezeitraum
- Standard: letzte **5 Jahre**
- Umsetzung ueber Konfigurationsdatei mit:
  - `start_date`
  - `end_date`

### 3.5 Preisbasis
- Primaer soll `Adj Close` verwendet werden, wenn dies fuer den jeweiligen Ticker sinnvoll verfuegbar ist.
- Falls `Adj Close` nicht vorhanden oder nicht sinnvoll nutzbar ist, wird `Close` verwendet.
- Die verwendete Preisbasis muss im Report explizit dokumentiert werden.

### 3.6 Return-Definitionen
Es werden beide Return-Arten berechnet:

#### Simple Return
`(P_t / P_{t-1}) - 1`

#### Log Return
`ln(P_t / P_{t-1})`

#### Hauptregel
- Die primaeren statistischen Analysen basieren auf **log returns**.
- Simple returns werden zusaetzlich fuer Vergleich und Vollstaendigkeit gespeichert.
- Drawdown und kumulierte Entwicklung werden ueber Preis- bzw. Vermoegenskurvenlogik berechnet.

### 3.7 Datenbereinigung
- Zeitreihe nach Datum sortieren
- ungueltige oder leere Beobachtungen entfernen
- keine aggressive Imputation fehlender Werte
- erste NaN-Zeile nach Return-Berechnung entfernen
- Datenbereinigung im Report kurz dokumentieren

### 3.8 Annualisierung
- Fuer Krypto wird mit **365 Tagen** annualisiert.
- Regeln:
  - annualisierte Volatilitaet = daily std * sqrt(365)
  - annualisierte Sharpe Ratio = daily Sharpe * sqrt(365)
- Diese Regel muss in Code und Report dokumentiert werden.

### 3.9 Sharpe Ratio
- Im MVP wird ein risikofreier Zins von **0.0** verwendet.
- Es soll aber bereits ein Konfigurationsparameter `risk_free_rate` vorbereitet werden.
- Im Report muss stehen, dass die Sharpe Ratio im MVP mit risikofreiem Zins = 0 berechnet wurde.

### 3.10 Statistische Kernanalysen im MVP
Im MVP verpflichtend:
- Jarque-Bera-Test auf Normalitaet
- ACF der log returns
- ACF der squared log returns
- Rolling Volatility
- Drawdown-Verlauf

Optional spaeter:
- PACF
- Shapiro-Wilk
- Anderson-Darling
- Ljung-Box
- GARCH-Modelle

### 3.11 Rolling Window
- Standardwert fuer Rolling Volatility: `30`
- Der Wert soll ueber die Konfiguration anpassbar sein.

### 3.12 Plot-Standard
Folgende Kernplots muessen erzeugt und gespeichert werden:
- Preisverlauf
- Histogramm der log returns
- QQ-Plot
- Rolling Volatility
- Drawdown-Verlauf
- ACF der log returns
- ACF der squared log returns

Speicherort:
- `reports/figures/`

Dateinamen sollen konsistent und klar sein, z. B.:
- `btc_price.png`
- `btc_histogram_log_returns.png`
- `btc_qqplot.png`
- `btc_rolling_volatility.png`

### 3.13 Bericht
- Es wird automatisch ein Markdown-Bericht erzeugt.
- Speicherort: `reports/summary.md`
- Inhalt:
  - kurze Projektbeschreibung
  - analysierte Assets
  - Analysezeitraum
  - verwendete Preisbasis
  - Kennzahlen in Tabellenform
  - Verweise auf Abbildungen
  - kurze sachliche Interpretation

### 3.14 Rolle der AI
- Die AI darf nur kommentieren, nicht rechnen.
- Erlaubt:
  - Zusammenfassung berechneter Ergebnisse
  - kurzes Fazit
  - Dokumentationshilfe
- Nicht erlaubt:
  - Kennzahlen schaetzen
  - statistische Resultate ersetzen
  - Tests ohne berechnete Werte interpretieren

**Leitregel:**
`Python rechnet, AI kommentiert.`

### 3.15 Architekturprinzip
Das Projekt soll modular umgesetzt werden mit mindestens folgenden Dateien:
- `src/data_loader.py`
- `src/preprocessing.py`
- `src/metrics.py`
- `src/stats_tests.py`
- `src/plots.py`
- `src/report_generator.py`
- `main.py`

### 3.16 Notebook-Regel
- Ein Notebook darf optional zusaetzlich existieren.
- Das Hauptprojekt soll aber als modulare Python-Struktur umgesetzt werden.
- Kein riesiges monolithisches Notebook als Kernarchitektur.

### 3.17 MVP-Prinzip
Das erste Ziel ist ein stabiles, reproduzierbares MVP.

Im MVP enthalten:
- 3 Assets
- daily data
- Kernkennzahlen
- Kernplots
- Markdown-Report
- einfache statistische Grundanalysen

Nicht Ziel des MVP:
- Trading-Bot
- Live-Daten
- Intraday-Forschung
- komplexe oekonometrische Modelle
- Machine Learning
- Web-Dashboard

### 3.18 Qualitaetsregeln fuer Codex
Codex soll:
- pragmatisch arbeiten
- keine overengineerte Architektur bauen
- keine unnoetigen Libraries hinzufuegen
- lesbaren und kommentierten Code schreiben
- Fehlerbehandlung sinnvoll umsetzen
- Konfiguration zentral halten
- klare Dateistruktur erzeugen

### 3.19 Zusammenfassung
Dieses Projekt ist ein erstes sauberes Quant-Research-MVP fuer Kryptowaehrungen. Die technische Umsetzung soll bewusst einfach, korrekt, erweiterbar und methodisch nachvollziehbar sein.

Alle spaeteren Erweiterungen wie Backtesting, ML oder Trading-Bots sollen erst auf Basis dieses Fundaments erfolgen.

---

## 4. Was du mit dieser Datei machen musst

1. Speichere diese Datei als `technical_decisions.md`.
2. Lege sie in deinen Projektordner `crypto-market-data-analysis`.
3. Verwende sie zusammen mit `project_spec.md` als Grundlage fuer den ersten Codex-Build.
4. Aendere diese Datei nur bewusst, wenn wir methodische Entscheidungen spaeter wirklich anpassen wollen.

---

## 5. Nächster Schritt

Als naechstes erstellen wir im gleichen Muster die Datei `codex_mvp_prompt.md`.
Diese Datei wird der erste produktive Build-Prompt fuer Codex sein.
