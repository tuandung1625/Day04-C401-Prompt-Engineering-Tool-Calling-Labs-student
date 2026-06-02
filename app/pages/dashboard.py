import streamlit as st
import pandas as pd
import altair as alt

st.title("📊 Evaluation Dashboard")

# Load data
df = pd.read_csv("../starter_v0/version_log.csv")

versions = df["version"].unique()
selected_version = st.selectbox("Select Version", versions)

filtered = df[df["version"] == selected_version]

# KPI Cards
st.subheader("📌 Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Case Accuracy", round(filtered["case_accuracy"].values[0], 2))
col2.metric("Tool Routing", round(filtered["tool_routing_accuracy"].values[0], 2))
col3.metric("Argument Accuracy", round(filtered["argument_accuracy"].values[0], 2))
col4.metric("Multi-turn Accuracy", round(filtered["multiturn_accuracy"].values[0], 2))


# Trend Chart
st.subheader("📈 Accuracy Trend")

melted = df.melt(id_vars=["version"], value_vars=[
    "case_accuracy",
    "tool_routing_accuracy",
    "argument_accuracy",
    "multiturn_accuracy"
], var_name="metric", value_name="value")

chart = alt.Chart(melted).mark_line(point=True).encode(
    x="version",
    y="value",
    color="metric"
)

st.altair_chart(chart, use_container_width=True)


# Version comparison
st.subheader("📊 Version Comparison")

bar = alt.Chart(melted).mark_bar().encode(
    x="version",
    y="value",
    color="metric",
    column="metric"
)

st.altair_chart(bar, use_container_width=True)


# Tool usage (mock)
st.subheader("🛠 Tool Usage Distribution")

tool_data = pd.DataFrame({
    "tool": ["lookup", "timeline", "clarify", "papers"],
    "count": [40, 25, 20, 15]
})

pie = alt.Chart(tool_data).mark_arc().encode(
    theta="count",
    color="tool"
)

st.altair_chart(pie, use_container_width=True)


# Pass/Fail
st.subheader("✅ Pass / Fail Distribution")

pf_data = pd.DataFrame({
    "result": ["Pass", "Fail"],
    "count": [75, 25]
})

pf_chart = alt.Chart(pf_data).mark_bar().encode(
    x="result",
    y="count",
    color="result"
)

st.altair_chart(pf_chart, use_container_width=True)
