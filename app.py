import streamlit as st
from app_layout import setup_page, setup_sidebar
from pages.overview import show_overview
from pages.employer_analysis import show_employer_analysis
from pages.geographic_analysis import show_geographic_analysis
from utils import load_data


def main():
    setup_page()

    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    if df is not None:
        # Setup sidebar and get filtered dataframe
        filtered_df = setup_sidebar(df)

        # Create tabs
        tab1, tab2, tab3 = st.tabs(
            ["Overview", "Employer Analysis", "Geographic Analysis"]
        )

        # Show content based on selected tab
        with tab1:
            show_overview(filtered_df)
        with tab2:
            show_employer_analysis(filtered_df)
        with tab3:
            show_geographic_analysis(filtered_df)

    else:
        st.error(
            "Failed to load data. Please check your internet connection and try again."
        )


if __name__ == "__main__":
    main()
