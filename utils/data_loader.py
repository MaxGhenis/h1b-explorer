import pandas as pd
import streamlit as st
import requests
import os
from typing import Optional
from .data_constants import (
    DATA_PATH,
    PROCESSED_DATA_FILE,
    RAW_DATA_FILE,
    DATA_URL,
    STRING_COLUMNS,
)
from .data_processor import process_data
from .data_validation import validate_data, validate_raw_data


def ensure_data_directory() -> None:
    """Create data directory if it doesn't exist"""
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)


def download_raw_data() -> bool:
    """
    Download the raw data file.

    Returns:
        bool: True if download was successful, False otherwise
    """
    st.info("Downloading LCA data... This may take a moment.")
    try:
        response = requests.get(DATA_URL, timeout=60)
        response.raise_for_status()

        ensure_data_directory()
        raw_data_path = os.path.join(DATA_PATH, RAW_DATA_FILE)

        with open(raw_data_path, "wb") as f:
            f.write(response.content)

        return True
    except Exception as e:
        st.error(f"Error downloading data: {str(e)}")
        return False


@st.cache_data
def load_data() -> Optional[pd.DataFrame]:
    """
    Load or download the H1B data.

    Returns:
        Optional[pd.DataFrame]: Processed DataFrame or None if error occurs
    """
    processed_data_path = os.path.join(DATA_PATH, PROCESSED_DATA_FILE)
    raw_data_path = os.path.join(DATA_PATH, RAW_DATA_FILE)

    # Try to load processed data first
    if os.path.exists(processed_data_path):
        try:
            df = pd.read_parquet(processed_data_path)
            if validate_data(df):
                return df
        except Exception:
            st.warning("Error reading processed data. Trying raw data...")

    # Download raw data if needed
    if not os.path.exists(raw_data_path):
        if not download_raw_data():
            return None

    try:
        # Read raw data with explicit dtypes
        df = pd.read_excel(raw_data_path, dtype={col: str for col in STRING_COLUMNS})

        if not validate_raw_data(df):
            st.error("Raw data validation failed")
            return None

        # Process the data
        processed_df = process_data(df)

        if validate_data(processed_df):
            # Save processed data
            ensure_data_directory()
            processed_df.to_parquet(processed_data_path)
            return processed_df
        else:
            st.error("Processed data validation failed")
            return None

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return None


def get_soc_title(df: pd.DataFrame, soc_code: str) -> str:
    """
    Get SOC title for a given SOC code.

    Args:
        df: DataFrame containing SOC data
        soc_code: SOC code to look up

    Returns:
        str: SOC title or empty string if not found
    """
    if soc_code == "All":
        return ""

    soc_titles = df[df["SOC_CODE"] == soc_code]["SOC_TITLE"].unique()
    return soc_titles[0] if len(soc_titles) > 0 else ""
