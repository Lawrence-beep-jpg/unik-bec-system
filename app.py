import streamlit as st
import pandas as pd
import datetime
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

query_params = st.query_params
is_public_vote = query_params.get("public", "") == "vote"

# ===== SINGLE HEADING - UNIK BEC UNASNM - ONLY ONCE + ICONS =====
try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
except:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
    st.caption("Hon. Lawrence Ssango - Speaker BEC - Chair Electoral & Disciplinary - University of Kisubi")

USERS={"principal":"Hon. Principal","patron":"Hon. Patron","president":"Hon. President","vice_president":"Hon. Vice President - Leader GP","speaker":"Hon. Lawrence Ssango - Speaker BEC - Chair Electoral","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys())
SUPER_4=["principal","patron","president","speaker"]
FINANCE_5=["principal","patron","president","speaker","finance"]
REPORT_TYPES=["Weekly","Monthly","Financial Excel/PPT","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Other"]
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret"]
ELECTION_POSITIONS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]

for k in ['reports','documents','candidates','votes','media','electoral_reports','disciplinary_reports','gp_reports','finance_docs','cabinets','pending_candidates']:
    if k not in st.session_state: st.session_state[k]=[]
if 'passwords' not in st.session_state: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=False
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

# ================= PUBLIC VOTING PORTAL - NO CABINET SECRETS =================
if is_public_vote:
    st.success("🏛️ UNIK BEC UNASNM Governance Portal - PUBLIC ELECTORAL COMMISSION")
    st.info("Students: Apply as Candidate (needs Chair approval) or Vote your leaders (email once). You CANNOT see cabinet secrets here.")
    if st.session_state.election_open: st.success("🟢 Voting OPEN - You can vote now")
    else: st.error("🔴 Voting CLOSED by Electoral Chair - Wait for OPEN")
    pub_tab1, pub_tab2, pub_tab3 = st.tabs(["📝 Apply as Candidate (Needs Approval)", "🗳️ Vote Leaders (Email Once)", "📊 Live Results"])
    with pub_tab1:
        st.subheader("Apply to be Leader - Needs Approval from Chair (Speaker)")
        rp=st.selectbox("Position You Want",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_cand_pos")
        rn=st.text_input("Full Names *",key="pub_cand_name")
        rclass=st.text_input("Class *",key="pub_cand_class")
        rcourse=st.text_input("Course *",key="pub_cand_course")
        remail=st.text_input("Email * (for approval notification)",key="pub_cand_email")
        rres=st.text_input("Results / Grades *",key="pub_cand_res")
        rreason=st.text_area("Why should students vote you? *",key="pub_cand_reason")
        rphoto=st.file_uploader("Your Photo * JPG/PNG",type=["jpg","png","jpeg"],key="pub_cand_photo")
        if st.button("📤 Submit Application for Approval",type="primary",use_container_width=True,key="pub_cand_submit"):
            if not rn or not rclass or not rcourse or not remail or not rres or not rreason or not rphoto:
                st.error("Fill ALL * fields")
            else:
                st.session_state.pending_candidates.append({"id":len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1,"position":rp,"name":rn,"class":rclass,"course":rcourse,"email":remail,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue(),"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success("Application Sent! Wait for Chair approval. Email: " + remail)
                st.balloons()
    with pub_tab2:
        if not st.session_state.election_open:
            st.error("Voting CLOSED by Chair"); st.stop()
        voter_email=st.text_input("Enter Your Email * (One email = One vote per position)",key="pub_voter_email")
        if not voter_email or "@" not in voter_email:
            st.warning("Enter valid email to continue"); st.stop()
        vp=st.selectbox("Choose Position to Vote",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        already_voted = [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
        if already_voted:
            st.error("You already voted for " + USERS[vp] + " with email " + voter_email)
            st.stop()
        approved_for_pos = [c for c in st.session_state.candidates if c['position']==vp]
        if not approved_for_pos: st.info("No approved candidates yet for this position. Wait for approval.")
        else:
            st.write("Candidates for " + USERS[vp])
            for c in approved_for_pos:
                with st.container(border=True):
                    st.image(c['photo_bytes'],width=150)
                    st.write(c['name'] + " - " + c['class'] + " - " + c['course'])
                    st.write("Results: " + c['results'])
                    st.info(c['reason'])
                    if st.button("Vote " + c['name'],key="pub_vote_" + str(c['id']) + "_" + voter_email):
                        st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                        st.success("Voted successfully with " + voter_email); st.balloons(); st.rerun()
    with pub_tab3:
        st.subheader("Live Results - Public")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[]
                for cc in cs:
                    vcount=len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])
                    rd.append({"Candidate":cc['name'],"Votes":vcount})
                if sum([x['Votes'] for x in rd])>0:
                    st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()

# ================= CABINET GOVERNANCE PORTAL =================
if not st.session_state.logged_in:
    st.subheader("Cabinet Login - UNIK BEC UNASNM Governance Portal")
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("🔐 LOGIN TO GOVERNANCE PORTAL",use_container_width=True,type="primary",key="login_btn"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password!")
    st.info("Default password: unik2025 | After changing, use YOUR OWN password")
    st.success("Public voting link for students (no cabinet secrets): Add ?public=vote to your app URL")
    st.code("https://unik-bec-system-edudypqshonywrcjbili.streamlit.app/?public=vote")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
st.sidebar.caption("UNIK BEC UNASNM Governance Portal")
if user in SUPER_4: st.sidebar.success("SUPER 4 - View ALL private reports")
if user in FINANCE_5: st.sidebar.success("FINANCE 5 - View Finance Portal")
with st.sidebar.expander("Change My Password - Own Password"):
    st.write("Changing password for: " + user_full)
    new_p=st.text_input("New Password",type="password",key="new_pass")
    confirm_p=st.text_input("Confirm",type="password",key="conf_pass")
    if st.button("Save New Password",key="save_pass"):
        if not new_p: st.error("Enter password")
        elif new_p!=confirm_p: st.error("Passwords dont match - Correct!")
        else: st.session_state.passwords[user]=new_p; st.success("Saved! New password: " + new_p + " - Use next login"); st.balloons()
st.sidebar.divider()
st.sidebar.info("Public Link: ?public=vote - Students vote without cabinet secrets")
if st.sidebar.button("Logout"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9=st.tabs(["📝 Submit Report","📂 Private Portal","🗳️ Electoral (Chair Approval)","⚖️ Disciplinary","📋 GP Committee","💰 Finance (5 Only)","🔐 Secret Store","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab1:
    st.subheader("Submit Report - Every command portal typing")
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt")
    rtitle=st.text_input("Report Title *",key="rtitle")
    rcontent=st.text_area("Details / Content *",height=150,key="rcontent")
    rfile=st.file_uploader("Attach File Excel/PPT/PDF/JPG/MP4/MP3",type=["xlsx","xls","pptx","ppt","pdf","jpg","png","docx","mp4","mp3","m4a","wav"],key="rfile")
    if st.button("📤 Submit Report",type="primary",use_container_width=True,key="rsubmit"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Title + Details required")
        else: st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":rfile.name if rfile else None,"file_bytes":rfile.getvalue() if rfile else None}); st.success("Submitted!"); st.balloons()

with tab2:
    st.subheader("Private Portal - " + user_full)
    if user in SUPER_4: show=st.session_state.reports; st.success("SUPER 4: Viewing ALL " + str(len(show)) + " reports")
    else: show=[r for r in st.session_state.reports if r['from']==user]; st.info("Private: Your reports " + str(len(show)) + " - Others cannot see yours")
    if show:
        df_list=[{"id":r["id"],"date":r["date"],"from_name":r["from_name"],"type":r["type"],"title":r["title"]} for r in show]
        st.dataframe(pd.DataFrame(df_list).sort_values(by="id",ascending=False),use_container_width=True)
        for r in reversed(show):
            with st.expander("#" + str(r['id']) + " " + r['title'] + " - " + r['from_name']):
                st.write("Type: " + r['type'] + " | Date: " + r['date'])
                st.info(r['content'])
                if r.get('file_bytes'): st.download_button("Download " + r['file_name'],r['file_bytes'],r['file_name'],key="dl_priv_" + str(r['id']))

with tab3:
    st.subheader("Electoral Commission - Chair Approval System")
    pending_len=len(st.session_state.pending_candidates)
    st.info("Pending approvals: " + str(pending_len) + " | Public Link: ?public=vote | Share to students")
    if user=="speaker":
        if not st.session_state.election_open:
            if st.button("🟢 OPEN VOTING (Public + Cabinet)",type="primary",key="open"): st.session_state.election_open=True;st.rerun()
        else:
            if st.button("🔴 CLOSE VOTING",key="close"): st.session_state.election_open=False;st.rerun()
        st.write("Status: OPEN" if st.session_state.election_open else "Status: CLOSED")
    t_pending, t_approved, t_reg, t_vote, t_res = st.tabs(["⏳ Pending Approval","✅ Approved","📝 Register Cabinet","🗳️ Vote Cabinet","📊 Results + Emails"])
    with t_pending:
        st.subheader("Pending Applications Need Chair Approval")
        if not st.session_state.pending_candidates: st.success("No pending")
        for pc in reversed(st.session_state.pending_candidates):
            with st.container(border=True):
                st.image(pc['photo_bytes'],width=120)
                st.write(pc['name'] + " | " + USERS[pc['position']] + " | Email: " + pc['email'])
                st.write("Class: " + pc['class'] + " | Course: " + pc['course'] + " | Results: " + pc['results'])
                st.info(pc['reason'])
                if st.button("✅ Approve " + pc['name'],key="ap_" + str(pc['id'])):
                    st.session_state.candidates.append({"id":pc['id'],"position":pc['position'],"name":pc['name'],"class":pc['class'],"course":pc['course'],"email":pc['email'],"results":pc['results'],"reason":pc['reason'],"photo_bytes":pc['photo_bytes']})
                    st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                    st.success("Approved " + pc['name']); st.balloons(); st.rerun()
                if st.button("❌ Reject " + pc['name'],key="rj_" + str(pc['id'])):
                    st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]; st.error("Rejected"); st.rerun()
    with t_approved:
        st.write("Total Approved: " + str(len(st.session_state.candidates)))
        for c in st.session_state.candidates:
            with st.container(border=True): st.image(c['photo_bytes'],width=80); st.write(c['name'] + " - " + USERS[c['position']])
    with t_reg:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos")
        rn=st.text_input("Full Names *",key="cand_name"); rclass=st.text_input("Class *",key="cand_class"); rcourse=st.text_input("Course *",key="cand_course"); rres=st.text_input("Results *",key="cand_res"); rreason=st.text_area("Reason *",key="cand_reason"); rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="cand_photo")
        if st.button("Register (Auto Approved Cabinet)",type="primary",key="cand_submit"):
            if rn and rclass and rcourse and rres and rreason and rphoto: st.session_state.candidates.append({"id":len(st.session_state.candidates)+len(st.session_state.pending_candidates)+1,"position":rp,"name":rn,"class":rclass,"course":rcourse,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue()}); st.success("Registered Auto Approved"); st.balloons()
            else: st.error("Fill ALL *")
    with t_vote:
        if not st.session_state.election_open: st.error("Voting Closed")
        else:
            vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos")
            for c in [x for x in st.session_state.candidates if x['position']==vp]:
                with st.container(border=True): st.image(c['photo_bytes'],width=120); st.write(c['name'])
                if st.button("Vote " + c['name'],key="vote_" + str(c['id'])): st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user+"@cabinet","position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("Voted!"); st.rerun()
    with t_res:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[]
                for cc in cs:
                    vcount=len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])
                    rd.append({"Candidate":cc['name'],"Votes":vcount})
                st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
        st.divider()
        st.subheader("Voter Emails Tracked - One email per position")
        if st.session_state.votes: st.dataframe(pd.DataFrame(st.session_state.votes),use_container_width=True)

with tab4:
    st.subheader("Disciplinary Reports - ALL 13")
    d_title=st.text_input("Case Title *",key="disc_title"); d_content=st.text_area("Details *",key="disc_content")
    if st.button("Save Disciplinary",type="primary",key="disc_save"):
        if d_title and d_content: st.session_state.disciplinary_reports.append({"id":len(st.session_state.disciplinary_reports)+1,"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("Saved!"); st.balloons()
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(dr['title'] + " - " + dr['by'] + " - " + dr['date']): st.warning(dr['content'])

with tab5:
    st.subheader("GP Committee Reports - ALL 13 - Leader Vice President")
    gp_title=st.text_input("GP Title *",key="gp_title"); gp_content=st.text_area("GP Details *",key="gp_content")
    if st.button("Save GP Report",type="primary",key="gp_save"):
        if gp_title and gp_content: st.session_state.gp_reports.append({"id":len(st.session_state.gp_reports)+1,"title":gp_title,"content":gp_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("Saved!"); st.balloons()
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(gpr['title'] + " - " + gpr['by']): st.info(gpr['content'])

with tab6:
    if user not in FINANCE_5: st.error("🔒 Finance Portal - ONLY 5 ALLOWED: Finance Secretary + Speaker + President + Patron + Principal"); st.stop()
    st.subheader("💰 Finance Portal - 5 ONLY - Excel PPT Budget")
    f_title=st.text_input("Finance Title *",key="fin_title"); f_type=st.selectbox("Type",["Budget Excel","PPT Report","Expense","Income","Other"],key="fin_type"); f_desc=st.text_area("Description",key="fin_desc"); f_file=st.file_uploader("Upload Excel / PPT / PDF *",type=["xlsx","xls","pptx","ppt","pdf","csv"],key="fin_file")
    if st.button("💰 Save Finance Document",type="primary",use_container_width=True,key="fin_save"):
        if not f_title.strip() or not f_file: st.error("Title + File required")
        else: st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title.strip(),"type":f_type,"description":f_desc,"file_name":f_file.name,"file_bytes":f_file.getvalue(),"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("Saved: " + f_file.name); st.balloons(); st.rerun()
    st.divider()
    st.write("Total Finance Docs: " + str(len(st.session_state.finance_docs)))
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True): st.write(fd['title'] + " | " + fd['file_name'] + " | " + fd['type'] + " | by " + fd['by'] + " | " + fd['date']); st.write(fd['description']); st.download_button("Download " + fd['file_name'],fd['file_bytes'],fd['file_name'],key="dl_fin_" + str(fd['id']))

with tab7:
    st.subheader("🔐 Secret Store - ALL 13 - Constitution Budget Minutes")
    dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat"); dt=st.text_input("Title *",key="secret_title"); dd=st.text_area("Description",key="secret_desc"); uf=st.file_uploader("Upload File (Optional) - Will save as note if no file",type=["pdf","docx","xlsx","pptx","jpg","png"],key="secret_file")
    if st.button("🔐 Save to Secret Store",type="primary",key="secret_save"):
        if not dt.strip(): st.error("Title required")
        else: st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"file_name":uf.name if uf else "Note Only","file_bytes":uf.getvalue() if uf else None,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("Saved to Secret Store!"); st.balloons(); st.rerun()
    for d in reversed(st.session_state.documents):
        with st.expander(d['category'] + " | " + d['title'] + " - " + d['by']):
            st.write(d['description']); st.write("Date: " + d['date'])
            if d['file_bytes']: st.download_button("Download " + d['file_name'],d['file_bytes'],d['file_name'],key="dl_sec_" + str(d['id']))

with tab8:
    st.subheader("📸 Media Gallery - EVERY MEMBER can upload Photo/Video/Music + EVERY MEMBER view!")
    st.success("ALL 13 can upload + view - Photos JPG PNG, Videos MP4 MOV, Music MP3 M4A WAV OGG")
    filter_type=st.selectbox("Filter Media Gallery", ["All Media","Photos Only JPG PNG","Videos Only MP4 MOV","Music Only MP3 WAV"], key="media_filter")
    c1,c2=st.columns([2,1])
    with c1: mt=st.text_input("Media Title * e.g. Sports Day 2025, Cultural Dance",key="media_title")
    with c2: st.write("Supported: JPG PNG MP4 MOV MP3 M4A WAV OGG")
    mf=st.file_uploader("Choose Photo / Video / Music File *",type=["jpg","png","jpeg","mp4","mov","avi","mp3","m4a","wav","ogg"],key="media_file")
    if st.button("📸 Upload to Media Gallery - Visible to ALL",type="primary",use_container_width=True,key="media_save"):
        if not mt.strip() or not mf: st.error("❌ ERROR: Title + File required - Type title + choose file first! Correct!")
        else: st.session_state.media.append({"id":len(st.session_state.media)+1,"title":mt.strip(),"file_name":mf.name,"file_bytes":mf.getvalue(),"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}); st.success("Media Saved: " + mf.name + "! Everyone can see it!"); st.balloons(); st.rerun()
    st.divider()
    st.write("Total Media: " + str(len(st.session_state.media)) + " - Visible to ALL 13 members")
    for m in reversed(st.session_state.media):
        ftype=m['file_type']
        if filter_type=="Photos Only JPG PNG" and "image" not in ftype: continue
        if filter_type=="Videos Only MP4 MOV" and "video" not in ftype: continue
        if filter_type=="Music Only MP3 WAV" and "audio" not in ftype: continue
        with st.container(border=True):
            st.write("**" + m['title'] + "** - " + m['file_name'] + " - by " + m['by'] + " - " + m['date'])
            if "image" in ftype: st.image(m['file_bytes'],use_container_width=True)
            elif "video" in ftype: st.video(m['file_bytes'])
            elif "audio" in ftype: st.audio(m['file_bytes'])
            st.download_button("📥 Download " + m['file_name'],m['file_bytes'],m['file_name'],key="dl_med_" + str(m['id']))

with tab9:
    st.subheader("🏛️ Cabinet Archive - Different Years - First BEC, Second BEC, Yearly")
    st.success("EVERY MEMBER can view all cabinets yearly + upload new cabinet! Examples: First BEC Leadership Cabinet 2024/2025")
    with st.container(border=True):
        st.write("Add New Yearly Cabinet - Everyone had space portal")
        cab_year=st.text_input("Year * e.g. 2024/2025, 2025/2026", key="cab_year")
        cab_name=st.text_input("Cabinet Name * e.g. First BEC Leadership Cabinet, Second BEC Cabinet", key="cab_name")
        cab_members=st.text_area("List All Members in Cabinet * e.g. President: John Doe, Speaker: Lawrence Ssango, Finance: Jane...", height=120, key="cab_members")
        cab_desc=st.text_area("Achievements / Description / What cabinet did", key="cab_desc")
        cab_photo=st.file_uploader("Cabinet Group Photo * JPG/PNG - Required", type=["jpg","png","jpeg"], key="cab_photo")
        cab_video=st.file_uploader("Cabinet Video (Optional) MP4/MOV - e.g. Handover ceremony", type=["mp4","mov","avi"], key="cab_video")
        if st.button("🏛️ Save Cabinet to Archive - Yearly", type="primary", use_container_width=True, key="cab_save"):
            if not cab_year.strip() or not cab_name.strip() or not cab_members.strip() or not cab_photo:
                st.error("❌ ERROR: Year + Cabinet Name + Members + Photo required! Correct!")
            else:
                st.session_state.cabinets.append({"id":len(st.session_state.cabinets)+1,"year":cab_year.strip(),"name":cab_name.strip(),"members":cab_members.strip(),"desc":cab_desc,"photo_bytes":cab_photo.getvalue(),"photo_name":cab_photo.name,"video_bytes":cab_video.getvalue() if cab_video else None,"video_name":cab_video.name if cab_video else None,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success("Cabinet Saved: " + cab_name + " - " + cab_year + "! Visible to ALL!"); st.balloons(); st.rerun()
    st.divider()
    st.write("Total Cabinets Archived: " + str(len(st.session_state.cabinets)) + " yearly cabinets")
    years = sorted(list(set([c['year'] for c in st.session_state.cabinets])), reverse=True) if st.session_state.cabinets else []
    if years: selected_year=st.selectbox("Filter by Year - View Different Years", ["All Years"] + years, key="cab_filter_year")
    else: selected_year="All Years"
    for cab in reversed(st.session_state.cabinets):
        if selected_year!="All Years" and cab['year']!=selected_year: continue
        with st.container(border=True):
            st.subheader(cab['name'] + " - " + cab['year'])
            st.write("Archived: " + cab['date'] + " | By: " + cab['by'])
            col1,col2=st.columns([1,1])
            with col1: st.image(cab['photo_bytes'], caption=cab['name'] + " Photo - " + cab['year'], use_container_width=True)
            with col2: st.write("**👥 Members in this Cabinet:**"); st.info(cab['members']); 
            if cab.get('desc'): st.write("**🏆 Achievements:**"); st.success(cab['desc'])
            if cab.get('video_bytes'): st.write("**🎥 Cabinet Video:**"); st.video(cab['video_bytes'])
            cA,cB=st.columns(2)
            with cA: st.download_button("📥 Download Photo " + cab['photo_name'], cab['photo_bytes'], cab['photo_name'], key="dl_cab_photo_" + str(cab['id']))
            with cB:
                if cab.get('video_bytes'): st.download_button("📥 Download Video " + cab['video_name'], cab['video_bytes'], cab['video_name'], key="dl_cab_video_" + str(cab['id']))
