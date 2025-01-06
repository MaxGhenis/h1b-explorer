import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def calculate_employer_stats(df):
    """Calculate statistics for top employers"""
    employer_stats = (
        df.groupby("EMPLOYER_NAME")
        .agg(
            {
                "ANNUAL_WAGE": ["count", "mean", "median", "std"],
                "WAGE_RATIO": "mean",
                "WORKSITE_STATE": lambda x: x.mode()[0],
                "SOC_CODE": lambda x: x.mode()[0],
            }
        )
        .reset_index()
    )

    employer_stats.columns = [
        "Employer",
        "Certifications",
        "Mean Wage",
        "Median Wage",
        "Wage Std Dev",
        "Avg Wage Ratio",
        "Primary State",
        "Primary SOC",
    ]

    employer_stats = employer_stats.sort_values("Certifications", ascending=False).head(
        15
    )
    total_certs = employer_stats["Certifications"].sum()
    employer_stats["Market Share"] = (
        employer_stats["Certifications"] / total_certs * 100
    )
    return employer_stats


def create_employer_table(employer_stats):
    """Create formatted table visualization"""
    table_data = go.Table(
        header=dict(
            values=[
                "Employer",
                "Certifications",
                "Market Share",
                "Mean Annual Wage",
                "Median Annual Wage",
                "Wage Ratio",
                "Primary State",
            ],
            align="left",
            font=dict(size=12),
        ),
        cells=dict(
            values=[
                employer_stats["Employer"],
                employer_stats["Certifications"].apply(lambda x: f"{x:,}"),
                employer_stats["Market Share"].apply(lambda x: f"{x:.1f}%"),
                employer_stats["Mean Wage"].apply(lambda x: f"${x:,.0f}"),
                employer_stats["Median Wage"].apply(lambda x: f"${x:,.0f}"),
                employer_stats["Avg Wage Ratio"].apply(lambda x: f"{x:.2f}"),
                employer_stats["Primary State"],
            ],
            align="left",
            font=dict(size=11),
        ),
    )

    fig = go.Figure(data=[table_data])
    fig.update_layout(title="Top 15 Employers by Number of Certifications", height=500)
    return fig


def show_detailed_stats(df, employer_stats):
    """Show detailed statistics in expandable section"""
    with st.expander("View Additional Statistics"):
        top_5_employers = employer_stats["Employer"].head().tolist()
        fig = go.Figure()

        for employer in top_5_employers:
            employer_data = df[df["EMPLOYER_NAME"] == employer]
            fig.add_trace(
                go.Box(y=employer_data["ANNUAL_WAGE"], name=employer, boxpoints="all")
            )

        fig.update_layout(
            title="Wage Distribution for Top 5 Employers",
            yaxis_title="Annual Wage ($)",
            yaxis=dict(tickformat="$,.0f"),
            height=400,
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)


def show_top_employers_table(df):
    """Display enhanced top employers table"""
    employer_stats = calculate_employer_stats(df)
    fig = create_employer_table(employer_stats)
    st.plotly_chart(fig, use_container_width=True)
    show_detailed_stats(df, employer_stats)
