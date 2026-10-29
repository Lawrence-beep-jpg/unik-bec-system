import streamlit as st
import pandas as pd
import datetime
import os, json
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# SAVE ON SERVER FOR YEARS
os.makedirs("data/media_files", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)
REPORTS_FILE="data/reports.json"
MEDIA_FILE="data/media.json"
CANDIDATES_FILE="data/candidates.json"
PENDING_FILE="data/pending.json"
VOTES_FILE="data/votes.json"
CABINETS_FILE="data/cabinets.json"
DOCS_FILE="data/docs.json"
FINANCE_FILE="data/finance.json"
DISC_FILE="data/disc.json"
GP_FILE="data/gp.json"
PASSWORDS_FILE="data/passwords.json"
UPLOADED_DOCS_FILE="data/uploaded_docs.json"
ANNOUNCEMENTS_FILE="data/announcements.json"
MEETINGS_FILE="data/meetings.json"

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path,'r') as f: return json.load(f)
        except: return default
    return default

def save_json(path, data):
    with open(path,'w') as f: json.dump(data, f, default=str)

params = st.query_params
is_public_vote = params.get("public", "") == "vote"

# ONLY ONE HEADING - UNIK BEC UNASNM Governance Portal
c1,c2,c3 = st.columns([1,3,1])
with c1:
    if os.path.exists("unik_badge.png"): st.image("unik_badge.png", width=90)
with c2:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM<br>Governance Portal</h2>", unsafe_allow_html=True)
with c3:
    if os.path.exists("unasnm_badge.png"): st.image("unasnm_badge.png", width=90)

USERS={
"principal":"Principal",
"patron":"Hon. Patron",
"president":"His Excellency President",
"vice_president":"Hon. Vice President - Leader GP",
"speaker":"Right Honourable Speaker - Hon. Lawrence Ssango",
"general_secretary":"Hon. General Secretary",
"finance":"Hon. Finance Secretary",
"information":"Hon. Information Secretary",
"class_rep":"Hon. Class Rep",
"grc_male":"Hon. GRC Male",
"grc_female":"Hon. GRC Female",
"hostel_male":"Hon. Hostel Male",
"hostel_female":"Hon. Hostel Female",
"nursing_affairs":"Hon. Nursing Affairs"
}
LOGIN_USERS=list(USERS.keys())
SUPER_4=["principal","patron","president","speaker"]
FINANCE_5=["principal","patron","president","speaker","finance"]
ELECTION_POSITIONS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]
REPORT_TYPES=["Weekly","Monthly","Financial","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Other"]
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint","Public Information","Meeting Minutes"]

if 'reports' not in st.session_state: st.session_state.reports=load_json(REPORTS_FILE, [])
if 'media' not in st.session_state: st.session_state.media=load_json(MEDIA_FILE, [])
if 'candidates' not in st.session_state: st.session_state.candidates=load_json(CANDIDATES_FILE, [])
if 'pending_candidates' not in st.session_state: st.session_state.pending_candidates=load_json(PENDING_FILE, [])
if 'votes' not in st.session_state: st.session_state.votes=load_json(VOTES_FILE, [])
if 'cabinets' not in st.session_state: st.session_state.cabinets=load_json(CABINETS_FILE, [])
if 'documents' not in st.session_state: st.session_state.documents=load_json(DOCS_FILE, [])
if 'finance_docs' not in st.session_state: st.session_state.finance_docs=load_json(FINANCE_FILE, [])
if 'disciplinary_reports' not in st.session_state: st.session_state.disciplinary_reports=load_json(DISC_FILE, [])
if 'gp_reports' not in st.session_state: st.session_state.gp_reports=load_json(GP_FILE, [])
if 'uploaded_docs' not in st.session_state: st.session_state.uploaded_docs=load_json(UPLOADED_DOCS_FILE, [])
if 'announcements' not in st.session_state: st.session_state.announcements=load_json(ANNOUNCEMENTS_FILE, [])
if 'meetings' not in st.session_state: st.session_state.meetings=load_json(MEETINGS_FILE, [])
if 'passwords' not in st.session_state: 
    pw=load_json(PASSWORDS_FILE, {})
    st.session_state.passwords = pw if pw else {u:"unik2025" for u in LOGIN_USERS}
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

if is_public_vote:
    st.markdown("<h3 style='text-align:center;'>🏛️ UNIK BEC UNASNM - PUBLIC ELECTORAL COMMISSION</h3>", unsafe_allow_html=True)
    st.info("Public Link ?public=vote - No Secrets - One Email Once Per Position - Works For Years")
    t1,t2,t3,t4 = st.tabs(["Apply Candidate","Vote One Email Once","Live Results","Public Info from SUPER 4"])
    with t1:
        rp=st.selectbox("Position You Want",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names *",key="pub_name")
        rclass=st.text_input("Class *",key="pub_class")
        remail=st.text_input("Email *",key="pub_email")
        rreason=st.text_area("Why should students vote you? *",key="pub_reason")
        rphoto=st.file_uploader("Your Photo * JPG/PNG",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit (Needs Right Honourable Speaker Approval)",type="primary",use_container_width=True,key="pub_submit"):
            if not rn or not rclass or not remail or not rreason or not rphoto: st.error("Fill ALL * fields")
            else:
                nid=len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                with open(fpath,'wb') as out: out.write(rphoto.getvalue())
                st.session_state.pending_candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(PENDING_FILE, st.session_state.pending_candidates)
                st.success("Sent! Wait approval from Right Honourable Speaker"); st.balloons()
    with t2:
        voter_email=st.text_input("Your Email * (One email once per position)",key="pub_voter_email", placeholder="student@unik.ac.ug")
        if voter_email and "@" in voter_email:
            vp=st.selectbox("Choose Position to Vote",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
            already=[v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
            if already: st.error(f"Already voted for {USERS[vp]} with {voter_email} - One email once per position!")
            else:
                for c in [x for x in st.session_state.candidates if x['position']==vp]:
                    with st.container(border=True):
                        if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=150)
                        st.write(f"**{c['name']}** - {c.get('class','')}")
                        st.info(c.get('reason',''))
                        if st.button(f"Vote {c['name']}",key=f"pv_{c['id']}_{voter_email}", type="primary"):
                            st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                            save_json(VOTES_FILE, st.session_state.votes)
                            st.success("Voted!"); st.balloons(); st.rerun()
        else: st.warning("Enter valid email to see candidates")
    with t3:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(f"**{USERS[pos]}**"); st.dataframe(pd.DataFrame(rd),use_container_width=True)
    with t4:
        st.subheader("Public Information from SUPER 4")
        all_anns=load_json(ANNOUNCEMENTS_FILE, [])
        pub_anns=[a for a in all_anns if a.get('is_public')]
        if not pub_anns: st.warning("No public info yet from SUPER 4")
        for ann in reversed(pub_anns):
            with st.container(border=True):
                st.markdown(f"**{ann['title']}** | {ann['from_name']} | {ann['date']}")
                st.info(ann['content'])
                if ann.get('file_path','') and os.path.exists(ann['file_path']):
                    st.download_button(f"Download {ann['file_name']}", open(ann['file_path'],'rb').read(), file_name=ann['file_name'], key=f"dl_pub_{ann['id']}")
    st.stop()

if not st.session_state.logged_in:
    st.markdown("### Cabinet Login - 13 Departments Only - Secrets Inside")
    u=st.selectbox("Select Your Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("LOGIN TO GOVERNANCE PORTAL",type="primary", use_container_width=True):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True; st.session_state.user=u; st.rerun()
        else: st.error("Wrong Password! Default unik2025")
    st.info("Default: unik2025 | Public Voting: ?public=vote - One email once - Works for years")
    st.stop()

user=st.session_state.user
user_full=USERS[user]

st.sidebar.title(user_full)
st.sidebar.success(f"Logged: {user_full}")
st.sidebar.divider()
st.sidebar.subheader("Change My Password - My Bottle")
with st.sidebar.expander("Change My Own Password - Every Member Can!", expanded=False):
    cur=st.text_input("Current Password *",type="password",key="cur_pw")
    new=st.text_input("New Password *",type="password",key="new_pw")
    conf=st.text_input("Confirm New *",type="password",key="conf_pw")
    if st.button("Save New Password - My Bottle Only",type="primary",use_container_width=True,key="save_pw"):
        if not cur or not new or not conf: st.sidebar.error("Fill ALL!")
        elif cur!=st.session_state.passwords.get(user,"unik2025"): st.sidebar.error("Current wrong!")
        elif new!=conf: st.sidebar.error("Don't match!")
        elif len(new)<4: st.sidebar.error("Min 4 chars!")
        else:
            st.session_state.passwords[user]=new
            save_json(PASSWORDS_FILE, st.session_state.passwords)
            st.sidebar.success(f"Changed! New: {new}"); st.balloons()

st.sidebar.divider()
if user in SUPER_4:
    st.sidebar.info("SUPER 4: You control Broadcast + ALL Reports + Online Meetings!")
else:
    st.sidebar.info(f"You are {user_full} - Can read + join meetings")
if st.sidebar.button("Logout", use_container_width=True): st.session_state.logged_in=False; st.rerun()

tab0,tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11 = st.tabs([
"📢 Public Portal SUPER 4 Broadcast",
"🎥 Online Meeting Audio/Video",
"📝 Submit Report",
"📂 Private Portal",
"🗳️ Electoral Chair Full",
"⚖️ Disciplinary",
"📋 GP VP Leader",
"💰 Finance 5 Excel/PDF/PPT",
"🔐 Secret Store",
"📄 Documents PDF/PPT/Word/Excel ALL 13",
"📸 Media Gallery ALL SEE",
"🏛️ Cabinet Archive For Years"
])

with tab0:
    st.subheader("Public Portal - SUPER 4 sends ONE message to ALL 13 + Public Info")
    anns=load_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
    st.session_state.announcements=anns
    if anns: st.success(f"{len(anns)} Announcements from SUPER 4")
    if user in SUPER_4:
        st.markdown(f"**Post as {user_full} - ONE MESSAGE → ALL 13 AT ONCE**")
        at=st.text_input("Title *",key="ann_t", placeholder="Meeting Tomorrow 9am All Must Attend")
        acat=st.selectbox("Where to show?",["Internal - All 13 Only","Public Information - Also Show to Students in ?public=vote","Both Internal + Public"],key="ann_cat")
        ap=st.selectbox("Priority",["Normal","Urgent","Very Urgent - All Must Read"],key="ann_p")
        acont=st.text_area("Message to ALL 13 Departments *",key="ann_c",height=150)
        af=st.file_uploader("Attach PDF/Excel/PPT/Word/Photo (Optional)",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","jpg","png","jpeg"],key="ann_f")
        if st.button("BROADCAST TO ALL 13 + PUBLIC OPTION",type="primary",use_container_width=True,key="ann_btn"):
            if not at.strip() or not acont.strip(): st.error("Title + Message required!")
            else:
                fpath=""; fname=""
                if af:
                    fname=af.name.replace(" ","_")
                    fpath=f"data/documents/ann_{len(anns)+1}_{fname}"
                    with open(fpath,'wb') as out: out.write(af.getvalue())
                is_pub="Public" in acat or "Both" in acat
                anns.append({"id":len(anns)+1,"title":at.strip(),"category":acat,"priority":ap,"content":acont.strip(),"file_name":fname,"file_path":fpath,"from":user,"from_name":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"read_by":[],"is_public":is_pub})
                save_json(ANNOUNCEMENTS_FILE, anns)
                st.session_state.announcements=anns
                st.success(f"Broadcasted! ALL 13 see + {'Public students also see' if is_pub else 'Internal only'}"); st.balloons(); st.rerun()
    else:
        st.info(f"You are {user_full} - You can READ announcements from SUPER 4")
    st.divider()
    for ann in reversed(anns):
        pub_tag="🌐 PUBLIC" if ann.get('is_public') else "🔒 INTERNAL"
        pri_icon="🔴" if "Very Urgent" in ann['priority'] else "🟡" if "Urgent" in ann['priority'] else "🟢"
        with st.container(border=True):
            st.markdown(f"{pri_icon} {pub_tag} **{ann['title']}** | {ann['priority']} | {ann['from_name']} | {ann['date']}")
            st.info(ann['content'])
            if ann.get('file_path','') and os.path.exists(ann['file_path']):
                st.download_button(f"Download {ann['file_name']}", open(ann['file_path'],'rb').read(), file_name=ann['file_name'], key=f"dl_ann_{ann['id']}")
            if user not in ann.get('read_by',[]):
                if st.button("Mark as Read",key=f"read_{ann['id']}"):
                    for a in anns:
                        if a['id']==ann['id'] and user not in a['read_by']: a['read_by'].append(user)
                    save_json(ANNOUNCEMENTS_FILE, anns); st.rerun()
            else: st.caption(f"Read - {len(ann.get('read_by',[]))}/13 read")

with tab1:
    st.subheader("Online Meeting - Audio & Video Calls - Controlled by SUPER 4")
    st.info("SUPER 4 creates meeting - ALL 13 join - Audio + Video + Chat + Screen Share!")
    meetings=load_json(MEETINGS_FILE, st.session_state.meetings)
    st.session_state.meetings=meetings
    active_meetings=[m for m in meetings if m.get('is_active')]
    if active_meetings:
        am=active_meetings[-1]
        st.success(f"LIVE NOW: {am['title']} | Created by {am['from_name']} | {am['date']}")
        st.warning(f"Topic: {am['topic']}")
        meeting_id = am['meeting_id']
        st.markdown(f"""
        <div style="background:#f0f0f0; padding:15px; border-radius:10px; margin:10px 0;">
            <p><b>Meeting ID:</b> {meeting_id}</p>
            <p><b>Your Name:</b> {user_full}</p>
            <a href="https://meet.jit.si/{meeting_id}" target="_blank" style="background:#25D366; color:white; padding:12px 25px; border-radius:8px; text-decoration:none; font-weight:bold; display:inline-block;">
                JOIN MEETING NOW - Click to open in new tab (Audio + Video)
            </a>
        </div>
        """, unsafe_allow_html=True)
        jitsi_html = f"""
        <iframe src="https://meet.jit.si/{meeting_id}#userInfo.displayName='{user_full}'" 
        style="width:100%; height:600px; border:0; border-radius:10px;" allow="camera; microphone; fullscreen; display-capture"></iframe>
        """
        st.components.v1.html(jitsi_html, height=650)
        if user in SUPER_4:
            if st.button("END MEETING FOR ALL", type="primary", key="end_meeting"):
                for m in meetings:
                    if m['meeting_id']==meeting_id: m['is_active']=False; m['ended_by']=user_full; m['ended_date']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                save_json(MEETINGS_FILE, meetings)
                st.success("Meeting ended for all 13"); st.rerun()
    else:
        st.warning("No active meeting now - SUPER 4 will start when needed")
    st.divider()
    if user in SUPER_4:
        st.markdown(f"### Create New Online Meeting as {user_full} - SUPER 4 Only")
        m_title=st.text_input("Meeting Title *", key="m_title")
        m_topic=st.text_area("Meeting Topic / Agenda *", key="m_topic")
        m_type=st.selectbox("Meeting Type", ["Audio + Video - All 13 can see each other","Audio Only - Voice meeting","Emergency - Very Urgent"], key="m_type")
        if st.button("START MEETING NOW - ALL 13 CAN JOIN", type="primary", use_container_width=True, key="start_meeting"):
            if not m_title.strip() or not m_topic.strip(): st.error("Title + Topic required!")
            else:
                meeting_id = f"UNIK-BEC-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}-{m_title.replace(' ','')[:10]}"
                meetings.append({
                    "id": len(meetings)+1,
                    "meeting_id": meeting_id,
                    "title": m_title.strip(),
                    "topic": m_topic.strip(),
                    "type": m_type,
                    "from": user,
                    "from_name": user_full,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "is_active": True,
                    "joined_by": []
                })
                save_json(MEETINGS_FILE, meetings)
                st.session_state.meetings=meetings
                st.success(f"Meeting '{m_title}' started! ID: {meeting_id} - ALL 13 can now join!"); st.balloons(); st.rerun()
    st.divider()
    st.subheader("Past Meetings - Archive for Years")
    for m in reversed(meetings):
        status="LIVE NOW" if m.get('is_active') else "Ended"
        with st.container(border=True):
            st.markdown(f"{status} **{m['title']}** | {m['type']} | by {m['from_name']} | {m['date']} | ID: {m['meeting_id']}")
            st.caption(f"Topic: {m['topic']}")

with tab2:
    st.subheader("Submit Report - Where Principal Looks")
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt")
    rtitle=st.text_input("Report Title *",key="rtitle", placeholder="Weekly Report - Class Rep")
    rcontent=st.text_area("Details *",key="rcontent", height=150)
    if st.button("Submit Report - Saved on Server - Principal Will See",type="primary",use_container_width=True,key="rsubmit"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Title + Details required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip()})
            save_json(REPORTS_FILE, st.session_state.reports)
            st.success("Saved - Principal will see!"); st.balloons(); st.rerun()

with tab3:
    st.subheader("Private Portal - Reports - Principal Looks Here")
    reports=load_json(REPORTS_FILE, st.session_state.reports)
    show=reports if user in SUPER_4 else [r for r in reports if r['from']==user]
    st.write(f"Reports: {len(show)}")
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['type']} - {r['date']}"):
            st.info(r['content'])

with tab4:
    st.subheader("Electoral Chair - Full - Pending, Approved, Register, Vote, Results")
    pend=load_json(PENDING_FILE, st.session_state.pending_candidates)
    cand=load_json(CANDIDATES_FILE, st.session_state.candidates)
    votes=load_json(VOTES_FILE, st.session_state.votes)
    st.session_state.pending_candidates=pend
    st.session_state.candidates=cand
    st.session_state.votes=votes
    t_a,t_b,t_c,t_d,t_e=st.tabs(["Pending Approval","Approved","Register + Photo","Vote Cabinet","Results"])
    with t_a:
        st.write(f"Pending: {len(pend)} - Need Speaker Approval")
        for pc in reversed(pend):
            with st.container(border=True):
                if os.path.exists(pc.get('photo_path','')): st.image(pc.get('photo_path',''),width=120)
                st.write(f"**{pc['name']}** - {USERS[pc['position']]}")
                st.info(pc.get('reason',''))
                if user=="speaker":
                    c1,c2=st.columns(2)
                    with c1:
                        if st.button(f"Approve {pc['name']}",key=f"ap_{pc['id']}", type="primary"):
                            st.session_state.candidates.append(pc)
                            st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                            save_json(CANDIDATES_FILE, st.session_state.candidates)
                            save_json(PENDING_FILE, st.session_state.pending_candidates)
                            st.success(f"Approved {pc['name']}"); st.rerun()
                    with c2:
                        if st.button(f"Reject {pc['name']}",key=f"rj_{pc['id']}"):
                            st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                            save_json(PENDING_FILE, st.session_state.pending_candidates)
                            st.warning("Rejected"); st.rerun()
    with t_b:
        st.write(f"Approved: {len(cand)}")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in cand if c['position']==pos]
            if cs:
                st.write(f"**{USERS[pos]}: {len(cs)}**")
                for c in cs:
                    with st.container(border=True):
                        if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=100)
                        st.write(c['name'])
    with t_c:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos")
        rn=st.text_input("Full Names *",key="cand_name")
        rclass=st.text_input("Class",key="cand_class")
        rreason=st.text_area("Why vote you?",key="cand_reason")
        rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="cand_photo")
        if st.button("Register - Auto Approved",type="primary",key="cand_submit"):
            if not rn or not rphoto: st.error("Names + Photo required")
            else:
                nid=len(cand)+len(pend)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                with open(fpath,'wb') as out: out.write(rphoto.getvalue())
                st.session_state.candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"reason":rreason if rreason else "Cabinet","photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(CANDIDATES_FILE, st.session_state.candidates)
                st.success(f"Registered {rn}")
    with t_d:
        vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos")
        for c in [x for x in cand if x['position']==vp]:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=100)
                st.write(c['name'])
                if st.button(f"Vote {c['name']}",key=f"vote_{c['id']}"):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success("Voted")
    with t_e:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in cand if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in votes if v['candidate_id']==cc['id']])} for cc in cs]
                st.write(f"**{USERS[pos]}**"); st.dataframe(pd.DataFrame(rd),use_container_width=True)

with tab5:
    st.subheader("Disciplinary Reports")
    disc=load_json(DISC_FILE, st.session_state.disciplinary_reports)
    st.session_state.disciplinary_reports=disc
    d_t=st.text_input("Case Title *",key="disc_t")
    d_c=st.text_area("Details *",key="disc_c", height=120)
    if st.button("Save Disciplinary",type="primary",key="disc_s"):
        if not d_t or not d_c: st.error("Required")
        else:
            disc.append({"id":len(disc)+1,"title":d_t,"content":d_c,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(DISC_FILE, disc); st.success("Saved"); st.rerun()
    for dr in reversed(disc):
        with st.expander(f"{dr['title']} - {dr['by']} - {dr['date']}"):
            st.info(dr['content'])

with tab6:
    st.subheader("GP Reports - General Purpose - Vice President Leader")
    gp=load_json(GP_FILE, st.session_state.gp_reports)
    st.session_state.gp_reports=gp
    gp_t=st.text_input("GP Title *",key="gp_t")
    gp_c=st.text_area("GP Details *",key="gp_c", height=120)
    if st.button("Save GP",type="primary",key="gp_s"):
        if not gp_t or not gp_c: st.error("Required")
        else:
            gp.append({"id":len(gp)+1,"title":gp_t,"content":gp_c,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(GP_FILE, gp); st.success("Saved"); st.rerun()
    for gpr in reversed(gp):
        with st.expander(f"{gpr['title']} - {gpr['by']} - {gpr['date']}"):
            st.info(gpr['content'])

with tab7:
    st.subheader("Finance Portal - 5 Only - Principal, Patron, President, Speaker, Finance")
    fin=load_json(FINANCE_FILE, st.session_state.finance_docs)
    st.session_state.finance_docs=fin
    if user not in FINANCE_5: st.error("Finance ONLY 5: Principal, Patron, His Excellency President, Right Honourable Speaker, Finance"); st.stop()
    st.success(f"Finance 5 Access - {len(fin)} docs")
    f_t=st.text_input("Finance Title *",key="fin_t")
    f_d=st.text_area("Description",key="fin_d")
    f_f=st.file_uploader("Upload Excel / PPT / PDF / Word",type=["xlsx","xls","pptx","ppt","pdf","docx","doc","csv"],key="fin_f")
    if st.button("Save Finance Doc - Finance 5 Only",type="primary",key="fin_s"):
        if not f_t: st.error("Title required")
        else:
            fname=""; fpath=""
            if f_f:
                fname=f_f.name.replace(" ","_")
                fpath=f"data/documents/finance_{len(fin)+1}_{fname}"
                with open(fpath,'wb') as out: out.write(f_f.getvalue())
            fin.append({"id":len(fin)+1,"title":f_t,"description":f_d,"file_name":fname,"file_path":fpath,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(FINANCE_FILE, fin); st.success("Saved"); st.rerun()
    for fd in reversed(fin):
        with st.container(border=True):
            st.write(f"**{fd['title']}** - {fd['by']} - {fd['date']}")
            if fd.get('file_name',''): st.write(f"File: {fd['file_name']}")
            if fd.get('file_path','') and os.path.exists(fd['file_path']):
                st.download_button(f"Download {fd['file_name']}", open(fd['file_path'],'rb').read(), file_name=fd['file_name'], key=f"dl_fin_{fd['id']}", type="primary")

with tab8:
    st.subheader("Secret Store - Cabinet Secrets")
    sec=load_json(DOCS_FILE, st.session_state.documents)
    st.session_state.documents=sec
    dc=st.selectbox("Category",DOC_CATEGORIES,key="sec_cat")
    dt=st.text_input("Title *",key="sec_t")
    dd=st.text_area("Description",key="sec_d", height=120)
    if st.button("Save Secret Text",type="primary",key="sec_s"):
        if not dt.strip(): st.error("Title required")
        else:
            sec.append({"id":len(sec)+1,"category":dc,"title":dt.strip(),"description":dd,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DOCS_FILE, sec); st.success("Saved")
    for d in reversed(sec):
        with st.expander(f"{d['category']} | {d['title']} - {d['by']}"):
            st.write(d['description'])

with tab9:
    st.subheader("Documents - PDF, PowerPoint, Word, Excel - For ALL 13 Departments!")
    st.info("ALL 13 can upload: PDF (.pdf), PowerPoint (.pptx/.ppt), Word (.docx/.doc), Excel (.xlsx/.xls) - All see & download - Saved for years!")
    docs=load_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
    st.session_state.uploaded_docs=docs
    dcat=st.selectbox("Category",DOC_CATEGORIES,key="doc_cat")
    dt=st.text_input("Title *",key="doc_t", placeholder="e.g. Budget 2026, Constitution")
    dd=st.text_area("Description",key="doc_d")
    df=st.file_uploader("Upload File * PDF / PPT / Word / Excel - Any of 13 can upload",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv"],key="doc_f")
    if st.button("Upload Document - Visible to ALL 13",type="primary",use_container_width=True,key="doc_s"):
        if not dt.strip() or not df: st.error("Title + File required!")
        else:
            safe=df.name.replace(" ","_")
            fpath=f"data/documents/doc_{len(docs)+1}_{safe}"
            with open(fpath,'wb') as out: out.write(df.getvalue())
            ext=safe.split('.')[-1].lower()
            icon="PDF" if ext=="pdf" else "PowerPoint" if ext in ["pptx","ppt"] else "Word" if ext in ["docx","doc"] else "Excel"
            docs.append({"id":len(docs)+1,"category":dcat,"title":dt.strip(),"description":dd.strip(),"file_name":df.name,"file_path":fpath,"file_ext":ext,"file_icon":icon,"size":df.size,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(UPLOADED_DOCS_FILE, docs)
            st.success(f"Uploaded {icon} {df.name}! ALL 13 can see!"); st.balloons(); st.rerun()
    st.divider()
    for doc in reversed(docs):
        with st.container(border=True):
            st.markdown(f"{doc.get('file_icon','Doc')} **{doc['title']}** | {doc['category']} | by {doc['by']} | {doc['date']}")
            if doc.get('description',''): st.write(doc['description'])
            st.caption(f"File: {doc['file_name']} | {doc.get('file_ext','').upper()} | {doc.get('size',0)//1024} KB")
            if os.path.exists(doc.get('file_path','')):
                st.download_button(f"Download {doc['file_name']}", open(doc['file_path'],'rb').read(), file_name=doc['file_name'], key=f"dl_doc_{doc['id']}", type="primary", use_container_width=True)

with tab10:
    st.subheader("Media Gallery - ALL SEE - Photos, Videos, Music - ALL 13")
    med=load_json(MEDIA_FILE, st.session_state.media)
    st.session_state.media=med
    mt=st.text_input("Media Title *",key="media_t")
    mf=st.file_uploader("File * JPG/PNG/MP4/MP3",type=["jpg","png","jpeg","mp4","mp3","m4a","wav"],key="media_f")
    if st.button("Upload - Visible to ALL 13",type="primary",use_container_width=True,key="media_s"):
        if not mt.strip() or not mf: st.error("Title + File required")
        else:
            fpath=f"data/media_files/media_{len(med)+1}_{mf.name.replace(' ','_')}"
            with open(fpath,'wb') as out: out.write(mf.getvalue())
            med.append({"id":len(med)+1,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(MEDIA_FILE, med)
            st.success("Saved - ALL 13 can see!"); st.rerun()
    for m in reversed(med):
        with st.container(border=True):
            st.write(f"**{m['title']}** - by {m['by']} - {m['date']}")
            if os.path.exists(m['file_path']):
                if "image" in m['file_type']: st.image(m['file_path'],use_container_width=True)
                elif "video" in m['file_type']: st.video(m['file_path'])
                elif "audio" in m['file_type']: st.audio(m['file_path'])

with tab11:
    st.subheader("Cabinet Archive - For Years - First BEC, Second BEC...")
    cabs=load_json(CABINETS_FILE, st.session_state.cabinets)
    st.session_state.cabinets=cabs
    st.info("Save cabinets for future years - Works for years!")
    cy=st.text_input("Year *",key="cab_y")
    cn=st.text_input("Cabinet Name * (e.g. First BEC 2026)",key="cab_n")
    cm=st.text_area("Members *",key="cab_m")
    cp=st.file_uploader("Cabinet Photo *",type=["jpg","png","jpeg"],key="cab_p")
    if st.button("Save Cabinet - For Future Years",type="primary",use_container_width=True,key="cab_s"):
        if not cy or not cn or not cm or not cp: st.error("All fields required!")
        else:
            fpath=f"data/media_files/cab_{len(cabs)+1}.jpg"
            with open(fpath,'wb') as out: out.write(cp.getvalue())
            cabs.append({"id":len(cabs)+1,"year":cy.strip(),"name":cn.strip(),"members":cm.strip(),"photo_path":fpath,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(CABINETS_FILE, cabs)
            st.success("Saved for years!"); st.rerun()
    for cab in reversed(cabs):
        with st.container(border=True):
            st.markdown(f"**{cab['name']} - {cab['year']}** - {cab['by']}")
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'],use_container_width=True)
            st.info(cab['members'])
