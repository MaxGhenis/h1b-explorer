import streamlit as st
import plotly.graph_objects as go


def show_wage_analysis(df):
    """Display wage analysis section"""
    st.subheader("💰 Wage Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Average Actual Wage", f"${df['ANNUAL_WAGE'].mean():,.0f}")
        st.metric("Median Actual Wage", f"${df['ANNUAL_WAGE'].median():,.0f}")

    with col2:
        st.metric(
            "Average Prevailing Wage", f"${df['ANNUAL_PREVAILING_WAGE'].mean():,.0f}"
        )
        st.metric(
            "Median Prevailing Wage", f"${df['ANNUAL_PREVAILING_WAGE'].median():,.0f}"
        )

        above_prevailing = (
            df["ANNUAL_WAGE"] > df["ANNUAL_PREVAILING_WAGE"]
        ).mean() * 100
        st.metric("% Above Prevailing Wage", f"{above_prevailing:.1f}%")

    st.plotly_chart(plot_wage_distribution(df), use_container_width=True)


def plot_wage_distribution(df):
    """Create wage distribution plot"""
    actual = df["ANNUAL_WAGE"].sort_values()
    prevailing = df["ANNUAL_PREVAILING_WAGE"].sort_values()
    n = len(df)
    percentiles = [i / (n - 1) for i in range(n)]

    fig = go.Figure()

    # Add actual wage CDF (blue line)
    fig.add_trace(
        go.Scatter(
            x=actual,
            y=percentiles,
            name="Actual Wage",
            line=dict(color="rgb(0, 0, 255)"),
            customdata=prevailing,
            hovertemplate=(
                "%{y:.0%} of actual wages are less than $%{x:,.0f}.<br>"
                + "%{y:.0%} of prevailing wages are less than $%{customdata:,.0f}"
                + "<extra></extra>"
            ),
        )
    )

    # Add prevailing wage CDF (gray line)
    fig.add_trace(
        go.Scatter(
            x=prevailing,
            y=percentiles,
            name="Prevailing Wage",
            line=dict(color="rgb(128, 128, 128)"),
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        title="Cumulative Distribution of Wages",
        xaxis_title="Annual Wage ($)",
        yaxis_title="Cumulative Probability",
        xaxis=dict(
            tickformat="$,",
            gridcolor="rgb(220, 220, 220)",
            gridwidth=1,
            showgrid=True,
            range=[0, 600000],
            dtick=200000,
        ),
        yaxis=dict(
            tickformat=".0%",
            gridcolor="rgb(220, 220, 220)",
            gridwidth=1,
            showgrid=True,
            dtick=0.2,
        ),
        height=500,
        showlegend=True,
        hoverlabel=dict(bgcolor="white"),
        plot_bgcolor="white",
        legend=dict(yanchor="bottom", y=1.02, xanchor="center", x=0.5, orientation="h"),
    )

    return fig
