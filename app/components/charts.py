import streamlit as st
import pandas as pd
import altair as alt

def render_accuracy_chart():
    try:
        # Đường dẫn từ file main.py chạy lên nên sẽ là data/...
        df = pd.read_csv("data/artifacts/version_log.csv")
        
        chart = alt.Chart(df).mark_line(point=True).encode(
            x='version:N',
            y='case_accuracy:Q',
            color='metric:N'
        )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Không thể tải biểu đồ: {e}")