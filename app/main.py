import streamlit as st
# Khai báo import các component đã viết
from components.metric_card import metric_card
from components.badges import badge
from components.charts import render_accuracy_chart

st.set_page_config(layout="wide", page_title="AI Agent OS")

st.title("AI Agent Platform Dashboard")

# Khởi tạo các Tabs
tab1, tab2, tab3 = st.tabs([
    "Agent Playground",
    "Evaluation Dashboard",
    "Run Log Inspector"
])

with tab1:
    st.header("Agent Playground")
    st.write("Thử nghiệm Prompt và Model tại đây.")
    # Bạn có thể gọi render_step từ trace_card ở đây nếu có data test

with tab2:
    st.header("Evaluation Metrics")
    # Hiển thị Metric mẫu
    col1, col2 = st.columns(2)
    with col1:
        metric_card("Tổng số Run", "1,240", "+12%")
    with col2:
        st.write("Trạng thái:")
        badge("Failed", "#ff4b4b")
        badge("Success", "#00cc66")
    
    st.markdown("---")
    st.subheader("Đồ thị chính xác (Accuracy Trend)")
    render_accuracy_chart()

with tab3:
    st.header("Run Log Inspector")
    st.write("Xem chi tiết các bước chạy của Agent.")