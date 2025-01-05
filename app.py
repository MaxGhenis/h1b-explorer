import streamlit as st
import pandas as pd
from utils.data_utils import load_data
from utils.visualizations import (
    plot_wage_distribution,
    plot_top_employers,
    plot_employer_wages,
    plot_wage_ratio_distribution,
)


def main():
    st.title("H1B LCA Wage Analysis Dashboard")

    # Load the data
    df = load_data()

    if df is not None:
        # Add a data refresh button
        if st.button("Refresh Data"):
            st.cache_data.clear()
            df = load_data()
            st.rerun()

        # SOC code filter
        st.sidebar.header("Filters")
        soc_codes = sorted(df["SOC_CODE"].unique())
        selected_soc = st.sidebar.selectbox(
            "Filter by SOC Code", ["All"] + list(soc_codes)
        )

        # Apply filter
        if selected_soc != "All":
            df = df[df["SOC_CODE"] == selected_soc]
            st.subheader(f"Showing data for SOC Code: {selected_soc}")

        # Calculate statistics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Actual Wage", f"${df['ANNUAL_WAGE'].mean():,.2f}")
            st.metric("Median Actual Wage", f"${df['ANNUAL_WAGE'].median():,.2f}")

        with col2:
            st.metric(
                "Average Prevailing Wage",
                f"${df['ANNUAL_PREVAILING_WAGE'].mean():,.2f}",
            )
            st.metric(
                "Median Prevailing Wage",
                f"${df['ANNUAL_PREVAILING_WAGE'].median():,.2f}",
            )

        # Calculate percentage above prevailing wage
        above_prevailing = (
            df["ANNUAL_WAGE"] > df["ANNUAL_PREVAILING_WAGE"]
        ).mean() * 100
        st.metric(
            "Percentage of Jobs Above Prevailing Wage", f"{above_prevailing:.1f}%"
        )

        # Show wage distributions
        st.subheader("Wage Distributions")
        st.plotly_chart(plot_wage_distribution(df))

        # Show wage ratio distribution
        st.plotly_chart(plot_wage_ratio_distribution(df))

        # Show employer analysis
        st.subheader("Employer Analysis")
        st.plotly_chart(plot_top_employers(df))
        st.plotly_chart(plot_employer_wages(df))

        # Additional Statistics
        st.subheader("Additional Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Wage Percentiles:")
            percentiles = df["ANNUAL_WAGE"].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
            for p, v in percentiles.items():
                st.write(f"{int(p*100)}th percentile: ${v:,.2f}")

        with col2:
            st.write("Sample Size:")
            st.write(f"Total number of cases: {len(df):,}")
            st.write(f"Number of unique employers: {df['EMPLOYER_NAME'].nunique():,}")


if __name__ == "__main__":
    main()
