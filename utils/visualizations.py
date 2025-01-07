import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def plot_wage_distribution(df):
    """Create wage distribution plot"""
    fig = go.Figure()

    # Add offered wage CDF
    sorted_actual = np.sort(df["ANNUAL_WAGE"].dropna())
    yvals = np.arange(1, len(sorted_actual) + 1) / len(sorted_actual)
    fig.add_trace(
        go.Scatter(
            x=sorted_actual,
            y=yvals,
            name="Offered Wage",
            line=dict(color="rgb(0, 0, 255)"),  # Blue
        )
    )

    # Add prevailing wage CDF
    sorted_prev = np.sort(df["ANNUAL_PREVAILING_WAGE"].dropna())
    yvals_prev = np.arange(1, len(sorted_prev) + 1) / len(sorted_prev)
    fig.add_trace(
        go.Scatter(
            x=sorted_prev,
            y=yvals_prev,
            name="Prevailing Wage",
            line=dict(color="rgb(128, 128, 128)"),  # Gray
        )
    )

    fig.update_layout(
        title="Cumulative Distribution of Wages",
        xaxis_title="Annual Wage ($)",
        yaxis_title="Cumulative Probability",
        height=500,
        xaxis=dict(tickformat="$,.0f"),  # Format x-axis ticks as dollars
    )

    return fig


def create_employer_table(df):
    """Create employer statistics table"""
    employer_stats = (
        df.groupby("EMPLOYER_NAME")
        .agg({"ANNUAL_WAGE": ["count", "mean", "median"]})
        .reset_index()
    )

    employer_stats.columns = ["Employer", "Number of H1Bs", "Mean Wage", "Median Wage"]
    employer_stats = employer_stats.sort_values("Number of H1Bs", ascending=False).head(
        10
    )

    # Round wage columns to nearest dollar
    employer_stats["Mean Wage"] = employer_stats["Mean Wage"].round(0)
    employer_stats["Median Wage"] = employer_stats["Median Wage"].round(0)

    # Format table data
    table_data = go.Table(
        header=dict(
            values=[
                "Employer",
                "Number of H1Bs",
                "Mean Annual Wage",
                "Median Annual Wage",
            ],
            align="left",
            font=dict(size=12),
        ),
        cells=dict(
            values=[
                employer_stats["Employer"],
                employer_stats["Number of H1Bs"].apply(lambda x: f"{x:,}"),
                employer_stats["Mean Wage"].apply(lambda x: f"${x:,.0f}"),
                employer_stats["Median Wage"].apply(lambda x: f"${x:,.0f}"),
            ],
            align="left",
            font=dict(size=11),
        ),
    )

    fig = go.Figure(data=[table_data])
    fig.update_layout(title="Top 10 Employers by Number of Certified H1Bs", height=400)

    return fig


def plot_wage_ratio_distribution(df):
    """Create wage ratio distribution plot"""
    fig = px.histogram(
        df,
        x="WAGE_RATIO",
        nbins=50,
        title="Distribution of Actual/Prevailing Wage Ratio",
        labels={"WAGE_RATIO": "Offered Wage / Prevailing Wage"},
    )

    fig.update_layout(
        showlegend=False,
        height=400,
        xaxis=dict(tickformat=".2f"),  # Format x-axis ticks to 2 decimal places
    )

    return fig
