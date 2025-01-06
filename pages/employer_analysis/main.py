import streamlit as st
from .size_analysis import show_employer_size_distribution
from .wage_analysis import show_wage_by_employer_size
from .top_employers import show_top_employers_table


def show_employer_analysis(df):
    """Display employer analysis page content"""
    st.subheader("🏢 Employer Analysis")

    # Overview metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Employers",
            f"{df['EMPLOYER_NAME'].nunique():,}",
            help="Number of unique employers",
        )

    with col2:
        top_10_share = df["EMPLOYER_NAME"].value_counts().head(10).sum() / len(df) * 100
        st.metric(
            "Top 10 Employers Share",
            f"{top_10_share:.1f}%",
            help="Percentage of certifications from top 10 employers",
        )

    with col3:
        median_certs = df["EMPLOYER_NAME"].value_counts().median()
        st.metric(
            "Median Certifications per Employer",
            f"{median_certs:.0f}",
            help="Median number of certifications per employer",
        )

    # Employer Analysis Tabs
    tab1, tab2, tab3 = st.tabs(["Top Employers", "Size Distribution", "Wage Analysis"])

    with tab1:
        show_top_employers_table(df)

    with tab2:
        show_employer_size_distribution(df)

    with tab3:
        show_wage_by_employer_size(df)
