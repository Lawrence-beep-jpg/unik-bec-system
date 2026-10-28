import streamlit as st
import pandas as pd
import datetime

# --- CONFIG ---
st.set_page_config(page_title="UNIK - University of Kisubi", page_icon="🏛️", layout="wide")

# --- USERS ---
USERS = {
    "principal": "Hon. Principal", "patron": "Hon. Patron", "president": "Hon. President UNASNM",
    "speaker": "Hon. Lawrence Ssango - Speaker BEC", "finance": "Hon. Finance",
    "general_secretary": "Hon. General Secretary", "information": "Hon. Information",
    "class_rep": "Hon. Class Rep", "grc_male": "Hon. GRC Male", "grc_female": "Hon. GRC Female",
    "hostel_male": "Hon. Hostel Male", "hostel_female": "Hon. Hostel Female",
    "nursing_affairs": "Hon. Nursing Affairs"
}
PASSWORD = "unik2025"
BOSSES = ["principal", "patron", "president", "speaker"]
REPORT_TYPES = ["Weekly Report", "Monthly Report", "Financial Report", "Activity Report", "GRC Report", "Hostel Report", "Emergency Report", "Other"]

if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🏛️ UNIK - University of Kisubi")
    st.subheader("School of Nursing and Midwifery - BEC-UNASNM Official Governance Portal")
    st.info("Office of the Speaker - Hon. Lawrence Ssango - Secure Department Access System")
    username = st.selectbox("Username", list(USERS.keys()))
    password = st.text_input("Password", type="password")
    if st.button("Login to Portal"):
        if password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Wrong Password!")
    st.stop()

user = st.session_state.user
st.sidebar.title(f"Logged as: {USERS[user]}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- ANALYTICS BOX - YOU ASKED FOR THIS ---
st.title(f"Dashboard - {USERS[user]}")
total = len(st.session_state.reports)
pending = len([r for r in st.session_state.reports if r['status']=="Pending"])
reviewed = len([r for r in st.session_state.reports if r['status']=="Reviewed"])
private = len([r for r in st.session_state.reports if r.get('private_reply')])

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Total Reports Submitted", total)
col2.metric("⏳ Pending Reports", pending)
col3.metric("✅ Reviewed", reviewed)
col4.metric("🔒 Private Replies", private)

# --- SUBMIT REPORT - WITH REPORT TYPE TABLE ---
tab1, tab2 = st.tabs(["📝 Submit Report", "📋 View All Reports + Private Reply"])

with tab1:
    st.subheader("Submit New Report")
    # THIS IS THE TABLE YOU SAID - REPORT TYPE
    report_type = st.selectbox("Which kind of report do you want to submit?", REPORT_TYPES)
    title = st.text_input("Report Title")
    content = st.text_area("Report Details", height=200)
    if st.button("Submit Report"):
        if title and content:
            st.session_state.reports.append({
                "id": len(st.session_state.reports)+1,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "from": user,
                "from_name": USERS[user],
                "type": report_type,
                "title": title,
                "content": content,
                "status": "Pending",
                "private_reply": "",
                "private_from": ""
            })
            st.success(f"{report_type} Submitted Successfully!")
        else:
            st.warning("Fill Title and Content!")

with tab2:
    st.subheader("All Reports - Table View")
    if not st.session_state.reports:
        st.info("No reports yet")
    else:
        # TABLE VIEW YOU ASKED FOR
        df = pd.DataFrame(st.session_state.reports)
        st.dataframe(df[["id","date","from_name","type","title","status"]], use_container_width=True)

        st.divider()
        for r in reversed(st.session_state.reports):
            # GRC VIEWER ONLY + BOSSES
            can_view = (user in BOSSES) or (user == r['from']) or (user.startswith("grc_") and r['type']=="GRC Report") or (user=="grc_male") or (user=="grc_female")
            
            # Private reply visible only to owner and bosses
            can_see_private = (user in BOSSES) or (user == r['from'])

            with st.expander(f"#{r['id']} | {r['type']} | {r['title']} - {r['from_name']} ({r['status']})"):
                st.write(f"**Date:** {r['date']}")
                st.write(f"**From:** {r['from_name']}")
                st.write(f"**Content:** {r['content']}")
                
                if r['private_reply'] and can_see_private:
                    st.warning(f"🔒 Private Reply from {r['private_from']}: {r['private_reply']}")
                
                if user in BOSSES:
                    new_status = st.selectbox(f"Change Status for #{r['id']}", ["Pending","Reviewed"], key=f"status{r['id']}")
                    if st.button(f"Update Status #{r['id']}", key=f"btnstatus{r['id']}"):
                        r['status'] = new_status
                        st.rerun()
                    
                    st.write("---")
                    st.write(f"🔒 Reply Privately to {r['from']}")
                    reply = st.text_area(f"Private feedback to {r['from']}", key=f"reply{r['id']}")
                    if st.button(f"Send Private Reply to {r['from']}", key=f"btnreply{r['id']}"):
                        r['private_reply'] = reply
                        r['private_from'] = USERS[user]
                        st.success("Private Reply Sent! Only that department + Bosses can see it")
                        st.rerun()
