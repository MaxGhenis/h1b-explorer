import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show_certification_map(df):
    """Display choropleth map of certifications by state"""
    state_stats = df.groupby("WORKSITE_STATE").size().reset_index()
    state_stats.columns = [
        "WORKSITE_STATE",
        "Certifications",
    ]  # Changed from State to WORKSITE_STATE

    fig = create_choropleth(
        state_stats,
        "Certifications",
        "Number of H-1B Certifications by State",
        "Certifications",
        "blues",
    )

    st.plotly_chart(fig, use_container_width=True)


def show_wage_map(df):
    """Display choropleth map of median wages by state"""
    state_wages = (
        df.groupby("WORKSITE_STATE").agg({"ANNUAL_WAGE": "median"}).reset_index()
    )

    fig = create_choropleth(
        state_wages,
        "ANNUAL_WAGE",
        "Median H-1B Wages by State",
        "Median Wage ($)",
        "blues",
        number_format="$,.0f",
    )

    st.plotly_chart(fig, use_container_width=True)


def create_choropleth(
    df, value_col, title, colorbar_title, colorscale, number_format=",d"
):
    """Create a choropleth map"""
    fig = go.Figure(
        data=go.Choropleth(
            locations=df["WORKSITE_STATE"],  # Changed from State to WORKSITE_STATE
            z=df[value_col],
            locationmode="USA-states",
            colorscale=colorscale,
            colorbar_title=colorbar_title,
            colorbar=dict(tickformat=number_format),
        )
    )

    fig.update_layout(title=title, geo_scope="usa", height=600)
    return fig


def show_wage_boxplot(df):
    """Display wage box plot for top states"""
    # Get top 10 states by number of certifications
    top_states = df["WORKSITE_STATE"].value_counts().head(10).index

    fig = go.Figure()
    for state in top_states:
        state_data = df[df["WORKSITE_STATE"] == state]
        fig.add_trace(
            go.Box(
                y=state_data["ANNUAL_WAGE"],
                name=state,
                boxpoints=False,  # Removed all points
            )
        )

    fig.update_layout(
        title="Wage Distribution in Top 10 States",
        yaxis_title="Annual Wage ($)",
        yaxis=dict(tickformat="$,.0f"),
        height=500,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)
