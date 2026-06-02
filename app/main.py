import streamlit as st
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "starter_v0"))

from components.metric_card import stat_row
from components.badges import (
    pass_fail_badge, failure_badge, tool_badge, render_badge_row
)
from components.charts import (
    render_accuracy_chart,
    render_tool_usage_chart,
    render_pass_fail_chart,
    render_failure_chart,
    render_version_comparison,
    render_multiturn_chart,
)

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Research Agent Platform",
    page_icon="🕵️",
    initial_sidebar_state="expanded",
)

# Load custom CSS
CSS_PATH = Path(__file__).parent / "styles" / "main.css"
if CSS_PATH.exists():
    with open(CSS_PATH, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent / "starter_v0"
RUNS_DIR = ROOT / "runs"
ARTIFACTS_DIR = ROOT / "artifacts"
VERSION_LOG_PATH = ARTIFACTS_DIR / "version_log.csv"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"

# ─── Load Data Helpers ─────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_run_files():
    """Load all run JSON files from runs directory."""
    if not RUNS_DIR.exists():
        return []
    files = sorted(RUNS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)
    data = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fp:
                data.append(json.load(fp))
        except Exception:
            pass
    return data


@st.cache_data(ttl=60)
def get_latest_run():
    """Get the most recent run file."""
    runs = load_run_files()
    return runs[0] if runs else None


@st.cache_data
def load_tools():
    """Load tool declarations from tools.yaml."""
    if not TOOLS_PATH.exists():
        return []
    import yaml
    try:
        with open(TOOLS_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("tools", [])
    except Exception:
        return []


# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:24px;">
            <h1 style="font-size:2rem;margin:0;">🕵️ Research Agent</h1>
            <p style="color:#8B949E;font-size:0.875rem;margin-top:4px;">
                Tool-Calling Evaluation Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 📂 Data Sources")
    latest = get_latest_run()
    if latest:
        st.success(f"✅ Latest: `{latest.get('version', '?')}`")
        st.caption(f"🕒 {latest.get('generated_at', 'N/A')}")
    else:
        st.warning("⚠️ No run data found")

    st.divider()

    # Quick Stats
    if latest:
        st.markdown("### 📊 Quick Stats")
        s = latest.get("summary", {})
        st.metric("Case Accuracy", f"{s.get('case_accuracy', 0):.0%}")
        st.metric("Routing Accuracy", f"{s.get('tool_routing_accuracy', 0):.0%}")
        st.metric("Total Cases", s.get("total_cases", 0))

    st.divider()

    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.divider()

    # Links
    st.markdown("### 🔗 Quick Links")
    st.markdown(
        """
        - [📋 README](../README.md)
        - [📜 System Prompt](../starter_v0/artifacts/system_prompt.md)
        - [🔧 Tools Config](../starter_v0/artifacts/tools.yaml)
        - [📊 Version Log](../starter_v0/artifacts/version_log.csv)
        """
    )

# ─── Main Content ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style="
        font-size:2.5rem;
        background: linear-gradient(135deg, #2F81F7, #A371F7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom:8px;
    ">Research Agent Platform</h1>
    <p style="color:#8B949E;font-size:1.125rem;margin-bottom:32px;">
        Evidence-driven optimization for tool-calling AI agents
    </p>
    """,
    unsafe_allow_html=True,
)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "🔍 Run Inspector",
    "🧪 Playground",
    "🛠️ Tools",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    latest = get_latest_run()
    if not latest:
        st.info("🔍 No evaluation data found. Run `python run_eval.py` to generate data.")
        st.stop()

    summary = latest.get("summary", {})

    # ─── Top KPIs ──────────────────────────────────────────────────────────────
    st.markdown("### 📈 Key Performance Indicators")
    stat_row([
        {
            "title": "Case Accuracy",
            "value": f"{summary.get('case_accuracy', 0):.0%}",
            "delta": "+10%" if summary.get('case_accuracy', 0) > 0.8 else None,
            "icon": "🎯",
            "color": "#3FB950",
        },
        {
            "title": "Tool Routing",
            "value": f"{summary.get('tool_routing_accuracy', 0):.0%}",
            "icon": "🔀",
            "color": "#2F81F7",
        },
        {
            "title": "Argument Accuracy",
            "value": f"{summary.get('argument_accuracy', 0):.0%}",
            "icon": "📝",
            "color": "#A371F7",
        },
        {
            "title": "Total Cases",
            "value": str(summary.get("total_cases", 0)),
            "icon": "📋",
            "color": "#D29922",
        },
    ])

    st.divider()

    # ─── Charts Row 1 ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Accuracy Trend")
        if VERSION_LOG_PATH.exists():
            render_accuracy_chart(str(VERSION_LOG_PATH))
        else:
            render_accuracy_chart()  # Sample data

    with col2:
        st.markdown("#### ✅ Pass / Fail Distribution")
        passed = summary.get("passed_cases", 0)
        failed = summary.get("measured_cases", 0) - passed
        render_pass_fail_chart(passed, failed)

    st.divider()

    # ─── Charts Row 2 ──────────────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### 🔧 Tool Usage Distribution")
        all_runs = load_run_files()
        render_tool_usage_chart(all_runs)

    with col4:
        st.markdown("#### 🚨 Failure Type Breakdown")
        failure_counts = summary.get("failure_counts", {})
        render_failure_chart(failure_counts)

    st.divider()

    # ─── Version Comparison ────────────────────────────────────────────────────
    st.markdown("#### 📊 Version Comparison")
    all_runs = load_run_files()
    render_version_comparison(all_runs)

    st.divider()

    # ─── Multi-turn Accuracy ───────────────────────────────────────────────────
    st.markdown("#### 🔄 Single-turn vs Multi-turn Accuracy")
    render_multiturn_chart(all_runs)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RUN INSPECTOR
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🔍 Run Log Inspector")
    st.caption("Deep dive into individual evaluation runs")

    run_files = load_run_files()
    if not run_files:
        st.info("No run files found. Execute `python run_eval.py` first.")
        st.stop()

    # Run selector
    run_ids = [r.get("run_id", "unknown") for r in run_files]
    selected_id = st.selectbox("📂 Select Run", run_ids, index=0)
    selected_run = next((r for r in run_files if r.get("run_id") == selected_id), None)

    if not selected_run:
        st.stop()

    # Run metadata
    with st.expander("🔖 Run Metadata", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Version", selected_run.get("version", "?"))
        col2.metric("Provider", selected_run.get("provider", "?"))
        col3.metric("Model", selected_run.get("model", "?"))
        col4.metric("Phase", selected_run.get("phase", "?"))

    st.divider()

    # Case results
    results = selected_run.get("results", [])
    st.markdown(f"### 📋 Case Results ({len(results)} total)")

    # Filter controls
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_status = st.selectbox("Filter", ["All", "Pass", "Fail"])
    with col2:
        search_query = st.text_input("🔍 Search by case ID or skill", "")

    filtered = results
    if filter_status == "Pass":
        filtered = [r for r in results if r.get("result", {}).get("passed")]
    elif filter_status == "Fail":
        filtered = [r for r in results if not r.get("result", {}).get("passed")]

    if search_query:
        filtered = [
            r for r in filtered
            if search_query.lower() in r.get("id", "").lower()
            or search_query.lower() in str(r.get("metadata", {})).lower()
        ]

    # Display results
    for i, case in enumerate(filtered):
        case_id = case.get("id", "unknown")
        result = case.get("result", {})
        passed = result.get("passed", False)
        metadata = case.get("metadata", {})

        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{case_id}**")
                st.caption(metadata.get("what_it_tests", ""))
            with col2:
                pass_fail_badge(passed)

            # Tool calls
            st.markdown("**🔧 Actual Tool Calls:**")
            actual_calls = result.get("actual_tool_calls", [])
            if actual_calls:
                for call in actual_calls:
                    tool_badge(call.get("name", "?"), is_correct=passed)
            else:
                st.caption("_No tools called_")

            # Expected
            expect = case.get("expect", {})
            if expect.get("no_tool"):
                st.caption("Expected: No tool call")
            else:
                expected_calls = expect.get("tool_calls", [])
                if expected_calls:
                    st.markdown("**✅ Expected:**")
                    for call in expected_calls:
                        tool_badge(call.get("name", "?"))

            # Failures
            failures = result.get("failures", [])
            if failures:
                st.markdown("**❌ Failures:**")
                for f in failures:
                    st.caption(f"• {f}")

            # Failure type badge
            ftype = result.get("failure_type")
            if ftype:
                failure_badge(ftype)

            # Show input query in expander
            with st.expander("📝 Query"):
                st.code(case.get("input", ""), language="text")

            # Show tool results in expander
            tool_results = case.get("tool_results", [])
            if tool_results:
                with st.expander("🔧 Tool Results"):
                    st.json(tool_results)

            st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PLAYGROUND
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🧪 Agent Playground")
    st.caption("Test your agent with custom queries")

    st.markdown(
        """
        <div class="info-box">
            💡 <strong>Tip:</strong> This playground connects to your actual agent.
            Try queries like:<br>
            • "Tweet mới nhất của Sam Altman là gì?"<br>
            • "Tin tức AI hôm nay có gì nổi bật?"<br>
            • "Tóm tắt bài này: https://example.com/article"
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Config
    col1, col2, col3 = st.columns(3)
    with col1:
        provider = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini"])
    with col2:
        model = st.text_input("Model (optional)", "")
    with col3:
        max_rounds = st.number_input("Max Tool Rounds", 1, 10, 4)

    # Query input
    user_query = st.text_area("🔍 Enter your query", height=120, placeholder="Type your research request here...")

    if st.button("▶️ Run Agent", type="primary", use_container_width=True):
        if not user_query.strip():
            st.warning("Please enter a query")
        else:
            with st.spinner("🤖 Agent is working..."):
                try:
                    # Import agent
                    from agent import ResearchAgent
                    from providers import make_provider
                    from tools import load_tool_declarations, to_openai_tools

                    # Load resources
                    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
                    tool_declarations = load_tool_declarations(TOOLS_PATH)
                    openai_tools = to_openai_tools(tool_declarations)
                    provider_obj = make_provider(provider)

                    # Create agent
                    agent = ResearchAgent(
                        provider=provider_obj,
                        system_prompt=system_prompt,
                        tools=openai_tools,
                        model=model if model else None,
                    )

                    # Run
                    messages = [{"role": "user", "content": user_query}]
                    run = agent.run(messages)

                    # Display results
                    st.success("✅ Agent execution completed")

                    # Assistant text
                    if run.text:
                        st.markdown("#### 💬 Assistant Response")
                        st.info(run.text)

                    # Tool calls
                    if run.tool_calls:
                        st.markdown("#### 🔧 Tool Calls")
                        for i, call in enumerate(run.tool_calls, 1):
                            with st.expander(f"Call {i}: {call.name}"):
                                st.json(call.args)

                    # Tool results
                    if run.tool_results:
                        st.markdown("#### 📦 Tool Results")
                        for i, result in enumerate(run.tool_results, 1):
                            with st.expander(f"Result {i}: {result.get('tool', '?')}"):
                                st.json(result)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.exception(e)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TOOLS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🛠️ Available Tools")
    st.caption("All tools registered in the agent")

    tools = load_tools()
    if not tools:
        st.warning("No tools found in tools.yaml")
        st.stop()

    # Tool icons
    TOOL_ICONS = {
        "clarify": "❓", "timeline": "📅", "social_search": "🔍",
        "lookup": "🌐", "fetch": "📥", "format": "📋",
        "send": "📨", "policy": "📜", "papers": "📚",
        "paper_text": "📄", "market_tracker": "📈", "image_analyzer": "🖼️",
    }

    # Grid layout
    cols = st.columns(3)
    for idx, tool in enumerate(tools):
        name = tool.get("name", "unknown")
        desc = tool.get("description", "No description")
        params = tool.get("parameters", {}).get("properties", {})
        required = tool.get("parameters", {}).get("required", [])

        with cols[idx % 3]:
            icon = TOOL_ICONS.get(name, "🔧")
            st.markdown(
                f"""
                <div class="tool-card">
                    <div class="tool-icon">{icon}</div>
                    <div class="tool-name">{name}</div>
                    <div class="tool-description">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("📋 Parameters"):
                if params:
                    for pname, pspec in params.items():
                        is_required = pname in required
                        req_badge = "🔴" if is_required else "⚪"
                        ptype = pspec.get("type", "?")
                        pdesc = pspec.get("description", "")
                        st.caption(f"{req_badge} **{pname}** (`{ptype}`): {pdesc}")
                else:
                    st.caption("No parameters")


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:#6E7681;font-size:0.875rem;">
        Built with Streamlit • Research Agent Platform • Day 04 Lab v2
    </div>
    """,
    unsafe_allow_html=True,
)