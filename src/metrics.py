from typing import Dict

import numpy as np
import pandas as pd


def calculate_max_drawdown(prices: pd.Series) -> float:
    if prices.empty:
        return float("nan")
    running_max = prices.cummax()
    drawdown = prices / running_max - 1.0
    return float(drawdown.min())


def calculate_metrics(
    asset_df: pd.DataFrame,
    risk_free_rate: float,
    annualization_factor: int,
) -> Dict[str, float]:
    log_returns = asset_df["log_return"].dropna()

    observations = int(log_returns.shape[0])
    mean_daily = float(log_returns.mean()) if observations else float("nan")
    median_return = float(log_returns.median()) if observations else float("nan")
    std_daily = float(log_returns.std(ddof=1)) if observations > 1 else float("nan")

    annualized_volatility = (
        std_daily * float(np.sqrt(annualization_factor))
        if np.isfinite(std_daily)
        else float("nan")
    )

    rf_daily = risk_free_rate / annualization_factor
    if np.isfinite(std_daily) and std_daily > 0:
        daily_sharpe = (mean_daily - rf_daily) / std_daily
        annualized_sharpe = daily_sharpe * float(np.sqrt(annualization_factor))
    else:
        annualized_sharpe = float("nan")

    return {
        "observations": observations,
        "mean_daily_log_return": mean_daily,
        "std_daily_log_return": std_daily,
        "annualized_volatility": annualized_volatility,
        "annualized_sharpe_ratio": annualized_sharpe,
        "max_drawdown": calculate_max_drawdown(asset_df["price"]),
        "skewness": float(log_returns.skew()) if observations > 2 else float("nan"),
        "kurtosis": float(log_returns.kurtosis()) if observations > 3 else float("nan"),
        "min_log_return": float(log_returns.min()) if observations else float("nan"),
        "max_log_return": float(log_returns.max()) if observations else float("nan"),
        "median_log_return": median_return,
    }