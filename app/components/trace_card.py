import streamlit as st
import json


TOOL_ICONS = {
    "clarify": "❓", "timeline": "📅", "social_search": "🔍",
    "lookup": "🌐", "fetch": "📥", "format": "📋",
    "send": "📨", "policy": "📜", "papers": "📚",
    "paper_text": "📄", "market_tracker": "📈", "image_analyzer": "🖼️",
}

STEP_BG = "#161B22"
STEP_BORDER = "#30363D"
CONNECTOR_COLOR = "#2F81F7"


def render_step(step: dict, step_index: int = 1):
    """
    Render a single agent execution step as a card.

    Args:
        step: Dict with keys: thought, action, arguments, output
        step_index: Step number for display
    """
    tool_name = step.get("action", step.get("name", ""))
    icon = TOOL_ICONS.get(tool_name, "🔧")
    thought = step.get("thought", "")
    arguments = step.get("arguments", step.get("args", {}))
    output = step.get("output", step.get("result", ""))

    st.markdown(
        f"""
        <div style="
            background:{STEP_BG};
            border:1px solid {STEP_BORDER};
            border-left: 3px solid {CONNECTOR_COLOR};
            border-radius:8px;
            padding:16px;
            margin-bottom:12px;
            position:relative;
        ">
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                margin-bottom:12px;
            ">
                <span style="
                    background:#1C2128;
                    border:1px solid #30363D;
                    border-radius:50%;
                    width:30px;height:30px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:12px;font-weight:700;color:#8B949E;
                ">{step_index}</span>
                <span style="font-size:20px;">{icon}</span>
                <code style="
                    font-size:14px;font-weight:600;
                    color:#58A6FF;
                    background:rgba(88,166,255,0.1);
                    padding:3px 10px;
                    border-radius:6px;
                    border:1px solid rgba(88,166,255,0.25);
                ">{tool_name or "Thinking..."}</code>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Thought
    if thought:
        st.markdown(
            f"""
            <div style="
                margin-bottom:12px;
                padding:10px 14px;
                background:#1C2128;
                border-radius:6px;
                border:1px solid #21262D;
            ">
                <span style="font-size:11px;color:#8B949E;text-transform:uppercase;letter-spacing:0.05em;">💭 THOUGHT</span>
                <div style="color:#E6EDF3;margin-top:4px;font-size:14px;line-height:1.6;">{thought}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Arguments as JSON
    if arguments:
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except Exception:
                pass
        st.markdown(
            "<span style='font-size:12px;color:#8B949E;text-transform:uppercase;letter-spacing:0.05em;'>📦 Arguments</span>",
            unsafe_allow_html=True,
        )
        st.code(json.dumps(arguments, indent=2, ensure_ascii=False), language="json")

    # Tool output
    if output:
        with st.expander("📤 Tool Output"):
            if isinstance(output, (dict, list)):
                st.json(output)
            else:
                st.write(output)


def render_agent_trace(
    steps: list[dict],
    final_answer: str = None,
    tool_calls: list[dict] = None,
    tool_results: list[dict] = None,
):
    """
    Render the full agent execution trace.

    Args:
        steps: List of step dicts (thought/action/arguments/output)
        final_answer: Final text response from the agent
        tool_calls: List of actual tool call dicts from run data
        tool_results: List of tool result dicts from run data
    """
    # If we have run-format data (tool_calls + tool_results)
    if tool_calls is not None:
        if not tool_calls:
            st.info("No tool calls were made for this case.")
        else:
            for i, call in enumerate(tool_calls, 1):
                result_data = {}
                if tool_results:
                    matching = [tr for tr in tool_results if tr.get("tool") == call.get("name")]
                    if matching:
                        result_data = matching[0].get("result", {})

                render_step(
                    {
                        "action": call.get("name", ""),
                        "arguments": call.get("args", {}),
                        "output": result_data,
                    },
                    step_index=i,
                )
    # If we have step-format data (legacy)
    elif steps:
        for i, step in enumerate(steps, 1):
            render_step(step, step_index=i)

    # Final answer
    if final_answer:
        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg, rgba(63,185,80,0.1), rgba(47,129,247,0.1));
                border:1px solid rgba(63,185,80,0.3);
                border-radius:8px;
                padding:16px;
                margin-top:16px;
            ">
                <div style="
                    font-size:11px;color:#3FB950;
                    text-transform:uppercase;letter-spacing:0.05em;
                    margin-bottom:8px;
                ">✅ FINAL RESPONSE</div>
                <div style="color:#E6EDF3;font-size:14px;line-height:1.7;">{final_answer}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_round_trace(rounds: list[dict]):
    """
    Render multi-round tool loop trace from chat.py transcripts.

    Args:
        rounds: List of round dicts with tool_calls, tool_results, assistant_text
    """
    for round_num, round_data in enumerate(rounds, 1):
        st.markdown(f"**Round {round_num}**")
        assistant_text = round_data.get("assistant_text")
        if assistant_text:
            st.info(f"💬 {assistant_text}")

        for call in round_data.get("tool_calls", []):
            # Find matching result
            results = round_data.get("tool_results", [])
            matching_result = next(
                (r for r in results if r.get("tool") == call.get("name")),
                {}
            )
            render_step(
                {
                    "action": call.get("name", ""),
                    "arguments": call.get("args", {}),
                    "output": matching_result.get("result", {}),
                },
                step_index=round_num,
            )
