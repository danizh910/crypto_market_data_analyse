from pathlib import Path
from typing import Dict, List


def _is_finite_number(value: object) -> bool:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return False
    return v == v and v not in (float("inf"), float("-inf"))


def _fmt(value: object, digits: int = 6) -> str:
    if not _is_finite_number(value):
        return "NA"
    return f"{float(value):.{digits}f}"


def _markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([head, sep] + body)


def _interpret_asset(metrics: Dict[str, float], tests: Dict[str, object]) -> str:
    jb_p_raw = tests.get("jarque_bera_pvalue")
    if _is_finite_number(jb_p_raw) and float(jb_p_raw) < 0.05:
        normality = "Der Jarque-Bera-Test deutet auf eine Abweichung von Normalitaet hin (p < 0.05)."
    else:
        normality = "Der Jarque-Bera-Test liefert keine starke Evidenz gegen Normalitaet auf 5%-Niveau."

    annual_vol = metrics.get("annualized_volatility", float("nan"))
    if _is_finite_number(annual_vol):
        annual_vol = float(annual_vol)
        if annual_vol >= 1.0:
            vol_text = "Die annualisierte Volatilitaet ist sehr hoch."
        elif annual_vol >= 0.6:
            vol_text = "Die annualisierte Volatilitaet ist hoch."
        else:
            vol_text = "Die annualisierte Volatilitaet ist im Vergleich moderat."
    else:
        vol_text = "Die Volatilitaet konnte nicht stabil geschaetzt werden."

    max_dd = metrics.get("max_drawdown", float("nan"))
    if _is_finite_number(max_dd):
        dd_text = f"Der maximale Drawdown liegt bei {_fmt(max_dd, 4)}."
    else:
        dd_text = "Der maximale Drawdown konnte nicht berechnet werden."

    acf_log = tests.get("acf_log_returns", [])
    acf_sq = tests.get("acf_squared_log_returns", [])

    acf1 = float(acf_log[1]) if isinstance(acf_log, list) and len(acf_log) > 1 else float("nan")
    acf1_sq = float(acf_sq[1]) if isinstance(acf_sq, list) and len(acf_sq) > 1 else float("nan")

    if _is_finite_number(acf1) and abs(acf1) > 0.1:
        acf_text = "Es gibt einen sichtbaren kurzfristigen linearen Autokorrelationseffekt in den Log Returns."
    else:
        acf_text = "Die lineare Autokorrelation der Log Returns wirkt schwach."

    if _is_finite_number(acf1_sq) and abs(acf1_sq) > 0.1:
        vol_cluster_text = "Die ACF der quadrierten Log Returns spricht fuer Volatility Clustering."
    else:
        vol_cluster_text = "Die ACF der quadrierten Log Returns zeigt nur schwache Persistenz."

    return " ".join([normality, vol_text, dd_text, acf_text, vol_cluster_text])


def generate_markdown_report(
    output_path: Path,
    config: Dict[str, object],
    analysis_start: str,
    analysis_end: str,
    metrics_by_asset: Dict[str, Dict[str, float]],
    tests_by_asset: Dict[str, Dict[str, object]],
    plots_by_asset: Dict[str, Dict[str, str]],
    price_basis_by_asset: Dict[str, str],
    cleaning_by_asset: Dict[str, Dict[str, int]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    tickers = list(metrics_by_asset.keys())

    lines: List[str] = []
    lines.append("# Crypto Market Data Analysis - Summary")
    lines.append("")
    lines.append("## Projektbeschreibung")
    lines.append(
        "Dieses MVP analysiert taegliche historische Marktdaten fuer BTC-USD, ETH-USD und SOL-USD. "
        "Python berechnet Kennzahlen, statistische Tests und Grafiken; der Bericht dokumentiert diese Ergebnisse regelbasiert."
    )
    lines.append("")
    lines.append("## Analysierte Assets")
    lines.append(", ".join(tickers))
    lines.append("")
    lines.append("## Analysezeitraum")
    lines.append(f"- Start: {analysis_start}")
    lines.append(f"- Ende: {analysis_end}")
    lines.append("")
    lines.append("## Methodische Annahmen")
    lines.append("- Primaere statistische Basis: log returns")
    lines.append(f"- Annualisierung: {config['annualization_factor']} Tage (Krypto 24/7)")
    lines.append(f"- Risk-free rate fuer Sharpe Ratio: {config['risk_free_rate']}")
    lines.append(
        "- Annualisierte Sharpe Ratio: ((mean_daily_log_return - rf_daily) / std_daily_log_return) * sqrt(annualization_factor)"
    )
    lines.append("")

    lines.append("## Verwendete Preisbasis je Asset")
    price_rows = [[ticker, basis] for ticker, basis in price_basis_by_asset.items()]
    lines.append(_markdown_table(["Asset", "Preisbasis"], price_rows))
    lines.append("")

    lines.append("## Datenbereinigung je Asset")
    clean_rows: List[List[str]] = []
    for ticker, info in cleaning_by_asset.items():
        clean_rows.append(
            [
                ticker,
                str(info.get("rows_raw", "NA")),
                str(info.get("rows_removed_before_returns", "NA")),
                str(info.get("rows_removed_after_return_calc", "NA")),
                str(info.get("rows_final", "NA")),
            ]
        )
    lines.append(
        _markdown_table(
            [
                "Asset",
                "Rows raw",
                "Removed pre-returns",
                "Removed post-returns",
                "Rows final",
            ],
            clean_rows,
        )
    )
    lines.append("")

    lines.append("## Kennzahlen (pro Asset)")
    metric_rows: List[List[str]] = []
    for ticker, m in metrics_by_asset.items():
        metric_rows.append(
            [
                ticker,
                str(m.get("observations", "NA")),
                _fmt(m.get("mean_daily_log_return")),
                _fmt(m.get("std_daily_log_return")),
                _fmt(m.get("annualized_volatility")),
                _fmt(m.get("annualized_sharpe_ratio")),
                _fmt(m.get("max_drawdown"), 4),
                _fmt(m.get("skewness")),
                _fmt(m.get("kurtosis")),
                _fmt(m.get("min_log_return")),
                _fmt(m.get("max_log_return")),
                _fmt(m.get("median_log_return")),
            ]
        )

    lines.append(
        _markdown_table(
            [
                "Asset",
                "N",
                "Mean daily log ret",
                "Std daily log ret",
                "Ann. Vol",
                "Ann. Sharpe",
                "Max Drawdown",
                "Skewness",
                "Kurtosis",
                "Min log ret",
                "Max log ret",
                "Median log ret",
            ],
            metric_rows,
        )
    )
    lines.append("")

    lines.append("## Jarque-Bera-Test")
    jb_rows: List[List[str]] = []
    for ticker, t in tests_by_asset.items():
        reject = "Ja" if t.get("jarque_bera_reject_normality_5pct") else "Nein"
        jb_rows.append(
            [
                ticker,
                _fmt(t.get("jarque_bera_stat")),
                _fmt(t.get("jarque_bera_pvalue")),
                reject,
            ]
        )
    lines.append(_markdown_table(["Asset", "JB Statistic", "p-value", "Reject normality (5%)"], jb_rows))
    lines.append("")

    lines.append("## Sachliche Interpretation je Asset")
    for ticker in tickers:
        lines.append(f"### {ticker}")
        lines.append(_interpret_asset(metrics_by_asset[ticker], tests_by_asset[ticker]))
        lines.append("")

    lines.append("## Abbildungen")
    for ticker in tickers:
        lines.append(f"### {ticker}")
        plot_map = plots_by_asset[ticker]
        lines.append(f"- Preisverlauf: {plot_map['price']}")
        lines.append(f"- Histogramm log returns: {plot_map['histogram_log_returns']}")
        lines.append(f"- QQ-Plot log returns: {plot_map['qq_log_returns']}")
        lines.append(f"- Rolling Volatility: {plot_map['rolling_volatility']}")
        lines.append(f"- Drawdown-Verlauf: {plot_map['drawdown']}")
        lines.append(f"- ACF log returns: {plot_map['acf_log_returns']}")
        lines.append(f"- ACF squared log returns: {plot_map['acf_squared_log_returns']}")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")