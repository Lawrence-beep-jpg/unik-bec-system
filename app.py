import streamlit as st
import pandas as pd
import datetime
st.set_page_config(page_title="UNIK BEC Governance Portal System", page_icon="🏛️", layout="wide")

# CHECK PUBLIC MODE
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

# ================= PUBLIC VOTING PORTAL - NO CABINET DETAILS =================
if is_public_vote:
    st.success("🏛️ UNIK BEC GOVERNANCE PORTAL - PUBLIC ELECTORAL COMMISSION")
    st.info("Welcome Students! You can Apply as Candidate (needs approval) or Vote your leaders (once per email). You CANNOT see cabinet secrets here.")
    st.warning(f"Election Status: {'🟢 OPEN - You can vote now!' if st.session_state.election_open else '🔴 CLOSED - Wait for Chair to open'}")
    
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
                st.success(f"✅ Application Sent! Wait for Chair (Speaker) to approve. You will be notified via email {remail}")
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
        # Check if this email already voted for this position
        already_voted = [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
        if already_voted:
            st.error(f"❌ You already voted for {USERS[vp]} with email {voter_email}. One email = One vote per position!")
            st.stop()
        approved_for_pos = [c for c in st.session_state.candidates if c['position']==vp]
        if not approved_for_pos:
            st.info(f"No approved candidates yet for {USERS[vp]}. Wait for approval.")
        else:
            st.write(f"**Candidates for {USERS[vp]}:**")
            for c in approved_for_pos:
                with st.container(border=True):
                    st.image(c['photo_bytes'],width=150)
                    st.write(f"**{c['name']}** - {c['class']} - {c['course']}")
                    st.write(f"Results: {c['results']}")
                    st.info(c['reason'])
                    if st.button(f"✅ Vote {c['name']}",key=f"pub_vote_{c['id']}_{voter_email}"):
                        st.session_state.votes.append({"candidate_id":c['id'],"voter":f"public_{voter_email}","voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                        st.success(f"✅ Voted successfully with {voter_email} for {c['name']}! You cannot vote again for this position with same email.")
                        st.balloons()
                        st.rerun()
        # Results public view
        st.divider()
        st.subheader("📊 Live Results (Public)")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":c['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==c['id']])} for c in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(f"**{USERS[pos]}**")
                    st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()
# ================= END PUBLIC PORTAL =================

# ================= CABINET LOGIN PORTAL (YOUR ORIGINAL CODE - NOT CHANGED) =================
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
    st.success("🔗 PUBLIC VOTING LINK TO SHARE TO ALL STUDENTS (They won't see cabinet secrets):")
    st.code(f"{st.context.headers.get('host','your-app') if hasattr(st,'context') else 'https://your-app.streamlit.app'}?public=vote", language="text")
    st.write("Copy this link with ?public=vote and share to students WhatsApp groups!")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
st.sidebar.caption("UNIK BEC Governance Portal")
if user in SUPER_4: st.sidebar.success("✅ SUPER 4")
if user in FINANCE_5: st.sidebar.success("💰 FINANCE 5")
with st.sidebar.expander("🔑 Change My Password"):
    new_p=st.text_input("New Password",type="password",key="new_pass_ff")
    confirm_p=st.text_input("Confirm",type="password",key="confirm_pass_ff")
    if st.button("Save Password",key="save_pass_ff"):
        if not new_p: st.error("Enter password")
        elif new_p!=confirm_p: st.error("❌ Don't match - Correct!")
        else: st.session_state.passwords[user]=new_p; st.success(f"✅ New password: {new_p}"); st.balloons()

st.sidebar.divider()
st.sidebar.success("🔗 Public Voting Link for Students:")
st.sidebar.code("?public=vote - Add to your app URL", language="text")
st.sidebar.info("Students vote without seeing cabinet secrets!")

if st.sidebar.button("Logout",key="logout_ff"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9=st.tabs(["📝 Submit","📂 Private Portal","🗳️ Electoral (Chair Approval)","⚖️ Disciplinary","📋 GP","💰 Finance (5 Only)","🔐 Secret Store","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt_ff1")
    rtitle=st.text_input("Report Title *",key="rtitle_ff2")
    rcontent=st.text_area("Details *",height=150,key="rcontent_ff3")
    rfile=st.file_uploader("Attach File",type=["xlsx","xls","pptx","ppt","pdf","jpg","png","docx","mp4","mp3"],key="rfile_ff4")
    if st.button("📤 Submit",type="primary",use_container_width=True,key="rsubmit_ff"):
        if not rtitle.strip() or not rcontent.strip(): st.error("❌ Title + Details required")
        else: st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":rfile.name if rfile else None,"file_bytes":rfile.getvalue() if rfile else None}); st.success("✅ Submitted!"); st.balloons()

with tab2:
    st.subheader(f"📂 PRIVATE - {user_full} - UNIK BEC Governance Portal")
    if user in SUPER_4: show=st.session_state.reports
    else: show=[r for r in st.session_state.reports if r['from']==user]
    st.dataframe(pd.DataFrame(show)[["id","date","from_name","type","title"]].sort_values(by="id",ascending=False) if show else pd.DataFrame(),use_container_width=True)
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']}"):
            st.info(r['content'])
            if r.get('file_bytes'): st.download_button(f"Download {r['file_name']}",r['file_bytes'],r['file_name'],key=f"dl_priv_{r['id']}_ff")

with tab3:
    st.subheader("🗳️ Electoral Commission - UNIK BEC Governance Portal - ALL 13 + PUBLIC")
    st.info(f"Public Voting Link: ?public=vote - Share to students. They vote without cabinet secrets. | Pending Approvals: {len(st.session_state.pending_candidates)}")
    if user=="speaker":
        colA,colB=st.columns(2)
        with colA:
            if not st.session_state.election_open:
                if st.button("🟢 OPEN VOTING (Public + Cabinet)",type="primary",key="open_ff"): st.session_state.election_open=True;st.rerun()
            else:
                if st.button("🔴 CLOSE VOTING",key="close_ff"): st.session_state.election_open=False;st.rerun()
        with colB:
            st.write(f"Status: {'🟢 OPEN' if st.session_state.election_open else '🔴 CLOSED'} | Share Link: ?public=vote")
    
    t_pending, t_approve, t_register, t_vote, t_results = st.tabs(["⏳ Pending Approval (Students Applied)", "✅ Approved Candidates", "Register Cabinet Candidate", "Vote (Cabinet)", "Results + Voter Emails"])
    
    with t_pending:
        st.subheader(f"Pending Candidate
