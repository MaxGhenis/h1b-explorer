import streamlit as st
from utils import get_soc_title


def setup_page():
    """Configure initial page settings"""
    # Hide default menu items
    st.set_page_config(
        page_title="H-1B Visa Analysis Dashboard",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("H-1B Visa Analysis Dashboard")
    st.caption(
        "Analysis of Labor Condition Applications (LCA) from July-September 2024"
    )

    with st.expander("ℹ️ About DOL Certification"):
        st.info(
            "This data shows Labor Condition Applications certified by the Department of Labor (DOL), "
            "which verifies wage requirements. Final H-1B approval requires additional Department of "
            "Homeland Security verification of job qualifications and eligibility criteria."
        )


def setup_sidebar(df):
    """Setup sidebar filters and return filtered dataframe"""
    st.sidebar.header("Filters")

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

    # Apply and show filters
    filtered_df = apply_filters(df, selected_soc, selected_state, wage_range)

    with st.sidebar.expander("📋 Active Filters"):
        st.write("SOC Code:", selected_soc)
        st.write("State:", selected_state)
        st.write("Wage Range: ${:,.0f} - ${:,.0f}".format(wage_range[0], wage_range[1]))
        st.write("Filtered Records: {:,}".format(len(filtered_df)))

    # About section at the bottom
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        **About**\n
        Data source: [DOL LCA Disclosure Data FY2024 Q4](https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2024_Q1.xlsx)\n
        Creators: [Max Ghenis](https://maxghenis.com) and [Sam Peak](https://x.com/SpeakSamuel)\n
        Source code: [GitHub](https://github.com/maxghenis/h1b-explorer)
    """
    )

    return filtered_df


def apply_filters(df, selected_soc, selected_state, wage_range):
    """Apply selected filters to dataframe"""
    filtered_df = df.copy()

    if selected_soc != "All":
        filtered_df = filtered_df[filtered_df["SOC_CODE"] == selected_soc]
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df["WORKSITE_STATE"] == selected_state]

    filtered_df = filtered_df[
        (filtered_df["ANNUAL_WAGE"] >= wage_range[0])
        & (filtered_df["ANNUAL_WAGE"] <= wage_range[1])
    ]

    return filtered_df
