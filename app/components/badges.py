import streamlit as st


# Failure type color mapping
FAILURE_COLORS = {
    "wrong_tool":       {"bg": "rgba(248, 81, 73, 0.15)",   "text": "#F85149",  "border": "rgba(248, 81, 73, 0.35)"},
    "wrong_arg_value":  {"bg": "rgba(210, 153, 34, 0.15)",  "text": "#D29922",  "border": "rgba(210, 153, 34, 0.35)"},
    "wrong_boundary":   {"bg": "rgba(163, 113, 247, 0.15)", "text": "#A371F7",  "border": "rgba(163, 113, 247, 0.35)"},
    "unnecessary_tool": {"bg": "rgba(118, 227, 234, 0.15)", "text": "#76E3EA",  "border": "rgba(118, 227, 234, 0.35)"},
    "out_of_scope":     {"bg": "rgba(139, 148, 158, 0.15)", "text": "#8B949E",  "border": "rgba(139, 148, 158, 0.35)"},
    "missing_info":     {"bg": "rgba(47, 129, 247, 0.15)",  "text": "#58A6FF",  "border": "rgba(47, 129, 247, 0.35)"},
}

PASS_STYLE = {"bg": "rgba(63, 185, 80, 0.15)", "text": "#3FB950", "border": "rgba(63, 185, 80, 0.35)"}
FAIL_STYLE = {"bg": "rgba(248, 81, 73, 0.15)", "text": "#F85149", "border": "rgba(248, 81, 73, 0.35)"}


def badge(label: str, color: str = "#2F81F7", bg_color: str = None):
    """Render a simple colored pill badge."""
    if bg_color is None:
        # Auto-derive background from color with low opacity
        bg_color = f"rgba(47, 129, 247, 0.15)"

    st.markdown(
        f"""
        <span style="
            display:inline-flex;
            align-items:center;
            padding:4px 10px;
            border-radius:9999px;
            background:{bg_color};
            color:{color};
            border:1px solid {color}44;
            font-size:12px;
            font-weight:600;
            margin-right:6px;
            margin-bottom:6px;
        ">{label}</span>
        """,
        unsafe_allow_html=True,
    )


def pass_fail_badge(passed: bool):
    """Render a PASS/FAIL pill badge."""
    style = PASS_STYLE if passed else FAIL_STYLE
    label = "✅ PASS" if passed else "❌ FAIL"
    st.markdown(
        f"""
        <span style="
            display:inline-flex;
            align-items:center;
            padding:4px 12px;
            border-radius:9999px;
            background:{style['bg']};
            color:{style['text']};
            border:1px solid {style['border']};
            font-size:12px;
            font-weight:700;
            letter-spacing:0.05em;
        ">{label}</span>
        """,
        unsafe_allow_html=True,
    )


def failure_badge(failure_type: str):
    """Render a failure type badge with semantic coloring."""
    style = FAILURE_COLORS.get(failure_type, {"bg": "#1C2128", "text": "#8B949E", "border": "#30363D"})
    icons = {
        "wrong_tool": "🔀",
        "wrong_arg_value": "📝",
        "wrong_boundary": "🚧",
        "unnecessary_tool": "⚠️",
        "out_of_scope": "🚫",
        "missing_info": "❓",
    }
    icon = icons.get(failure_type, "⚡")
    st.markdown(
        f"""
        <span style="
            display:inline-flex;
            align-items:center;
            gap:4px;
            padding:4px 12px;
            border-radius:9999px;
            background:{style['bg']};
            color:{style['text']};
            border:1px solid {style['border']};
            font-size:12px;
            font-weight:600;
        ">{icon} {failure_type}</span>
        """,
        unsafe_allow_html=True,
    )


def tool_badge(tool_name: str, is_correct: bool = True):
    """Render a tool name badge."""
    TOOL_ICONS = {
        "clarify": "❓",
        "timeline": "📅",
        "social_search": "🔍",
        "lookup": "🌐",
        "fetch": "📥",
        "format": "📋",
        "send": "📨",
        "policy": "📜",
        "papers": "📚",
        "paper_text": "📄",
        "market_tracker": "📈",
        "image_analyzer": "🖼️",
    }
    icon = TOOL_ICONS.get(tool_name, "🔧")
    color = "#58A6FF" if is_correct else "#F85149"
    bg = "rgba(88, 166, 255, 0.12)" if is_correct else "rgba(248, 81, 73, 0.12)"
    border = "rgba(88, 166, 255, 0.3)" if is_correct else "rgba(248, 81, 73, 0.3)"
    st.markdown(
        f"""
        <code style="
            display:inline-flex;
            align-items:center;
            gap:4px;
            padding:3px 10px;
            border-radius:6px;
            background:{bg};
            color:{color};
            border:1px solid {border};
            font-size:12px;
            font-weight:600;
            font-family:monospace;
        ">{icon} {tool_name}</code>
        """,
        unsafe_allow_html=True,
    )


def render_badge_row(items: list[str], badge_type: str = "info"):
    """Render multiple badges inline in a single row."""
    colors = {
        "info": ("#58A6FF", "rgba(88, 166, 255, 0.15)"),
        "success": ("#3FB950", "rgba(63, 185, 80, 0.15)"),
        "warning": ("#D29922", "rgba(210, 153, 34, 0.15)"),
        "error": ("#F85149", "rgba(248, 81, 73, 0.15)"),
        "purple": ("#A371F7", "rgba(163, 113, 247, 0.15)"),
    }
    color, bg = colors.get(badge_type, colors["info"])
    badges_html = " ".join([
        f"""<span style="
            display:inline-flex;
            align-items:center;
            padding:4px 10px;
            border-radius:9999px;
            background:{bg};
            color:{color};
            border:1px solid {color}44;
            font-size:12px;
            font-weight:600;
            margin-right:6px;
        ">{item}</span>"""
        for item in items
    ])
    st.markdown(f"<div style='display:flex;flex-wrap:wrap;gap:4px;'>{badges_html}</div>", unsafe_allow_html=True)
