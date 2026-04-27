import streamlit as st
import time
from core.state_manager import StateManager

st.set_page_config(page_title="Self-Defending Vault", layout="wide")

state = StateManager()

st.title("🛡️ Proactive Deception Vault")

status = state.get_status()

if status == "Normal":
    st.success("🟢 STATUS: ARMED & WAITING FOR HACKER")
    st.markdown("The Deception Agent has pre-generated **Honey Assets** in the `/my_vault/` directory. Open and Modify any of those files to trigger the Tripwire!")
else:
    st.error("🔴 STATUS: ACTIVE COUNTER-OPERATION IN PROGRESS")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📡 Live Hacker Traceback Terminal")
    if status != "Normal":
        logs = state.get_traceback_logs()
        box = st.empty()
        text_display = ""
        for line in logs:
            text_display += f"> {line}\n"
        box.code(text_display, language="bash")
        if not logs:
             st.info("Tracing source...")
    else:
        st.code("> Standby...\n> Listening for unauthorized file access.", language="bash")

with col2:
    st.subheader("📁 System Event Log")
    import sqlite3
    import pandas as pd
    from core.config import DB_PATH
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql("SELECT timestamp, event_type, file_path FROM file_events ORDER BY id DESC LIMIT 15", conn)
            st.dataframe(df, width='stretch')
    except Exception:
        pass

time.sleep(1)
st.rerun()
