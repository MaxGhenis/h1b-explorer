import pandas as pd
import numpy as np
import streamlit as st
import requests
from io import BytesIO
import os

# Constants
DATA_PATH = "data"
PROCESSED_DATA_FILE = "processed_h1b_data.parquet"
RAW_DATA_FILE = "raw_h1b_data.xlsx"
DATA_URL = "https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2024_Q1.xlsx"


def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)


def download_raw_data():
    """Download the raw data file"""
    st.info("Downloading LCA data... This may take a moment.")
    try:
        response = requests.get(DATA_URL, timeout=30)
        response.raise_for_status()  # Raise an error for bad status codes

        ensure_data_directory()
        raw_data_path = os.path.join(DATA_PATH, RAW_DATA_FILE)

        # Save the raw Excel file
        with open(raw_data_path, "wb") as f:
            f.write(response.content)

        return True
    except Exception as e:
        st.error(f"Error downloading data: {str(e)}")
        return False


def clean_wage(wage_str):
    """Clean wage string and convert to float"""
    if pd.isna(wage_str):
        return np.nan
    if isinstance(wage_str, (int, float)):
        return float(wage_str)
    cleaned = str(wage_str).replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return np.nan


def process_data(df):
    """Process the raw H1B data"""
    # Convert problematic columns to string first
    str_columns = [
        "CASE_STATUS",
        "FULL_TIME_POSITION",
        "WAGE_UNIT_OF_PAY",
        "PW_UNIT_OF_PAY",
    ]
    for col in str_columns:
        df[col] = df[col].astype(str)

    # Filter for certified cases and full-time positions
    df = df[
        (df["CASE_STATUS"].str.contains("Certified", case=False, na=False))
        & (df["FULL_TIME_POSITION"].str.contains("Y", case=False, na=False))
    ]

    # Clean wage columns - handle both string and numeric inputs
    for col in ["WAGE_RATE_OF_PAY_FROM", "PREVAILING_WAGE"]:
        df[col] = df[col].apply(clean_wage)

    # Annualize wages using correct unit columns
    df["ANNUAL_WAGE"] = df.apply(
        lambda x: annualize_wage(
            x, wage_col="WAGE_RATE_OF_PAY_FROM", unit_col="WAGE_UNIT_OF_PAY"
        ),
        axis=1,
    )
    df["ANNUAL_PREVAILING_WAGE"] = df.apply(
        lambda x: annualize_wage(
            x, wage_col="PREVAILING_WAGE", unit_col="PW_UNIT_OF_PAY"
        ),
        axis=1,
    )

    # Filter out unreasonable wages (e.g., above $10M annually)
    df = df[
        (df["ANNUAL_WAGE"] > 10000)  # Filter out very low wages
        & (df["ANNUAL_WAGE"] < 10000000)  # Filter out unreasonably high wages
        & (df["ANNUAL_PREVAILING_WAGE"] > 10000)
        & (df["ANNUAL_PREVAILING_WAGE"] < 10000000)
    ]

    # Calculate wage ratio
    df["WAGE_RATIO"] = df["ANNUAL_WAGE"] / df["ANNUAL_PREVAILING_WAGE"]

    # Filter out extreme ratios
    df = df[
        (df["WAGE_RATIO"] > 0.5)  # Filter out wages less than half prevailing
        & (df["WAGE_RATIO"] < 5)  # Filter out wages more than 5x prevailing
    ]

    # Select needed columns
    columns_to_keep = [
        "EMPLOYER_NAME",
        "JOB_TITLE",
        "SOC_CODE",
        "SOC_TITLE",
        "WAGE_RATE_OF_PAY_FROM",
        "PREVAILING_WAGE",
        "WAGE_UNIT_OF_PAY",
        "PW_UNIT_OF_PAY",
        "ANNUAL_WAGE",
        "ANNUAL_PREVAILING_WAGE",
        "WAGE_RATIO",
        "WORKSITE_STATE",
    ]

    return df[columns_to_keep]


def annualize_wage(row, wage_col="WAGE_RATE_OF_PAY_FROM", unit_col="WAGE_UNIT_OF_PAY"):
    """Convert wage to annual based on unit of pay"""
    wage = row[wage_col]
    if pd.isna(wage):
        return np.nan

    unit = str(row[unit_col]).lower() if pd.notna(row[unit_col]) else "year"

    if "hour" in unit:
        return wage * 40 * 52
    elif "week" in unit:
        return wage * 52
    elif "bi" in unit or "semi" in unit:
        return wage * 24
    elif "month" in unit:
        return wage * 12
    else:
        return wage


@st.cache_data
def load_data():
    """Load or download the H1B data"""
    raw_data_path = os.path.join(DATA_PATH, RAW_DATA_FILE)
    processed_data_path = os.path.join(DATA_PATH, PROCESSED_DATA_FILE)

    # Check for processed data first
    if os.path.exists(processed_data_path):
        try:
            return pd.read_parquet(processed_data_path)
        except Exception as e:
            st.warning("Error reading processed data. Will try raw data...")

    # Check for raw data and process it
    if not os.path.exists(raw_data_path):
        if not download_raw_data():
            return None

    try:
        # Read raw data with explicit dtypes
        df = pd.read_excel(
            raw_data_path,
            dtype={
                "CASE_STATUS": str,
                "FULL_TIME_POSITION": str,
                "WAGE_UNIT_OF_PAY": str,
                "PW_UNIT_OF_PAY": str,
                "WAGE_RATE_OF_PAY_FROM": str,
                "PREVAILING_WAGE": str,
                "EMPLOYER_NAME": str,
                "JOB_TITLE": str,
                "SOC_CODE": str,
                "SOC_TITLE": str,
                "WORKSITE_STATE": str,
            },
        )

        processed_df = process_data(df)

        # Save processed data
        ensure_data_directory()
        processed_df.to_parquet(processed_data_path)

        return processed_df

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None
