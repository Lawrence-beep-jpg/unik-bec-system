import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="UNIK - University of Kisubi", page_icon="🏛️", layout="wide")

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
# ONLY THESE 5 CAN VIEW EVERYONE AS YOU REQUESTED
SUPER_VIEWERS = ["speaker", "president", "patron", "general_secretary", "principal"]
# PRIVATE PORTALS - NO ONE CAN VIEW PRINCIPAL & PATRON
ULTRA_PRIVATE = ["principal", "patron"]
REPORT_TYPES = ["Weekly Report", "Monthly Report", "Financial Report", "Activity Report", "GRC Report", "Hostel Report", "Nursing Affairs Report", "Other"]
DOC_CATEGORIES = ["Constitution", "Annual Work Plan", "Budget", "Meeting Minutes", "Strategic Plan", "Rules & Regulations", "Other Secret Document"]
ELECTION_POSITIONS = ["president", "speaker", "finance", "general_secretary", "information", "grc_male", "grc_female", "hostel_male", "hostel_female", "nursing_affairs"]

if 'reports' not in st.session_state:
    st.session_state.reports = []
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'candidates' not in st.session_state:
    st.session_state.candidates = []
if 'votes' not in st.session_state:
    st.session_state.votes = []
if 'media' not in st.session_state:
    st.session_state.media = [] # UNASNM Photos & Videos
if 'election_open' not in st.session_state:
    st.session_state.election_open = False
if 'election_title' not in st.session_state:
    st.session_state.election_title = "UNIK BEC General Elections 2025/2026"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""

if not st.session_state.logged_in:
    st.title("🏛️ UNIK - University of Kisubi")
    st.subheader("BEC-UNASNM Portal - Speaker Hon. Lawrence Ssango")
    c1,c2 = st.columns([1,1])
    with c1:
        st.markdown("#### Department Login")
        username = st.selectbox("Select Office", list(USERS.keys()))
        password = st.text_input("Password", type="password")
        if st.button("🔐 Login", use_container_width=True):
            if password == PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Wrong Password! Use unik2025")
    with c2:
        st.info("**NEW PRIVACY RULES:**\n\n✅ Only Speaker, President, Patron, Gen Sec, Principal can view all\n\n🔒 Principal & Patron portals are PRIVATE - No one can view them\n\n🗳️ Election + Media Gallery Added")
    st.stop()

user = st.session_state.user
user_full = USERS[user]

st.sidebar.title(f"👤 {user_full}")
if user in SUPER_VIEWERS:
    st.sidebar.success(f"✅ SUPER VIEWER - You can view all departments\nExcept Principal & Patron private")
    if user in ULTRA_PRIVATE:
        st.sidebar.warning("🔒 Your portal is ULTRA PRIVATE - No one else can view it")
else:
    st.sidebar.info("You can only view your own reports")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.title(f"Dashboard - {user_full}")
st.caption(f"{st.session_state.election_title} | {datetime.datetime.now().strftime('%A, %d %B %Y')}")

# Privacy function - YOUR REQUEST
def can_view_report(viewer, report_owner):
    # Principal and Patron are ultra private - only they can see their own
    if report_owner in ULTRA_PRIVATE:
        return viewer == report_owner
    # Super viewers can see everyone else
    if viewer in SUPER_VIEWERS:
        return True
    # Others can only see their own
    return viewer == report_owner

total = len([r for r in st.session_state.reports if can_view_report(user, r['from'])])
pending = len([r for r in st.session_state.reports if can_view_report(user, r['from']) and r['status']=="Pending"])
doc_total = len(st.session_state.documents)
cand_total = len(st.session_state.candidates)
votes_total = len(st.session_state.votes)
media_total = len(st.session_state.media)

col1,col2,col3,col4,col5,col6 = st.columns(6)
col1.metric("📊 Visible Reports", total)
col2.metric("⏳ Pending", pending)
col3.metric("🔐 Secrets", doc_total)
col4.metric("🗳️ Candidates", cand_total)
col5.metric("✅ Votes", votes_total)
col6.metric("📸 Media", media_total)

st.divider()

# TABS - 5 TABS NOW
if user in SUPER_VIEWERS:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Submit Report", "📋 View Reports (Privacy Applied)", "🔐 Secret Store", "🗳️ Election Portal", "📸 UNASNM Media Gallery"])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Submit Report", "📂 My Reports", "🔐 Secret Store", "🗳️ Vote & Register", "📸 Media Gallery"])

with tab1:
    st.subheader("Submit Report")
    report_type = st.selectbox("Report Type", REPORT_TYPES)
    title = st.text_input("Title *")
    content = st.text_area("Details *", height=180)
    if st.button("📤 Submit Report", type="primary", use_container_width=True):
        if title.strip() and content.strip():
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":report_type,"title":title.strip(),"content":content.strip(),"status":"Pending","private_reply":"","private_from":""})
            st.success("Report Submitted!"); st.balloons()
        else:
            st.warning("Fill Title and Details!")

with tab2:
    # Apply privacy filter
    visible_reports = [r for r in st.session_state.reports if can_view_report(user, r['from'])]
    
    if user in ULTRA_PRIVATE:
        st.warning(f"🔒 {user_full} - Your portal is ULTRA PRIVATE. No one else can see your reports, even other bosses.")
    
    if user in SUPER_VIEWERS and user not in ULTRA_PRIVATE:
        st.info(f"✅ You are one of the 5 Super Viewers: Speaker, President, Patron, General Secretary, Principal. You can view all departments EXCEPT Principal & Patron private portals")
    elif user in SUPER_VIEWERS and user in ULTRA_PRIVATE:
        st.info(f"✅ You are Super Viewer BUT your own portal is private. You can view all other departments except Patron/Principal's private reports")

    if not visible_reports:
        st.info("No reports visible for you (Privacy rules applied)")
    else:
        df = pd.DataFrame(visible_reports)
        st.dataframe(df[["id","date","from_name","type","title","status"]].sort_values(by="id",ascending=False), use_container_width=True, hide_index=True)
        st.divider()
        for r in reversed(visible_reports):
            with st.expander(f"#{r['id']} | {r['type']} | {r['title']} - {r['from_name']} ({r['status']})"):
                st.write(f"From: {r['from_name']} | Date: {r['date']} | Type: {r['type']}")
                st.info(r['content'])
                if r.get('private_reply'):
                    st.warning(f"🔒 Private Reply from {r['private_from']}: {r['private_reply']}")
                if user in SUPER_VIEWERS:
                    c1,c2 = st.columns(2)
                    with c1:
                        ns = st.selectbox(f"Status #{r['id']}",["Pending","Reviewed","Needs Revision"],key=f"s{r['id']}")
                        if st.button(f"Update #{r['id']}",key=f"bs{r['id']}"):
                            r['status']=ns; st.rerun()
                    with c2:
                        rt = st.text_area(f"Private to {r['from']}",key=f"r{r['id']}")
                        if st.button(f"Send Private #{r['id']}",key=f"br{r['id']}",type="primary"):
                            if rt.strip():
                                r['private_reply']=rt.strip(); r['private_from']=user_full; st.success("Sent!"); st.rerun()
                else:
                    if r.get('private_reply'):
                        st.success(f"Feedback: {r['private_reply']}")

with tab3:
    st.subheader("🔐 Secret Store - Constitution & Work Plans")
    if user in SUPER_VIEWERS:
        with st.expander("📤 Upload Secret Document (Super Viewers Only)", expanded=False):
            dc = st.selectbox("Category", DOC_CATEGORIES)
            dt = st.text_input("Title *")
            dd = st.text_area("Description")
            uf = st.file_uploader("File", type=None)
            if st.button("🔐 Save", type="primary", use_container_width=True):
                if dt.strip():
                    st.session_state.documents.append({"id":len(st.session_state.documents)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"category":dc,"title":dt.strip(),"description":dd,"file_name":uf.name if uf else "Text Note","file_bytes":uf.getvalue() if uf else None,"uploaded_by":user_full})
                    st.success("Saved!"); st.rerun()
    if not st.session_state.documents:
        st.warning("No documents yet")
    else:
        dfd = pd.DataFrame([{"ID":d["id"],"Category":d["category"],"Title":d["title"],"File":d["file_name"],"By":d["uploaded_by"]} for d in st.session_state.documents])
        st.dataframe(dfd, use_container_width=True, hide_index=True)
        for d in reversed(st.session_state.documents):
            with st.expander(f"{d['category']} | {d['title']}"):
                st.write(d['description'])
                if d['file_bytes']:
                    st.download_button(f"⬇️ Download {d['file_name']}", d['file_bytes'], d['file_name'], key=f"dl{d['id']}")
                if user in SUPER_VIEWERS:
                    if st.button(f"🗑️ Delete #{d['id']}", key=f"del{d['id']}"):
                        st.session_state.documents = [x for x in st.session_state.documents if x['id']!=d['id']]; st.rerun()

with tab4:
    st.subheader(f"🗳️ {st.session_state.election_title}")
    if user in SUPER_VIEWERS:
        c1,c2,c3 = st.columns(3)
        with c1:
            nt = st.text_input("Election Title", value=st.session_state.election_title)
            if st.button("Update Title"):
                st.session_state.election_title = nt; st.rerun()
        with c2:
            if not st.session_state.election_open:
                if st.button("🟢 OPEN VOTING", type="primary", use_container_width=True):
                    st.session_state.election_open = True; st.rerun()
            else:
                if st.button("🔴 CLOSE VOTING", use_container_width=True):
                    st.session_state.election_open = False; st.rerun()
        with c3:
            if st.button("🗑️ Reset Election"):
                st.session_state.candidates = []; st.session_state.votes = []; st.rerun()

    if st.session_state.election_open:
        st.success("🟢 VOTING OPEN - Share your Streamlit link!")
    else:
        st.warning("🔴 Voting CLOSED")

    ta, tb, tc = st.tabs(["📝 Register (Full Details)", "✅ Vote", "📊 Results"])
    with ta:
        st.markdown("#### Candidate Registration - Full Details As You Requested")
        st.info("Principal, Patron, Class Rep EXCLUDED - Only 10 BEC positions")
        rp = st.selectbox("Position to Contest", ELECTION_POSITIONS, format_func=lambda x: USERS[x])
        # NEW FIELDS AS YOU REQUESTED
        rn = st.text_input("Full Names *", value=user_full if user not in ULTRA_PRIVATE else "")
        rclass = st.text_input("Class *", placeholder="e.g. Year 2, Year 3")
        rcourse = st.text_input("Course *", placeholder="e.g. BSc Nursing, Diploma Midwifery")
        rresults = st.text_input("Previous UCE/UACE/UNEB Results *", placeholder="e.g. UCE: 1st Grade, UACE: 12 points, Previous Semester CGPA 4.2")
        rprev = st.text_input("Previous Leadership Experience", placeholder="e.g. Former Class Rep, Former GRC")
        rreason = st.text_area("Reason Why You Are Contesting For This Post *", height=150, placeholder="Type why you want this position, your vision for UNASNM...")
        rphoto = st.file_uploader("Upload Your Photo *", type=["jpg","jpeg","png"])
        
        if st.button("📝 Submit Candidature", type="primary", use_container_width=True):
            if rn.strip() and rclass.strip() and rcourse.strip() and rresults.strip() and rreason.strip() and rphoto:
                already = [c for c in st.session_state.candidates if c['registered_by']==user and c['position']==rp]
                if already:
                    st.error("You already registered for this position!")
                else:
                    st.session_state.candidates.append({
                        "id": len(st.session_state.candidates)+1,
                        "position": rp,
                        "position_name": USERS[rp],
                        "name": rn.strip(),
                        "class": rclass.strip(),
                        "course": rcourse.strip(),
                        "results": rresults.strip(),
                        "prev_exp": rprev.strip(),
                        "reason": rreason.strip(),
                        "photo_bytes": rphoto.getvalue(),
                        "registered_by": user,
                        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    })
                    st.success(f"Registered for {USERS[rp]}!"); st.balloons()
            else:
                st.warning("Please fill ALL * fields + Photo!")

    with tb:
        st.markdown("#### Vote")
        if not st.session_state.election_open:
            st.error("Voting CLOSED")
        elif not st.session_state.candidates:
            st.warning("No candidates")
        else:
            vp = st.selectbox("Position to Vote", ELECTION_POSITIONS, format_func=lambda x: USERS[x], key="vp")
            cands = [c for c in st.session_state.candidates if c['position']==vp]
            if not cands:
                st.info(f"No candidates for {USERS[vp]}")
            else:
                av = [v for v in st.session_state.votes if v['voter']==user and v['position']==vp]
                if av:
                    st.warning(f"You already voted for {USERS[vp]}")
                else:
                    cols = st.columns(2)
                    for idx, cand in enumerate(cands):
                        with cols[idx % 2]:
                            with st.container(border=True):
                                st.image(cand['photo_bytes'], width=200)
                                st.markdown(f"**{cand['name']}**")
                                st.caption(f"{cand['class']} | {cand['course']}")
                                st.write(f"Results: {cand['results']}")
                                st.write(f"Reason: {cand['reason'][:150]}...")
                                if st.button(f"✅ Vote {cand['name']}", key=f"vote{cand['id']}", type="primary", use_container_width=True):
                                    st.session_state.votes.append({"voter":user,"voter_name":user_full,"position":vp,"candidate_id":cand['id'],"candidate_name":cand['name'],"time":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                                    st.success(f"Voted for {cand['name']}!"); st.rerun()

    with tc:
        st.markdown("#### Live Results")
        if not st.session_state.candidates:
            st.info("No results")
        else:
            for pos in ELECTION_POSITIONS:
                cs = [c for c in st.session_state.candidates if c['position']==pos]
                if cs:
                    st.markdown(f"##### {USERS[pos]}")
                    rd = []
                    for c in cs:
                        vc = len([v for v in st.session_state.votes if v['candidate_id']==c['id']])
                        rd.append({"Candidate":c['name'],"Votes":vc,"Class":c['class'],"Course":c['course']})
                    df_res = pd.DataFrame(rd).sort_values(by="Votes", ascending=False)
                    st.bar_chart(df_res.set_index("Candidate")["Votes"])
                    st.dataframe(df_res, use_container_width=True, hide_index=True)
                    st.divider()

# NEW TAB 5 - UNASNM MEDIA GALLERY
with tab5:
    st.subheader("📸 UNASNM Media Gallery - Videos & Photos")
    st.info("Keep all UNASNM videos, photos, events here - For history and memories")
    
    if user in SUPER_VIEWERS:
        st.markdown("#### 📤 Upload UNASNM Photo/Video (Super Viewers Only)")
        m_title = st.text_input("Media Title *", placeholder="e.g. UNASNM Sports Day 2025, Nursing Conference")
        m_desc = st.text_area("Description / Event Details")
        m_category = st.selectbox("Category", ["Event Photos", "Event Videos", "Sports", "Conference", "Graduation", "Community Outreach", "Class Activities", "Other"])
        m_file = st.file_uploader("Upload Photo or Video", type=["jpg","jpeg","png","mp4","mov","avi","mp3","pdf"])
        
        if st.button("📸 Save to Gallery", type="primary", use_container_width=True):
            if m_title.strip() and m_file:
                st.session_state.media.append({
                    "id": len(st.session_state.media)+1,
                    "title": m_title.strip(),
                    "description": m_desc,
                    "category": m_category,
                    "file_name": m_file.name,
                    "file_bytes": m_file.getvalue(),
                    "file_type": m_file.type,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "by": user_full
                })
                st.success("Media Saved to Gallery!"); st.balloons(); st.rerun()
            else:
                st.warning("Enter Title and select file")
    
    st.divider()
    st.markdown(f"#### Gallery - Total Items: {len(st.session_state.media)}")
    if not st.session_state.media:
        st.warning("No media yet - Upload UNASNM photos & videos!")
    else:
        filter_media = st.selectbox("Filter by Category", ["All"] + ["Event Photos", "Event Videos", "Sports", "Conference", "Graduation", "Community Outreach", "Class Activities", "Other"])
        media_show = st.session_state.media
        if filter_media != "All":
            media_show = [m for m in media_show if m['category']==filter_media]
        
        # Grid view
        cols = st.columns(3)
        for idx, m in enumerate(reversed(media_show)):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"**{m['title']}**")
                    st.caption(f"{m['category']} | {m['date']} | By {m['by']}")
                    if m['file_type'].startswith("image"):
                        st.image(m['file_bytes'], use_container_width=True)
                    elif m['file_type'].startswith("video"):
                        st.video(m['file_bytes'])
                    else:
                        st.write(f"File: {m['file_name']}")
                    if m['description']:
                        st.write(m['description'][:100])
                    st.download_button(f"⬇️ Download", m['file_bytes'], m['file_name'], key=f"meddl{m['id']}")
                    if user in SUPER_VIEWERS:
                        if st.button(f"🗑️ Delete #{m['id']}", key=f"delmed{m['id']}"):
                            st.session_state.media = [x for x in st.session_state.media if x['id']!=m['id']]
                            st.rerun()
