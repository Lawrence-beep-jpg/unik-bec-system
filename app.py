import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="UNIK BEC-UNASNM GOVERNANCE PORTAL", layout="wide", page_icon="🏛️")

st.markdown("""
<style>
    .report-card {
        background-color: #E8F4FF;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #0A4A7A;
        margin-bottom: 15px;
    }
    .report-card * {
        color: #000000 !important;
    }
    .report-content {
        background-color: #FFFFFF;
        color: #000000 !important;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #cccccc;
        white-space: pre-wrap;
        font-size: 16px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "reports.csv"

USERS = {
    "speaker": {"password": "unik2025", "dept": "Office of the Speaker", "role": "Speaker", "access": "all"},
    "president": {"password": "unik2025", "dept": "Office of the President", "role": "President", "access": "all"},
    "patron": {"password": "unik2025", "dept": "Office of the Patron", "role": "Patron", "access": "all"},
    "principal": {"password": "unik2025", "dept": "Office of the Principal", "role": "Principal", "access": "all"},
    "general_secretary": {"password": "unik2025", "dept": "Office of the General Secretary", "role": "General Secretary", "access": "all"},
    "finance": {"password": "unik2025", "dept": "Finance Department", "role": "Finance", "access": "own"},
    "nursing": {"password": "unik2025", "dept": "Nursing Affairs", "role": "Nursing Affairs", "access": "own"},
    "info": {"password": "unik2025", "dept": "Information Department", "role": "Information", "access": "own"},
    "hostel_boys": {"password": "unik2025", "dept": "Boys Hostel", "role": "Hostel Leader Boys", "access": "own"},
    "hostel_girls": {"password": "unik2025", "dept": "Girls Hostel", "role": "Hostel Leader Girls", "access": "own"},
    "class_rep": {"password": "unik2025", "dept": "Class Representatives", "role": "Class Representative", "access": "own"},
    "grc_male": {"password": "unik2025", "dept": "GRC Male", "role": "GRC Male", "access": "own"},
    "grc_female": {"password": "unik2025", "dept": "GRC Female", "role": "GRC Female", "access": "own"},
}

def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["date","time","dept","role","report_type","title","content","status","submitted_by"])
        df.to_csv(DATA_FILE, index=False)
        return df
    return pd.read_csv(DATA_FILE)

def save_report(dept, role, report_type, title, content, submitted_by):
    df = load_data()
    now = datetime.datetime.now()
    new_row = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "dept": dept,
        "role": role,
        "report_type": report_type,
        "title": title,
        "content": content,
        "status": "Pending",
        "submitted_by": submitted_by
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#0A4A7A;'>🏛️ UNIK BEC-UNASNM<br>OFFICIAL GOVERNANCE PORTAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Office of the Speaker | Hon. Lawrence Ssango<br>Secure Department Access System</p>", unsafe_allow_html=True)
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("🔐 Department Login")
        username = st.text_input("Username").lower().strip()
        password = st.text_input("Password", type="password")
        if st.button("Login to Portal", use_container_width=True, type="primary"):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.dept = USERS[username]["dept"]
                st.session_state.role = USERS[username]["role"]
                st.session_state.access = USERS[username]["access"]
                st.rerun()
            else:
                st.error("Invalid username or password!")
    st.stop()

st.sidebar.markdown(f"### 🏛️ UNIK BEC-UNASNM\n**{st.session_state.dept}**\nRole: {st.session_state.role}")
st.sidebar.divider()
menu = st.sidebar.radio("Navigation", ["Dashboard", "Submit Report", "Letter Generator", "Archive"])
st.sidebar.divider()
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.markdown(f"## 🏛️ {st.session_state.dept} Portal")
st.markdown(f"**Role:** {st.session_state.role} | **Date:** {datetime.date.today().strftime('%d/%m/%Y')} | **Access:** {'All Departments' if st.session_state.access=='all' else 'Own Department Only'}")
st.divider()

df = load_data()
if st.session_state.access == "own":
    df_view = df[df["dept"] == st.session_state.dept]
else:
    df_view = df

if menu == "Dashboard":
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Reports", len(df_view))
    c2.metric("Pending", len(df_view[df_view["status"]=="Pending"]) if not df_view.empty else 0)
    c3.metric("Finance Reports", len(df[df["dept"]=="Finance Department"]))
    c4.metric("Hostel Reports", len(df[df["dept"].str.contains("Hostel", na=False)]))
    st.subheader("📋 Recent Reports")
    if df_view.empty:
        st.info("No reports submitted yet. Go to Submit Report to create your first report.")
    else:
        st.dataframe(df_view.sort_values(by=["date","time"], ascending=False), use_container_width=True)
        st.subheader("📖 Read Report Details")
        titles = df_view["title"].tolist()[::-1]
        selected = st.selectbox("Select report title to read", titles)
        if selected:
            row = df_view[df_view["title"]==selected].iloc[-1]
            st.markdown(f"""
            <div class="report-card">
                <h4 style="margin:0;">{row['title']}</h4>
                <p><b>Department:</b> {row['dept']} | <b>Role:</b> {row['role']} | <b>Date:</b> {row['date']} {row['time']} | <b>Type:</b> {row['report_type']} | <b>Status:</b> {row['status']}</p>
                <div class="report-content">{row['content']}</div>
            </div>
            """, unsafe_allow_html=True)

elif menu == "Submit Report":
    st.subheader("📝 Submit Official Report")
    report_type = st.selectbox("Report Type", ["Weekly Report","Financial Report","Hostel Report","Nursing Report","GRC Report","Class Report","Incident Report","Other"])
    title = st.text_input("Report Title")
    content = st.text_area("Report Content - Detailed Explanation", height=250, placeholder="Write full report here...")
    if st.button("📤 Submit Report to Speaker & President", type="primary"):
        if title and content:
            save_report(st.session_state.dept, st.session_state.role, report_type, title, content, st.session_state.username)
            st.success(f"Report '{title}' submitted successfully!")
            st.balloons()
        else:
            st.warning("Please fill Title and Content!")

elif menu == "Letter Generator":
    st.subheader("✉️ Official Letter Generator")
    to = st.text_input("To (e.g., Dean, Principal)")
    subject = st.text_input("Subject / RE:")
    body = st.text_area("Letter Body", height=250)
    if st.button("Generate Letter"):
        if to and subject and body:
            letter = f"""
UNIK BEC-UNASNM - OFFICE OF THE {st.session_state.role.upper()}
BWEYOGERE CAMPUS
Date: {datetime.date.today().strftime('%d %B %Y')}
To: {to}
RE: {subject}
Dear Sir/Madam,
{body}
Yours faithfully,
______________________________
{st.session_state.role}
{st.session_state.dept}
"""
            st.text_area("Generated Letter - Copy and Print", letter, height=350)
        else:
            st.warning("Fill all fields!")

elif menu == "Archive":
    st.subheader("📁 Archive - All Records")
    if df_view.empty:
        st.info("Archive is empty.")
    else:
        st.download_button("📥 Download CSV Backup", df_view.to_csv(index=False), file_name=f"unik_bec_archive_{datetime.date.today()}.csv", mime="text/csv")
        st.dataframe(df_view, use_container_width=True)
