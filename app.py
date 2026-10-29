import streamlit as st
import pandas as pd
import datetime
st.set_page_config(page_title="UNIK BEC Governance Portal System", page_icon="🏛️", layout="wide")

query_params = st.query_params
is_public_vote = query_params.get("public", "") == "vote"

try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
except:
    st.title("🏛️ UNIK BEC GOVERNANCE PORTAL SYSTEM")
    st.caption("Hon. Lawrence Ssango - Speaker BEC - Governance Portal")

USERS={"principal":"Hon. Principal","patron":"Hon. Patron","president":"Hon. President","vice_president":"Hon. Vice President - Leader GP","speaker":"Hon. Lawrence Ssango - Speaker BEC - Chair Electoral & Disciplinary","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys())
SUPER_4=["principal","patron","president","speaker"]
FINANCE_5=["principal","patron","president","speaker","finance"]
REPORT_TYPES=["Weekly","Monthly","Financial Excel/PPT","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Other"]
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret"]
ELECTION_POSITIONS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]

for k in ['reports','documents','candidates','votes','media','electoral_reports','disciplinary_reports','gp_reports','finance_docs','cabinets','pending_candidates','approved_voter_emails']:
    if k not in st.session_state: st.session_state[k]=[]
if 'passwords' not in st.session_state: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=False
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

if is_public_vote:
    st.success("🏛️ UNIK BEC GOVERNANCE PORTAL - PUBLIC ELECTORAL COMMISSION")
    st.info("Welcome Students! Apply as Candidate (needs approval) or Vote leaders (once per email). No cabinet secrets here.")
    status_text = "OPEN - You can vote now!" if st.session_state.election_open else "CLOSED - Wait for Chair to open"
    st.warning("Election Status: " + status_text)
    pub_tab1, pub_tab2 = st.tabs(["📝 Apply as Candidate (Needs Approval)", "🗳️ Vote Leaders (Email Once)"])
    with pub_tab1:
        st.subheader("Apply to be a Leader - Needs Approval from Electoral Chair")
        rp=st.selectbox("Position You Want",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_cand_pos")
        rn=st.text_input("Your Full Names *",key="pub_cand_name")
        rclass=st.text_input("Your Class *",key="pub_cand_class")
        rcourse=st.text_input("Your Course *",key="pub_cand_course")
        remail=st.text_input("Your Email * (for approval)",key="pub_cand_email")
        rres=st.text_input("Your Results / Grades *",key="pub_cand_res")
        rreason=st.text_area("Why should students vote you? *",key="pub_cand_reason")
        rphoto=st.file_uploader("Your Photo * JPG/PNG",type=["jpg","png","jpeg"],key="pub_cand_photo")
        if st.button("📤 Submit Application for Approval",type="primary",use_container_width=True,key="pub_cand_submit"):
            if not rn or not rclass or not rcourse or not remail or not rres or not rreason or not rphoto:
                st.error("❌ Fill ALL * fields - Correct!")
            else:
                st.session_state.pending_candidates.append({"id":len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1,"position":rp,"name":rn,"class":rclass,"course":rcourse,"email":remail,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue(),"status":"pending","date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success("✅ Application Sent! Wait for Chair (Speaker) to approve. Email: " + remail)
                st.balloons()
    with pub_tab2:
        if not st.session_state.election_open:
            st.error("🔴 Voting is CLOSED now by Electoral Chair. Please wait for OPEN.")
            st.stop()
        st.subheader("Vote Your Leaders - One Email = One Vote per Position")
        voter_email=st.text_input("Enter Your Email * (One vote per position - email tracked)",key="pub_voter_email")
        if not voter_email or "@" not in voter_email:
            st.warning("Enter valid email to continue voting")
            st.stop()
        vp=st.selectbox("Choose Position to Vote",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        already_voted = [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
        if already_voted:
            st.error("❌ You already voted for this position with email " + voter_email + ". One email = One vote per position!")
            st.stop()
        approved_for_pos = [c for c in st.session_state.candidates if c['position']==vp]
        if not approved_for_pos:
            st.info("No approved candidates yet for this position. Wait for approval.")
        else:
            st.write("Candidates for " + USERS[vp] + ":")
            for c in approved_for_pos:
                with st.container(border=True):
                    st.image(c['photo_bytes'],width=150)
                    st.write("**" + c['name'] + "** - " + c['class'] + " - " + c['course'])
                    st.write("Results: " + c['results'])
                    st.info(c['reason'])
                    if st.button("✅ Vote " + c['name'],key="pub_vote_" + str(c['id']) + "_" + voter_email):
                        st.session_state.votes.append({"candidate_id":c['id'],"voter":"public_" + voter_email,"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                        st.success("✅ Voted successfully with " + voter_email + " for " + c['name'] + "! You cannot vote again for this position with same email.")
                        st.balloons()
                        st.rerun()
        st.divider()
        st.subheader("📊 Live Results (Public)")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":c['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==c['id']])} for c in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write("**" + USERS[pos] + "**")
                    st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()

if not st.session_state.logged_in:
    st.title("🏛️ UNIK BEC GOVERNANCE PORTAL SYSTEM - Cabinet Login")
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login_finalfinal")
    p=st.text_input("Password",type="password",key="pass_finalfinal")
    if st.button("🔐 LOGIN TO GOVERNANCE PORTAL",use_container_width=True,type="primary",key="login_btn_finalfinal"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password!")
    st.info("Default: unik2025 | After change, use YOUR OWN password")
    st.divider()
    st.success("🔗 PUBLIC VOTING LINK TO SHARE TO ALL STUDENTS (They won't see cabinet secrets): Add ?public=vote to your app URL")
    st.code("?public=vote - Add to end of your app URL", language="text")
    st.write("Example: https://unik-bec-system-edudypqshonywrcjbili.streamlit.app/?public=vote")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
st.sidebar.caption("UNIK BEC Governance Portal")
if user in SUPER_4: st.sidebar.success("✅ SUPER 4 - View ALL private")
if user in FINANCE_5: st.sidebar.success("💰 FINANCE 5 - View Finance Portal")
with st.sidebar.expander("🔑 Change My Password - Own Password"):
    st.write("Current: " + user_full)
    new_p=st.text_input("New Password",type="password",key="new_pass_ff")
    confirm_p=st.text_input("Confirm New Password",type="password",key="confirm_pass_ff")
    if st.button("Save New Password",key="save_pass_ff"):
        if not new_p: st.error("Enter new password")
        elif new_p!=confirm_p: st.error("❌ Passwords don't match - Correct!")
        else: st.session_state.passwords[user]=new_p; st.success("✅ Password changed! New: " + new_p + " - Use it next login!"); st.balloons()
st.sidebar.divider()
st.sidebar.success("🔗 Public Voting Link for Students:")
st.sidebar.code("?public=vote - Add to your app URL", language="text")
st.sidebar.info("Students vote without seeing cabinet secrets!")
if st.sidebar.button("Logout",key="logout_ff"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9=st.tabs(["📝 Submit","📂 Private Portal","🗳️ Electoral (Chair Approval)","⚖️ Disciplinary","📋 GP Committee","💰 Finance (5 Only)","🔐 Secret Store","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt_ff1")
    rtitle=st.text_input("Report Title *",key="rtitle_ff2")
    rcontent=st.text_area("Details *",height=150,key="rcontent_ff3")
    rfile=st.file_uploader("Attach File",type=["xlsx","xls","pptx","ppt","pdf","jpg","png","docx","mp4","mp3"],key="rfile_ff4")
    if st.button("📤 Submit",type="primary",use_container_width=True,key="rsubmit_ff"):
        if not rtitle.strip() or not rcontent.strip(): st.error("❌ Title + Details required")
        else: st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":rfile.name if rfile else None,"file_bytes":rfile.getvalue() if rfile else None}); st.success("✅ Submitted!"); st.balloons()

with tab2:
    st.subheader("📂 PRIVATE - " + user_full + " - UNIK BEC Governance Portal")
    if user in SUPER_4: show=st.session_state.reports; st.info("SUPER 4 ACCESS: Viewing ALL " + str(len(show)) + " reports")
    else: show=[r for r in st.session_state.reports if r['from']==user]; st.info("Private: You have " + str(len(show)) + " reports. Others cannot see yours.")
    if show:
        df_data = [{"id":r["id"],"date":r["date"],"from_name":r["from_name"],"type":r["type"],"title":r["title"]} for r in show]
        st.dataframe(pd.DataFrame(df_data).sort_values(by="id",ascending=False),use_container_width=True)
        for r in reversed(show):
            with st.expander("#" + str(r['id']) + " " + r['title'] + " - " + r['from_name']):
                st.info(r['content'])
                if r.get('file_bytes'): st.download_button("Download " + r['file_name'],r['file_bytes'],r['file_name'],key="dl_priv_" + str(r['id']) + "_ff")

with tab3:
    st.subheader("🗳️ Electoral Commission - UNIK BEC Governance Portal - ALL 13 + PUBLIC")
    pending_len = len(st.session_state.pending_candidates)
    st.info("Public Voting Link: ?public=vote - Share to students. They vote without cabinet secrets. | Pending Approvals: " + str(pending_len))
    if user=="speaker":
        colA,colB=st.columns(2)
        with colA:
            if not st.session_state.election_open:
                if st.button("🟢 OPEN VOTING (Public + Cabinet)",type="primary",key="open_ff"): st.session_state.election_open=True;st.rerun()
            else:
                if st.button("🔴 CLOSE VOTING",key="close_ff"): st.session_state.election_open=False;st.rerun()
        with colB:
            st.write("Status: OPEN" if st.session_state.election_open else "Status: CLOSED")
    t_pending, t_approve, t_register, t_vote, t_results = st.tabs(["⏳ Pending Approval (Students Applied)", "✅ Approved Candidates", "Register Cabinet Candidate", "Vote (Cabinet)", "Results + Voter Emails"])
    with t_pending:
        st.subheader("Pending Candidate Applications - Need Your Approval as Chair")
        st.write("Total pending: " + str(pending_len))
        if not st.session_state.pending_candidates: st.success("No pending applications")
        for pc in reversed(st.session_state.pending_candidates):
            with st.container(border=True):
                col1,col2=st.columns([1,2])
                with col1: st.image(pc['photo_bytes'],width=150)
                with col2:
                    st.write("**" + pc['name'] + "** | " + USERS[pc['position']])
                    st.write("Class: " + pc['class'] + " | Course: " + pc['course'] + " | Email: " + pc['email'])
                    st.write("Results: " + pc['results'] + " | Date: " + pc['date'])
                    st.info(pc['reason'])
                    cA,cB=st.columns(2)
                    with cA:
                        if st.button("✅ Approve " + pc['name'],key="approve_" + str(pc['id'])):
                            st.session_state.candidates.append({"id":pc['id'],"position":pc['position'],"name":pc['name'],"class":pc['class'],"course":pc['course'],"email":pc['email'],"results":pc['results'],"reason":pc['reason'],"photo_bytes":pc['photo_bytes']})
                            st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                            st.success("Approved " + pc['name'] + "!"); st.balloons(); st.rerun()
                    with cB:
                        if st.button("❌ Reject " + pc['name'],key="reject_" + str(pc['id'])):
                            st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                            st.error("Rejected " + pc['name']); st.rerun()
    with t_approve:
        st.write("Total Approved Candidates: " + str(len(st.session_state.candidates)))
        for c in st.session_state.candidates:
            with st.container(border=True):
                st.image(c['photo_bytes'],width=100)
                st.write(c['name'] + " - " + USERS[c['position']] + " - " + c['class'])
    with t_register:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos_ff")
        rn=st.text_input("Full Names *",key="cand_name_ff"); rclass=st.text_input("Class *",key="cand_class_ff"); rcourse=st.text_input("Course *",key="cand_course_ff"); rres=st.text_input("Results *",key="cand_res_ff"); rreason=st.text_area("Reason *",key="cand_reason_ff"); rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="cand_photo_ff")
        if st.button("Register Cabinet Candidate (Auto Approved)",type="primary",key="cand_submit_ff"):
            if rn and rclass and rcourse and rres and rreason and rphoto: st.session_state.candidates.append({"id":len(st.session_state.candidates)+len(st.session_state.pending_candidates)+1,"position":rp,"name":rn,"class":rclass,"course":rcourse,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue()}); st.success("✅ Registered Auto Approved (Cabinet)"); st.balloons()
            else: st.error("❌ Fill ALL *")
    with t_vote:
        if not st.session_state.election_open: st.error("Voting Closed")
        else:
            vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos_ff")
            for c in [x for x in st.session_state.candidates if x['position']==vp]:
                with st.container(border=True): st.image(c['photo_bytes'],width=120); st.write("**" + c['name'] + "**"); 
                if st.button("Vote " + c['name'],key="vote_" + str(c['id']) + "_ff"): st.session_state.votes.append({"candidate_id":c['id'],"voter":user,"voter_email":user + "@cabinet","position":vp}); st.success("Voted!"); st.rerun()
    with t_results:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs: rd=[{"Candidate":c['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==c['id']])} for c in cs]; st.write("**" + USERS[pos] + "**"); st.dataframe(pd.DataFrame(rd),use_container_width=True)
        st.divider()
        st.subheader("📧 Voter Emails (One vote per position tracked)")
        if st.session_state.votes:
            vote_data = [{"voter_email":v.get("voter_email",""),"position":v.get("position",""),"date":v.get("date","")} for v in st.session_state.votes]
            st.dataframe(pd.DataFrame(vote_data).sort_values(by="date",ascending=False),use_container_width=True)
        else: st.info("No votes yet")

with tab4:
    st.subheader("⚖️ Disciplinary - ALL 13"); d_title=st.text_input("Case Title *",key="disc_title_ff"); d_content=st.text_area("Details *",key="disc_content_ff")
    if st.button("Save",type="primary",key="disc_save_ff"):
        if d_title and d_content: st.session_state.disciplinary_reports.append({"id":len(st.session_state.disciplinary_reports)+1,"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("✅ Saved!"); st.balloons()
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(dr['title'] + " - " + dr['by']): st.warning(dr['content'])

with tab5:
    st.subheader("📋 GP Committee - ALL 13"); gp_title=st.text_input("GP Title *",key="gp_title_ff"); gp_content=st.text_area("Details *",key="gp_content_ff")
    if st.button("Save GP",type="primary",key="gp_save_ff"):
        if gp_title and gp_content: st.session_state.gp_reports.append({"id":len(st.session_state.gp_reports)+1,"title":gp_title,"content":gp_content,"by":user_full}); st.success("✅ Saved!"); st.balloons()
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(gpr['title'] + " - " + gpr['by']): st.info(gpr['content'])

with tab6:
    if user not in FINANCE_5: st.error("🔒 Finance only 5: Finance + Speaker + President + Patron + Principal"); st.stop()
    st.subheader("💰 Finance - 5 Only - Governance Portal"); f_title=st.text_input("Title *",key="fin_title_ff"); f_type=st.selectbox("Type",["Budget Excel","PPT Report","Expense","Other"],key="fin_type_ff"); f_desc=st.text_area("Description",key="fin_desc_ff"); f_file=st.file_uploader("Excel/PPT *",type=["xlsx","xls","pptx","ppt","pdf","csv"],key="fin_file_ff")
    if st.button("Save Finance",type="primary",use_container_width=True,key="fin_save_ff"):
        if not f_title.strip() or not f_file: st.error("❌ Title + File required")
        else: st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title.strip(),"type":f_type,"description":f_desc,"file_name":f_file.name,"file_bytes":f_file.getvalue(),"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("✅ Saved: " + f_file.name + "!"); st.balloons(); st.rerun()
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True): st.write("**" + fd['title'] + "** | " + fd['file_name'] + " | by " + fd['by']); st.download_button("Download " + fd['file_name'],fd['file_bytes'],fd['file_name'],key="dl_fin_" + str(fd['id']) + "_ff")

with tab7:
    st.subheader("🔐 Secret Store - ALL 13"); dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat_ff"); dt=st.text_input("Title *",key="secret_title_ff"); dd=st.text_area("Description",key="secret_desc_ff"); uf=st.file_uploader("File",key="secret_file_ff")
    if st.button("Save Secret",type="primary",key="secret_save_ff"):
        if not dt.strip(): st.error("❌ Title required")
        else: st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"file_name":uf.name if uf else "Note","file_bytes":uf.getvalue() if uf else None,"by":user_full}); st.success("✅ Saved!"); st.rerun()
    for d in reversed(st.session_state.documents):
        with st.expander(d['category'] + " | " + d['title'] + " - " + d['by']):
            if d['file_bytes']: st.download_button("Download",d['file_bytes'],d['file_name'],key="dl_sec_" + str(d['id']) + "_ff")

with tab8:
    st.subheader("📸 MEDIA GALLERY - ALL 13 - EVERY MEMBER can upload Photo/Video/Music!")
    filter_type=st.selectbox("Filter Media", ["All","Photos Only","Videos Only","Music Only"], key="media_filter_ff")
    c1,c2=st.columns([2,1])
    with c1: mt=st.text_input("Media Title *",key="media_title_ff")
    with c2: st.write("JPG, PNG, MP4, MOV, MP3, WAV")
    mf=st.file_uploader("Choose Photo / Video / Music File *",type=["jpg","png","jpeg","mp4","mov","avi","mp3","m4a","wav","ogg"],key="media_file_ff")
    if st.button("📸 Upload to Media Gallery",type="primary",use_container_width=True,key="media_save_ff"):
        if not mt.strip() or not mf: st.error("❌ ERROR: Title + File required")
        else: st.session_state.media.append({"id":len(st.session_state.media)+1,"title":mt.strip(),"file_name":mf.name,"file_bytes":mf.getvalue(),"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}); st.success("✅ Media Saved: " + mf.name + "!"); st.balloons(); st.rerun()
    st.divider()
    for m in reversed(st.session_state.media):
        ftype=m['file_type']
        if filter_type=="Photos Only" and "image" not in ftype: continue
        if filter_type=="Videos Only" and "video" not in ftype: continue
        if filter_type=="Music Only" and "audio" not in ftype: continue
        with st.container(border=True):
            st.write("**" + m['title'] + "** - " + m['file_name'] + " - by " + m['by'] + " - " + m['date'])
            if "image" in ftype: st.image(m['file_bytes'],use_container_width=True)
            elif "video" in ftype: st.video(m['file_bytes'])
            elif "audio" in ftype: st.audio(m['file_bytes'])
            st.download_button("📥 Download " + m['file_name'],m['file_bytes'],m['file_name'],key="dl_med_" + str(m['id']) + "_ff")

with tab9:
    st.subheader("🏛️ Leadership Cabinet Archive - Different Years - ALL 13")
    with st.container(border=True):
        cab_year=st.text_input("Year * e.g. 2024/2025", key="cab_year_ff")
        cab_name=st.text_input("Cabinet Name * e.g. First BEC Leadership Cabinet", key="cab_name_ff")
        cab_members=st.text_area("List Members in Cabinet *", height=100, key="cab_members_ff")
        cab_desc=st.text_area("Achievements / Description", key="cab_desc_ff")
        cab_photo=st.file_uploader("Cabinet Group Photo * JPG/PNG", type=["jpg","png","jpeg"], key="cab_photo_ff")
        cab_video=st.file_uploader("Cabinet Video (Optional) MP4/MOV", type=["mp4","mov","avi"], key="cab_video_ff")
        if st.button("🏛️ Save Cabinet to Archive", type="primary", use_container_width=True, key="cab_save_ff"):
            if not cab_year.strip() or not cab_name.strip() or not cab_members.strip() or not cab_photo:
                st.error("❌ ERROR: Year + Cabinet Name + Members + Photo required!")
            else:
                st.session_state.cabinets.append({"id":len(st.session_state.cabinets)+1,"year":cab_year.strip(),"name":cab_name.strip(),"members":cab_members.strip(),"desc":cab_desc,"photo_bytes":cab_photo.getvalue(),"photo_name":cab_photo.name,"video_bytes":cab_video.getvalue() if cab_video else None,"video_name":cab_video.name if cab_video else None,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success("✅ Cabinet Saved: " + cab_name + " - " + cab_year + "!"); st.balloons(); st.rerun()
    st.divider()
    st.write("🏛️ Total Cabinets Archived: " + str(len(st.session_state.cabinets)))
    years = sorted(list(set([c['year'] for c in st.session_state.cabinets])), reverse=True) if st.session_state.cabinets else []
    if years: selected_year=st.selectbox("Filter by Year", ["All Years"] + years, key="cab_filter_year_ff")
    else: selected_year="All Years"
    for cab in reversed(st.session_state.cabinets):
        if selected_year!="All Years" and cab['year']!=selected_year: continue
        with st.container(border=True):
            st.subheader(cab['name'] + " - " + cab['year'])
            col1,col2=st.columns([1,1])
            with col1: st.image(cab['photo_bytes'], caption=cab['name'] + " Photo", use_container_width=True)
            with col2: st.write("**👥 Members:**"); st.info(cab['members']); 
            if cab.get('desc'): st.write("**Achievements:**"); st.success(cab['desc'])
            if cab.get('video_bytes'): st.video(cab['video_bytes'])
