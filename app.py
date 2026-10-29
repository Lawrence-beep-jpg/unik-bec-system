import streamlit as st
import pandas as pd
import datetime
import os, json, base64
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# ===== CREATE SERVER FOLDER TO SAVE FOR ALL USERS =====
os.makedirs("data/media_files", exist_ok=True)
REPORTS_FILE="data/reports.json"
MEDIA_FILE="data/media.json"
CANDIDATES_FILE="data/candidates.json"
PENDING_FILE="data/pending.json"
VOTES_FILE="data/votes.json"
CABINETS_FILE="data/cabinets.json"

def load_json(path, default):
    if os.path.exists(path):
        try: return json.loads(open(path).read())
        except: return default
    return default
def save_json(path, data):
    open(path,'w').write(json.dumps(data))

query_params = st.query_params
is_public_vote = query_params.get("public", "") == "vote"

# SINGLE HEADING ONCE + ICONS
try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
except:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)

# ===== CORRECTED TITLES =====
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
ELECTION_POSITIONS=list(USERS.keys())[:11]

# LOAD FROM DISK - SHARED FOR ALL 13
if 'reports' not in st.session_state: st.session_state.reports=load_json(REPORTS_FILE, [])
if 'media' not in st.session_state: st.session_state.media=load_json(MEDIA_FILE, [])
if 'candidates' not in st.session_state: st.session_state.candidates=load_json(CANDIDATES_FILE, [])
if 'pending_candidates' not in st.session_state: st.session_state.pending_candidates=load_json(PENDING_FILE, [])
if 'votes' not in st.session_state: st.session_state.votes=load_json(VOTES_FILE, [])
if 'cabinets' not in st.session_state: st.session_state.cabinets=load_json(CABINETS_FILE, [])

for k in ['documents','finance_docs','electoral_reports','disciplinary_reports','gp_reports']:
    if k not in st.session_state: st.session_state[k]=[]
if 'passwords' not in st.session_state: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=True
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

# PUBLIC VOTING
if is_public_vote:
    st.success("PUBLIC VOTING - UNIK BEC UNASNM Governance Portal")
    pub_tab1, pub_tab2 = st.tabs(["Apply as Candidate", "Vote"])
    with pub_tab1:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names",key="pub_name")
        rclass=st.text_input("Class",key="pub_class")
        remail=st.text_input("Email",key="pub_email")
        rreason=st.text_area("Why vote you?",key="pub_reason")
        rphoto=st.file_uploader("Photo",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit",type="primary",key="pub_submit"):
            if not rn or not rclass or not remail or not rreason or not rphoto: st.error("Fill ALL")
            else:
                new_id=len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1
                fname=f"data/media_files/cand_{new_id}.jpg"
                open(fname,'wb').write(rphoto.getvalue())
                st.session_state.pending_candidates.append({"id":new_id,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fname,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(PENDING_FILE, st.session_state.pending_candidates)
                st.success("Sent! Wait Chair approval"); st.balloons()
    with pub_tab2:
        voter_email=st.text_input("Your Email",key="pub_voter_email")
        if not voter_email or "@" not in voter_email: st.warning("Enter email"); st.stop()
        vp=st.selectbox("Choose Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        already=[v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
        if already: st.error("Already voted"); st.stop()
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c['photo_path'],width=150)
                st.write(c['name']); st.info(c['reason'])
                if st.button("Vote "+c['name'],key="pv_"+str(c['id'])+"_"+voter_email):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success("Voted!"); st.rerun()
    st.stop()

# LOGIN
if not st.session_state.logged_in:
    u=st.selectbox("Select Office",LOGIN_USERS,format_func=lambda x:USERS[x])
    p=st.text_input("Password",type="password")
    if st.button("LOGIN",type="primary"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password")
    st.info("Default unik2025 | Public link: ?public=vote")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
if st.sidebar.button("Logout"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab8,tab3=st.tabs(["📝 Submit Report","📂 Private Portal","📸 Media Gallery (ALL SEE)","🗳️ Electoral"])

with tab1:
    rtitle=st.text_input("Report Title *")
    rcontent=st.text_area("Details *")
    if st.button("Submit Report",type="primary"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Title+Details required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"title":rtitle.strip(),"content":rcontent.strip()})
            save_json(REPORTS_FILE, st.session_state.reports)
            st.success("Report Submitted! Now visible to you and SUPER 4!"); st.balloons()

with tab2:
    st.subheader("Private Portal - Reports")
    if user in SUPER_4:
        show=st.session_state.reports
        st.success(f"SUPER 4 - You see ALL reports: Total {len(show)} reports from all departments")
        # Count per department
        if show:
            df=pd.DataFrame(show)
            st.write("Reports per department:")
            st.dataframe(df['from_name'].value_counts(),use_container_width=True)
    else:
        show=[r for r in st.session_state.reports if r['from']==user]
        st.info(f"Your reports: {len(show)} - SUPER 4 can also see them")
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']}"):
            st.info(r['content'])

with tab8:
    st.subheader("📸 Media Gallery - EVERY MEMBER CAN POST AND SEE")
    st.success("FIXED: Now when you post on PC, everyone on phone sees it! ALL 13 can upload and view.")
    mt=st.text_input("Media Title *")
    mf=st.file_uploader("Photo / Video / Audio *",type=["jpg","png","jpeg","mp4","mov","mp3","m4a","wav"],key="media_file")
    if st.button("Upload - Visible to ALL 13",type="primary",use_container_width=True):
        if not mt.strip() or not mf: st.error("Title + File required")
        else:
            fid=len(st.session_state.media)+1
            fpath=f"data/media_files/media_{fid}_{mf.name}"
            open(fpath,'wb').write(mf.getvalue())
            st.session_state.media.append({"id":fid,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(MEDIA_FILE, st.session_state.media)
            st.success(f"Saved! {mf.name} now visible to ALL 13 departments!"); st.balloons(); st.rerun()
    st.divider()
    st.write(f"Total Media visible to ALL: {len(st.session_state.media)}")
    for m in reversed(st.session_state.media):
        with st.container(border=True):
            st.write(f"**{m['title']}** - {m['file_name']} - by {m['by']} - {m['date']}")
            if os.path.exists(m['file_path']):
                if "image" in m['file_type']: st.image(m['file_path'],use_container_width=True)
                elif "video" in m['file_type']: st.video(m['file_path'])
                elif "audio" in m['file_type']: st.audio(m['file_path'])
                with open(m['file_path'],'rb') as f:
                    st.download_button(f"Download {m['file_name']}",f,m['file_name'],key=f"dl_{m['id']}")

with tab3:
    st.subheader("Electoral - Chair Approval")
    for pc in reversed(st.session_state.pending_candidates):
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
