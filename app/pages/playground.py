import streamlit as st
import json
import time

st.title("Agent Playground")

# Mock agent step data
def mock_agent(query):
    steps = [
        {
            "thought": "User is asking about timeline → use timeline tool",
            "action": "timeline",
            "arguments": {"topic": query},
            "output": "AI agents evolved from rule-based → ML → LLM agents..."
        },
        {
            "thought": "Now format answer for readability",
            "action": "format",
            "arguments": {"style": "summary"},
            "output": "Formatted clean response"
        }
    ]

    final_answer = f"Here is the timeline for: {query}"
    return steps, final_answer


# Input
query = st.text_input("Enter your query")

if st.button("Run Agent") and query:

    steps, final_answer = mock_agent(query)

    st.subheader("🔍 Agent Trace")

    for i, step in enumerate(steps):
        with st.container():
            st.markdown(f"### Step {i+1}")

            # Thought
            st.markdown(f"🧠 **Thought**")
            st.write(step["thought"])

            # Action
            st.markdown(f"⚙️ **Action:** `{step['action']}`")

            # Arguments
            st.markdown("📦 **Arguments**")
            st.code(json.dumps(step["arguments"], indent=2), language="json")

            # Tool output
            with st.expander("Tool Output"):
                st.write(step["output"])

            st.divider()

    # Final answer
    st.success("✅ Final Answer")
    st.write(final_answer)
