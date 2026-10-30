import streamlit as st, os, json, datetime, pandas as pd
from datetime import datetime as dt
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# --- INIT DIRECTORIES ---
os.makedirs("data/media_files", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)
os.makedirs("data/personal", exist_ok=True)

FILES = {
    "reports": "data/reports.json",
    "media": "data/media.json",
    "candidates": "data/candidates.json",
    "pending": "data/pending.json",
    "votes": "data/votes.json",
    "cabinets": "data/cabinets.json",
    "docs": "data/docs.json",
    "finance": "data/finance.json",
    "disc": "data/disc.json",
    "gp": "data/gp.json",
    "passwords": "data/passwords.json",
    "uploaded": "data/uploaded_docs.json",
    "ann": "data/announcements.json",
    "meet": "data/meetings.json",
    "personal": "data/personal.json",
    "audit": "data/audit.json",
    "tasks": "data/tasks.json",
    "budget": "data/budget.json",
}

def load_json(p, d):
    if os.path.exists(p):
        try:
            with open(p, 'r') as f:
                return json.load(f)
        except:
            return d
    return d

def save_json(p, data):
    with open(p, 'w') as f:
        json.dump(data, f, default=str, indent=2)

def add_audit(action, user_full, details=""):
    audit = load_json(FILES["audit"], [])
    audit.append({"id": len(audit)+1, "time": dt.now().strftime("%Y-%m-%d %H:%M:%S"), "user": user_full, "action": action, "details": details})
    save_json(FILES["audit"], audit)

is_public = st.query_params.get("public", "") == "vote"

st.markdown("<h2 style='text-align:center; color:#1a5c2a;'>🏛️ UNIK BEC UNASNM<br>Governance Portal - 800+ Edition</h2><p style='text-align:center;'>Bishop Cipriano Kihangire University - School of Nursing & Midwifery</p>", unsafe_allow_html=True)

USERS = {
    "principal": "Principal - School Head",
    "patron": "Hon. Patron - Staff Patron",
    "president": "His Excellency President - UNASNM President",
    "vice_president": "Hon. Vice President - Leader GP",
    "speaker": "Right Honourable Speaker - Hon. Lawrence Ssango",
    "general_secretary": "Hon. General Secretary",
    "finance": "Hon. Finance Secretary",
    "information": "Hon. Information Secretary",
    "class_rep": "Hon. Class Representative",
    "grc_male": "Hon. GRC Male",
    "grc_female": "Hon. GRC Female",
    "hostel_male": "Hon. Hostel Male",
    "hostel_female": "Hon. Hostel Female",
    "nursing_affairs": "Hon. Nursing Affairs Secretary"
}
LOGIN_USERS = list(USERS.keys())
SUPER_4 = ["principal", "patron", "president", "speaker"]
FINANCE_5 = ["principal", "patron", "president", "speaker", "finance"]

ELECTION_POS = ["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]
REPORT_TYPES = ["Weekly","Monthly","Financial","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Audit","Budget","Other"]
DOC_CATS = ["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint","Public Information","Meeting Minutes","Academic","Welfare","Nursing Affairs"]

# Load session
for k, f in FILES.items():
    if k not in st.session_state:
        if k == "passwords":
            pw = load_json(f, {})
            st.session_state[k] = pw if pw else {u: "unik2025" for u in LOGIN_USERS}
        else:
            st.session_state[k] = load_json(f, [])

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""

# PUBLIC VOTING PAGE
if is_public:
    st.markdown("<h3 style='text-align:center;'>🗳️ PUBLIC ELECTORAL COMMISSION - UNIK BEC</h3><p style='text-align:center;'>One Email = One Vote - Secured</p>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["📝 Apply Candidate", "✅ Vote One Email Once", "📊 Live Results"])
    with t1:
        st.info("Apply - Needs Speaker Approval")
        rp = st.selectbox("Position", ELECTION_POS, format_func=lambda x: USERS[x], key="pub_pos")
        c1, c2 = st.columns(2)
        rn = c1.text_input("Full Names *", key="pub_name")
        rclass = c2.text_input("Class * e.g. BNS 3", key="pub_class")
        remail = st.text_input("Email *", key="pub_email")
        rreason = st.text_area("Why should students vote you? *", key="pub_reason", height=120)
        rphoto = st.file_uploader("Passport Photo *", type=["jpg","png","jpeg"], key="pub_photo")
        if st.button("Submit Application (Speaker Will Approve)", type="primary", use_container_width=True):
            if not rn or not rclass or not remail or not rreason or not rphoto:
                st.error("Fill ALL fields *")
            else:
                nid = len(st.session_state.pending) + len(st.session_state.candidates) + 1
                fpath = f"data/media_files/cand_{nid}.jpg"
                open(fpath, 'wb').write(rphoto.getvalue())
                st.session_state.pending.append({"id": nid, "position": rp, "name": rn, "class": rclass, "email": remail, "reason": rreason, "photo_path": fpath, "date": str(dt.now())[:16], "status": "pending"})
                save_json(FILES["pending"], st.session_state.pending)
                add_audit("New Candidate Applied", rn, f"Position {USERS[rp]}")
                st.success("Sent to Speaker! Wait approval.")
                st.balloons()
    with t2:
        voter_email = st.text_input("Your University Email * - One vote per position", key="pub_voter_email")
        if voter_email and "@" in voter_email:
            vp = st.selectbox("Choose Position to Vote", ELECTION_POS, format_func=lambda x: USERS[x], key="pub_vote_pos")
            already = [v for v in st.session_state.votes if v.get('voter_email','').lower()==voter_email.lower() and v['position']==vp]
            if already:
                st.error(f"❌ You already voted for {USERS[vp]} with this email! One email once!")
            else:
                candidates_here = [x for x in st.session_state.candidates if x['position']==vp]
                if not candidates_here:
                    st.warning(f"No approved candidates for {USERS[vp]} yet")
                for c in candidates_here:
                    with st.container(border=True):
                        col1, col2 = st.columns([1,3])
                        if os.path.exists(c.get('photo_path','')):
                            col1.image(c.get('photo_path',''), width=130)
                        col2.write(f"**{c['name']}** - {c.get('class','')}"); col2.info(c.get('reason',''))
                        if col2.button(f"VOTE {c['name']}", key=f"pv_{c['id']}_{voter_email}", type="primary", use_container_width=True):
                            st.session_state.votes.append({"candidate_id": c['id'], "voter_email": voter_email.lower(), "position": vp, "candidate_name": c['name'], "date": str(dt.now())})
                            save_json(FILES["votes"], st.session_state.votes)
                            add_audit("Public Vote Cast", voter_email, f"Voted {c['name']} for {vp}")
                            st.success(f"Voted {c['name']}!"); st.balloons(); st.rerun()
        else:
            st.warning("Enter valid university email to vote")
    with t3:
        votes = load_json(FILES["votes"], st.session_state.votes)
        st.success(f"Total Votes Cast: {len(votes)}")
        for pos in ELECTION_POS:
            cs = [c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd = [{"Candidate": cc['name'], "Class": cc.get('class',''), "Votes": len([v for v in votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(f"**{USERS[pos]} - Results**")
                    df = pd.DataFrame(rd).sort_values("Votes", ascending=False)
                    st.dataframe(df, use_container_width=True)
                    st.bar_chart(df.set_index("Candidate")["Votes"])
    st.stop()

# LOGIN PAGE
if not st.session_state.logged_in:
    st.markdown("### 🔐 Cabinet Login - 13 Departments Only - UNIK BEC")
    col1, col2 = st.columns([2,1])
    with col1:
        u = st.selectbox("Select Your Office (13 Departments)", LOGIN_USERS, format_func=lambda x: USERS[x], key="login")
        p = st.text_input("Password - My Bottle - Changeable", type="password", key="pass")
        if st.button("LOGIN TO PORTAL", type="primary", use_container_width=True):
            if p == st.session_state.passwords.get(u, "unik2025"):
                st.session_state.logged_in = True
                st.session_state.user = u
                add_audit("Login", USERS[u], f"User {u} logged in")
                st.rerun()
            else:
                st.error("Wrong password! Default is unik2025")
    with col2:
        st.info("**Default Password:**\\nunik2025\\n\\n**Public Vote:**\\n?public=vote\\n\\n**My Bottle:** Each office has own password, changeable in sidebar")
        st.warning("Speaker: Hon. Lawrence Ssango")
    st.stop()

# AUTHENTICATED
user = st.session_state.user
user_full = USERS[user]

st.sidebar.title(user_full)
st.sidebar.success(f"Logged: {user_full} | ID: {user}")
st.sidebar.caption(f"Time: {dt.now().strftime('%d-%m-%Y %H:%M')}")

# Change password - My Bottle
with st.sidebar.expander("🔑 Change My Password - My Bottle - Personal"):
    cur = st.text_input("Current Password", type="password", key="cur_pw")
    new = st.text_input("New Password", type="password", key="new_pw")
    conf = st.text_input("Confirm New Password", type="password", key="conf_pw")
    if st.button("Save My New Bottle Password", key="save_pw"):
        if cur != st.session_state.passwords.get(user, "unik2025"):
            st.sidebar.error("Wrong current password")
        elif len(new) < 4:
            st.sidebar.error("Password too short - min 4")
        elif new != conf:
            st.sidebar.error("New passwords don't match")
        else:
            st.session_state.passwords[user] = new
            save_json(FILES["passwords"], st.session_state.passwords)
            add_audit("Password Changed", user_full, "Changed personal bottle")
            st.sidebar.success(f"✅ Changed! New: {new} - Remember it!")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    add_audit("Logout", user_full, "Logged out")
    st.session_state.logged_in = False
    st.session_state.user = ""
    st.rerun()

# DASHBOARD STATS
reports = load_json(FILES["reports"], st.session_state.reports)
media = load_json(FILES["media"], st.session_state.media)
candidates = load_json(FILES["candidates"], st.session_state.candidates)
votes = load_json(FILES["votes"], st.session_state.votes)
docs_uploaded = load_json(FILES["uploaded"], st.session_state.uploaded)

st.sidebar.divider()
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Reports", len(reports))
st.sidebar.metric("Media", len(media))
st.sidebar.metric("Docs", len(docs_uploaded))
st.sidebar.metric("Votes", len(votes))

# MAIN TABS - 15 TABS - 800+ EDITION
tabs = st.tabs([
    "📊 Dashboard", "👤 My Personal Portal", "📢 Public Portal OPEN 13", "🎥 Meeting OPEN 13",
    "📝 Submit Report", "🔒 Private SUPER 4", "🗳️ Electoral OPEN 13", "⚖️ Disciplinary OPEN 13",
    "📋 GP OPEN 13", "💰 Finance 5 ONLY", "🔐 Secret OPEN 13", "📄 Documents OPEN 13",
    "📸 Media Gallery OPEN 13", "🏛️ Cabinet Archive OPEN 13", "📜 Audit Log"
])

# TAB 0 DASHBOARD
with tabs[0]:
    st.subheader(f"📊 Dashboard - Welcome {user_full}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reports", len(reports), f"From {len(set([r['from'] for r in reports]))} offices")
    c2.metric("Media Files", len(media))
    c3.metric("Documents", len(docs_uploaded))
    c4.metric("Total Votes", len(votes))
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Recent Reports (Last 5)**")
        for r in reversed(reports[-5:]):
            st.info(f"{r['date']} | {r['from_name']}: {r['title']}")
    with c2:
        st.write("**Recent Media (Last 5)**")
        for m in reversed(media[-5:]):
            st.success(f"{m['date']} | {m['by']}: {m['title']}")
    st.divider()
    st.write("**Election Results Overview**")
    for pos in ELECTION_POS[:5]:
        cs = [c for c in candidates if c['position']==pos]
        if cs:
            rd = [{"Candidate": cc['name'], "Votes": len([v for v in votes if v['candidate_id']==cc['id']])} for cc in cs]
            if sum([x['Votes'] for x in rd])>0:
                st.write(f"{USERS[pos]}")
                st.bar_chart(pd.DataFrame(rd).set_index("Candidate"))

# TAB 1 MY PERSONAL PORTAL - ONLY OWNER
with tabs[1]:
    st.subheader(f"👤 My Personal Portal - ONLY YOU CAN OPEN - {user_full}")
    st.warning("🔐 PRIVATE BOTTLE: Only you (owner) can see files here! Other 12 CANNOT open your personal portal! This is your private office!")
    personal = load_json(FILES["personal"], st.session_state.personal)
    my_personal = [p for p in personal if p['owner']==user]
    st.success(f"Your Personal Files: {len(my_personal)} - Only you see this!")
    pt = st.text_input("Personal Title * - Only you see", key="pers_t")
    pc = st.text_area("Personal Notes * - Private", key="pers_c", height=100)
    pf = st.file_uploader("Personal File - PDF/Excel/Word/Photo - ONLY YOU CAN OPEN", type=["pdf","xlsx","xls","pptx","ppt","docx","doc","jpg","png","jpeg","mp4","mp3"], key="pers_f")
    if st.button("Save To My Personal Portal - PRIVATE", type="primary", use_container_width=True, key="pers_s"):
        if not pt.strip():
            st.error("Title required")
        else:
            fpath = ""; fname = ""
            if pf:
                fname = pf.name.replace(" ", "_")
                fpath = f"data/personal/{user}_{len(personal)+1}_{fname}"
                open(fpath, 'wb').write(pf.getvalue())
            personal.append({"id": len(personal)+1, "owner": user, "owner_name": user_full, "title": pt.strip(), "content": pc.strip(), "file_name": fname, "file_path": fpath, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
            save_json(FILES["personal"], personal)
            add_audit("Personal File Saved", user_full, pt.strip())
            st.success(f"Saved to YOUR personal portal only! {pt.strip()}"); st.balloons(); st.rerun()
    st.divider()
    for p in reversed(my_personal):
        with st.container(border=True):
            st.markdown(f"**{p['title']}** | {p['date']} | 🔒 Only you")
            if p.get('content'): st.info(p['content'])
            if p.get('file_path','') and os.path.exists(p['file_path']):
                if p['file_path'].endswith(('.jpg','.png','.jpeg')):
                    st.image(p['file_path'], width=300)
                st.download_button(f"Download {p['file_name']}", open(p['file_path'],'rb').read(), file_name=p['file_name'], key=f"dl_pers_{p['id']}", type="primary")

# TAB 2 PUBLIC PORTAL - OPEN ALL 13
with tabs[2]:
    st.subheader("📢 Public Portal - OPEN TO ALL 13 - Anyone Can Broadcast!")
    st.success("OPEN: All 13 departments can POST and ALL 13 SEE SAME! No restriction!")
    anns = load_json(FILES["ann"], st.session_state.ann)
    at = st.text_input("Title * - All 13 will see", key="ann_t")
    acont = st.text_area("Message to ALL 13 Departments *", key="ann_c", height=120)
    af = st.file_uploader("Attach File (PDF/Excel/PPT/Word/Photo) - Optional", type=["pdf","xlsx","xls","pptx","ppt","docx","doc","jpg","png","jpeg"], key="ann_f")
    if st.button("📢 BROADCAST TO ALL 13 DEPARTMENTS", type="primary", use_container_width=True):
        if not at.strip() or not acont.strip():
            st.error("Title + Message required")
        else:
            fpath = ""; fname = ""
            if af:
                fname = af.name.replace(" ", "_")
                fpath = f"data/documents/ann_{len(anns)+1}_{fname}"
                open(fpath, 'wb').write(af.getvalue())
            anns.append({"id": len(anns)+1, "title": at.strip(), "content": acont.strip(), "file_name": fname, "file_path": fpath, "from": user, "from_name": user_full, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
            save_json(FILES["ann"], anns)
            add_audit("Public Broadcast", user_full, at.strip())
            st.success(f"Broadcasted to ALL 13! {at.strip()}"); st.balloons(); st.rerun()
    st.divider()
    st.write(f"**Total Broadcasts: {len(anns)} - Visible to ALL 13**")
    for ann in reversed(anns):
        with st.container(border=True):
            st.markdown(f"**{ann['title']}** | {ann['from_name']} | {ann['date']}")
            st.info(ann['content'])
            if ann.get('file_path','') and os.path.exists(ann['file_path']):
                st.download_button(f"Download {ann['file_name']}", open(ann['file_path'],'rb').read(), file_name=ann['file_name'], key=f"dl_ann_{ann['id']}")

# TAB 3 MEETING - OPEN ALL 13
with tabs[3]:
    st.subheader("🎥 Online Meeting - OPEN TO ALL 13 - Anyone Can Start!")
    st.success("OPEN: Any of 13 can START meeting and ALL 13 can JOIN with Audio/Video!")
    meetings = load_json(FILES["meet"], st.session_state.meet)
    active = [m for m in meetings if m.get('is_active')]
    if active:
        am = active[-1]
        st.success(f"🔴 LIVE NOW: {am['title']} by {am['from_name']} | Topic: {am['topic']}")
        mid = am['meeting_id']
        st.markdown(f"<a href='https://meet.jit.si/{mid}' target='_blank' style='background:#25D366;color:white;padding:12px 25px;border-radius:8px;text-decoration:none;font-weight:bold;display:inline-block;'>🎥 JOIN MEETING NOW - Click Here</a>", unsafe_allow_html=True)
        st.components.v1.html(f"<iframe src='https://meet.jit.si/{mid}#userInfo.displayName='{user_full}'' style='width:100%;height:600px;border:0;border-radius:10px;' allow='camera; microphone; fullscreen; display-capture'></iframe>", height=650)
        if st.button("🔴 END MEETING FOR ALL 13", key="end_meet"):
            for m in meetings:
                if m['meeting_id']==mid:
                    m['is_active']=False
            save_json(FILES["meet"], meetings)
            add_audit("Meeting Ended", user_full, am['title'])
            st.success("Meeting ended for all"); st.rerun()
    else:
        st.warning("No active meeting - Any of 13 can start one below")
    st.divider()
    mt = st.text_input("Meeting Title *", key="m_title")
    mtop = st.text_area("Meeting Topic/Agenda *", key="m_topic")
    if st.button("🎥 START MEETING - ALL 13 CAN JOIN", type="primary", use_container_width=True):
        if not mt.strip() or not mtop.strip():
            st.error("Title + Topic required")
        else:
            mid = f"UNIK-BEC-{dt.now().strftime('%Y%m%d-%H%M')}-{mt.replace(' ','')[:8]}"
            meetings.append({"id": len(meetings)+1, "meeting_id": mid, "title": mt.strip(), "topic": mtop.strip(), "from": user, "from_name": user_full, "date": dt.now().strftime("%Y-%m-%d %H:%M"), "is_active": True})
            save_json(FILES["meet"], meetings)
            add_audit("Meeting Started", user_full, mt.strip())
            st.success(f"Meeting Started! ID: {mid} - All 13 can join now!"); st.balloons(); st.rerun()

# TAB 4 SUBMIT REPORT
with tabs[4]:
    st.subheader("📝 Submit Report - Goes to Private Portal (SUPER 4 sees)")
    rt = st.selectbox("Report Type", REPORT_TYPES, key="rt")
    rtitle = st.text_input("Report Title *", key="rtitle")
    rcontent = st.text_area("Report Details * - Principal + Patron + President + Speaker will see", key="rcontent", height=150)
    if st.button("📤 Submit Report to SUPER 4", type="primary", use_container_width=True):
        if not rtitle.strip() or not rcontent.strip():
            st.error("Title + Content required")
        else:
            reports.append({"id": len(reports)+1, "date": dt.now().strftime("%Y-%m-%d %H:%M"), "from": user, "from_name": user_full, "type": rt, "title": rtitle.strip(), "content": rcontent.strip()})
            save_json(FILES["reports"], reports)
            add_audit("Report Submitted", user_full, rtitle.strip())
            st.success("Saved! SUPER 4 will see it in Private Portal!"); st.balloons()

# TAB 5 PRIVATE - SUPER 4 ONLY
with tabs[5]:
    st.subheader("🔒 Private Portal - SUPER 4 ONLY - Principal, Patron, President, Speaker")
    if user not in SUPER_4:
        st.error("🚫 RESTRICTED: Only SUPER 4 can access!")
        st.stop()
    reports = load_json(FILES["reports"], st.session_state.reports)
    st.success(f"🔐 SUPER 4 ACCESS: Total Reports from All 13: {len(reports)}")
    ftype = st.selectbox("Filter by Type", ["All"] + REPORT_TYPES, key="filter_type")
    filtered = reports if ftype=="All" else [r for r in reports if r['type']==ftype]
    for r in reversed(filtered):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']} - {r['type']}"):
            st.info(r['content'])

# TAB 6 ELECTORAL
with tabs[6]:
    st.subheader("🗳️ Electoral Commission - OPEN TO ALL 13")
    pend = load_json(FILES["pending"], st.session_state.pending)
    cand = load_json(FILES["candidates"], st.session_state.candidates)
    votes = load_json(FILES["votes"], st.session_state.votes)
    t_a, t_b, t_c = st.tabs(["⏳ Pending - Speaker Approves", "📝 Register - OPEN ALL 13", "📊 Results - OPEN ALL 13"])
    with t_a:
        st.write(f"Pending: {len(pend)}")
        for pc in reversed(pend):
            with st.container(border=True):
                col1, col2 = st.columns([1,3])
                if os.path.exists(pc.get('photo_path','')):
                    col1.image(pc.get('photo_path',''), width=120)
                col2.write(f"**{pc['name']}** - {USERS[pc['position']]} - {pc.get('class','')}")
                col2.info(pc.get('reason',''))
                if user == "speaker":
                    if col2.button(f"✅ Approve {pc['name']}", key=f"ap_{pc['id']}", type="primary"):
                        st.session_state.candidates.append(pc)
                        st.session_state.pending = [x for x in st.session_state.pending if x['id']!=pc['id']]
                        save_json(FILES["candidates"], st.session_state.candidates)
                        save_json(FILES["pending"], st.session_state.pending)
                        st.success(f"Approved!"); st.balloons(); st.rerun()
    with t_b:
        rp = st.selectbox("Position", ELECTION_POS, format_func=lambda x: USERS[x], key="cand_pos")
        rn = st.text_input("Full Names *", key="cand_name")
        rclass = st.text_input("Class e.g. BNS 2", key="cand_class")
        rreason = st.text_area("Why vote you?", key="cand_reason")
        rphoto = st.file_uploader("Passport Photo *", type=["jpg","png","jpeg"], key="cand_photo")
        if st.button("📝 Register as Candidate", type="primary"):
            if not rn or not rphoto:
                st.error("Names + Photo required")
            else:
                nid = len(cand)+len(pend)+1
                fpath = f"data/media_files/cand_{nid}.jpg"
                open(fpath, 'wb').write(rphoto.getvalue())
                st.session_state.candidates.append({"id": nid, "position": rp, "name": rn, "class": rclass, "reason": rreason if rreason else "Cabinet Member", "photo_path": fpath, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
                save_json(FILES["candidates"], st.session_state.candidates)
                st.success(f"Registered {rn}!")
    with t_c:
        st.write(f"Total Votes: {len(votes)}")
        for pos in ELECTION_POS:
            cs = [c for c in cand if c['position']==pos]
            if cs:
                rd = [{"Candidate": cc['name'], "Votes": len([v for v in votes if v['candidate_id']==cc['id']])} for cc in cs]
                if len(rd)>0:
                    st.write(f"**{USERS[pos]}**")
                    df = pd.DataFrame(rd).sort_values("Votes", ascending=False)
                    st.dataframe(df, use_container_width=True)
                    if df["Votes"].sum()>0:
                        st.bar_chart(df.set_index("Candidate")["Votes"])

# TAB 7 DISCIPLINARY - OPEN
with tabs[7]:
    st.subheader("⚖️ Disciplinary - OPEN TO ALL 13")
    disc = load_json(FILES["disc"], st.session_state.disc)
    d_t = st.text_input("Case Title *", key="disc_t")
    d_c = st.text_area("Case Details *", key="disc_c")
    if st.button("Save Disciplinary", type="primary", key="disc_s"):
        disc.append({"id": len(disc)+1, "title": d_t.strip(), "content": d_c.strip(), "by": user_full, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["disc"], disc)
        st.success("Saved!"); st.rerun()
    for dr in reversed(disc):
        with st.expander(f"#{dr['id']} {dr['title']} - {dr['by']}"):
            st.info(dr['content'])

# TAB 8 GP - OPEN
with tabs[8]:
    st.subheader("📋 GP - OPEN TO ALL 13")
    gp = load_json(FILES["gp"], st.session_state.gp)
    gp_t = st.text_input("GP Title *", key="gp_t")
    gp_c = st.text_area("GP Details *", key="gp_c")
    if st.button("Save GP", type="primary", key="gp_s"):
        gp.append({"id": len(gp)+1, "title": gp_t.strip(), "content": gp_c.strip(), "by": user_full, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["gp"], gp)
        st.success("Saved!"); st.rerun()
    for gpr in reversed(gp):
        with st.expander(f"{gpr['title']} - {gpr['by']}"):
            st.info(gpr['content'])

# TAB 9 FINANCE - 5 ONLY
with tabs[9]:
    st.subheader("💰 Finance - 5 ONLY")
    if user not in FINANCE_5:
        st.error("🚫 RESTRICTED: Finance 5 Only!")
        st.stop()
    fin = load_json(FILES["finance"], st.session_state.finance)
    f_t = st.text_input("Finance Title *", key="fin_t")
    f_d = st.text_area("Description", key="fin_d")
    f_f = st.file_uploader("Upload Excel / PPT / PDF / Word", type=["xlsx","xls","pptx","ppt","pdf","docx","doc","csv"], key="fin_f")
    f_amount = st.number_input("Amount UGX", min_value=0, step=1000, key="fin_amount")
    if st.button("💰 Save Finance", type="primary", key="fin_s2"):
        fname = ""; fpath = ""
        if f_f:
            fname = f_f.name.replace(" ", "_")
            fpath = f"data/documents/finance_{len(fin)+1}_{fname}"
            open(fpath, 'wb').write(f_f.getvalue())
        fin.append({"id": len(fin)+1, "title": f_t.strip(), "description": f_d.strip(), "amount": f_amount, "file_name": fname, "file_path": fpath, "by": user_full, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["finance"], fin)
        st.success("Saved!"); st.rerun()
    for fd in reversed(fin):
        with st.container(border=True):
            st.markdown(f"**{fd['title']}** - {fd['by']} - UGX {fd.get('amount',0):,}")
            if fd.get('file_path','') and os.path.exists(fd['file_path']):
                st.download_button(f"Download {fd['file_name']}", open(fd['file_path'],'rb').read(), file_name=fd['file_name'], key=f"dl_fin_{fd['id']}", type="primary")

# TAB 10 SECRET - OPEN
with tabs[10]:
    st.subheader("🔐 Secret - OPEN ALL 13")
    sec = load_json(FILES["docs"], st.session_state.docs)
    dc = st.selectbox("Category", DOC_CATS, key="sec_cat")
    dt_ = st.text_input("Title *", key="sec_t")
    dd = st.text_area("Description", key="sec_d")
    if st.button("Save Secret", type="primary", key="sec_s"):
        sec.append({"id": len(sec)+1, "category": dc, "title": dt_.strip(), "description": dd.strip(), "by": user_full, "date": dt.now().strftime("%Y-%m-%d")})
        save_json(FILES["docs"], sec)
        st.success("Saved!")
    for d in reversed(sec):
        with st.expander(f"{d['category']} | {d['title']} - {d['by']}"):
            st.write(d['description'])

# TAB 11 DOCUMENTS - OPEN ALL 13
with tabs[11]:
    st.subheader("📄 Documents - OPEN TO ALL 13")
    docs = load_json(FILES["uploaded"], st.session_state.uploaded)
    st.success(f"OPEN: ALL 13 can upload & see same! Total: {len(docs)}")
    dcat = st.selectbox("Category", DOC_CATS, key="doc_cat")
    dtit = st.text_input("Title *", key="doc_t")
    dd = st.text_area("Description", key="doc_d")
    df = st.file_uploader("Upload File *", type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv","jpg","png"], key="doc_f")
    if st.button("📤 Upload Document - ALL 13 SEE SAME!", type="primary", use_container_width=True, key="doc_s"):
        safe = df.name.replace(" ", "_")
        fpath = f"data/documents/doc_{len(docs)+1}_{safe}"
        open(fpath, 'wb').write(df.getvalue())
        docs.append({"id": len(docs)+1, "category": dcat, "title": dtit.strip(), "description": dd.strip(), "file_name": df.name, "file_path": fpath, "by": user_full, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["uploaded"], docs)
        st.success("Uploaded!"); st.balloons(); st.rerun()
    for doc in reversed(docs):
        with st.container(border=True):
            st.markdown(f"**{doc['title']}** | {doc['category']} | by {doc['by']}")
            if os.path.exists(doc.get('file_path','')):
                st.download_button(f"Download {doc['file_name']}", open(doc['file_path'],'rb').read(), file_name=doc['file_name'], key=f"dl_doc_{doc['id']}", type="primary")

# TAB 12 MEDIA GALLERY - OPEN ALL 13
with tabs[12]:
    st.subheader("📸 Media Gallery - OPEN TO ALL 13 - EVERYONE SEES SAME!")
    med = load_json(FILES["media"], st.session_state.media)
    st.success(f"FIXED! ALL 13 can post! Total: {len(med)} - Class Rep posts, President sees same!")
    mt = st.text_input("Media Title *", key="media_t")
    mf = st.file_uploader("File * JPG/PNG/MP4/MP3", type=["jpg","png","jpeg","mp4","mp3","m4a","wav","mov"], key="media_f")
    if st.button("📸 Upload - ALL 13 SEE SAME!", type="primary", use_container_width=True, key="media_s"):
        fpath = f"data/media_files/media_{len(med)+1}_{mf.name.replace(' ','_')}"
        open(fpath, 'wb').write(mf.getvalue())
        med.append({"id": len(med)+1, "title": mt.strip(), "file_name": mf.name, "file_path": fpath, "file_type": mf.type, "by": user_full, "date": dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["media"], med)
        st.success("Saved! NOW ALL 13 SEE!"); st.balloons(); st.rerun()
    cols = st.columns(3)
    for idx, m in enumerate(reversed(med)):
        with cols[idx % 3]:
            with st.container(border=True):
                st.write(f"**{m['title']}** - {m['by']}")
                if os.path.exists(m['file_path']):
                    if "image" in m['file_type']:
                        st.image(m['file_path'], use_container_width=True)
                    elif "video" in m['file_type']:
                        st.video(m['file_path'])
                    elif "audio" in m['file_type']:
                        st.audio(m['file_path'])
                if os.path.exists(m['file_path']):
                    st.download_button(f"Download {m['file_name']}", open(m['file_path'],'rb').read(), file_name=m['file_name'], key=f"dl_med_{m['id']}")

# TAB 13 CABINET ARCHIVE
with tabs[13]:
    st.subheader("🏛️ Cabinet Archive - OPEN TO ALL 13")
    cabs = load_json(FILES["cabinets"], st.session_state.cabinets)
    cy = st.text_input("Year *", key="cab_y")
    cn = st.text_input("Cabinet Name *", key="cab_n")
    cm = st.text_area("Members List *", key="cab_m")
    cp = st.file_uploader("Group Photo *", type=["jpg","png","jpeg"], key="cab_p")
    if st.button("🏛️ Save Cabinet", type="primary", use_container_width=True, key="cab_s"):
        fpath = f"data/media_files/cab_{len(cabs)+1}.jpg"
        open(fpath, 'wb').write(cp.getvalue())
        cabs.append({"id": len(cabs)+1, "year": cy.strip(), "name": cn.strip(), "members": cm.strip(), "photo_path": fpath, "by": user_full, "date": dt.now().strftime("%Y-%m-%d")})
        save_json(FILES["cabinets"], cabs)
        st.success("Saved!"); st.rerun()
    for cab in reversed(cabs):
        with st.container(border=True):
            st.markdown(f"**{cab['name']} - {cab['year']}**")
            if os.path.exists(cab['photo_path']):
                st.image(cab['photo_path'], use_container_width=True)
            st.info(cab['members'])

# TAB 14 AUDIT LOG
with tabs[14]:
    st.subheader("📜 Audit Log")
    audit = load_json(FILES["audit"], st.session_state.audit)
    st.success(f"Total Actions: {len(audit)}")
    if audit:
        df_audit = pd.DataFrame(reversed(audit))
        st.dataframe(df_audit, use_container_width=True)
