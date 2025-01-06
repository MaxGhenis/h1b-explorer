import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show_wage_size_stats(df):
    """Show detailed wage statistics by employer size"""
    wage_stats = (
        df.groupby("Size Category")
        .agg({"ANNUAL_WAGE": ["mean", "median", "std", "count"], "WAGE_RATIO": "mean"})
        .round(2)
    )

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

    correlation = df[["Employer Size", "ANNUAL_WAGE"]].corr().iloc[0, 1]
    st.write(f"Correlation between employer size and wages: {correlation:.3f}")


def show_wage_by_employer_size(df):
    """Display wage analysis by employer size"""
    employer_sizes = df.groupby("EMPLOYER_NAME").size()
    df = df.copy()  # Create a copy to avoid modifying the original
    df["Employer Size"] = df["EMPLOYER_NAME"].map(employer_sizes)

    size_bins = [0, 10, 50, 100, 500, float("inf")]
    size_labels = ["1-10", "11-50", "51-100", "101-500", "500+"]
    df["Size Category"] = pd.cut(
        df["Employer Size"], bins=size_bins, labels=size_labels, right=False
    )

    fig = go.Figure()
    for category in sorted(df["Size Category"].unique()):
        subset = df[df["Size Category"] == category]
        fig.add_trace(go.Box(y=subset["ANNUAL_WAGE"], name=category, boxpoints="all"))

    fig.update_layout(
        title="Annual Wage Distribution by Employer Size",
        yaxis_title="Annual Wage ($)",
        yaxis=dict(tickformat="$,.0f"),
        height=500,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
    show_wage_size_stats(df)
