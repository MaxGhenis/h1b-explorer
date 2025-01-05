import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def plot_wage_distribution(df):
    """Create wage distribution plot"""
    fig = go.Figure()

    # Add actual wage CDF
    sorted_actual = np.sort(df["ANNUAL_WAGE"].dropna())
    yvals = np.arange(1, len(sorted_actual) + 1) / len(sorted_actual)
    fig.add_trace(
        go.Scatter(
            x=sorted_actual, y=yvals, name="Actual Wage", line=dict(color="blue")
        )
    )

    # Add prevailing wage CDF
    sorted_prev = np.sort(df["ANNUAL_PREVAILING_WAGE"].dropna())
    yvals_prev = np.arange(1, len(sorted_prev) + 1) / len(sorted_prev)
    fig.add_trace(
        go.Scatter(
            x=sorted_prev, y=yvals_prev, name="Prevailing Wage", line=dict(color="red")
        )
    )

    fig.update_layout(
        title="Cumulative Distribution of Wages",
        xaxis_title="Annual Wage ($)",
        yaxis_title="Cumulative Probability",
        height=500,
    )

    return fig


def plot_top_employers(df):
    """Create top employers plot"""
    top_employers = df["EMPLOYER_NAME"].value_counts().head(10)

    fig = go.Figure(
        data=[
            go.Bar(
                x=top_employers.index,
                y=top_employers.values,
                text=top_employers.values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Top 10 Employers",
        xaxis_title="Employer",
        yaxis_title="Number of Applications",
        xaxis_tickangle=45,
        height=500,
    )

    return fig


def plot_employer_wages(df):
    """Create employer wages plot"""
    top_employers = df["EMPLOYER_NAME"].value_counts().head(10).index
    employer_wages = (
        df[df["EMPLOYER_NAME"].isin(top_employers)]
        .groupby("EMPLOYER_NAME")
        .agg({"ANNUAL_WAGE": "mean", "ANNUAL_PREVAILING_WAGE": "mean"})
        .sort_values("ANNUAL_WAGE")
    )

    fig = go.Figure()

    # Add actual wages
    fig.add_trace(
        go.Bar(
            y=employer_wages.index,
            x=employer_wages["ANNUAL_WAGE"],
            name="Actual Wage",
            orientation="h",
            text=[f"${x:,.0f}" for x in employer_wages["ANNUAL_WAGE"]],
            textposition="auto",
        )
    )

    # Add prevailing wages
    fig.add_trace(
        go.Bar(
            y=employer_wages.index,
            x=employer_wages["ANNUAL_PREVAILING_WAGE"],
            name="Prevailing Wage",
            orientation="h",
            text=[f"${x:,.0f}" for x in employer_wages["ANNUAL_PREVAILING_WAGE"]],
            textposition="auto",
        )
    )

    fig.update_layout(
        barmode="group",
        title="Average Wages by Top Employers",
        xaxis_title="Annual Wage ($)",
        yaxis_title="Employer",
        height=500,
    )

    return fig


def plot_wage_ratio_distribution(df):
    """Create wage ratio distribution plot"""
    fig = px.histogram(
        df,
        x="WAGE_RATIO",
        nbins=50,
        title="Distribution of Actual/Prevailing Wage Ratio",
        labels={"WAGE_RATIO": "Actual Wage / Prevailing Wage"},
    )

    fig.update_layout(showlegend=False, height=400)

    return fig
