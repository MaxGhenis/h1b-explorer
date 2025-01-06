import pandas as pd
from .data_constants import COLUMNS_TO_KEEP, MIN_WAGE, MAX_WAGE
from .wage_utils import (
    clean_wage,
    annualize_wage,
    calculate_wage_ratio,
    filter_invalid_wages,
)


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the raw H1B data.

    Args:
        df: Raw DataFrame to process

    Returns:
        pd.DataFrame: Processed DataFrame
    """
    # Make a copy to avoid modifying input
    df = df.copy()

    # Filter for certified cases and full-time positions
    df = df[
        (df["CASE_STATUS"].str.contains("Certified", case=False, na=False))
        & (df["FULL_TIME_POSITION"].str.contains("Y", case=False, na=False))
    ]

    # Clean wage columns
    for col in ["WAGE_RATE_OF_PAY_FROM", "PREVAILING_WAGE"]:
        df[col] = df[col].apply(clean_wage)

    # Annualize wages
    df["ANNUAL_WAGE"] = df.apply(
        lambda x: annualize_wage(x, "WAGE_RATE_OF_PAY_FROM", "WAGE_UNIT_OF_PAY"), axis=1
    )
    df["ANNUAL_PREVAILING_WAGE"] = df.apply(
        lambda x: annualize_wage(x, "PREVAILING_WAGE", "PW_UNIT_OF_PAY"), axis=1
    )

    # Filter out invalid wages
    df = filter_invalid_wages(df, MIN_WAGE, MAX_WAGE)

    # Calculate wage ratio
    df["WAGE_RATIO"] = calculate_wage_ratio(df)

    # Filter out extreme ratios
    df = df[df["WAGE_RATIO"].between(0.5, 5)]

    # Select final columns
    return df[COLUMNS_TO_KEEP]
