import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show_top_states_table(df):
    """Display table of top states"""
    state_stats = calculate_state_stats(df)
    fig = create_state_table(state_stats)
    st.plotly_chart(fig, use_container_width=True)


def calculate_state_stats(df):
    """Calculate statistics for each state"""
    state_stats = df.groupby("WORKSITE_STATE").size().reset_index()
    state_stats.columns = ["State", "Certifications"]

    # Calculate percentage of total
    total_certs = state_stats["Certifications"].sum()
    state_stats["Share"] = state_stats["Certifications"] / total_certs * 100

    # Sort and get top 10
    return state_stats.sort_values("Certifications", ascending=False).head(10)


def create_state_table(state_stats):
    """Create formatted table of state statistics"""
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=["State", "Certifications", "Share of Total"],
                    align="left",
                    font=dict(size=12),
                ),
                cells=dict(
                    values=[
                        state_stats["State"],
                        state_stats["Certifications"].apply(lambda x: f"{x:,}"),
                        state_stats["Share"].apply(lambda x: f"{x:.1f}%"),
                    ],
                    align="left",
                    font=dict(size=11),
                ),
            )
        ]
    )

    fig.update_layout(title="Top 10 States by Number of Certifications", height=400)

    return fig
