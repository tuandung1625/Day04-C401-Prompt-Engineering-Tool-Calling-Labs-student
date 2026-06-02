import streamlit as st
import json
import os

st.title("🔍 Run Log Inspector")

RUN_DIR = "../starter_v0/artifacts/runs"  # Đường dẫn đến thư mục chứa các file log JSON


# Load run files
files = [f for f in os.listdir(RUN_DIR) if f.endswith(".json")]

selected = st.selectbox("Select Run", files)

if selected:
    with open(os.path.join(RUN_DIR, selected), "r") as f:
        data = json.load(f)

    st.subheader("🧾 Query")
    st.write(data["query"])

    # Expected vs Actual
    st.subheader("🎯 Expected vs Actual")

    col1, col2 = st.columns(2)

    expected = data.get("expected_tool", "N/A")
    actual = data.get("actual_tool", "N/A")

    col1.markdown(f"**Expected:** `{expected}`")
    col2.markdown(f"**Actual:** `{actual}`")

    if expected != actual:
        col2.error("Mismatch detected ❌")
    else:
        col2.success("Correct ✅")

    # Steps
    st.subheader("🔄 Execution Steps")

    for i, step in enumerate(data.get("steps", [])):
        with st.container():
            st.markdown(f"### Step {i+1}")

            st.markdown("🧠 Thought")
            st.write(step.get("thought", ""))

            st.markdown(f"⚙️ Action: `{step.get('action','')}`")

            st.markdown("📦 Arguments")
            st.code(json.dumps(step.get("arguments", {}), indent=2))

            with st.expander("📤 Tool Output"):
                st.write(step.get("output", ""))

            st.divider()

    # Final response
    st.subheader("✅ Final Response")
    st.write(data.get("final_answer", ""))


    # Failures
    failures = data.get("failure_types", [])

    if failures:
        st.subheader("🚨 Failure Types")

        colors = {
            "wrong_tool": "red",
            "wrong_arg_value": "orange",
            "wrong_boundary": "purple",
            "unnecessary_tool": "gold",
            "out_of_scope": "gray",
            "missing_info": "blue"
        }

        for ftype in failures:
            color = colors.get(ftype, "white")
            st.markdown(
                f"<span style='background:{color};padding:5px;border-radius:6px'>{ftype}</span>",
                unsafe_allow_html=True
            )

    # Raw JSON
    with st.expander("📂 Raw JSON"):
        st.json(data)