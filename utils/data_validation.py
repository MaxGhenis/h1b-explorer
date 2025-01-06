import pandas as pd
from typing import List
from .data_constants import COLUMNS_TO_KEEP, MIN_WAGE, MAX_WAGE, MIN_ROWS


def validate_data(df: pd.DataFrame) -> bool:
    """
    Validate the processed data meets requirements.

    Args:
        df: DataFrame to validate

    Returns:
        bool: True if data is valid, False otherwise
    """
    try:
        # Check all required columns exist
        if not all(col in df.columns for col in COLUMNS_TO_KEEP):
            return False

        # Check for minimum number of rows
        if len(df) < MIN_ROWS:
            return False

        # Check for reasonable wage ranges
        if not (
            df["ANNUAL_WAGE"].between(MIN_WAGE, MAX_WAGE).all()
            and df["ANNUAL_PREVAILING_WAGE"].between(MIN_WAGE, MAX_WAGE).all()
        ):
            return False

        # Check for non-empty required fields
        required_non_empty = ["EMPLOYER_NAME", "SOC_CODE", "WORKSITE_STATE"]
        if df[required_non_empty].isna().any().any():
            return False

        return True

    except Exception:
        return False


def validate_raw_data(df: pd.DataFrame) -> bool:
    """
    Validate raw data before processing.

    Args:
        df: Raw DataFrame to validate

    Returns:
        bool: True if data is valid, False otherwise
    """
    required_columns = [
        "CASE_STATUS",
        "FULL_TIME_POSITION",
        "EMPLOYER_NAME",
        "SOC_CODE",
        "WAGE_RATE_OF_PAY_FROM",
        "WAGE_UNIT_OF_PAY",
        "PREVAILING_WAGE",
        "PW_UNIT_OF_PAY",
        "WORKSITE_STATE",
    ]

    return all(col in df.columns for col in required_columns)
