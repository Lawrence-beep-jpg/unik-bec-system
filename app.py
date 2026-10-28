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
.feedback-card {background-color: #FFF3E0; padding: 15px; border-radius: 8px; border-left: 5px solid #EF6C00; margin-top:10px;}
</style>
""", unsafe_allow_html=True)

USERS = {
    "principal": {"name": "Principal, UNIK - University of Kisubi", "role": "Principal - UNIK", "password": "unik2025"},
    "patron": {"name": "Patron UNASNM - UNIK", "role": "Patron UNASNM", "password": "unik2025"},
    "president": {"name": "President BEC - UNIK", "role": "President BEC", "password": "unik2025"},
    "speaker": {"name": "Hon. Lawrence Ssango - Speaker BEC", "role": "Speaker BEC - Office of the Speaker", "password": "unik2025"},
    "finance": {"name": "Finance Secretary BEC", "role": "Finance BEC", "password": "unik2025"},
    "general_secretary": {"name": "General Secretary BEC", "role": "General Secretary BEC", "password": "unik2025"},
    "information": {"name": "Information Ministry BEC", "role": "Information BEC", "password": "unik2025"},
    "class_rep": {"name": "Class Representatives", "role": "Class Representatives", "password": "unik2025"},
    "grc_male": {"name": "GRC Male / Galaxy Male", "role": "GRC Male - Viewer Only", "password": "unik2025"},
    "grc_female": {"name": "GRC Female / Galaxy Female", "role": "GRC Female - Viewer Only", "password": "unik2025"},
    "hostel_male": {"name": "Male Hostel Representative", "role": "Hostel Rep Male", "password": "unik2025"},
    "hostel_female": {"name": "Female Hostel Representative", "role": "Hostel Rep Female", "password": "unik2025"},
    "nursing_affairs": {"name": "Nursing Affairs / Non-Resident", "role": "Nursing Affairs", "password": "unik2025"},
}

REPORT_FILE = "unik_reports_permanent.csv"
FEEDBACK_FILE = "unik_private_feedback.csv"

CAN_REPLY = ["principal", "patron", "president", "speaker"]
IS_ADMIN = ["principal", "patron", "president", "speaker", "general_secretary"]

def load_reports():
    if os.path.exists(REPORT_FILE):
        try: return pd.read_csv(REPORT_FILE)
        except: return pd.DataFrame(columns=["timestamp", "username", "department", "title", "report"])
    else:
        df = pd.DataFrame(columns=["timestamp", "username", "department", "title", "report"])
        df.to_csv(REPORT_FILE, index=False)
        return df

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        try: return pd.read_csv(FEEDBACK_FILE)
        except: return pd.DataFrame(columns=["timestamp", "reply_from", "reply_to_user", "report_title", "report_timestamp", "feedback"])
    else:
        df = pd.DataFrame(columns=["timestamp", "reply_from", "reply_to_user", "report_title", "report_timestamp", "feedback"])
        df.to_csv(FEEDBACK_FILE, index=False)
        return df

def save_report(username, title, report_text):
    df = load_reports()
    new_row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "username": username, "department": USERS[username]["role"], "title": title, "report": report_text}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(REPORT_FILE, index=False)

def save_feedback(reply_from, reply_to_user, report_title, report_timestamp, feedback_text):
    df = load_feedback()
    new_row = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "reply_from": reply_from, "reply_to_user": reply_to_user, "report_title": report_title, "report_timestamp": report_timestamp, "feedback": feedback_text}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#1565C0;'>🏛️ UNIK - UNIVERSITY OF KISUBI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'><b>School of Nursing and Midwifery<br>BEC-UNASNM Official Governance Portal<br>Office of the Speaker - Hon. Lawrence Ssango</b><br>Secure Department Access System</p>", unsafe_allow_html=True)
    st.markdown("---")
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        st.subheader("🔐 Department Login")
        u = st.text_input("Username").lower().strip()
        p = st.text_input("Password", type="password")
        st.info("13 Offices: principal, patron, president, speaker, finance, general_secretary, information, class_rep, grc_male, grc_female, hostel_male, hostel_female, nursing_affairs | Pass: unik2025")
        if st.button("Login to Portal", use_container_width=True, type="primary"):
            if u in USERS and p == USERS[u]["password"]:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else: st.error("❌ Wrong username or password!")
else:
    user = USERS[st.session_state.username]
    cur_user = st.session_state.username
    with st.sidebar:
        st.success(f"Logged as: {user['name']}")
        st.caption(f"Role: {user['role']}")
        if cur_user in CAN_REPLY: st.info("✅ You CAN reply privately")
        else: st.warning("🔒 You CANNOT reply - Viewer/Submit only")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    reports_df = load_reports()
    feedback_df = load_feedback()

    # ADMIN VIEW - Principal, Patron, President, Speaker, General Secretary
    if cur_user in IS_ADMIN:
        st.title(f"📊 Dashboard - {user['name']}")
        tab1, tab2 = st.tabs(["📄 View All Reports + Private Reply", "✍️ Submit Report"])
        with tab1:
            if reports_df.empty: st.warning("No reports yet")
            else:
                for idx, row in reports_df.sort_values(by="timestamp", ascending=False).iterrows():
                    st.markdown(f"""<div class="report-card"><h4 style="color:#0D47A1; margin:0;">{row['title']} - {row['department']}</h4><small style="color:#555;">{row['timestamp']} | By: {row['username']}</small><div class="report-inner"><p>{row['report']}</p></div></div>""", unsafe_allow_html=True)
                    
                    # Show private feedbacks for this report
                    related_fb = feedback_df[(feedback_df["report_title"]==row["title"]) & (feedback_df["report_timestamp"]==row["timestamp"])]
                    if not related_fb.empty:
                        for f_idx, f_row in related_fb.iterrows():
                            st.markdown(f"""<div class="feedback-card"><b>🔒 Private Reply from {USERS[f_row['reply_from']]['name']} to {f_row['reply_to_user']}:</b><br><small>{f_row['timestamp']}</small><br><p style="color:black;">{f_row['feedback']}</p></div>""", unsafe_allow_html=True)
                    
                    # ONLY 4 can reply
                    if cur_user in CAN_REPLY:
                        with st.expander(f"🔒 Reply Privately to {row['username']} - {row['title']}"):
                            fb_text = st.text_area(f"Private feedback for {row['username']}", key=f"fb_{idx}_{row['timestamp']}", height=100)
                            if st.button(f"Send Private Reply to {row['username']}", key=f"btn_{idx}_{row['timestamp']}"):
                                if fb_text:
                                    save_feedback(cur_user, row["username"], row["title"], row["timestamp"], fb_text)
                                    st.success(f"✅ Private reply sent to {row['username']}! Only you 4 bosses and {row['username']} will see it.")
                                    st.rerun()
                                else: st.error("Type feedback first")
                    st.markdown("---")
                st.download_button("📥 Download Reports CSV", reports_df.to_csv(index=False).encode('utf-8'), "unik_reports.csv")
                st.download_button("📥 Download Private Feedbacks CSV", feedback_df.to_csv(index=False).encode('utf-8'), "unik_private_feedback.csv")

        with tab2:
            t = st.text_input("Report Title")
            r = st.text_area("Report Content", height=250)
            if st.button("Submit Report", type="primary"):
                if t and r:
                    save_report(cur_user, t, r)
                    st.success("✅ Report submitted permanently!")
                    st.rerun()
    # NORMAL USER VIEW
    else:
        st.title(f"✍️ {user['name']}")
        if cur_user in ["grc_male", "grc_female"]:
            st.warning("🔒 GRC Account: You can VIEW and SUBMIT reports, but you CANNOT reply to others. Only Speaker, President, Patron, Principal can reply.")
        
        st.subheader("Submit Weekly Report")
        t = st.text_input("Report Title")
        r = st.text_area("Detailed Report", height=300)
        if st.button("Submit Report Permanently", type="primary", use_container_width=True):
            if t and r:
                save_report(cur_user, t, r)
                st.success("✅ Report submitted!")
                st.balloons()
                st.rerun()
        
        # Show my reports + private feedbacks I received
        my_reports = reports_df[reports_df["username"] == cur_user]
        if not my_reports.empty:
            st.markdown("---")
            st.subheader("My Previous Reports + Private Feedback Received")
            for idx, row in my_reports.sort_values(by="timestamp", ascending=False).iterrows():
                st.markdown(f"""<div class="report-card"><h4 style="color:#0D47A1;">{row['title']}</h4><small>{row['timestamp']}</small><div class="report-inner"><p>{row['report']}</p></div></div>""", unsafe_allow_html=True)
                my_fb = feedback_df[feedback_df["reply_to_user"]==cur_user]
                my_fb = my_fb[(my_fb["report_title"]==row["title"]) & (my_fb["report_timestamp"]==row["timestamp"])]
                if not my_fb.empty:
                    for f_idx, f_row in my_fb.iterrows():
                        st.markdown(f"""<div class="feedback-card"><b>🔒 Private Reply from {USERS[f_row['reply_from']]['name']}:</b><br><small>{f_row['timestamp']}</small><br><p style="color:black;">{f_row['feedback']}</p></div>""", unsafe_allow_html=True)
