from typing import Dict, List

import numpy as np
import pandas as pd
from scipy.stats import jarque_bera
from statsmodels.tsa.stattools import acf


def _safe_acf(series: pd.Series, nlags: int) -> List[float]:
    clean = series.dropna()
    if clean.shape[0] < 2:
        return []
    used_lags = min(nlags, clean.shape[0] - 1)
    acf_values = acf(clean, nlags=used_lags, fft=True, missing="drop")
    return [float(x) for x in acf_values]


def run_statistical_tests(asset_df: pd.DataFrame, nlags: int = 30) -> Dict[str, object]:
    log_returns = asset_df["log_return"].dropna()
    squared_log_returns = asset_df["squared_log_return"].dropna()

    if log_returns.shape[0] < 2:
        jb_stat = float("nan")
        jb_pvalue = float("nan")
    else:
        jb_result = jarque_bera(log_returns)
        jb_stat = float(jb_result.statistic)
        jb_pvalue = float(jb_result.pvalue)

    acf_log = _safe_acf(log_returns, nlags=nlags)
    acf_squared = _safe_acf(squared_log_returns, nlags=nlags)

    return {
        "jarque_bera_stat": jb_stat,
        "jarque_bera_pvalue": jb_pvalue,
        "jarque_bera_reject_normality_5pct": bool(np.isfinite(jb_pvalue) and jb_pvalue < 0.05),
        "acf_log_returns": acf_log,
        "acf_squared_log_returns": acf_squared,
    }