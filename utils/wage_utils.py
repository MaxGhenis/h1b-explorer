import pandas as pd
import numpy as np
from typing import Any
from .data_constants import WAGE_MULTIPLIERS


def clean_wage(wage_str: Any) -> float:
    """
    Clean wage string and convert to float.

    Args:
        wage_str: The wage value to clean (can be string, float, or int)

    Returns:
        float: Cleaned wage value or np.nan if invalid
    """
    if pd.isna(wage_str):
        return np.nan
    if isinstance(wage_str, (int, float)):
        return float(wage_str)

    try:
        cleaned = str(wage_str).replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return np.nan


def annualize_wage(
    row: pd.Series,
    wage_col: str = "WAGE_RATE_OF_PAY_FROM",
    unit_col: str = "WAGE_UNIT_OF_PAY",
) -> float:
    """
    Convert wage to annual based on unit of pay.

    Args:
        row: DataFrame row containing wage and unit information
        wage_col: Name of the wage column
        unit_col: Name of the unit column

    Returns:
        float: Annualized wage value
    """
    wage = row[wage_col]
    if pd.isna(wage):
        return np.nan

    unit = str(row[unit_col]).lower() if pd.notna(row[unit_col]) else "year"

    for key, multiplier in WAGE_MULTIPLIERS.items():
        if key in unit:
            return wage * multiplier

    return wage  # Default to assuming annual if unit not recognized


def calculate_wage_ratio(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the ratio between actual and prevailing wages.

    Args:
        df: DataFrame containing wage information

    Returns:
        pd.Series: Series containing wage ratios
    """
    return df["ANNUAL_WAGE"] / df["ANNUAL_PREVAILING_WAGE"]


def filter_invalid_wages(
    df: pd.DataFrame, min_wage: float, max_wage: float
) -> pd.DataFrame:
    """
    Filter out rows with invalid wage values.

    Args:
        df: DataFrame to filter
        min_wage: Minimum valid wage
        max_wage: Maximum valid wage

    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    wage_mask = (df["ANNUAL_WAGE"].between(min_wage, max_wage)) & (
        df["ANNUAL_PREVAILING_WAGE"].between(min_wage, max_wage)
    )
    return df[wage_mask]
