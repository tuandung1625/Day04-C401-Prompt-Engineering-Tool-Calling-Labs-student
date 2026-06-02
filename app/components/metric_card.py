import streamlit as st


def metric_card(title: str, value: str, delta: str = None, icon: str = "📊", color: str = "#2F81F7"):
    """
    Render a stylized metric card with optional delta indicator.
    
    Args:
        title: Card title label
        value: Main metric value
        delta: Optional change indicator (e.g. "+12%", "-3%")
        icon: Emoji icon to display
        color: Accent color for the top border
    """
    delta_html = ""
    if delta:
        is_positive = delta.startswith("+")
        delta_color = "#3FB950" if is_positive else "#F85149"
        arrow = "↑" if is_positive else "↓"
        delta_html = f"""
        <div style="
            font-size:12px;
            font-weight:600;
            color:{delta_color};
            margin-top:4px;
            display:flex;
            align-items:center;
            gap:4px;
        ">
            {arrow} {delta}
        </div>
        """

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #161B22, #1C2128);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #30363D;
            border-top: 3px solid {color};
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease;
        ">
            <div style="
                position:absolute;
                top:12px;
                right:16px;
                font-size:28px;
                opacity:0.25;
            ">{icon}</div>
            <div style="
                font-size:12px;
                color:#8B949E;
                text-transform:uppercase;
                letter-spacing:0.05em;
                font-weight:600;
                margin-bottom:8px;
            ">{title}</div>
            <div style="
                font-size:32px;
                font-weight:700;
                color:#E6EDF3;
                line-height:1.1;
            ">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_row(items: list[dict]):
    """
    Render a row of metric cards.
    
    Args:
        items: List of dicts with keys: title, value, delta (optional), icon (optional), color (optional)
    """
    cols = st.columns(len(items))
    colors = ["#2F81F7", "#A371F7", "#3FB950", "#D29922"]
    for i, (col, item) in enumerate(zip(cols, items)):
        with col:
            metric_card(
                title=item.get("title", ""),
                value=item.get("value", "-"),
                delta=item.get("delta"),
                icon=item.get("icon", "📊"),
                color=item.get("color", colors[i % len(colors)]),
            )
