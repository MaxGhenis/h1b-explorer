import streamlit as st


def show_key_metrics(df):
    """Display key metrics in columns"""
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
