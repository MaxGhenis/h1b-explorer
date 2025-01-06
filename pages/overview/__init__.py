from .wage_analysis import show_wage_analysis
from .metrics import show_key_metrics
from .job_analysis import show_top_jobs


def show_overview(df):
    """Display overview page content"""
    # Key metrics section
    show_key_metrics(df)

    # Wage analysis section
    show_wage_analysis(df)

    # Top job titles section
    show_top_jobs(df)


__all__ = ["show_overview"]
