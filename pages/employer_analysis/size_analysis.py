import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show_employer_size_distribution(df):
    """Display employer size distribution analysis"""
    employer_sizes = df.groupby("EMPLOYER_NAME").size().reset_index()
    employer_sizes.columns = ["Employer", "Size"]

    size_bins = [0, 10, 50, 100, 500, float("inf")]
    size_labels = ["1-10", "11-50", "51-100", "101-500", "500+"]
    employer_sizes["Size Category"] = pd.cut(
        employer_sizes["Size"], bins=size_bins, labels=size_labels, right=False
    )

    size_distribution = employer_sizes["Size Category"].value_counts().sort_index()

    fig = go.Figure(
        data=[
            go.Bar(
                x=size_distribution.index,
                y=size_distribution.values,
                text=size_distribution.values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Distribution of Employers by Size Category",
        xaxis_title="Number of Certifications",
        yaxis_title="Number of Employers",
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

    cols = st.columns(len(size_labels))
    total_employers = len(employer_sizes)

    for i, (label, count) in enumerate(size_distribution.items()):
        with cols[i]:
            percentage = (count / total_employers) * 100
            st.metric(
                label,
                f"{count:,}",
                f"{percentage:.1f}%",
                help=f"Number of employers with {label} certifications",
            )
