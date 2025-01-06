import streamlit as st
from . import maps, tables, metrics


def show_geographic_analysis(df):
    """Display geographic analysis page content"""
    st.subheader("🗺️ Geographic Analysis")

    # Overview metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "States with H-1B Certifications",
            f"{df['WORKSITE_STATE'].nunique()}",
            help="Number of states with at least one H-1B certification",
        )
    with col2:
        top_state = df["WORKSITE_STATE"].mode()[0]
        top_state_pct = len(df[df["WORKSITE_STATE"] == top_state]) / len(df) * 100
        st.metric(
            "Top State",
            f"{top_state} ({top_state_pct:.1f}%)",
            help="State with the most H-1B certifications",
        )

    # State-level analysis tabs
    tab1, tab2, tab3 = st.tabs(
        ["Certifications by State", "Wage Analysis", "Detailed Statistics"]
    )

    with tab1:
        maps.show_certification_map(df)
        tables.show_top_states_table(df)

    with tab2:
        maps.show_wage_map(df)
        maps.show_wage_boxplot(df)

    with tab3:
        metrics.show_detailed_stats(df)
