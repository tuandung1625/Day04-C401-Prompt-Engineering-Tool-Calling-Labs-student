import streamlit as st

def badge(label, color):
    st.markdown(
        f"<span style='background:{color}; padding:4px 8px; border-radius:6px; color:white;'>{label}</span>",
        unsafe_allow_html=True
    )