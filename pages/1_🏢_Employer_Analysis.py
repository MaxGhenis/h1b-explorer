import streamlit as st
from employer_analysis import show_employer_analysis
from app_layout import setup_page, setup_sidebar
from utils import load_data

setup_page()
df = load_data()

if df is not None:
    filtered_df = setup_sidebar(df)
    show_employer_analysis(filtered_df)
