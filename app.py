import streamlit as st
import pandas as pd
from utils.data_utils import load_data
from utils.visualizations import (
    plot_wage_distribution,
    create_employer_table,
    plot_wage_ratio_distribution,
)


def main():
    st.title("H1B Visa Wage Analysis Dashboard")

    # Sidebar information
    st.sidebar.header("About")
    st.sidebar.markdown(
        """
    This dashboard analyzes H1B visa application data from July-September 2024.
    
    Data source: [DOL LCA Disclosure Data FY2024 Q4](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2024_Q1.xlsx)
    
    Created by [Max Ghenis](https://maxghenis.com) and [Sam Peak](https://x.com/SpeakSamuel)
    """
    )

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

        # Apply filter and get total count
        total_count = len(df)
        if selected_soc != "All":
            df = df[df["SOC_CODE"] == selected_soc]
            st.subheader(f"Showing data for SOC Code: {selected_soc}")

        # Display total count
        st.metric("Number of Certified Full-time H1Bs", f"{len(df):,}")

        # Calculate statistics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Actual Wage", f"${df['ANNUAL_WAGE'].mean():,.0f}")
            st.metric("Median Actual Wage", f"${df['ANNUAL_WAGE'].median():,.0f}")

        with col2:
            st.metric(
                "Average Prevailing Wage",
                f"${df['ANNUAL_PREVAILING_WAGE'].mean():,.0f}",
            )
            st.metric(
                "Median Prevailing Wage",
                f"${df['ANNUAL_PREVAILING_WAGE'].median():,.0f}",
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
        st.plotly_chart(create_employer_table(df))

        # Additional Statistics
        st.subheader("Additional Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Wage Percentiles:")
            percentiles = df["ANNUAL_WAGE"].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
            for p, v in percentiles.items():
                st.write(f"{int(p*100)}th percentile: ${v:,.0f}")

        with col2:
            st.write("Sample Size:")
            st.write(f"Total number of cases: {len(df):,}")
            st.write(f"Number of unique employers: {df['EMPLOYER_NAME'].nunique():,}")


if __name__ == "__main__":
    main()
