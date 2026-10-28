import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="UNIK - University of Kisubi Portal", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
.report-card {background-color: #E3F2FD; padding: 20px; border-radius: 10px; border-left: 5px solid #1565C0; margin-bottom: 15px;}
.report-inner {background-color: white !important; padding: 15px; border-radius: 8px; color: black !important; border: 1px solid #90CAF9;}
.report-inner p {color: black !important; font-size: 16px !important;}
</style>
""", unsafe_allow_html=True)

USERS = {
    "principal": {"name": "Principal, School of Nursing & Midwifery", "role": "Principal - UNIK University of Kisubi", "password": "unik2025"},
    "patron": {"name": "Patron UNASNM", "role": "Patron UNASNM", "password": "unik2025"},
    "president": {"name": "President BEC", "role": "President BEC", "password": "unik2025"},
    "speaker": {"name": "Hon. Lawrence Ssango - Speaker BEC", "role": "Speaker BEC - Office of the Speaker", "password": "unik2025"},
    "finance": {"name": "Finance Secretary BEC", "role": "Finance BEC", "password": "unik2025"},
    "general_secretary": {"name": "General Secretary BEC", "role": "General Secretary BEC", "password": "unik2025"},
    "information": {"name": "Information Ministry BEC", "role": "Information BEC", "password": "unik2025"},
    "class_rep": {"name": "Class Representatives", "role": "Class Representatives", "password": "unik2025"},
    "grc_male": {"name": "GRC Male / Galaxy Male", "role": "GRC Male", "password": "unik2025"},
    "grc_female": {"name": "GRC Female / Galaxy Female", "role": "GRC Female", "password": "unik2025"},
    "hostel_male": {"name": "Male Hostel Representative", "role": "Hostel Rep Male", "password": "unik2025"},
    "hostel_female": {"name": "Female Hostel Representative", "role": "Hostel Rep Female", "password": "unik2025"},
    "nursing_affairs": {"name": "Nursing Affairs / Non-Resident", "role": "Nursing Affairs", "password": "unik2025"},
}

DATA_FILE = "unik_reports_permanent.csv"

def load_reports():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            return pd.DataFrame(columns=["timestamp", "username", "department", "title", "report"])
    else:
        df = pd.DataFrame(columns=["timestamp", "username", "department", "title", "report"])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_report(username, title, report_text):
    df = load_reports()
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "department": USERS[username]["role"],
        "title": title,
        "report": report_text
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#1565C0;'>🏛️ UNIK - UNIVERSITY OF KISUBI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'><b>School of Nursing and Midwifery<br>BEC-UNASNM Official Governance Portal<br>Office of the Speaker - Hon. Lawrence Ssango</b><br>Secure Department Access System</p>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("🔐 Department Login")
        username = st.text_input("Username").lower().strip()
        password = st.text_input("Password", type="password")
        st.info("13 Offices: principal, patron, president, speaker, finance, general_secretary, information, class_rep, grc_male, grc_female, hostel_male, hostel_female, nursing_affairs | Password: unik2025")
        if st.button("Login to Portal", use_container_width=True, type="primary"):
            if username in USERS and password == USERS[username]["password"]:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Wrong username or password!")
else:
    user = USERS[st.session_state.username]
    with st.sidebar:
        st.success(f"Logged as: {user['name']}")
        st.caption(f"Role: {user['role']}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    is_admin = st.session_state.username in ["principal", "patron", "president", "speaker", "general_secretary"]
    if is_admin:
        st.title(f"📊 Dashboard - {user['name']}")
        tab1, tab2 = st.tabs(["📄 View All Reports", "✍️ Submit Report"])
        df = load_reports()
        with tab1:
            if df.empty:
                st.warning("No reports submitted yet.")
            else:
                titles = ["All Reports"] + sorted(df["title"].unique().tolist())
                selected = st.selectbox("Select report title to read", titles)
                display_df = df if selected == "All Reports" else df[df["title"] == selected]
                for idx, row in display_df.sort_values(by="timestamp", ascending=False).iterrows():
                    st.markdown(f"""<div class="report-card"><h4 style="color:#0D47A1; margin:0;">{row['title']} - {row['department']}</h4><small style="color:#555;">{row['timestamp']} | By: {row['username']}</small><div class="report-inner"><p>{row['report']}</p></div></div>""", unsafe_allow_html=True)
                st.download_button("📥 Download All Reports CSV", df.to_csv(index=False).encode('utf-8'), "unik_reports.csv")
        with tab2:
            t = st.text_input("Report Title")
            r = st.text_area("Report Content", height=250)
            if st.button("Submit Report", type="primary"):
                if t and r:
                    save_report(st.session_state.username, t, r)
                    st.success("✅ Report submitted permanently!")
                    st.rerun()
    else:
        st.title(f"✍️ {user['name']}")
        st.subheader("Submit Weekly Report")
        t = st.text_input("Report Title")
        r = st.text_area("Detailed Report", height=300)
        if st.button("Submit Report Permanently", type="primary", use_container_width=True):
            if t and r:
                save_report(st.session_state.username, t, r)
                st.success("✅ Report submitted! Speaker & Principal can now see it.")
                st.balloons()
        df = load_reports()
        my_reports = df[df["username"] == st.session_state.username]
        if not my_reports.empty:
            st.markdown("---")
            st.subheader("My Previous Reports")
            for idx, row in my_reports.sort_values(by="timestamp", ascending=False).iterrows():
                st.markdown(f"""<div class="report-card"><h4 style="color:#0D47A1;">{row['title']}</h4><small>{row['timestamp']}</small><div class="report-inner"><p>{row['report']}</p></div></div>""", unsafe_allow_html=True)
