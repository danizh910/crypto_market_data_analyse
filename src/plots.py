from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.graphics.tsaplots import plot_acf


def _slugify_ticker(ticker: str) -> str:
    return ticker.lower().replace("-usd", "").replace("-", "_")


def _save_no_data_plot(path: Path, title: str, message: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=11)
    ax.set_title(title)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _plot_price(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["Date"], df["price"], linewidth=1.6)
    ax.set_title(f"{ticker} Price Series")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_histogram(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    series = df["log_return"].dropna()
    if series.empty:
        _save_no_data_plot(out_path, f"{ticker} Histogram of Log Returns", "No data after cleaning")
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(series, bins=50, alpha=0.8, edgecolor="black")
    ax.set_title(f"{ticker} Histogram of Log Returns")
    ax.set_xlabel("Log Return")
    ax.set_ylabel("Frequency")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_qq(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    series = df["log_return"].dropna()
    if series.shape[0] < 2:
        _save_no_data_plot(out_path, f"{ticker} QQ Plot (Log Returns)", "Insufficient data")
        return

    fig, ax = plt.subplots(figsize=(6, 6))
    stats.probplot(series, dist="norm", plot=ax)
    ax.set_title(f"{ticker} QQ Plot of Log Returns")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_rolling_volatility(
    df: pd.DataFrame,
    ticker: str,
    rolling_window: int,
    annualization_factor: int,
    out_path: Path,
) -> None:
    rolling_vol = df["log_return"].rolling(window=rolling_window).std(ddof=1) * np.sqrt(annualization_factor)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["Date"], rolling_vol, linewidth=1.4)
    ax.set_title(f"{ticker} Rolling Volatility ({rolling_window}D, annualized)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_drawdown(df: pd.DataFrame, ticker: str, out_path: Path) -> None:
    running_max = df["price"].cummax()
    drawdown = df["price"] / running_max - 1.0

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["Date"], drawdown, linewidth=1.4)
    ax.set_title(f"{ticker} Drawdown Series")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_acf(series: pd.Series, ticker: str, title: str, nlags: int, out_path: Path) -> None:
    clean = series.dropna()
    if clean.shape[0] < 3:
        _save_no_data_plot(out_path, title, "Insufficient data")
        return

    lags = min(nlags, clean.shape[0] - 1)
    fig, ax = plt.subplots(figsize=(10, 5))
    plot_acf(clean, lags=lags, ax=ax, alpha=0.05, zero=True)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def generate_all_plots(
    asset_df: pd.DataFrame,
    ticker: str,
    rolling_window: int,
    annualization_factor: int,
    figure_dir: Path,
    acf_lags: int = 30,
) -> Dict[str, str]:
    figure_dir.mkdir(parents=True, exist_ok=True)

    slug = _slugify_ticker(ticker)

    filenames = {
        "price": f"{slug}_price.png",
        "histogram_log_returns": f"{slug}_histogram_log_returns.png",
        "qq_log_returns": f"{slug}_qq_log_returns.png",
        "rolling_volatility": f"{slug}_rolling_volatility.png",
        "drawdown": f"{slug}_drawdown.png",
        "acf_log_returns": f"{slug}_acf_log_returns.png",
        "acf_squared_log_returns": f"{slug}_acf_squared_log_returns.png",
    }

    _plot_price(asset_df, ticker, figure_dir / filenames["price"])
    _plot_histogram(asset_df, ticker, figure_dir / filenames["histogram_log_returns"])
    _plot_qq(asset_df, ticker, figure_dir / filenames["qq_log_returns"])
    _plot_rolling_volatility(
        asset_df,
        ticker,
        rolling_window=rolling_window,
        annualization_factor=annualization_factor,
        out_path=figure_dir / filenames["rolling_volatility"],
    )
    _plot_drawdown(asset_df, ticker, figure_dir / filenames["drawdown"])
    _plot_acf(
        asset_df["log_return"],
        ticker,
        title=f"{ticker} ACF of Log Returns",
        nlags=acf_lags,
        out_path=figure_dir / filenames["acf_log_returns"],
    )
    _plot_acf(
        asset_df["squared_log_return"],
        ticker,
        title=f"{ticker} ACF of Squared Log Returns",
        nlags=acf_lags,
        out_path=figure_dir / filenames["acf_squared_log_returns"],
    )

    return {key: f"figures/{value}" for key, value in filenames.items()}