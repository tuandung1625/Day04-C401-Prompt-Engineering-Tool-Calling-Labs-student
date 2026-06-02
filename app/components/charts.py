import streamlit as st
import pandas as pd
import altair as alt
import json
import os
from pathlib import Path


# ─── Shared Theme ──────────────────────────────────────────────────────────────
CHART_BG = "#0D1117"
GRID_COLOR = "#21262D"
TEXT_COLOR = "#8B949E"
ACCENT_COLORS = ["#2F81F7", "#A371F7", "#3FB950", "#D29922", "#F85149", "#76E3EA"]

BASE_THEME = {
    "config": {
        "background": "transparent",
        "view": {"stroke": "transparent"},
        "axis": {
            "gridColor": GRID_COLOR,
            "domainColor": GRID_COLOR,
            "tickColor": GRID_COLOR,
            "labelColor": TEXT_COLOR,
            "titleColor": TEXT_COLOR,
            "labelFontSize": 12,
            "titleFontSize": 13,
        },
        "legend": {
            "labelColor": TEXT_COLOR,
            "titleColor": TEXT_COLOR,
            "labelFontSize": 12,
        },
        "title": {"color": TEXT_COLOR, "fontSize": 14},
    }
}

alt.themes.register("dark_theme", lambda: BASE_THEME)
alt.themes.enable("dark_theme")


# ─── Accuracy Trend Chart ──────────────────────────────────────────────────────
def render_accuracy_chart(version_log_path: str = None):
    """
    Line chart showing accuracy metrics across versions.
    Reads version_log.csv if exists, otherwise shows sample data.
    """
    if version_log_path and Path(version_log_path).exists():
        df = pd.read_csv(version_log_path)
        # Check required columns exist
        required = ["version", "metric_after"]
        if not all(col in df.columns for col in required):
            df = _sample_version_df()
    else:
        df = _sample_version_df()

    if df.empty:
        st.info("No version data yet. Run eval to populate.")
        return

    # Melt accuracy columns
    metric_cols = [c for c in df.columns if "accuracy" in c.lower()]
    if not metric_cols and "metric_after" in df.columns:
        # Use metric_after as single line
        melted = df[["version", "metric_after"]].rename(columns={"metric_after": "value"})
        melted["metric"] = "case_accuracy"
    else:
        id_cols = ["version"] + [c for c in df.columns if c not in metric_cols and c != "version"]
        try:
            melted = df.melt(id_vars=["version"], value_vars=metric_cols, var_name="metric", value_name="value")
        except Exception:
            melted = _sample_melted_df()

    chart = (
        alt.Chart(melted)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=80))
        .encode(
            x=alt.X("version:N", axis=alt.Axis(title="Version"), sort=None),
            y=alt.Y(
                "value:Q",
                axis=alt.Axis(title="Score", format=".0%"),
                scale=alt.Scale(domain=[0, 1]),
            ),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(range=ACCENT_COLORS),
                legend=alt.Legend(orient="bottom", title=None),
            ),
            tooltip=[
                alt.Tooltip("version:N", title="Version"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("value:Q", title="Score", format=".1%"),
            ],
        )
        .properties(height=320)
    )

    st.altair_chart(chart, use_container_width=True)


# ─── Tool Usage Distribution (from run files) ─────────────────────────────────
def render_tool_usage_chart(run_files: list[dict] = None):
    """
    Horizontal bar chart of tool call frequency from actual run data.
    """
    if run_files:
        tool_counts: dict[str, int] = {}
        for run in run_files:
            for result in run.get("results", []):
                for call in result.get("result", {}).get("actual_tool_calls", []):
                    name = call.get("name", "unknown")
                    tool_counts[name] = tool_counts.get(name, 0) + 1
    else:
        # Sample data
        tool_counts = {
            "lookup": 38, "timeline": 22, "social_search": 18,
            "clarify": 15, "fetch": 12, "format": 10,
            "papers": 8, "market_tracker": 6, "send": 4,
            "policy": 3, "paper_text": 3, "image_analyzer": 2,
        }

    df = pd.DataFrame(
        sorted(tool_counts.items(), key=lambda x: x[1], reverse=True),
        columns=["tool", "calls"],
    )

    TOOL_ICONS = {
        "lookup": "🌐", "timeline": "📅", "social_search": "🔍",
        "clarify": "❓", "fetch": "📥", "format": "📋",
        "papers": "📚", "market_tracker": "📈", "send": "📨",
        "policy": "📜", "paper_text": "📄", "image_analyzer": "🖼️",
    }
    df["label"] = df["tool"].apply(lambda t: f"{TOOL_ICONS.get(t, '🔧')} {t}")

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
        .encode(
            y=alt.Y("label:N", sort="-x", axis=alt.Axis(title=None, labelLimit=200)),
            x=alt.X("calls:Q", axis=alt.Axis(title="Total Calls")),
            color=alt.Color(
                "calls:Q",
                scale=alt.Scale(scheme="blues", reverse=False),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("tool:N", title="Tool"),
                alt.Tooltip("calls:Q", title="Calls"),
            ],
        )
        .properties(height=320)
    )

    st.altair_chart(chart, use_container_width=True)


# ─── Pass / Fail Distribution ─────────────────────────────────────────────────
def render_pass_fail_chart(passed: int, failed: int):
    """Donut chart showing pass/fail ratio."""
    df = pd.DataFrame({
        "status": ["Pass ✅", "Fail ❌"],
        "count": [passed, failed],
    })

    base = alt.Chart(df).encode(
        theta=alt.Theta("count:Q", stack=True),
        color=alt.Color(
            "status:N",
            scale=alt.Scale(
                domain=["Pass ✅", "Fail ❌"],
                range=["#3FB950", "#F85149"],
            ),
            legend=alt.Legend(orient="bottom", title=None),
        ),
        tooltip=[
            alt.Tooltip("status:N", title="Status"),
            alt.Tooltip("count:Q", title="Cases"),
        ],
    )

    chart = base.mark_arc(innerRadius=60, outerRadius=100) + base.mark_text(
        radius=130, fontSize=12, fontWeight="bold"
    ).encode(
        text=alt.Text("count:Q"),
        color=alt.value(TEXT_COLOR),
    )

    st.altair_chart(chart.properties(height=280), use_container_width=True)


# ─── Failure Type Breakdown ────────────────────────────────────────────────────
def render_failure_chart(failure_counts: dict[str, int]):
    """
    Horizontal bar chart showing failure type distribution.
    """
    if not failure_counts:
        st.info("No failures — all cases passed 🎉")
        return

    FAILURE_COLORS_MAP = {
        "wrong_tool":       "#F85149",
        "wrong_arg_value":  "#D29922",
        "wrong_boundary":   "#A371F7",
        "unnecessary_tool": "#76E3EA",
        "out_of_scope":     "#8B949E",
        "missing_info":     "#58A6FF",
    }

    df = pd.DataFrame([
        {"type": k, "count": v, "color": FAILURE_COLORS_MAP.get(k, "#8B949E")}
        for k, v in sorted(failure_counts.items(), key=lambda x: x[1], reverse=True)
    ])

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6)
        .encode(
            y=alt.Y("type:N", sort="-x", axis=alt.Axis(title=None)),
            x=alt.X("count:Q", axis=alt.Axis(title="Count")),
            color=alt.Color("type:N", scale=alt.Scale(
                domain=list(FAILURE_COLORS_MAP.keys()),
                range=list(FAILURE_COLORS_MAP.values()),
            ), legend=None),
            tooltip=[
                alt.Tooltip("type:N", title="Failure Type"),
                alt.Tooltip("count:Q", title="Count"),
            ],
        )
        .properties(height=240)
    )

    st.altair_chart(chart, use_container_width=True)


# ─── Version Comparison Bar ────────────────────────────────────────────────────
def render_version_comparison(runs_data: list[dict]):
    """
    Grouped bar chart comparing accuracy metrics across versions.
    """
    if not runs_data:
        runs_data = _sample_runs()

    rows = []
    for run in runs_data:
        v = run.get("version", "?")
        s = run.get("summary", {})
        for metric in ["case_accuracy", "tool_routing_accuracy", "argument_accuracy"]:
            val = s.get(metric)
            if val is not None:
                rows.append({"version": v, "metric": metric, "value": float(val)})

    if not rows:
        st.info("No run data found.")
        return

    df = pd.DataFrame(rows)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("version:N", axis=alt.Axis(title=None), sort=None),
            y=alt.Y("value:Q", axis=alt.Axis(title="Score", format=".0%"), scale=alt.Scale(domain=[0, 1])),
            color=alt.Color(
                "metric:N",
                scale=alt.Scale(
                    domain=["case_accuracy", "tool_routing_accuracy", "argument_accuracy"],
                    range=["#2F81F7", "#A371F7", "#3FB950"],
                ),
                legend=alt.Legend(orient="bottom", title=None),
            ),
            xOffset="metric:N",
            tooltip=[
                alt.Tooltip("version:N", title="Version"),
                alt.Tooltip("metric:N", title="Metric"),
                alt.Tooltip("value:Q", title="Score", format=".1%"),
            ],
        )
        .properties(height=320)
    )

    st.altair_chart(chart, use_container_width=True)


# ─── Multi-turn vs Single-turn Accuracy ───────────────────────────────────────
def render_multiturn_chart(runs_data: list[dict]):
    """Compare single-turn vs multi-turn accuracy per version."""
    rows = []
    for run in runs_data:
        v = run.get("version", "?")
        s = run.get("summary", {})
        rows.append({"version": v, "type": "Single-turn", "value": s.get("case_accuracy", 0)})
        mt = s.get("multiturn_accuracy")
        if mt is not None:
            rows.append({"version": v, "type": "Multi-turn", "value": float(mt)})

    if not rows:
        return

    df = pd.DataFrame(rows)
    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("version:N", sort=None, axis=alt.Axis(title="Version")),
            y=alt.Y("value:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(title="Accuracy", format=".0%")),
            color=alt.Color(
                "type:N",
                scale=alt.Scale(domain=["Single-turn", "Multi-turn"], range=["#2F81F7", "#3FB950"]),
                legend=alt.Legend(orient="bottom", title=None),
            ),
            tooltip=[
                alt.Tooltip("version:N", title="Version"),
                alt.Tooltip("type:N", title="Type"),
                alt.Tooltip("value:Q", title="Accuracy", format=".1%"),
            ],
        )
        .properties(height=260)
    )
    st.altair_chart(chart, use_container_width=True)


# ─── Sample/Fallback Data ──────────────────────────────────────────────────────
def _sample_version_df():
    return pd.DataFrame({
        "version": ["v0", "v1", "v2", "v3"],
        "case_accuracy": [0.70, 0.80, 0.85, 0.90],
        "tool_routing_accuracy": [0.75, 0.85, 0.90, 1.00],
        "argument_accuracy": [0.65, 0.75, 0.80, 0.90],
        "multiturn_accuracy": [0.50, 0.67, 0.83, 1.00],
    })


def _sample_melted_df():
    df = _sample_version_df()
    return df.melt(
        id_vars=["version"],
        value_vars=["case_accuracy", "tool_routing_accuracy", "argument_accuracy", "multiturn_accuracy"],
        var_name="metric",
        value_name="value",
    )


def _sample_runs():
    return [
        {"version": "v0", "summary": {"case_accuracy": 0.70, "tool_routing_accuracy": 0.75, "argument_accuracy": 0.65}},
        {"version": "v1", "summary": {"case_accuracy": 0.80, "tool_routing_accuracy": 0.85, "argument_accuracy": 0.75}},
        {"version": "v2", "summary": {"case_accuracy": 0.85, "tool_routing_accuracy": 0.90, "argument_accuracy": 0.80}},
        {"version": "v3", "summary": {"case_accuracy": 0.90, "tool_routing_accuracy": 1.00, "argument_accuracy": 0.90}},
    ]
