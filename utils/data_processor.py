import pandas as pd
from .data_constants import COLUMNS_TO_KEEP
from .wage_utils import clean_wage, annualize_wage, calculate_wage_ratio


def standardize_soc_code(soc_code: str) -> str:
    """
    Standardize SOC code format by removing trailing zeros after decimal.
    E.g., '11-1011.00' -> '11-1011'
    """
    if pd.isna(soc_code):
        return soc_code

    # Convert to string and clean
    soc_str = str(soc_code).strip()

    # Split on decimal if present
    parts = soc_str.split(".")

    # Return base code if decimal part is all zeros or empty
    if len(parts) > 1 and (not parts[1] or parts[1].strip("0") == ""):
        return parts[0]

    return soc_str


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

    # Standardize SOC codes first
    df["SOC_CODE"] = df["SOC_CODE"].apply(standardize_soc_code)

    # Create SOC title map using first encountered title for each code
    soc_title_map = df.groupby("SOC_CODE")["SOC_TITLE"].first()
    df["SOC_TITLE"] = df["SOC_CODE"].map(soc_title_map)

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

    # Calculate wage ratio
    df["WAGE_RATIO"] = calculate_wage_ratio(df)

    # Select final columns
    return df[COLUMNS_TO_KEEP]
