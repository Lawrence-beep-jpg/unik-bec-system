import streamlit as st
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="UNIK - University of Kisubi", page_icon="🏛️", layout="wide")

# --- USERS - ALL 13 OFFICES ONLY ---
USERS = {
    "principal": "Hon. Principal - University of Kisubi",
    "patron": "Hon. Patron - UNASNM",
    "president": "Hon. President - UNASNM BEC",
    "speaker": "Hon. Lawrence Ssango - Speaker BEC",
    "finance": "Hon. Finance Secretary",
    "general_secretary": "Hon. General Secretary",
    "information": "Hon. Information Secretary",
    "class_rep": "Hon. Class Representative",
    "grc_male": "Hon. GRC - Male",
    "grc_female": "Hon. GRC - Female",
    "hostel_male": "Hon. Hostel - Male",
    "hostel_female": "Hon. Hostel - Female",
    "nursing_affairs": "Hon. Nursing Affairs"
}
PASSWORD = "unik2025"
BOSSES = ["principal", "patron", "president", "speaker"]
REPORT_TYPES = ["Weekly Report", "Monthly Report", "Financial Report", "Activity Report", "GRC Report", "Hostel Report", "Nursing Affairs Report", "Other"]
# NEW - SECRET STORE CATEGORIES
DOC_CATEGORIES = ["Constitution", "Annual Work Plan", "Budget", "Meeting Minutes", "Strategic Plan", "Rules & Regulations", "Other Secret Document"]

if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""

# --- LOGIN ---
if not st.session_state.logged_in:
    st.title("🏛️ UNIK - University of Kisubi")
    st.subheader("School of Nursing and Midwifery")
    st.markdown("### BEC-UNASNM Official Governance Portal")
    st.info("Office of the Speaker - Hon. Lawrence Ssango - Secure Department Access System")
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("#### Department Login")
        username = st.selectbox("Select Your Office / Username", list(USERS.keys()))
        password = st.text_input("Password", type="password")
        if st.button("🔐 Login to Portal", use_container_width=True):
            if password == PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Wrong Password! Use unik2025")
    with col2:
        st.markdown("#### 13 Offices - BEC")
        for k,v in USERS.items():
            st.write(f"- {v} (`{k}`)")
    st.stop()

user = st.session_state.user
user_full = USERS[user]

st.sidebar.title(f"👤 {user_full}")
st.sidebar.write(f"Username: `{user}`")
st.sidebar.divider()
if user in BOSSES:
    st.sidebar.success("✅ Boss - You can send Private Reply & Upload Secrets")
else:
    st.sidebar.info("You can view Secret Store")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

st.title(f"📊 Dashboard - {user_full}")
st.caption(f"BEC-UNASNM | {datetime.datetime.now().strftime('%A, %d %B %Y')}")

# --- ANALYTICS ---
total = len(st.session_state.reports)
pending = len([r for r in st.session_state.reports if r['status']=="Pending"])
reviewed = len([r for r in st.session_state.reports if r['status']=="Reviewed"])
private_count = len([r for r in st.session_state.reports if r.get('private_reply')])
doc_total = len(st.session_state.documents)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📊 Total Reports", total)
col2.metric("⏳ Pending", pending)
col3.metric("✅ Reviewed", reviewed)
col4.metric("🔒 Private Replies", private_count)
col5.metric("🔐 Secret Docs", doc_total)

if total > 0:
    df_all = pd.DataFrame(st.session_state.reports)
    dept_counts = df_all['from_name'].value_counts().reset_index()
    dept_counts.columns = ['Department', 'Number of Reports']
    st.markdown("#### 📋 Reports by Department - 13 Departments")
    st.dataframe(dept_counts, use_container_width=True, hide_index=True)

st.divider()

if user in BOSSES:
    tab1, tab2, tab3 = st.tabs(["📝 Submit Report", "📋 View All Reports + Private Reply", "🔐 Secret Store - Constitution & Plans"])
else:
    tab1, tab2, tab3 = st.tabs(["📝 Submit Report", "📂 My Previous Reports + Private Feedback", "🔐 Secret Store - View Constitution & Plans"])

with tab1:
    st.subheader("Submit New Report")
    st.markdown("**Which kind of report do you want to submit?**")
    report_type = st.selectbox("Report Type", REPORT_TYPES)
    title = st.text_input("Report Title *")
    content = st.text_area("Report Details *", height=220)
    if st.button("📤 Submit Report", type="primary", use_container_width=True):
        if title.strip() and content.strip():
            st.session_state.reports.append({
                "id": len(st.session_state.reports)+1,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "from": user,
                "from_name": user_full,
                "type": report_type,
                "title": title.strip(),
                "content": content.strip(),
                "status": "Pending",
                "private_reply": "",
                "private_from": ""
            })
            st.success(f"✅ {report_type} Submitted!")
            st.balloons()
        else:
            st.warning("Fill Title and Details!")

with tab2:
    if user in BOSSES:
        st.subheader("All Reports - Full Table View")
        if not st.session_state.reports:
            st.info("No reports yet")
        else:
            df = pd.DataFrame(st.session_state.reports)
            st.dataframe(df[["id","date","from_name","type","title","status"]].sort_values(by="id", ascending=False), use_container_width=True, hide_index=True)
            st.divider()
            st.markdown("### Detailed View + Private Reply")
            filter_dept = st.selectbox("Filter by Department", ["All"] + list(USERS.keys()))
            reports_to_show = st.session_state.reports
            if filter_dept != "All":
                reports_to_show = [r for r in reports_to_show if r['from']==filter_dept]
            for r in reversed(reports_to_show):
                with st.expander(f"#{r['id']} | {r['type']} | {r['title']} - {r['from_name']} ({r['status']})"):
                    st.write(f"**From:** {r['from_name']}")
                    st.write(f"**Date:** {r['date']}")
                    st.write(f"**Type:** {r['type']}")
                    st.info(r['content'])
                    if r.get('private_reply'):
                        st.warning(f"🔒 Private Reply from {r['private_from']}: {r['private_reply']}")
                    st.markdown("---")
                    c1, c2 = st.columns(2)
                    with c1:
                        new_status = st.selectbox(f"Status #{r['id']}", ["Pending","Reviewed","Needs Revision"], index=0, key=f"status{r['id']}")
                        if st.button(f"Update Status #{r['id']}", key=f"btnstatus{r['id']}"):
                            r['status'] = new_status
                            st.rerun()
                    with c2:
                        reply_text = st.text_area(f"Private feedback to {r['from']}", key=f"reply{r['id']}")
                        if st.button(f"Send Private Reply to {r['from']}", key=f"btnreply{r['id']}", type="primary"):
                            if reply_text.strip():
                                r['private_reply'] = reply_text.strip()
                                r['private_from'] = user_full
                                st.success(f"Private Reply Sent to {r['from_name']}!")
                                st.rerun()
    else:
        st.subheader("My Reports + Private Feedback")
        my_reports = [r for r in st.session_state.reports if r['from']==user]
        if not my_reports:
            st.info("No reports yet")
        else:
            if user.startswith("grc_"):
                st.markdown("**GRC View - You can view GRC Reports**")
                grc_reports = [r for r in st.session_state.reports if r['type']=="GRC Report"]
                if grc_reports:
                    st.dataframe(pd.DataFrame(grc_reports)[["id","date","from_name","type","title","status"]], use_container_width=True)
            for r in reversed(my_reports):
                with st.expander(f"#{r['id']} | {r['type']} | {r['title']} - {r['status']}"):
                    st.write(f"**Content:** {r['content']}")
                    if r.get('private_reply'):
                        st.success(f"🔒 Private Feedback from {r['private_from']}:")
                        st.warning(r['private_reply'])

# --- NEW TAB 3 - SECRET STORE ---
with tab3:
    st.subheader("🔐 Secret Store - Constitution, Work Plans & Special Documents")
    st.info("This is the secure vault for BEC secrets. Only Bosses can upload. All 13 offices can view/download.")

    if user in BOSSES:
        st.markdown("#### 📤 Upload Secret Document (Bosses Only)")
        doc_cat = st.selectbox("Document Category", DOC_CATEGORIES)
        doc_title = st.text_input("Document Title *", placeholder="e.g. UNASNM Constitution 2025")
        doc_desc = st.text_area("Description / Notes", placeholder="Brief description...")
        uploaded_file = st.file_uploader("Choose File (PDF, DOCX, XLSX, Image, etc)", type=None)
        
        if st.button("🔐 Save to Secret Store", type="primary", use_container_width=True):
            if doc_title.strip() and uploaded_file is not None:
                file_bytes = uploaded_file.getvalue()
                st.session_state.documents.append({
                    "id": len(st.session_state.documents)+1,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "category": doc_cat,
                    "title": doc_title.strip(),
                    "description": doc_desc,
                    "file_name": uploaded_file.name,
                    "file_bytes": file_bytes,
                    "uploaded_by": user_full
                })
                st.success(f"✅ {doc_cat} - {doc_title} Saved to Secret Store!")
                st.balloons()
            elif doc_title.strip() and not uploaded_file:
                # Allow saving without file as text note
                st.session_state.documents.append({
                    "id": len(st.session_state.documents)+1,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "category": doc_cat,
                    "title": doc_title.strip(),
                    "description": doc_desc,
                    "file_name": "Text Note",
                    "file_bytes": None,
                    "uploaded_by": user_full
                })
                st.success(f"✅ {doc_title} Saved as Text Note!")
            else:
                st.warning("Please enter Title and select a file")

        st.divider()

    # VIEW ALL DOCUMENTS
    st.markdown(f"#### 📚 Stored Documents - Total: {len(st.session_state.documents)}")
    if not st.session_state.documents:
        st.warning("No secret documents yet. Bosses should upload Constitution and Annual Work Plan.")
    else:
        filter_cat = st.selectbox("Filter by Category", ["All"] + DOC_CATEGORIES)
        docs_to_show = st.session_state.documents
        if filter_cat != "All":
            docs_to_show = [d for d in docs_to_show if d['category']==filter_cat]
        
        df_docs = pd.DataFrame([{"ID":d["id"], "Date":d["date"], "Category":d["category"], "Title":d["title"], "File":d["file_name"], "By":d["uploaded_by"]} for d in docs_to_show])
        st.dataframe(df_docs.sort_values(by="ID", ascending=False), use_container_width=True, hide_index=True)
        
        for d in reversed(docs_to_show):
            with st.expander(f"🔐 {d['category']} | {d['title']} - {d['file_name']}"):
                st.write(f"**Category:** {d['category']}")
                st.write(f"**Title:** {d['title']}")
                st.write(f"**Date:** {d['date']} | **By:** {d['uploaded_by']}")
                if d['description']:
                    st.info(f"Description: {d['description']}")
                if d['file_bytes']:
                    st.download_button(f"⬇️ Download {d['file_name']}", data=d['file_bytes'], file_name=d['file_name'], key=f"dl{d['id']}")
                if user in BOSSES:
                    if st.button(f"🗑️ Delete This Document #{d['id']}", key=f"deldoc{d['id']}"):
                        st.session_state.documents = [x for x in st.session_state.documents if x['id']!=d['id']]
                        st.success("Document Deleted from Secret Store")
                        st.rerun()
