import streamlit as st

def render_step(step):
    with st.container():
        st.markdown(f"### 🧠 Thought\n{step['thought']}")
        st.markdown(f"⚙️ **Action:** `{step['action']}`")
        st.code(step['arguments'], language='json')
        
        with st.expander("📤 Tool Output"):
            st.write(step['output'])