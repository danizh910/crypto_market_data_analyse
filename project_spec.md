# Project Specification: crypto-market-data-analysis

## 0. Arbeitsweise fuer dieses Projekt

Dieses Projekt wird bewusst in drei Schritten entwickelt:

1. **Vorschlag**  
   Zuerst wird eine sinnvolle erste Version der Projektdefinition erstellt.

2. **Kritische Verbesserung**  
   Danach werden methodische Schwaechen, unklare Punkte und typische Fehlerquellen aktiv verbessert.

3. **Finale Spezifikation**  
   Erst danach wird die finale Datei erstellt, die als verbindliche Grundlage fuer Codex und die weitere Umsetzung dient.

### Rolle von ChatGPT in diesem Projekt
ChatGPT uebernimmt hier nicht primaer das Coden, sondern:
- Spezifikation
- methodische Strukturierung
- Priorisierung
- Qualitaetskontrolle
- Review von Statistik und Logik
- Verbesserungsvorschlaege
- Prompt-Engineering fuer Codex

### Rolle von Codex in diesem Projekt
Codex soll auf Basis der finalen Spezifikation:
- die Projektstruktur erzeugen
- Python-Code schreiben
- Dateien anlegen
- Plots und Reports generieren
- technische Verbesserungen umsetzen

### Grundprinzip
**Python rechnet, AI kommentiert.**  
Alle Kennzahlen, Tests und Plots muessen deterministisch in Python erzeugt werden. Ein LLM darf spaeter nur auf Basis bereits berechneter Resultate ein kleines Fazit formulieren.

---

## 1. Vorschlag: erste Projektdefinition

### Projektname
`crypto-market-data-analysis`

### Grundidee
Ein erstes Quant-Research-Projekt zur statistischen Analyse historischer Kryptomarktdaten.

### Primaziel
Untersuchung der statistischen Eigenschaften von BTC, ETH und SOL anhand taeglicher historischer Kursdaten.

### Erste geplante Inhalte
- Datenimport historischer Tagesdaten
- Berechnung von Returns
- Berechnung zentraler Risikokennzahlen
- Analyse der Renditeverteilung
- Analyse von Volatilitaet und Drawdown
- einfache Zeitreihenanalyse mit Autokorrelation
- automatischer Markdown-Report
- optional kleines AI-Fazit auf Basis der Resultate

### Erste geplante Assets
- BTC-USD
- ETH-USD
- SOL-USD

### Erste geplante Bibliotheken
- pandas
- numpy
- matplotlib
- scipy
- statsmodels
- yfinance

### Erste geplante Outputs
- gespeicherte Rohdaten
- verarbeitete Daten
- Kennzahlen pro Asset
- gespeicherte Plots
- Markdown-Report

---

## 2. Eingebaute Verbesserungen gegenueber dem ersten Vorschlag

Die folgende finale Spezifikation basiert nicht nur auf dem ersten Vorschlag, sondern bereits auf aktiv eingebauten Verbesserungen.

### Verbesserung 1: Daily statt Intraday
Es werden fuer den Start bewusst **taegliche Daten** verwendet.  
Begruendung:
- stabiler
- weniger Datenprobleme
- schneller umsetzbar
- statistisch leichter interpretierbar

### Verbesserung 2: Wenige Assets im MVP
Es werden zunaechst nur **BTC, ETH und SOL** verwendet.  
Begruendung:
- geringere Komplexitaet
- besserer Vergleich
- schnelleres Debugging
- sauberes MVP

### Verbesserung 3: Log Returns als Hauptbasis
Es werden simple returns und log returns berechnet, aber die Hauptanalysen basieren primaer auf **log returns**.  
Begruendung:
- methodisch sauberer fuer Finanzstatistik
- besser fuer Verteilungs- und Zeitreihenanalyse

### Verbesserung 4: 365 statt 252 fuer Annualisierung
Da Kryptomaerkte jeden Tag handeln, wird im Projekt mit **365 Tagen** annualisiert.  
Begruendung:
- fachlich passender fuer Krypto
- sauber dokumentierte Annahme

### Verbesserung 5: Sharpe Ratio bewusst einfach halten
Im MVP wird der risikofreie Zins standardmaessig auf **0** gesetzt, aber als Konfigurationswert vorbereitet.  
Begruendung:
- klarer MVP
- spaeter leicht erweiterbar

### Verbesserung 6: Nicht zu viele Tests im MVP
Es werden nur wenige, aber sinnvolle Kernanalysen aufgenommen:
- Jarque-Bera-Test
- ACF der log returns
- ACF der squared log returns

Begruendung:
- Fokus auf Stabilitaet
- keine unnoetige Ueberkomplexitaet

### Verbesserung 7: AI nur fuer Schlussfazit
Die AI wird nicht zur Berechnung verwendet, sondern nur fuer ein kleines beschreibendes Fazit auf Basis bereits berechneter Resultate.

---

## 3. Finale Spezifikation

### 3.1 Projektuebersicht

#### Projektname
`crypto-market-data-analysis`

#### Projekttyp
Quant-Research / statistische Marktanalyse

#### Projektziel
Ziel des Projekts ist die statistische Untersuchung historischer Kryptomarktdaten, um zentrale Eigenschaften von Renditen, Risiko und Zeitreihenverhalten zu analysieren.

Das Projekt ist **kein Trading-Bot** und auch **keine AI-Handelslogik**, sondern ein sauberes quantitativeres Grundlagenprojekt. Es soll eine wissenschaftlich nachvollziehbare Basis schaffen, auf der spaeter Backtesting, Faktoranalysen oder Machine-Learning-Modelle aufbauen koennen.

#### Primare Assets
- BTC-USD
- ETH-USD
- SOL-USD

#### Optionale spaetere Erweiterungen
- ADA-USD
- LINK-USD
- AVAX-USD

---

### 3.2 Problemstellung

Kryptomaerkte sind durch hohe Volatilitaet, starke Drawdowns und haeufige Extrembewegungen gekennzeichnet. Fuer die Entwicklung spaeterer quantitativer Handels- oder Analysemodelle ist es notwendig, zuerst die grundlegenden statistischen Eigenschaften dieser Maerkte zu verstehen.

Insbesondere ist relevant:
- ob taegliche Returns normalverteilt sind
- ob fat tails vorliegen
- ob Volatility Clustering beobachtbar ist
- ob lineare Autokorrelation in den Returns besteht
- ob einfache Hinweise auf Momentum oder Mean Reversion sichtbar sind

---

### 3.3 Forschungsfragen

1. Sind taegliche Returns von BTC, ETH und SOL annaehernd normalverteilt?
2. Zeigen die Return-Verteilungen Hinweise auf fat tails und Ausreisser?
3. Wie unterscheiden sich BTC, ETH und SOL hinsichtlich Volatilitaet und Maximum Drawdown?
4. Gibt es Hinweise auf Volatility Clustering?
5. Gibt es signifikante lineare Autokorrelation in den taeglichen Returns?
6. Gibt es erste Hinweise auf Momentum oder Mean Reversion auf einfacher Zeitreihenebene?
7. Wie unterscheiden sich die Assets in ihrer risikoadjustierten Performance?

---

### 3.4 Hypothesen

#### H1: Nicht-Normalitaet
Die taeglichen Returns der untersuchten Kryptowaehrungen sind nicht normalverteilt.

#### H2: Fat Tails
Die Return-Verteilungen weisen erhoehte Kurtosis auf und enthalten haeufiger extreme Beobachtungen als eine Normalverteilung.

#### H3: Volatility Clustering
Phasen hoher Volatilitaet treten gebuendelt auf.

#### H4: Schwache lineare Autokorrelation der Returns
Die lineare Autokorrelation der taeglichen Returns ist gering oder instabil.

#### H5: Staerkere Abhaengigkeit in quadrierten Returns
Quadrierte Returns weisen staerkere Autokorrelationsmuster auf als rohe Returns und deuten damit auf zeitlich persistente Volatilitaet hin.

---

### 3.5 Methodischer Rahmen

#### Datenquelle
- `yfinance`

#### Datenfrequenz
- taegliche Daten

#### Zeitraum
- Standard: letzte 5 Jahre
- steuerbar ueber `start_date` und `end_date`

#### Preisbasis
- primaer `Adj Close`, falls sinnvoll verfuegbar
- falls nicht sinnvoll oder identisch, dokumentiert `Close`

#### Return-Definitionen
Es werden zwei Return-Typen berechnet:

1. **Simple Return**  
   `(P_t / P_{t-1}) - 1`

2. **Log Return**  
   `ln(P_t / P_{t-1})`

#### Hauptregel fuer Analysen
- statistische Hauptanalysen: **log returns**
- Drawdown- und Performance-Logik: Preis- bzw. Vermoegenskurvenbasis

#### Fehlende Werte
- Daten nach Datum sortieren
- ungueltige Beobachtungen entfernen
- keine blinde Auffuellung von fehlenden Werten
- erste NaN-Zeile nach Return-Berechnung entfernen
- Datenbereinigung im Report knapp dokumentieren

---

### 3.6 Kennzahlen

Pro Asset sollen mindestens folgende Kennzahlen berechnet werden:

#### Basiskennzahlen
- Anzahl Beobachtungen
- durchschnittlicher taeglicher Return
- Median Return
- Standardabweichung der Returns
- Minimum Return
- Maximum Return

#### Annualisierte Kennzahlen
- annualisierte Volatilitaet
- annualisierte Sharpe Ratio

#### Risikokennzahlen
- Maximum Drawdown

#### Verteilungseigenschaften
- Skewness
- Kurtosis

#### Annualisierungsregel
Es wird mit **365 Tagen** annualisiert.

#### Sharpe-Regel
Im MVP wird mit einem risikofreien Zins von **0** gerechnet. Ein Konfigurationsparameter dafuer soll vorbereitet sein.

---

### 3.7 Statistische Tests und Analysen

#### Verteilungsanalyse
- Histogramm der log returns
- QQ-Plot der log returns
- Jarque-Bera-Test auf Normalitaet

#### Zeitreihenanalyse
- ACF der log returns
- optional spaeter PACF der log returns

#### Volatility-Clustering
- ACF der squared log returns
- Rolling Volatility

#### Heuristische Marktstruktur
- einfache Interpretation der Autokorrelationsstruktur
- vorsichtige Hinweise auf Momentum oder Mean Reversion

#### Nicht Teil des MVP
- GARCH
- ARIMA
- Regime-Switching
- Hurst Exponent
- ML-Modelle

---

### 3.8 Visualisierungen

Mindestens folgende Plots sollen erzeugt und gespeichert werden:

1. Preisverlauf pro Asset
2. Histogramm der log returns
3. QQ-Plot der log returns
4. Rolling Volatility
5. Drawdown-Verlauf
6. ACF der log returns
7. ACF der squared log returns

Speicherort:
- `reports/figures/`

---

### 3.9 Deliverables

Das Projekt soll mindestens folgende Ergebnisse liefern:

#### Daten
- Rohdaten in `data/raw/`
- verarbeitete Daten in `data/processed/`

#### Analyse
- Kennzahlen pro Asset
- statistische Testergebnisse
- gespeicherte Plot-Dateien

#### Bericht
Ein automatisch erzeugter Markdown-Bericht in:
- `reports/summary.md`

Der Bericht soll enthalten:
- kurze Projektbeschreibung
- analysierte Assets
- Analysezeitraum
- verwendete Preisbasis
- Tabellen mit Kennzahlen
- Verweise auf die wichtigsten Abbildungen
- kurze sachliche Interpretation der Resultate

#### Optionales AI-Fazit
Ein kleines Fazit darf generiert werden, aber nur auf Basis bereits berechneter Kennzahlen und Testergebnisse.

---

### 3.10 Technischer Stack

#### Sprache
- Python

#### Kernbibliotheken
- pandas
- numpy
- matplotlib
- scipy
- statsmodels
- yfinance

#### Optional
- jupyter

#### AI-Rollen
- ChatGPT: Spezifikation, Methodik, Review, Projektleitung
- Codex: technische Umsetzung, Refactoring, Struktur, README
- Ollama: kleines lokales Fazit oder Zusammenfassungen

---

### 3.11 Projektstruktur

```text
crypto-market-data-analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── reports/
│   ├── figures/
│   └── summary.md
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── metrics.py
│   ├── stats_tests.py
│   ├── plots.py
│   └── report_generator.py
│
├── config.yaml
├── main.py
├── requirements.txt
├── README.md
└── project_spec.md
```

---

### 3.12 Definition of Done

Das MVP gilt als fertig, wenn:

1. BTC, ETH und SOL automatisiert geladen werden koennen.
2. Rohdaten lokal gespeichert werden.
3. simple returns und log returns korrekt berechnet werden.
4. alle definierten Kennzahlen pro Asset berechnet werden.
5. Jarque-Bera und ACF-Analysen fehlerfrei laufen.
6. alle vorgesehenen Kernplots gespeichert werden.
7. ein Markdown-Bericht automatisch erzeugt wird.
8. Konfiguration ueber zentrale Parameter moeglich ist.
9. das Projekt lokal reproduzierbar laeuft.
10. die AI keine Berechnungen ersetzt, sondern nur kommentiert.

---

### 3.13 MVP-Abgrenzung

#### Im MVP enthalten
- BTC, ETH, SOL
- taegliche Daten
- yfinance
- simple returns + log returns
- Kennzahlen
- Jarque-Bera
- ACF der log returns
- ACF der squared log returns
- Rolling Volatility
- Drawdown
- Markdown-Report

#### Nicht im MVP enthalten
- Intraday-Daten
- Live-Daten
- Trading-Signale
- Backtesting
- Dashboard
- ML
- komplexe oekonometrische Modelle

---

### 3.14 Qualitaetsprinzipien

- zuerst korrekt, dann schoen
- zuerst MVP, dann Erweiterungen
- modularer Code statt Chaos im Notebook
- Python rechnet, AI kommentiert
- methodisch sauber statt kuenstlich komplex
- klare Dokumentation aller Annahmen

---

### 3.15 Spaetere Erweiterungen

1. mehr Coins
2. Korrelationsanalyse und Rolling Correlation
3. Backtesting einfacher Strategien
4. Faktor-Features
5. ML-Vorbereitung
6. Streamlit-Dashboard
7. lokales AI-Fazit aus JSON-Outputs

---

## 4. Was mit dieser Datei gemacht werden soll

1. Diese Datei als `project_spec.md` im Projektordner speichern.
2. Sie dient als **verbindliche fachliche Grundlage** fuer das gesamte Projekt.
3. Im naechsten Schritt wird darauf aufbauend eine Datei `technical_decisions.md` erstellt.
4. Danach wird ein gezielter `codex_mvp_prompt.md` erstellt, damit Codex exakt auf dieser Grundlage arbeitet.
5. Immer wenn spaeter etwas unklar ist, gilt zuerst diese Spezifikation.

---

## 5. Hinweis zur Zusammenarbeit

Ab jetzt soll fuer jeden weiteren Schritt dieselbe Logik gelten:

1. zuerst ein sinnvoller Vorschlag
2. dann aktive Verbesserung durch methodische Kritik
3. dann finale Datei
4. danach klare Anweisung, was du mit der Datei tun sollst

So bleibt das Projekt strukturiert, nachvollziehbar und sauber steuerbar.
