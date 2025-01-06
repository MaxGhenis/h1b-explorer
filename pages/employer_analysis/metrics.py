import pandas as pd


def show_wage_size_stats(df):
    """Show detailed wage statistics by employer size"""
    wage_stats = (
        df.groupby("Size Category")
        .agg({"ANNUAL_WAGE": ["mean", "median", "std", "count"], "WAGE_RATIO": "mean"})
        .round(2)
    )

    # Rename columns for better display
    wage_stats.columns = [
        "Mean Wage",
        "Median Wage",
        "Wage Std Dev",
        "Number of Certifications",
        "Average Wage Ratio",
    ]

    st.dataframe(
        wage_stats.style.format(
            {
                "Mean Wage": "${:,.0f}",
                "Median Wage": "${:,.0f}",
                "Wage Std Dev": "${:,.0f}",
                "Number of Certifications": "{:,}",
                "Average Wage Ratio": "{:.2f}",
            }
        )
    )

    # Add correlation analysis
    correlation = df[["Employer Size", "ANNUAL_WAGE"]].corr().iloc[0, 1]
    st.write(f"Correlation between employer size and wages: {correlation:.3f}")
