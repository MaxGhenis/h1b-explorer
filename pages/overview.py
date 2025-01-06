import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def show_overview(df):
    """Display overview page content"""
    # Key metrics in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Total H-1B Certifications",
            f"{len(df):,}",
            help="Number of certified full-time H-1B certifications",
        )
    with col2:
        st.metric(
            "Unique Employers",
            f"{df['EMPLOYER_NAME'].nunique():,}",
            help="Number of unique employers in the dataset",
        )
    with col3:
        st.metric(
            "Median Annual Wage",
            f"${df['ANNUAL_WAGE'].median():,.0f}",
            help="Median annual wage across all certifications",
        )

    # Wage statistics
    st.subheader("💰 Wage Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Average Actual Wage", f"${df['ANNUAL_WAGE'].mean():,.0f}")
        st.metric("Median Actual Wage", f"${df['ANNUAL_WAGE'].median():,.0f}")

    with col2:
        st.metric(
            "Average Prevailing Wage", f"${df['ANNUAL_PREVAILING_WAGE'].mean():,.0f}"
        )
        st.metric(
            "Median Prevailing Wage", f"${df['ANNUAL_PREVAILING_WAGE'].median():,.0f}"
        )

        above_prevailing = (
            df["ANNUAL_WAGE"] > df["ANNUAL_PREVAILING_WAGE"]
        ).mean() * 100
        st.metric("% Above Prevailing Wage", f"{above_prevailing:.1f}%")

    # Wage distribution plots
    st.subheader("📈 Wage Distributions")
    tab1, tab2 = st.tabs(["Distribution Plot", "Box Plot"])

    with tab1:
        st.plotly_chart(plot_wage_distribution(df), use_container_width=True)

    with tab2:
        st.plotly_chart(plot_wage_box(df), use_container_width=True)

    # Top job titles
    st.subheader("👨‍💼 Top Job Titles")
    show_top_jobs(df)


def plot_wage_distribution(df):
    """Create enhanced wage distribution plot"""
    fig = go.Figure()

    # Add actual wage distribution
    fig.add_trace(
        go.Violin(
            x=df["ANNUAL_WAGE"],
            name="Actual Wage",
            side="positive",
            line_color="blue",
            fillcolor="lightblue",
            opacity=0.6,
        )
    )

    # Add prevailing wage distribution
    fig.add_trace(
        go.Violin(
            x=df["ANNUAL_PREVAILING_WAGE"],
            name="Prevailing Wage",
            side="negative",
            line_color="gray",
            fillcolor="lightgray",
            opacity=0.6,
        )
    )

    fig.update_layout(
        title="Distribution of Actual vs Prevailing Wages",
        xaxis_title="Annual Wage ($)",
        xaxis=dict(tickformat="$,.0f"),
        showlegend=True,
        violinmode="overlay",
        height=500,
    )

    return fig


def plot_wage_box(df):
    """Create box plot of wages"""
    fig = go.Figure()

    fig.add_trace(
        go.Box(
            y=df["ANNUAL_WAGE"],
            name="Actual Wage",
            boxpoints="all",
            marker_color="blue",
        )
    )

    fig.add_trace(
        go.Box(
            y=df["ANNUAL_PREVAILING_WAGE"],
            name="Prevailing Wage",
            boxpoints="all",
            marker_color="gray",
        )
    )

    fig.update_layout(
        title="Box Plot of Wage Distribution",
        yaxis_title="Annual Wage ($)",
        yaxis=dict(tickformat="$,.0f"),
        height=500,
    )

    return fig


def show_top_jobs(df):
    """Display top job titles analysis"""
    job_stats = (
        df.groupby("JOB_TITLE")
        .agg({"ANNUAL_WAGE": ["count", "mean", "median"]})
        .reset_index()
    )

    job_stats.columns = ["Job Title", "Count", "Mean Wage", "Median Wage"]
    job_stats = job_stats.sort_values("Count", ascending=True).tail(10)

    fig = go.Figure(
        data=[
            go.Bar(
                y=job_stats["Job Title"],
                x=job_stats["Count"],
                text=job_stats["Count"].apply(lambda x: f"{x:,}"),
                textposition="auto",
                orientation="h",
            )
        ]
    )

    fig.update_layout(
        title="Top 10 Job Titles by Number of Certifications",
        yaxis_title="Job Title",
        xaxis_title="Number of Certifications",
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View Detailed Job Title Statistics"):
        st.dataframe(
            job_stats.style.format(
                {"Count": "{:,.0f}", "Mean Wage": "${:,.0f}", "Median Wage": "${:,.0f}"}
            ),
            hide_index=True,
        )
