from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from src.data_loader import DownloadResult


@dataclass
class PreprocessingResult:
    ticker: str
    data: pd.DataFrame
    processed_path: Path
    cleaning_summary: Dict[str, int]


def preprocess_asset_data(download_result: DownloadResult, processed_dir: Path) -> PreprocessingResult:
    processed_dir.mkdir(parents=True, exist_ok=True)

    ticker = download_result.ticker
    price_col = download_result.price_column
    df = download_result.data.copy()

    initial_rows = len(df)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.sort_values("Date").drop_duplicates(subset=["Date"])
    df = df.dropna(subset=["Date", price_col])
    df = df[df[price_col] > 0]

    cleaned_rows = len(df)

    df = df[["Date", price_col]].rename(columns={price_col: "price"})
    df["simple_return"] = df["price"].pct_change()
    df["log_return"] = np.log(df["price"] / df["price"].shift(1))
    df["squared_log_return"] = df["log_return"] ** 2

    before_drop_returns = len(df)
    df = df.dropna(subset=["simple_return", "log_return", "squared_log_return"]).reset_index(drop=True)
    final_rows = len(df)

    processed_path = processed_dir / f"{ticker.lower().replace('-', '_')}_processed.csv"
    df.to_csv(processed_path, index=False)

    cleaning_summary = {
        "rows_raw": initial_rows,
        "rows_after_basic_cleaning": cleaned_rows,
        "rows_removed_before_returns": initial_rows - cleaned_rows,
        "rows_removed_after_return_calc": before_drop_returns - final_rows,
        "rows_final": final_rows,
    }

    return PreprocessingResult(
        ticker=ticker,
        data=df,
        processed_path=processed_path,
        cleaning_summary=cleaning_summary,
    )