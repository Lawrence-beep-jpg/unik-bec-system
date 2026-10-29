import streamlit as st
import pandas as pd
import datetime
import os, json
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# ===== SERVER SAVE FOR ALL 13 - FIX FOR MEDIA + REPORTS VISIBLE TO ALL =====
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

# SINGLE HEADING ONCE + ICONS KEPT
try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
except:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
    st.caption("Hon. Lawrence Ssango - Right Honourable Speaker BEC")

# ===== CORRECTED TITLES AS YOU SAID =====
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
REPORT_TYPES=["Weekly","Monthly","Financial Excel/PPT","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Other"]
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret"]
ELECTION_POSITIONS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]

# LOAD FROM SERVER - NOW VISIBLE TO ALL PHONES
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

# ================= PUBLIC VOTING - NO SECRETS =================
if is_public_vote:
    st.success("🏛️ UNIK BEC UNASNM - PUBLIC ELECTORAL COMMISSION")
    if st.session_state.election_open: st.success("🟢 Voting OPEN")
    else: st.error("🔴 Voting CLOSED by Chair")
    pub_tab1, pub_tab2, pub_tab3 = st.tabs(["📝 Apply as Candidate (Needs Approval)", "🗳️ Vote Leaders", "📊 Live Results"])
    with pub_tab1:
        rp=st.selectbox("Position You Want",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names *",key="pub_name")
        rclass=st.text_input("Class *",key="pub_class")
        rcourse=st.text_input("Course *",key="pub_course")
        remail=st.text_input("Email *",key="pub_email")
        rres=st.text_input("Results *",key="pub_res")
        rreason=st.text_area("Why vote you? *",key="pub_reason")
        rphoto=st.file_uploader("Your Photo *",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit Application",type="primary",use_container_width=True,key="pub_submit"):
            if not rn or not rclass or not rcourse or not remail or not rres or not rreason or not rphoto: st.error("Fill ALL *")
            else:
                nid=len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.pending_candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"course":rcourse,"email":remail,"results":rres,"reason":rreason,"photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(PENDING_FILE, st.session_state.pending_candidates)
                st.success("Sent! Wait approval"); st.balloons()
    with pub_tab2:
        voter_email=st.text_input("Your Email *",key="pub_voter_email")
        if not voter_email or "@" not in voter_email: st.warning("Enter valid email"); st.stop()
        vp=st.selectbox("Choose Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        if [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]: st.error("You already voted for this position!"); st.stop()
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c['photo_path'],width=150)
                st.write(c['name']); st.info(c['reason'])
                if st.button("Vote "+c['name'],key="pv_"+str(c['id'])+"_"+voter_email):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success("Voted!"); st.rerun()
    with pub_tab3:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()

# ================= CABINET LOGIN =================
if not st.session_state.logged_in:
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("🔐 LOGIN TO GOVERNANCE PORTAL",use_container_width=True,type="primary",key="login_btn"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password!")
    st.info("Default unik2025 | Public link: ?public=vote")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
if user in SUPER_4: st.sidebar.success("SUPER 4 - View ALL reports")
if user in FINANCE_5: st.sidebar.success("FINANCE 5 - View Finance")
with st.sidebar.expander("Change My Password - Own Password"):
    new_p=st.text_input("New Password",type="password",key="new_pass")
    confirm_p=st.text_input("Confirm",type="password",key="conf_pass")
    if st.button("Save Password",key="save_pass"):
        if not new_p: st.error("Enter password")
        elif new_p!=confirm_p: st.error("Dont match")
        else: st.session_state.passwords[user]=new_p; st.success("Saved: "+new_p)
if st.sidebar.button("Logout"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9=st.tabs(["📝 Submit Report","📂 Private Portal","🗳️ Electoral (Chair Approval)","⚖️ Disciplinary","📋 GP Committee","💰 Finance (5 Only)","🔐 Secret Store","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt")
    rtitle=st.text_input("Report Title *",key="rtitle")
    rcontent=st.text_area("Details / Content *",height=150,key="rcontent")
    rfile=st.file_uploader("Attach File Excel/PPT/PDF/JPG/MP4/MP3",type=["xlsx","xls","pptx","ppt","pdf","jpg","png","docx","mp4","mp3","m4a","wav"],key="rfile")
    if st.button("📤 Submit Report",type="primary",use_container_width=True,key="rsubmit"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Title + Details required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":rfile.name if rfile else None})
            save_json(REPORTS_FILE, st.session_state.reports)
            st.success("Submitted! Now saved on server - SUPER 4 can see!"); st.balloons()

with tab2:
    st.subheader("Private Portal - " + user_full)
    if user in SUPER_4:
        show=st.session_state.reports
        st.success(f"SUPER 4: Viewing ALL {len(show)} reports from all departments")
        if show:
            df=pd.DataFrame(show)
            st.write("Reports per department:")
            st.dataframe(df['from_name'].value_counts(),use_container_width=True)
    else:
        show=[r for r in st.session_state.reports if r['from']==user]
        st.info(f"Your reports: {len(show)} - SUPER 4 sees them")
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']}"):
            st.write("Type: "+r['type'])
            st.info(r['content'])

with tab3:
    st.subheader("Electoral Commission - FULL AS BEFORE - With Chair Approval")
    st.info(f"Pending: {len(st.session_state.pending_candidates)} | Approved: {len(st.session_state.candidates)} | Public Link: ?public=vote")
    if user=="speaker":
        if not st.session_state.election_open:
            if st.button("🟢 OPEN VOTING",type="primary",key="open"): st.session_state.election_open=True;st.rerun()
        else:
            if st.button("🔴 CLOSE VOTING",key="close"): st.session_state.election_open=False;st.rerun()
    t_pending, t_approved, t_reg, t_vote, t_res = st.tabs(["⏳ Pending Approval","✅ Approved","📝 Register Cabinet + Upload Photo","🗳️ Vote Cabinet","📊 Results + Emails"])
    with t_pending:
        if not st.session_state.pending_candidates: st.success("No pending")
        for pc in reversed(st.session_state.pending_candidates):
            with st.container(border=True):
                if os.path.exists(pc.get('photo_path','')): st.image(pc['photo_path'],width=120)
                st.write(pc['name']+" | "+USERS[pc['position']]+" | Email: "+pc['email'])
                st.write(f"Class: {pc['class']} | Course: {pc['course']} | Results: {pc['results']}")
                st.info(pc['reason'])
                if st.button("✅ Approve "+pc['name'],key="ap_"+str(pc['id'])):
                    st.session_state.candidates.append(pc)
                    st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                    save_json(CANDIDATES_FILE, st.session_state.candidates)
                    save_json(PENDING_FILE, st.session_state.pending_candidates)
                    st.success("Approved"); st.balloons(); st.rerun()
                if st.button("❌ Reject "+pc['name'],key="rj_"+str(pc['id'])):
                    st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                    save_json(PENDING_FILE, st.session_state.pending_candidates)
                    st.rerun()
    with t_approved:
        st.write(f"Total Approved: {len(st.session_state.candidates)}")
        for c in st.session_state.candidates:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=80)
                st.write(c['name']+" - "+USERS[c['position']])
    with t_reg:
        st.subheader("Register Cabinet Candidate - Upload Photo")
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos")
        rn=st.text_input("Full Names *",key="cand_name")
        rclass=st.text_input("Class *",key="cand_class")
        rcourse=st.text_input("Course *",key="cand_course")
        rres=st.text_input("Results *",key="cand_res")
        rreason=st.text_area("Reason *",key="cand_reason")
        rphoto=st.file_uploader("Photo * JPG/PNG",type=["jpg","png","jpeg"],key="cand_photo")
        if st.button("Register Candidate (Auto Approved)",type="primary",key="cand_submit"):
            if not rn or not rclass or not rcourse or not rres or not rreason or not rphoto: st.error("Fill ALL *")
            else:
                nid=len(st.session_state.candidates)+len(st.session_state.pending_candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"course":rcourse,"results":rres,"reason":rreason,"photo_path":fpath})
                save_json(CANDIDATES_FILE, st.session_state.candidates)
                st.success("Registered Auto Approved!"); st.balloons()
    with t_vote:
        vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos")
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=120)
                st.write(c['name'])
                if st.button("Vote "+c['name'],key="vote_"+str(c['id'])):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user+"@cabinet","position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success("Voted!")
    with t_res:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
        st.divider()
        st.subheader("Voter Emails Tracked")
        if st.session_state.votes: st.dataframe(pd.DataFrame(st.session_state.votes),use_container_width=True)

with tab4:
    st.subheader("Disciplinary Reports - ALL 13")
    d_title=st.text_input("Case Title *",key="disc_title")
    d_content=st.text_area("Details *",key="disc_content")
    if st.button("Save Disciplinary",type="primary",key="disc_save"):
        if d_title and d_content:
            st.session_state.disciplinary_reports.append({"id":len(st.session_state.disciplinary_reports)+1,"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DISC_FILE, st.session_state.disciplinary_reports)
            st.success("Saved!"); st.balloons()
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(dr['title']+" - "+dr['by']): st.warning(dr['content'])

with tab5:
    st.subheader("GP Committee Reports - ALL 13")
    gp_title=st.text_input("GP Title *",key="gp_title")
    gp_content=st.text_area("GP Details *",key="gp_content")
    if st.button("Save GP Report",type="primary",key="gp_save"):
        if gp_title and gp_content:
            st.session_state.gp_reports.append({"id":len(st.session_state.gp_reports)+1,"title":gp_title,"content":gp_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(GP_FILE, st.session_state.gp_reports)
            st.success("Saved!"); st.balloons()
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(gpr['title']+" - "+gpr['by']): st.info(gpr['content'])

with tab6:
    if user not in FINANCE_5: st.error("🔒 Finance ONLY 5: Finance + Right Honourable Speaker + His Excellency President + Patron + Principal"); st.stop()
    st.subheader("💰 Finance Portal - 5 ONLY")
    f_title=st.text_input("Finance Title *",key="fin_title")
    f_file=st.file_uploader("Upload Excel / PPT / PDF *",type=["xlsx","xls","pptx","ppt","pdf"],key="fin_file")
    if st.button("Save Finance",type="primary",key="fin_save"):
        if not f_title or not f_file: st.error("Title + File required")
        else:
            st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title,"file_name":f_file.name,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(FINANCE_FILE, st.session_state.finance_docs)
            st.success("Saved!"); st.balloons()
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True): st.write(fd['title']+" | "+fd['file_name']+" | by "+fd['by'])

with tab7:
    st.subheader("🔐 Secret Store - ALL 13")
    dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat")
    dt=st.text_input("Title *",key="secret_title")
    dd=st.text_area("Description",key="secret_desc")
    uf=st.file_uploader("Upload File (Optional)",type=["pdf","docx","xlsx","pptx","jpg","png"],key="secret_file")
    if st.button("Save to Secret Store",type="primary",key="secret_save"):
        if not dt.strip(): st.error("Title required")
        else:
            st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"file_name":uf.name if uf else "Note","by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DOCS_FILE, st.session_state.documents)
            st.success("Saved!"); st.balloons()
    for d in reversed(st.session_state.documents):
        with st.expander(d['category']+" | "+d['title']+" - "+d['by']):
            st.write(d['description'])

with tab8:
    st.subheader("📸 Media Gallery - EVERY MEMBER CAN POST AND SEE - FIXED!")
    st.success("FIXED: Now saved on server disk - PC post, Phone sees! ALL 13 can upload and view!")
    filter_type=st.selectbox("Filter Media", ["All Media","Photos Only","Videos Only","Music Only"], key="media_filter")
    mt=st.text_input("Media Title *",key="media_title")
    mf=st.file_uploader("Photo / Video / Music File *",type=["jpg","png","jpeg","mp4","mov","mp3","m4a","wav","ogg"],key="media_file")
    if st.button("📸 Upload - Visible to ALL 13",type="primary",use_container_width=True,key="media_save"):
        if not mt.strip() or not mf: st.error("❌ ERROR: Title + File required - Correct!")
        else:
            fid=len(st.session_state.media)+1
            fpath=f"data/media_files/media_{fid}_{mf.name}"
            open(fpath,'wb').write(mf.getvalue())
            st.session_state.media.append({"id":fid,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(MEDIA_FILE, st.session_state.media)
            st.success(f"Saved! {mf.name} now visible to ALL!"); st.balloons(); st.rerun()
    st.divider()
    st.write(f"Total Media visible to ALL: {len(st.session_state.media)}")
    for m in reversed(st.session_state.media):
        ftype=m['file_type']
        if filter_type=="Photos Only" and "image" not in ftype: continue
        if filter_type=="Videos Only" and "video" not in ftype: continue
        if filter_type=="Music Only" and "audio" not in ftype: continue
        with st.container(border=True):
            st.write(f"**{m['title']}** - {m['file_name']} - by {m['by']} - {m['date']}")
            if os.path.exists(m['file_path']):
                if "image" in ftype: st.image(m['file_path'],use_container_width=True)
                elif "video" in ftype: st.video(m['file_path'])
                elif "audio" in ftype: st.audio(m['file_path'])
                with open(m['file_path'],'rb') as f:
                    st.download_button(f"Download {m['file_name']}",f,m['file_name'],key=f"dl_{m['id']}")

with tab9:
    st.subheader("🏛️ Cabinet Archive - Different Years - First BEC, Second BEC")
    st.success("EVERY MEMBER can view all cabinets yearly + upload new cabinet!")
    with st.container(border=True):
        cab_year=st.text_input("Year * e.g. 2024/2025", key="cab_year")
        cab_name=st.text_input("Cabinet Name * e.g. First BEC Leadership Cabinet", key="cab_name")
        cab_members=st.text_area("List All Members *", height=120, key="cab_members")
        cab_desc=st.text_area("Achievements", key="cab_desc")
        cab_photo=st.file_uploader("Cabinet Group Photo *", type=["jpg","png","jpeg"], key="cab_photo")
        cab_video=st.file_uploader("Cabinet Video (Optional) MP4", type=["mp4","mov"], key="cab_video")
        if st.button("🏛️ Save Cabinet to Archive", type="primary", use_container_width=True, key="cab_save"):
            if not cab_year.strip() or not cab_name.strip() or not cab_members.strip() or not cab_photo: st.error("Year + Name + Members + Photo required!")
            else:
                nid=len(st.session_state.cabinets)+1
                p_path=f"data/media_files/cab_{nid}_{cab_photo.name}"
                open(p_path,'wb').write(cab_photo.getvalue())
                v_path=None
                if cab_video:
                    v_path=f"data/media_files/cabvid_{nid}_{cab_video.name}"
                    open(v_path,'wb').write(cab_video.getvalue())
                st.session_state.cabinets.append({"id":nid,"year":cab_year.strip(),"name":cab_name.strip(),"members":cab_members.strip(),"desc":cab_desc,"photo_path":p_path,"video_path":v_path,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(CABINETS_FILE, st.session_state.cabinets)
                st.success(f"Cabinet Saved: {cab_name} - {cab_year}!"); st.balloons(); st.rerun()
    st.divider()
    years = sorted(list(set([c['year'] for c in st.session_state.cabinets])), reverse=True) if st.session_state.cabinets else []
    if years: selected_year=st.selectbox("Filter by Year", ["All Years"] + years, key="cab_filter_year")
    else: selected_year="All Years"
    for cab in reversed(st.session_state.cabinets):
        if selected_year!="All Years" and cab['year']!=selected_year: continue
        with st.container(border=True):
            st.subheader(cab['name']+" - "+cab['year'])
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'],use_container_width=True)
            st.info(cab['members'])
            if cab.get('desc'): st.success(cab['desc'])
            if cab.get('video_path') and os.path.exists(cab['video_path']): st.video(cab['video_path'])
