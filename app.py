import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="UNIK BEC-UNASNM Portal", page_icon="🏛️", layout="wide")

USERS = {
    "speaker": {"password": "unik2025", "role": "Speaker", "name": "Office of the Speaker", "icon": "🔨"},
    "president": {"password": "unik2025", "role": "President", "name": "Office of the President", "icon": "👑"},
    "finance": {"password": "unik2025", "role": "Finance", "name": "Finance Department", "icon": "💰"},
    "info": {"password": "unik2025", "role": "Information", "name": "Information Ministry", "icon": "📢"},
    "nursing": {"password": "unik2025", "role": "Nursing Affairs", "name": "Nursing Affairs Office", "icon": "🏥"},
    "hostel_boys": {"password": "unik2025", "role": "Hostel Boys", "name": "Hostel Manager - Boys", "icon": "🏠"},
    "hostel_girls": {"password": "unik2025", "role": "Hostel Girls", "name": "Hostel Manager - Girls", "icon": "🏠"}
}

REPORTS_FILE = "unik_reports.csv"

def load_reports():
    if os.path.exists(REPORTS_FILE):
        return pd.read_csv(REPORTS_FILE)
    else:
        return pd.DataFrame(columns=["Date","Time","Department","Role","Report_Type","Title","Content","Status"])

def save_report(dept_name, role, r_type, title, content):
    df = load_reports()
    new_row = {"Date": datetime.now().strftime("%Y-%m-%d"), "Time": datetime.now().strftime("%H:%M:%S"), "Department": dept_name, "Role": role, "Report_Type": r_type, "Title": title, "Content": content, "Status": "Pending Review"}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(REPORTS_FILE, index=False)

def login_page():
    st.markdown("<div style='text-align: center; padding: 20px;'><h1>🏛️ UNIK BEC-UNASNM</h1><h2>OFFICIAL GOVERNANCE PORTAL</h2><p>Uganda National Institute - Bweyogere Campus</p><p><b>Office of the Speaker | Hon. Lawrence Ssango</b></p></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 🔐 Department Login")
        username = st.text_input("Username (e.g. finance, speaker)").lower().strip()
        password = st.text_input("Password", type="password")
        st.info("Usernames: speaker, president, finance, info, nursing, hostel_boys, hostel_girls | Password for all: unik2025")
        if st.button("Login to Portal", use_container_width=True, type="primary"):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.session_state["role"] = USERS[username]["role"]
                st.session_state["dept_name"] = USERS[username]["name"]
                st.rerun()
            else:
                st.error("Wrong username or password! Try: speaker / unik2025")
    st.markdown("---")
    st.markdown("<p style='text-align:center;'>© 2025 UNIK BEC-UNASNM | Office of the Speaker</p>", unsafe_allow_html=True)

def main_portal():
    user = st.session_state["user"]
    role = st.session_state["role"]
    dept_name = st.session_state["dept_name"]
    icon = USERS[user]["icon"]
    with st.sidebar:
        st.markdown(f"## {icon} {dept_name}")
        st.markdown(f"**Role:** {role}")
        st.markdown(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}")
        st.divider()
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()
        st.divider()
        st.markdown("### 📋 Departments")
        for u, info in USERS.items():
            st.markdown(f"{info['icon']} {info['name']}")
    st.title(f"{icon} {dept_name}")
    if role in ["Speaker", "President"]:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard (All Reports)", "📝 Submit Report", "✉️ Letter Generator", "📁 Archive"])
    else:
        tab1, tab2 = st.tabs(["📝 Submit Report", "📊 My Reports"])
    submit_tab = tab2 if role in ["Speaker", "President"] else tab1
    with submit_tab:
        st.subheader("Submit Departmental Report")
        col1, col2 = st.columns(2)
        with col1:
            r_type = st.selectbox("Report Type", ["Weekly Report", "Financial Report", "Activity Report", "Budget Request", "Complaint / Issue", "Event Proposal", "Hostel Report"])
        with col2:
            title = st.text_input("Report Title", placeholder="e.g. Week 3 Financial Accountability")
        content = st.text_area("Detailed Content", height=200, placeholder="Write your full report here...")
        if st.button("📤 Submit Report to Speaker & President", type="primary", use_container_width=True):
            if title and content:
                save_report(dept_name, role, r_type, title, content)
                st.success(f"✅ Report submitted successfully! Speaker & President will review it.")
                st.balloons()
            else:
                st.error("Please fill Title and Content!")
    dashboard_tab = tab1 if role in ["Speaker", "President"] else tab2
    with dashboard_tab:
        df = load_reports()
        if role not in ["Speaker", "President"]:
            df = df[df["Department"] == dept_name]
            st.subheader(f"My Reports - {dept_name}")
        else:
            st.subheader("All Departments Reports - Speaker & President View Only")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Reports", len(df))
            c2.metric("Finance Reports", len(df[df["Role"]=="Finance"]) if not df.empty else 0)
            c3.metric("Hostel Reports", len(df[df["Role"].str.contains("Hostel")]) if not df.empty else 0)
            c4.metric("Pending", len(df[df["Status"]=="Pending Review"]) if not df.empty else 0)
        if df.empty:
            st.info("No reports submitted yet. Be the first!")
        else:
            if role in ["Speaker", "President"]:
                dept_filter = st.selectbox("Filter by Department", ["All"] + list(USERS[us]["name"] for us in USERS))
                if dept_filter != "All":
                    df = df[df["Department"] == dept_filter]
            df_sorted = df.sort_index(ascending=False)
            st.dataframe(df_sorted, use_container_width=True, height=400)
            st.divider()
            st.markdown("### 📖 Read Report Details")
            if not df_sorted.empty:
                selected_idx = st.selectbox("Select Report Title to Read", df_sorted["Title"].tolist())
                report = df_sorted[df_sorted["Title"] == selected_idx].iloc[0]
                st.markdown(f"<div style='border:1px solid #ddd; padding:20px; border-radius:10px; background:#f9f9f9;'><h3>{report['Title']}</h3><p><b>From:</b> {report['Department']} | <b>Type:</b> {report['Report_Type']} | <b>Date:</b> {report['Date']} {report['Time']}</p><p><b>Status:</b> {report['Status']}</p><hr><p>{report['Content']}</p></div>", unsafe_allow_html=True)
    if role in ["Speaker", "President"]:
        with tab3:
            st.subheader("✉️ Official Letter Generator")
            col1, col2 = st.columns(2)
            with col1:
                letter_type = st.selectbox("Letter Type", ["Appointment Letter", "Invitation Letter", "Official Communication", "Approval Letter", "Warning Letter"])
                ref_no = st.text_input("Ref No", value=f"UNIK/BEC/UNASNM/2025/{len(load_reports())+1:03d}")
            with col2:
                to_person = st.text_input("To", value="The Dean of Students")
                date = st.date_input("Date", datetime.now())
            subject = st.text_input("Subject / Regarding", value="Appointment and Official Duties")
            body = st.text_area("Letter Body", height=200, value=f"Following the report submitted, the Office of the {role} has approved...\n\nThis letter serves to...")
            if st.button("Generate Official Letter Preview", type="primary"):
                st.markdown(f"<div style='border:2px solid black; padding:30px; background:white; color:black; font-family: serif;'><div style='text-align:center;'><h2>UGANDA NURSES AND MIDWIVES UNION</h2><h3>UNIK - Bweyogere Campus</h3><p><b>Office of the {role} - UNIK BEC-UNASNM</b></p><hr></div><p><b>Ref:</b> {ref_no}<br><b>Date:</b> {date.strftime('%d/%m/%Y')}</p><p><b>To:</b> {to_person}<br><b>Re:</b> {subject}</p><p><b>{letter_type.upper()}</b></p><p>{body.replace(chr(10), '<br>')}</p><br><br><p>Yours faithfully,</p><p><b>Hon. Lawrence Ssango</b><br>Speaker, UNIK BEC-UNASNM<br>Bweyogere Campus</p></div>", unsafe_allow_html=True)
        with tab4:
            st.subheader("📁 Archive & Export")
            df = load_reports()
            if not df.empty:
                st.download_button("📥 Download All Reports as CSV", df.to_csv(index=False), "UNIK_BEC_ALL_REPORTS.csv", "text/csv", use_container_width=True)
            else:
                st.info("No data to export yet")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if not st.session_state["logged_in"]:
    login_page()
else:
    main_portal()
