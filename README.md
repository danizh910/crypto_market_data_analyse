# crypto-market-data-analysis

Ein einfaches, stabiles Python-MVP zur statistischen Analyse historischer Kryptomarktdaten.

## Projektziel
Das Projekt laedt taegliche historische Daten fuer:
- BTC-USD
- ETH-USD
- SOL-USD

und erzeugt automatisiert:
- Rohdaten
- verarbeitete Daten (inkl. Returns)
- Kernkennzahlen
- statistische Tests
- Visualisierungen
- Markdown-Report

Leitprinzip: **Python rechnet, AI kommentiert.**

## Setup
Voraussetzungen:
- Python 3.10+
- Internetzugang fuer den Download via `yfinance`

## Installation
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Startanleitung
```bash
python main.py
```

Ergebnisse liegen danach in:
- `data/raw/`
- `data/processed/`
- `reports/figures/`
- `reports/summary.md`

## Projektstruktur
```text
crypto-market-data-analysis/
|
|-- data/
|   |-- raw/
|   `-- processed/
|
|-- reports/
|   |-- figures/
|   `-- summary.md
|
|-- src/
|   |-- data_loader.py
|   |-- preprocessing.py
|   |-- metrics.py
|   |-- stats_tests.py
|   |-- plots.py
|   `-- report_generator.py
|
|-- config.yaml
|-- main.py
|-- requirements.txt
|-- README.md
|-- project_spec.md
`-- technical_decisions.md
```

## Methodische Hinweise (MVP)
- Statistik basiert primaer auf **log returns**.
- Annualisierung nutzt **365** Tage (Krypto handelt 7 Tage/Woche).
- Sharpe Ratio nutzt im MVP standardmaessig `risk_free_rate = 0.0`.
- Fehlende Werte werden konservativ behandelt (kein blindes Auffuellen).
- Preisbasis wird pro Asset geprueft (`Adj Close` vs. `Close`) und im Report dokumentiert.

## Grenzen des MVP
- Keine Intraday-Daten
- Kein Live-Trading
- Kein Backtesting
- Keine komplexen Modelle (z. B. GARCH, ARIMA)
- Keine ML-Pipeline

## Moegliche naechste Schritte
- Mehr Assets aufnehmen (z. B. ADA, LINK, AVAX)
- Rolling Correlations und Korrelationsmatrix ergaenzen
- Backtesting einfacher Regeln
- Feature-Engineering fuer spaetere ML-Modelle
- Dashboard (z. B. Streamlit)