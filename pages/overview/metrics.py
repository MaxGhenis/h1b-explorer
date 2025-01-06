import streamlit as st


def show_key_metrics(df):
    """Display key metrics in columns"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total DOL Certifications",
            f"{len(df):,}",
            help="Number of Labor Condition Applications (LCAs) certified by the Department of Labor",
        )

    with col2:
        st.metric(
            "Unique Employers",
            f"{df['EMPLOYER_NAME'].nunique():,}",
            help="Number of unique employers submitting certified LCAs",
        )

    with col3:
        st.metric(
            "Median Annual Wage",
            f"${df['ANNUAL_WAGE'].median():,.0f}",
            help="Median annual wage across all certified applications",
        )
