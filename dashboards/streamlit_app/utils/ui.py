# utils/ui.py

import streamlit as st

def apply_custom_styles():
    st.set_page_config(layout="wide")

    st.markdown("""
        <style>
            .main { padding: 2rem; }
            h1, h2, h3 { color: #1f77b4; }
            .stDataFrame { background-color: #f9f9f9; }
        </style>
    """, unsafe_allow_html=True)
