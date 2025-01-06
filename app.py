import streamlit as st
from pages import show_overview
from pages.employer_analysis.main import show_employer_analysis
from pages.geographic_analysis.main import show_geographic_analysis
from utils import load_data, get_soc_title

st.set_page_config(
    page_title="H-1B Visa Analysis Dashboard",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    st.title("🌎 H-1B Visa Analysis Dashboard")
    st.caption(
        "Analysis of Labor Condition Applications (LCA) from July-September 2024"
    )

    # Sidebar information
    st.sidebar.header("About")
    st.sidebar.markdown(
        """
        Data source: [DOL LCA Disclosure Data FY2024 Q4](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2024_Q1.xlsx)
        
        Created by [Max Ghenis](https://maxghenis.com) and [Sam Peak](https://x.com/SpeakSamuel)
        """
    )

    # Load the data
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    if df is not None:
        # Filters in sidebar
        st.sidebar.header("🔍 Filters")

        # SOC code filter
        soc_codes = sorted(df["SOC_CODE"].unique())
        selected_soc = st.sidebar.selectbox(
            "Filter by SOC Code",
            ["All"] + list(soc_codes),
            format_func=lambda x: (
                f"{x} - {get_soc_title(df, x)}" if x != "All" else "All"
            ),
        )

        # State filter
        states = sorted(df["WORKSITE_STATE"].unique())
        selected_state = st.sidebar.selectbox("Filter by State", ["All"] + list(states))

        # Wage range filter
        wage_min = float(df["ANNUAL_WAGE"].min())
        wage_max = float(df["ANNUAL_WAGE"].max())
        wage_range = st.sidebar.slider(
            "Annual Wage Range ($)",
            min_value=wage_min,
            max_value=wage_max,
            value=(wage_min, wage_max),
            format="$%d",
        )

        # Apply filters
        filtered_df = df.copy()
        if selected_soc != "All":
            filtered_df = filtered_df[filtered_df["SOC_CODE"] == selected_soc]
        if selected_state != "All":
            filtered_df = filtered_df[filtered_df["WORKSITE_STATE"] == selected_state]
        filtered_df = filtered_df[
            (filtered_df["ANNUAL_WAGE"] >= wage_range[0])
            & (filtered_df["ANNUAL_WAGE"] <= wage_range[1])
        ]

        # Show filters applied
        with st.sidebar.expander("🔍 Active Filters"):
            st.write("SOC Code:", selected_soc)
            st.write("State:", selected_state)
            st.write(
                "Wage Range: \\${:,.0f} - \\${:,.0f}".format(
                    wage_range[0], wage_range[1]
                )
            )
            st.write("Filtered Records: {:,}".format(len(filtered_df)))

        # Navigation
        page = st.sidebar.radio(
            "📊 Navigation", ["Overview", "Employer Analysis", "Geographic Analysis"]
        )

        # Show selected page
        if page == "Overview":
            show_overview(filtered_df)
        elif page == "Employer Analysis":
            show_employer_analysis(filtered_df)
        else:
            show_geographic_analysis(filtered_df)

    else:
        st.error(
            "Failed to load data. Please check your internet connection and try again."
        )


if __name__ == "__main__":
    main()
