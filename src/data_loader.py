from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import pandas as pd
import yfinance as yf


@dataclass
class DownloadResult:
    ticker: str
    data: pd.DataFrame
    price_column: str
    raw_path: Path
    price_basis_note: str


def _pick_price_column(df: pd.DataFrame) -> Tuple[str, str]:
    if "Adj Close" in df.columns and df["Adj Close"].notna().any():
        if "Close" in df.columns:
            valid = df[["Adj Close", "Close"]].dropna()
            if not valid.empty:
                max_diff = (valid["Adj Close"] - valid["Close"]).abs().max()
                if float(max_diff) > 1e-10:
                    return "Adj Close", "Adj Close genutzt (sinnvoll verfuegbar und nicht identisch zu Close)."
            return "Close", "Close genutzt (Adj Close vorhanden, aber nicht sinnvoll abweichend)."
        return "Adj Close", "Adj Close genutzt (Close nicht vorhanden)."

    if "Close" in df.columns and df["Close"].notna().any():
        return "Close", "Close genutzt (Adj Close fehlt oder ist nicht nutzbar)."

    raise ValueError("Keine nutzbare Preisspalte gefunden (weder 'Adj Close' noch 'Close').")


def download_ticker_data(
    ticker: str,
    start_date: str,
    end_date: str,
    raw_dir: Path,
) -> DownloadResult:
    raw_dir.mkdir(parents=True, exist_ok=True)

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=False,
        progress=False,
        threads=False,
    )

    if df.empty:
        raise ValueError(f"Keine Daten von yfinance fuer {ticker} erhalten.")

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df = df.reset_index()
    if "Date" not in df.columns:
        raise ValueError(f"Spalte 'Date' fehlt in den Rohdaten fuer {ticker}.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").drop_duplicates(subset=["Date"])

    price_column, note = _pick_price_column(df)

    raw_path = raw_dir / f"{ticker.lower().replace('-', '_')}_raw.csv"
    df.to_csv(raw_path, index=False)

    return DownloadResult(
        ticker=ticker,
        data=df,
        price_column=price_column,
        raw_path=raw_path,
        price_basis_note=note,
    )