import streamlit as st
import pandas as pd
import datetime
import os, json
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# ===== ADDED: SAVE TO SERVER SO ALL 13 SEE - PRINCIPAL SEES REPORTS =====
os.makedirs("data/media_files", exist_ok=True)
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

def load_json(path, default):
    if os.path.exists(path):
        try: return json.loads(open(path,'r').read())
        except: return default
    return default
def save_json(path, data):
    open(path,'w').write(json.dumps(data, default=str))

query_params = st.query_params
is_public_vote = query_params.get("public", "") == "vote"

# SINGLE HEADING ONCE + ICONS - KEPT AS BEFORE
try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
except:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)

# TITLES KEPT AS YOU SAID
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
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret"]

# LOAD FROM SERVER - SO ALL SEE - KEPT + ADDED SAVE
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
if 'passwords' not in st.session_state: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=True
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

# ===== PUBLIC ELECTORAL - VOTERS DON'T KNOW INSIDE - ONLY ELECTORAL - ONE EMAIL ONCE PER POSITION - KEPT =====
if is_public_vote:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM - PUBLIC ELECTORAL COMMISSION</h2>", unsafe_allow_html=True)
    st.info("You are voting as PUBLIC - You CANNOT see cabinet secrets inside - Only candidates")
    if st.session_state.election_open: st.success("🟢 Voting OPEN - One email = One vote per position")
    else: st.error("🔴 Voting CLOSED by Right Honourable Speaker")
    pub_tab1, pub_tab2, pub_tab3 = st.tabs(["📝 Apply as Candidate", "🗳️ Vote - Easy Click", "📊 Live Results"])
    with pub_tab1:
        rp=st.selectbox("Position You Want",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names *",key="pub_name")
        rclass=st.text_input("Class *",key="pub_class")
        rcourse=st.text_input("Course *",key="pub_course")
        remail=st.text_input("Your Email *",key="pub_email")
        rres=st.text_input("Results *",key="pub_res")
        rreason=st.text_area("Why should students vote you? *",key="pub_reason")
        rphoto=st.file_uploader("Your Photo * JPG/PNG",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit Application (Needs Chair Approval)",type="primary",use_container_width=True,key="pub_submit"):
            if not rn or not rclass or not rcourse or not remail or not rres or not rreason or not rphoto: st.error("Fill ALL *")
            else:
                nid=len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.pending_candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"course":rcourse,"email":remail,"results":rres,"reason":rreason,"photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(PENDING_FILE, st.session_state.pending_candidates)
                st.success("Sent! Wait approval from Right Honourable Speaker"); st.balloons()
    with pub_tab2:
        st.subheader("Vote - One Email Once Per Position - Easy Click")
        voter_email=st.text_input("Your Email * (One email works once per position)",key="pub_voter_email")
        if not voter_email or "@" not in voter_email: st.warning("Enter valid email to see candidates"); st.stop()
        vp=st.selectbox("Choose Position to Vote",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        already=[v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
        if already: st.error(f"❌ You already voted for {USERS[vp]} with email {voter_email} - One email once!"); st.stop()
        cands=[x for x in st.session_state.candidates if x['position']==vp]
        if not cands: st.warning("No approved candidates yet for this position")
        for c in cands:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c['photo_path'],width=150)
                st.write(f"**{c['name']}** - {c.get('class','')} - {c.get('course','')}")
                st.info(c['reason'])
                if st.button(f"✅ Vote {c['name']} - One Click",key=f"pv_{c['id']}_{voter_email}"):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success(f"Voted {c['name']} with {voter_email}! One email used for this position!"); st.balloons(); st.rerun()
    with pub_tab3:
        st.subheader("Live Results - Public")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()

# CABINET LOGIN - SECRETS INSIDE - NOT FOR PUBLIC
if not st.session_state.logged_in:
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("🔐 LOGIN TO GOVERNANCE PORTAL",use_container_width=True,type="primary",key="login_btn"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password!")
    st.info("Default unik2025 | Public link: ?public=vote - No secrets there")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
if user in SUPER_4: st.sidebar.success("SUPER 4 - View ALL reports")
if st.sidebar.button("Logout"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9=st.tabs(["📝 Submit Report","📂 Private Portal","🗳️ Electoral (Chair)","⚖️ Disciplinary","📋 GP","💰 Finance","🔐 Secret Store","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt")
    rtitle=st.text_input("Report Title *",key="rtitle")
    rcontent=st.text_area("Details *",key="rcontent")
    if st.button("📤 Submit Report - Saves to Server",type="primary",use_container_width=True,key="rsubmit"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Title + Details required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip()})
            save_json(REPORTS_FILE, st.session_state.reports)
            st.success("Submitted! Saved on server - Principal will see!"); st.balloons(); st.rerun()

with tab2:
    st.subheader("Private Portal - Where Principal Looks")
    st.session_state.reports=load_json(REPORTS_FILE, st.session_state.reports)
    if user in SUPER_4:
        show=st.session_state.reports
        st.success(f"SUPER 4: Viewing ALL {len(show)} reports from all 13")
        if show: st.dataframe(pd.DataFrame(show)['from_name'].value_counts(),use_container_width=True)
    else:
        show=[r for r in st.session_state.reports if r['from']==user]
        st.info(f"Your reports: {len(show)}")
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']}"):
            st.info(r['content'])

with tab3:
    st.subheader("Electoral Commission - Chair - FULL")
    t_pending, t_approved, t_reg, t_vote, t_res = st.tabs(["⏳ Pending","✅ Approved","📝 Register + Photo","🗳️ Vote Cabinet","📊 Results + Emails"])
    with t_pending:
        st.session_state.pending_candidates=load_json(PENDING_FILE, st.session_state.pending_candidates)
        for pc in reversed(st.session_state.pending_candidates):
            with st.container(border=True):
                if os.path.exists(pc.get('photo_path','')): st.image(pc['photo_path'],width=120)
                st.write(pc['name']+" - "+USERS[pc['position']]+" - "+pc['email'])
                if user=="speaker":
                    if st.button("✅ Approve "+pc['name'],key="ap_"+str(pc['id'])):
                        st.session_state.candidates.append(pc)
                        st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                        save_json(CANDIDATES_FILE, st.session_state.candidates)
                        save_json(PENDING_FILE, st.session_state.pending_candidates)
                        st.success("Approved"); st.rerun()
                    if st.button("❌ Reject",key="rj_"+str(pc['id'])):
                        st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                        save_json(PENDING_FILE, st.session_state.pending_candidates)
                        st.rerun()
    with t_approved:
        st.write(f"Approved: {len(st.session_state.candidates)}")
        for c in st.session_state.candidates:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=80)
                st.write(c['name']+" - "+USERS[c['position']])
    with t_reg:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos")
        rn=st.text_input("Names *",key="cand_name")
        rclass=st.text_input("Class *",key="cand_class")
        rphoto=st.file_uploader("Photo *",type=["jpg","png"],key="cand_photo")
        if st.button("Register Auto Approved",key="cand_submit"):
            if rn and rphoto:
                nid=len(st.session_state.candidates)+len(st.session_state.pending_candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"photo_path":fpath,"reason":"Cabinet Register","course":"","results":""})
                save_json(CANDIDATES_FILE, st.session_state.candidates)
                st.success("Registered Auto Approved")
    with t_vote:
        vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos")
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=100)
                st.write(c['name'])
                if st.button("Vote "+c['name'],key="vote_"+str(c['id'])):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success("Voted")
    with t_res:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
        st.divider()
        if st.session_state.votes: st.dataframe(pd.DataFrame(st.session_state.votes),use_container_width=True)

with tab4:
    d_title=st.text_input("Case Title *",key="disc_title")
    d_content=st.text_area("Details *",key="disc_content")
    if st.button("Save Disciplinary",key="disc_save"):
        if d_title and d_content:
            st.session_state.disciplinary_reports.append({"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DISC_FILE, st.session_state.disciplinary_reports)
            st.success("Saved")
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(dr['title']): st.info(dr['content'])

with tab5:
    gp_title=st.text_input("GP Title *",key="gp_title")
    gp_content=st.text_area("GP Details *",key="gp_content")
    if st.button("Save GP",key="gp_save"):
        if gp_title and gp_content:
            st.session_state.gp_reports.append({"title":gp_title,"content":gp_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(GP_FILE, st.session_state.gp_reports)
            st.success("Saved")
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(gpr['title']): st.info(gpr['content'])

with tab6:
    if user not in FINANCE_5: st.error("Finance ONLY 5"); st.stop()
    f_title=st.text_input("Finance Title *",key="fin_title")
    f_file=st.file_uploader("Excel/PPT/PDF",type=["xlsx","pptx","pdf"],key="fin_file")
    if st.button("Save Finance",key="fin_save"):
        if f_title:
            st.session_state.finance_docs.append({"title":f_title,"file_name":f_file.name if f_file else "","by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(FINANCE_FILE, st.session_state.finance_docs)
            st.success("Saved")
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True): st.write(fd['title']+" | "+fd['by'])

with tab7:
    dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat")
    dt=st.text_input("Title *",key="secret_title")
    dd=st.text_area("Description",key="secret_desc")
    if st.button("Save Secret",key="secret_save"):
        if dt.strip():
            st.session_state.documents.append({"category":dc,"title":dt.strip(),"description":dd,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DOCS_FILE, st.session_state.documents)
            st.success("Saved")
    for d in reversed(st.session_state.documents):
        with st.expander(d['category']+" | "+d['title']): st.write(d['description'])

with tab8:
    st.subheader("Media Gallery - ALL 13 Can Post and See - FIXED")
    mt=st.text_input("Media Title *",key="media_title")
    mf=st.file_uploader("Photo/Video/Music *",type=["jpg","png","mp4","mp3","m4a","wav"],key="media_file")
    if st.button("Upload Visible to ALL",type="primary",key="media_save"):
        if not mt.strip() or not mf: st.error("Title + File required")
        else:
            fid=len(st.session_state.media)+1
            fpath=f"data/media_files/media_{fid}_{mf.name}"
            open(fpath,'wb').write(mf.getvalue())
            st.session_state.media.append({"id":fid,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(MEDIA_FILE, st.session_state.media)
            st.success("Saved ALL can see!"); st.rerun()
    for m in reversed(load_json(MEDIA_FILE, st.session_state.media)):
        with st.container(border=True):
            st.write(f"{m['title']} - by {m['by']}")
            if os.path.exists(m['file_path']):
                if "image" in m['file_type']: st.image(m['file_path'],use_container_width=True)
                elif "video" in m['file_type']: st.video(m['file_path'])
                elif "audio" in m['file_type']: st.audio(m['file_path'])

with tab9:
    st.subheader("Cabinet Archive - Years - First BEC, Second BEC")
    cab_year=st.text_input("Year *",key="cab_year")
    cab_name=st.text_input("Cabinet Name *",key="cab_name")
    cab_members=st.text_area("Members *",key="cab_members")
    cab_photo=st.file_uploader("Photo *",type=["jpg","png"],key="cab_photo")
    if st.button("Save Cabinet",type="primary",key="cab_save"):
        if cab_year and cab_name and cab_members and cab_photo:
            nid=len(st.session_state.cabinets)+1
            p_path=f"data/media_files/cab_{nid}.jpg"
            open(p_path,'wb').write(cab_photo.getvalue())
            st.session_state.cabinets.append({"id":nid,"year":cab_year.strip(),"name":cab_name.strip(),"members":cab_members.strip(),"photo_path":p_path,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(CABINETS_FILE, st.session_state.cabinets)
            st.success("Saved"); st.rerun()
    for cab in reversed(load_json(CABINETS_FILE, st.session_state.cabinets)):
        with st.container(border=True):
            st.write(cab['name']+" - "+cab['year'])
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'],use_container_width=True)
            st.info(cab['members'])
