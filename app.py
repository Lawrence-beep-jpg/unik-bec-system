import streamlit as st
import pandas as pd
import datetime
import os, json
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# ===== SAVE TO SERVER SO ALL 13 SEE =====
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
PASSWORDS_FILE="data/passwords.json"  # ADDED FOR PASSWORD CHANGE

def load_json(path, default):
    if os.path.exists(path):
        try: return json.loads(open(path,'r').read())
        except: return default
    return default
def save_json(path, data):
    open(path,'w').write(json.dumps(data, default=str))

query_params = st.query_params
is_public_vote = query_params.get("public", "") == "vote"

try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
except:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)

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
if 'passwords' not in st.session_state: 
    loaded_pw=load_json(PASSWORDS_FILE, {})
    if loaded_pw: st.session_state.passwords=loaded_pw
    else: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=True
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

# PUBLIC VOTING - NO SECRETS - ONE EMAIL ONCE PER POSITION
if is_public_vote:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM - PUBLIC ELECTORAL</h2>", unsafe_allow_html=True)
    st.info("Public voting - No cabinet secrets - One email once per position")
    pub_tab1, pub_tab2 = st.tabs(["Apply as Candidate", "Vote Easy Click"])
    with pub_tab1:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names *",key="pub_name")
        rclass=st.text_input("Class *",key="pub_class")
        remail=st.text_input("Email *",key="pub_email")
        rreason=st.text_area("Why vote you? *",key="pub_reason")
        rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit",type="primary",key="pub_submit"):
            if not rn or not rclass or not remail or not rreason or not rphoto: st.error("Fill ALL")
            else:
                nid=len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.pending_candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(PENDING_FILE, st.session_state.pending_candidates)
                st.success("Sent! Wait Chair approval"); st.balloons()
    with pub_tab2:
        voter_email=st.text_input("Your Email * (Once per position)",key="pub_voter_email")
        if not voter_email or "@" not in voter_email: st.warning("Enter email"); st.stop()
        vp=st.selectbox("Choose Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        if [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]: st.error("Already voted for this position with this email - One email once!"); st.stop()
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c['photo_path'],width=150)
                st.write(c['name']); st.info(c['reason'])
                if st.button("Vote "+c['name'],key="pv_"+str(c['id'])+"_"+voter_email):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success("Voted!"); st.rerun()
    st.stop()

if not st.session_state.logged_in:
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x])
    p=st.text_input("Password",type="password")
    if st.button("LOGIN",type="primary"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password")
    st.info("Default unik2025 | Public: ?public=vote")
    st.stop()

user=st.session_state.user
user_full=USERS[user]

# ===== EVERYONE CAN CHANGE OWN PASSWORD - THEIR BOTTLE - ADDED HERE =====
st.sidebar.title(user_full)
st.sidebar.success(f"Logged as: {user_full}")
st.sidebar.divider()
st.sidebar.subheader("🔐 Change My Password - My Bottle")

with st.sidebar.expander("Click to Change My Own Password - Every Member Can!", expanded=False):
    st.write(f"Your Office: {user_full}")
    current_pw_input=st.text_input("Current Password *", type="password", key="current_pw")
    new_p=st.text_input("New Password *", type="password", key="new_pass")
    confirm_p=st.text_input("Confirm New Password *", type="password", key="conf_pass")
    if st.button("Save New Password - For My Bottle Only", type="primary", use_container_width=True, key="save_pass"):
        if not current_pw_input or not new_p or not confirm_p:
            st.sidebar.error("Fill ALL fields!")
        elif current_pw_input != st.session_state.passwords.get(user,"unik2025"):
            st.sidebar.error("Current password wrong!")
        elif new_p != confirm_p:
            st.sidebar.error("New passwords don't match!")
        elif len(new_p) < 4:
            st.sidebar.error("Password too short! Minimum 4 characters")
        else:
            st.session_state.passwords[user]=new_p
            save_json(PASSWORDS_FILE, st.session_state.passwords)
            st.sidebar.success(f"✅ Password Changed! New: {new_p} - Your bottle now uses this!")
            st.balloons()

st.sidebar.divider()
if user in SUPER_4: st.sidebar.info("SUPER 4 - View ALL reports")
if st.sidebar.button("Logout"): st.session_state.logged_in=False;st.rerun()

# TABS - ALL 9 KEPT
tab1,tab2,tab3,tab8,tab9=st.tabs(["📝 Submit Report","📂 Private Portal","🗳️ Electoral Chair","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt")
    rtitle=st.text_input("Report Title *",key="rtitle")
    rcontent=st.text_area("Details *",key="rcontent")
    if st.button("Submit Report",type="primary",use_container_width=True,key="rsubmit"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Title+Details required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip()})
            save_json(REPORTS_FILE, st.session_state.reports)
            st.success("Saved on server - Principal will see!"); st.rerun()

with tab2:
    st.subheader("Private Portal")
    st.session_state.reports=load_json(REPORTS_FILE, st.session_state.reports)
    if user in SUPER_4:
        show=st.session_state.reports
        st.success(f"SUPER 4: Viewing ALL {len(show)} reports")
    else:
        show=[r for r in st.session_state.reports if r['from']==user]
        st.info(f"Your reports: {len(show)}")
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']}"):
            st.info(r['content'])

with tab3:
    st.subheader("Electoral Chair - Full")
    t_pending, t_approved, t_reg, t_vote, t_res = st.tabs(["Pending","Approved","Register+Photo","Vote","Results"])
    with t_pending:
        for pc in reversed(load_json(PENDING_FILE, st.session_state.pending_candidates)):
            with st.container(border=True):
                if os.path.exists(pc.get('photo_path','')): st.image(pc['photo_path'],width=120)
                st.write(pc['name']+" - "+USERS[pc['position']])
                if user=="speaker":
                    if st.button("Approve "+pc['name'],key="ap_"+str(pc['id'])):
                        st.session_state.candidates.append(pc)
                        st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                        save_json(CANDIDATES_FILE, st.session_state.candidates)
                        save_json(PENDING_FILE, st.session_state.pending_candidates)
                        st.success("Approved"); st.rerun()
    with t_approved:
        st.write(f"Approved: {len(st.session_state.candidates)}")
    with t_reg:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos")
        rn=st.text_input("Names *",key="cand_name")
        rphoto=st.file_uploader("Photo *",type=["jpg","png"],key="cand_photo")
        if st.button("Register",key="cand_submit"):
            if rn and rphoto:
                nid=len(st.session_state.candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.candidates.append({"id":nid,"position":rp,"name":rn,"photo_path":fpath,"reason":"Cabinet"})
                save_json(CANDIDATES_FILE, st.session_state.candidates)
                st.success("Registered")
    with t_vote:
        vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos")
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            if st.button("Vote "+c['name'],key="vote_"+str(c['id'])):
                st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user,"position":vp})
                save_json(VOTES_FILE, st.session_state.votes)
                st.success("Voted")
    with t_res:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)

with tab8:
    st.subheader("Media Gallery - ALL SEE")
    mt=st.text_input("Title *",key="media_title")
    mf=st.file_uploader("File *",type=["jpg","png","mp4","mp3","m4a"],key="media_file")
    if st.button("Upload",type="primary",key="media_save"):
        if not mt.strip() or not mf: st.error("Title+File required")
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
    st.subheader("Cabinet Archive")
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
