import streamlit as st
import plotly.graph_objects as go


def show_top_jobs(df):
    """Display top job titles analysis"""
    st.subheader("👨‍💼 Top Job Titles")

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
