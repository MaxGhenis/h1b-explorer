import streamlit as st
import pandas as pd


def show_detailed_stats(df):
    """Display detailed statistics by state"""
    # Calculate comprehensive statistics
    state_stats = calculate_detailed_stats(df)

    # Display as interactive table
    st.dataframe(
        state_stats.style.format(
            {
                "Certifications": "{:,}",
                "Mean Wage": "${:,.0f}",
                "Median Wage": "${:,.0f}",
                "Wage Std Dev": "${:,.0f}",
                "Wage Ratio": "{:.2f}",
                "Unique Employers": "{:,}",
            }
        ),
        hide_index=True,
    )


def calculate_detailed_stats(df):
    """Calculate detailed statistics for each state"""
    state_stats = (
        df.groupby("WORKSITE_STATE")
        .agg(
            {
                "ANNUAL_WAGE": ["count", "mean", "median", "std"],
                "WAGE_RATIO": "mean",
                "EMPLOYER_NAME": "nunique",
            }
        )
        .round(2)
    )

    state_stats.columns = [
        "Certifications",
        "Mean Wage",
        "Median Wage",
        "Wage Std Dev",
        "Wage Ratio",
        "Unique Employers",
    ]

    # Reset index and sort by number of certifications
    return state_stats.reset_index().sort_values("Certifications", ascending=False)
