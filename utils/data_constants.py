from typing import List, Dict

# File paths and URLs
DATA_PATH = "data"
PROCESSED_DATA_FILE = "processed_h1b_data.parquet"
RAW_DATA_FILE = "raw_h1b_data.xlsx"
DATA_URL = "https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2024_Q1.xlsx"

# Column definitions
STRING_COLUMNS = [
    "CASE_STATUS",
    "FULL_TIME_POSITION",
    "WAGE_UNIT_OF_PAY",
    "PW_UNIT_OF_PAY",
    "EMPLOYER_NAME",
    "JOB_TITLE",
    "SOC_CODE",
    "SOC_TITLE",
    "WORKSITE_STATE",
]

WAGE_COLUMNS = ["WAGE_RATE_OF_PAY_FROM", "PREVAILING_WAGE"]

COLUMNS_TO_KEEP = [
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

# Wage multipliers for different pay periods
WAGE_MULTIPLIERS = {
    "hour": 40 * 52,  # 40 hours per week, 52 weeks per year
    "week": 52,  # 52 weeks per year
    "bi": 24,  # Bi-weekly (24 pay periods)
    "month": 12,  # 12 months per year
    "year": 1,  # Already annual
}

# Data validation constants
MIN_WAGE = 10000
MAX_WAGE = 10000000
MIN_ROWS = 100
