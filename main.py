from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import yaml

from src.data_loader import download_ticker_data
from src.metrics import calculate_metrics
from src.plots import generate_all_plots
from src.preprocessing import preprocess_asset_data
from src.report_generator import generate_markdown_report
from src.stats_tests import run_statistical_tests


def load_config(config_path: Path) -> Dict[str, object]:
    if not config_path.exists():
        raise FileNotFoundError(f"config.yaml nicht gefunden: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    defaults = {
        "tickers": ["BTC-USD", "ETH-USD", "SOL-USD"],
        "start_date": None,
        "end_date": None,
        "rolling_window": 30,
        "risk_free_rate": 0.0,
        "annualization_factor": 365,
        "acf_lags": 30,
        "paths": {
            "raw_data_dir": "data/raw",
            "processed_data_dir": "data/processed",
            "report_dir": "reports",
            "figures_dir": "reports/figures",
            "summary_report": "reports/summary.md",
        },
    }

    merged = defaults.copy()
    merged.update({k: v for k, v in config.items() if k != "paths"})

    merged_paths = defaults["paths"].copy()
    merged_paths.update(config.get("paths", {}))
    merged["paths"] = merged_paths

    return merged


def resolve_analysis_dates(start_date: object, end_date: object) -> Tuple[str, str]:
    if end_date:
        end = pd.Timestamp(end_date).normalize()
    else:
        end = pd.Timestamp.today().normalize()

    if start_date:
        start = pd.Timestamp(start_date).normalize()
    else:
        start = (end - pd.DateOffset(years=5)).normalize()

    if start >= end:
        raise ValueError("start_date muss vor end_date liegen.")

    return start.date().isoformat(), end.date().isoformat()


def ensure_directories(project_root: Path, config: Dict[str, object]) -> Dict[str, Path]:
    paths_cfg = config["paths"]

    raw_dir = project_root / paths_cfg["raw_data_dir"]
    processed_dir = project_root / paths_cfg["processed_data_dir"]
    report_dir = project_root / paths_cfg["report_dir"]
    figure_dir = project_root / paths_cfg["figures_dir"]
    summary_report = project_root / paths_cfg["summary_report"]

    for directory in [raw_dir, processed_dir, report_dir, figure_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    return {
        "raw_dir": raw_dir,
        "processed_dir": processed_dir,
        "report_dir": report_dir,
        "figure_dir": figure_dir,
        "summary_report": summary_report,
    }


def main() -> None:
    project_root = Path(__file__).resolve().parent
    config = load_config(project_root / "config.yaml")
    paths = ensure_directories(project_root, config)

    start_date, end_date = resolve_analysis_dates(config.get("start_date"), config.get("end_date"))
    end_date_for_yf = (pd.Timestamp(end_date) + pd.Timedelta(days=1)).date().isoformat()

    tickers: List[str] = config["tickers"]
    rolling_window = int(config["rolling_window"])
    risk_free_rate = float(config["risk_free_rate"])
    annualization_factor = int(config["annualization_factor"])
    acf_lags = int(config.get("acf_lags", 30))

    metrics_by_asset: Dict[str, Dict[str, float]] = {}
    tests_by_asset: Dict[str, Dict[str, object]] = {}
    plots_by_asset: Dict[str, Dict[str, str]] = {}
    price_basis_by_asset: Dict[str, str] = {}
    cleaning_by_asset: Dict[str, Dict[str, int]] = {}
    failures: Dict[str, str] = {}

    for ticker in tickers:
        try:
            dl = download_ticker_data(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date_for_yf,
                raw_dir=paths["raw_dir"],
            )
            prep = preprocess_asset_data(dl, processed_dir=paths["processed_dir"])

            metrics_by_asset[ticker] = calculate_metrics(
                prep.data,
                risk_free_rate=risk_free_rate,
                annualization_factor=annualization_factor,
            )
            tests_by_asset[ticker] = run_statistical_tests(prep.data, nlags=acf_lags)
            plots_by_asset[ticker] = generate_all_plots(
                prep.data,
                ticker=ticker,
                rolling_window=rolling_window,
                annualization_factor=annualization_factor,
                figure_dir=paths["figure_dir"],
                acf_lags=acf_lags,
            )
            price_basis_by_asset[ticker] = f"{dl.price_column} ({dl.price_basis_note})"
            cleaning_by_asset[ticker] = prep.cleaning_summary
        except Exception as exc:
            failures[ticker] = str(exc)

    if not metrics_by_asset:
        lines = [f"- {k}: {v}" for k, v in failures.items()]
        raise RuntimeError("Keine Assets konnten verarbeitet werden.\n" + "\n".join(lines))

    metrics_df = pd.DataFrame(metrics_by_asset).T
    metrics_df.index.name = "ticker"
    metrics_df.to_csv(paths["processed_dir"] / "metrics_summary.csv")

    generate_markdown_report(
        output_path=paths["summary_report"],
        config=config,
        analysis_start=start_date,
        analysis_end=end_date,
        metrics_by_asset=metrics_by_asset,
        tests_by_asset=tests_by_asset,
        plots_by_asset=plots_by_asset,
        price_basis_by_asset=price_basis_by_asset,
        cleaning_by_asset=cleaning_by_asset,
    )

    print("Pipeline abgeschlossen.")
    print(f"Verarbeitete Assets: {', '.join(metrics_by_asset.keys())}")
    print(f"Report: {paths['summary_report']}")
    if failures:
        print("Fehlgeschlagene Assets:")
        for ticker, reason in failures.items():
            print(f"- {ticker}: {reason}")


if __name__ == "__main__":
    main()