import streamlit as st

def metric_card(title, value, delta=None):
    """
    Reusable metric card component
    """

    st.markdown(
        f"""
        <div style="
            background-color:#161B22;
            padding:16px;
            border-radius:12px;
            border:1px solid #30363D;
        ">
            <div style="font-size:14px;color:#8B949E">{title}</div>
            <div style="font-size:28px;font-weight:bold;color:#E6EDF3">
                {value}
            </div>
            <div style="font-size:12px;color:#10B981">
                {delta if delta else ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )