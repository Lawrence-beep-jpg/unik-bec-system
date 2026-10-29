import streamlit as st
import pandas as pd
import datetime
import os, json
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# SAVE FOR YEARS - NO BLINK
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

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path,'r') as f: return json.load(f)
        except: return default
    return default
def save_json(path, data):
    with open(path,'w') as f: json.dump(data, f, default=str)

# FIXED QUERY PARAMS - NO BLINK
params = st.query_params
is_public_vote = params.get("public", "") == "vote"

# ===== ONLY ONE HEADING - UNIK BEC UNASNM Governance Portal =====
c1,c2,c3 = st.columns([1,3,1])
with c1:
    if os.path.exists("unik_badge.png"): st.image("unik_badge.png", width=90)
with c2:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM Governance Portal</h2>", unsafe_allow_html=True)
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
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint","Public Information"]

# INIT ONCE - STABLE - NO RELOAD
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
if 'passwords' not in st.session_state: 
    pw=load_json(PASSWORDS_FILE, {})
    st.session_state.passwords = pw if pw else {u:"unik2025" for u in LOGIN_USERS}
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

# ===== PUBLIC VOTING - NO BLINK - STABLE =====
if is_public_vote:
    st.markdown("<h3 style='text-align:center;'>🏛️ PUBLIC ELECTORAL COMMISSION - VOTE HERE</h3>", unsafe_allow_html=True)
    st.info("One Email Once Per Position - No Secrets - Works For Years")
    t1,t2,t3 = st.tabs(["Apply Candidate","Vote","Results"])
    with t1:
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
                with open(fpath,'wb') as out: out.write(rphoto.getvalue())
                st.session_state.pending_candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(PENDING_FILE, st.session_state.pending_candidates)
                st.success("Sent! Wait Speaker approval"); st.balloons()
    with t2:
        voter_email=st.text_input("Your Email * (Once per position)",key="pub_voter_email")
        if voter_email and "@" in voter_email:
            vp=st.selectbox("Position to Vote",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
            if [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]:
                st.error("Already voted for this position with this email!")
            else:
                for c in [x for x in st.session_state.candidates if x['position']==vp]:
                    with st.container(border=True):
                        if os.path.exists(c.get('photo_path','')): st.image(c['photo_path'],width=120)
                        st.write(c['name']); st.caption(c.get('reason',''))
                        if st.button(f"Vote {c['name']}",key=f"pv_{c['id']}_{voter_email}"):
                            st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                            save_json(VOTES_FILE, st.session_state.votes)
                            st.success("Voted!"); st.rerun()
        else:
            st.warning("Enter email to vote")
    with t3:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()

# CABINET LOGIN - STABLE
if not st.session_state.logged_in:
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x])
    p=st.text_input("Password",type="password")
    if st.button("LOGIN",type="primary"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True; st.session_state.user=u; st.rerun()
        else: st.error("Wrong Password - Default unik2025")
    st.info("Default unik2025 | Public link: ?public=vote")
    st.stop()

user=st.session_state.user
user_full=USERS[user]

# SIDEBAR - STABLE - NO COMPONENTS THAT RELOAD
st.sidebar.title(user_full)
st.sidebar.success(f"Logged: {user_full}")
st.sidebar.divider()
st.sidebar.subheader("🔐 Change My Password")
with st.sidebar.expander("Change My Password - Every Member", expanded=False):
    cur=st.text_input("Current Password",type="password",key="cur_pw")
    new=st.text_input("New Password",type="password",key="new_pw")
    conf=st.text_input("Confirm New",type="password",key="conf_pw")
    if st.button("Save New Password",key="save_pw"):
        if not cur or not new or not conf: st.sidebar.error("Fill all")
        elif cur!=st.session_state.passwords.get(user,"unik2025"): st.sidebar.error("Current wrong")
        elif new!=conf: st.sidebar.error("No match")
        elif len(new)<4: st.sidebar.error("Min 4 chars")
        else:
            st.session_state.passwords[user]=new
            save_json(PASSWORDS_FILE, st.session_state.passwords)
            st.sidebar.success(f"Changed to {new}"); st.balloons()

if user in SUPER_4: st.sidebar.info("SUPER 4 - Broadcast + See ALL Reports")
if st.sidebar.button("Logout"): st.session_state.logged_in=False; st.rerun()

# TABS - STABLE - NO AUTO RELOAD
tab0,tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10 = st.tabs([
"📢 Public Portal SUPER 4 Broadcast",
"📝 Submit Report",
"📂 Private Portal",
"🗳️ Electoral Chair",
"⚖️ Disciplinary",
"📋 GP",
"💰 Finance",
"🔐 Secret Store",
"📄 Documents PDF/PPT/Word/Excel",
"📸 Media Gallery",
"🏛️ Cabinet Archive"
])

with tab0:
    st.subheader("📢 Public Portal - SUPER 4 sends ONE message to ALL 13")
    # Load fresh but no reload loop
    anns = load_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
    st.session_state.announcements = anns
    if anns: st.success(f"{len(anns)} Announcements")
    if user in SUPER_4:
        st.markdown(f"**Post as {user_full} - Goes to ALL 13 at once**")
        at=st.text_input("Title *",key="ann_t")
        acat=st.selectbox("Category",["Internal - All 13 Only","Public Information - Also to Students","Both"],key="ann_cat")
        ap=st.selectbox("Priority",["Normal","Urgent","Very Urgent"],key="ann_p")
        acont=st.text_area("Message to ALL 13 *",key="ann_c",height=150)
        af=st.file_uploader("Attach PDF/Excel/PPT/Word/Photo",type=["pdf","xlsx","pptx","docx","jpg","png"],key="ann_f")
        if st.button("📢 BROADCAST TO ALL 13",type="primary",use_container_width=True,key="ann_btn"):
            if not at or not acont: st.error("Title + Message required")
            else:
                fpath=""; fname=""
                if af:
                    fname=af.name.replace(" ","_")
                    fpath=f"data/documents/ann_{len(anns)+1}_{fname}"
                    with open(fpath,'wb') as out: out.write(af.getvalue())
                is_pub = "Public" in acat or "Both" in acat
                anns.append({"id":len(anns)+1,"title":at,"category":acat,"priority":ap,"content":acont,"file_name":fname,"file_path":fpath,"from":user,"from_name":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"read_by":[],"is_public":is_pub})
                save_json(ANNOUNCEMENTS_FILE, anns)
                st.session_state.announcements=anns
                st.success("Broadcasted to ALL 13!"); st.balloons(); st.rerun()
    st.divider()
    for ann in reversed(anns):
        with st.container(border=True):
            pub_tag="🌐 PUBLIC" if ann.get('is_public') else "🔒 INTERNAL"
            st.markdown(f"**{ann['title']}** {pub_tag} | {ann['priority']} | {ann['from_name']} | {ann['date']}")
            st.info(ann['content'])
            if ann.get('file_path') and os.path.exists(ann['file_path']):
                st.download_button(f"Download {ann['file_name']}", open(ann['file_path'],'rb').read(), file_name=ann['file_name'], key=f"dl_ann_{ann['id']}")
            if user not in ann.get('read_by',[]):
                if st.button("Mark as Read",key=f"read_{ann['id']}"):
                    for a in anns:
                        if a['id']==ann['id'] and user not in a['read_by']: a['read_by'].append(user)
                    save_json(ANNOUNCEMENTS_FILE, anns)
                    st.rerun()
            else:
                st.caption(f"✅ Read - {len(ann.get('read_by',[]))}/13")

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt")
    rtitle=st.text_input("Title *",key="rtitle")
    rcontent=st.text_area("Details *",key="rcontent")
    if st.button("Submit Report",type="primary",key="rsubmit"):
        if not rtitle or not rcontent: st.error("Required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle,"content":rcontent})
            save_json(REPORTS_FILE, st.session_state.reports)
            st.success("Saved - Principal will see!"); st.rerun()

with tab2:
    st.subheader("Private Portal")
    reports=load_json(REPORTS_FILE, st.session_state.reports)
    show=reports if user in SUPER_4 else [r for r in reports if r['from']==user]
    st.write(f"Reports: {len(show)}")
    for r in reversed(show):
        with st.expander(f"{r['title']} - {r['from_name']} - {r['date']}"):
            st.info(r['content'])

with tab3:
    st.subheader("Electoral Chair")
    t_a,t_b,t_c,t_d,t_e=st.tabs(["Pending","Approved","Register","Vote","Results"])
    with t_a:
        pend=load_json(PENDING_FILE, st.session_state.pending_candidates)
        for pc in reversed(pend):
            with st.container(border=True):
                if os.path.exists(pc.get('photo_path','')): st.image(pc['photo_path'],width=100)
                st.write(pc['name']+" - "+USERS[pc['position']])
                if user=="speaker":
                    if st.button(f"Approve {pc['name']}",key=f"ap_{pc['id']}"):
                        st.session_state.candidates.append(pc)
                        st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                        save_json(CANDIDATES_FILE, st.session_state.candidates)
                        save_json(PENDING_FILE, st.session_state.pending_candidates)
                        st.rerun()
    with t_b: st.write(f"Approved: {len(st.session_state.candidates)}")
    with t_c:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos")
        rn=st.text_input("Names",key="cand_name")
        rphoto=st.file_uploader("Photo",type=["jpg","png"],key="cand_photo")
        if st.button("Register",key="cand_sub"):
            if rn and rphoto:
                fpath=f"data/media_files/cand_{len(st.session_state.candidates)+1}.jpg"
                with open(fpath,'wb') as out: out.write(rphoto.getvalue())
                st.session_state.candidates.append({"id":len(st.session_state.candidates)+1,"position":rp,"name":rn,"photo_path":fpath,"reason":"Cabinet"})
                save_json(CANDIDATES_FILE, st.session_state.candidates)
                st.success("Registered")
    with t_d:
        vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos")
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            if st.button(f"Vote {c['name']}",key=f"vote_{c['id']}"):
                st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user,"position":vp})
                save_json(VOTES_FILE, st.session_state.votes)
                st.success("Voted")
    with t_e:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)

with tab4:
    d_t=st.text_input("Case Title",key="disc_t")
    d_c=st.text_area("Details",key="disc_c")
    if st.button("Save Disciplinary",key="disc_s"):
        if d_t and d_c:
            st.session_state.disciplinary_reports.append({"title":d_t,"content":d_c,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DISC_FILE, st.session_state.disciplinary_reports)
            st.success("Saved")

with tab5:
    gp_t=st.text_input("GP Title",key="gp_t")
    gp_c=st.text_area("GP Details",key="gp_c")
    if st.button("Save GP",key="gp_s"):
        if gp_t and gp_c:
            st.session_state.gp_reports.append({"title":gp_t,"content":gp_c,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(GP_FILE, st.session_state.gp_reports)
            st.success("Saved")

with tab6:
    if user not in FINANCE_5: st.error("Finance 5 Only"); st.stop()
    f_t=st.text_input("Finance Title",key="fin_t")
    f_f=st.file_uploader("Upload Excel/PDF/PPT",type=["xlsx","pptx","pdf","csv"],key="fin_f")
    if st.button("Save Finance",key="fin_s"):
        if f_t:
            fname=""; fpath=""
            if f_f:
                fname=f_f.name.replace(" ","_")
                fpath=f"data/documents/finance_{len(st.session_state.finance_docs)+1}_{fname}"
                with open(fpath,'wb') as out: out.write(f_f.getvalue())
            st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_t,"file_name":fname,"file_path":fpath,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(FINANCE_FILE, st.session_state.finance_docs)
            st.success("Saved")
    for fd in reversed(load_json(FINANCE_FILE, st.session_state.finance_docs)):
        with st.container(border=True):
            st.write(fd['title']+" - "+fd.get('file_name',''))
            if fd.get('file_path') and os.path.exists(fd['file_path']):
                st.download_button(f"Download {fd['file_name']}", open(fd['file_path'],'rb').read(), file_name=fd['file_name'], key=f"dl_fin_{fd['id']}")

with tab7:
    dc=st.selectbox("Category",DOC_CATEGORIES,key="sec_cat")
    dt=st.text_input("Title",key="sec_t")
    dd=st.text_area("Description",key="sec_d")
    if st.button("Save Secret",key="sec_s"):
        if dt:
            st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt,"description":dd,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DOCS_FILE, st.session_state.documents)
            st.success("Saved")

with tab8:
    st.subheader("📄 Documents - PDF, PowerPoint, Word, Excel - ALL 13")
    st.info("ALL 13 can upload PDF, PPT, Word, Excel")
    docs=load_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
    st.session_state.uploaded_docs=docs
    dcat=st.selectbox("Category",DOC_CATEGORIES,key="doc_cat")
    dt=st.text_input("Title *",key="doc_t")
    dd=st.text_area("Description",key="doc_d")
    df=st.file_uploader("Upload PDF/PPT/Word/Excel",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv"],key="doc_f")
    if st.button("Upload Document",type="primary",key="doc_s"):
        if not dt or not df: st.error("Title + File required")
        else:
            safe=df.name.replace(" ","_")
            fpath=f"data/documents/doc_{len(docs)+1}_{safe}"
            with open(fpath,'wb') as out: out.write(df.getvalue())
            ext=safe.split('.')[-1].lower()
            icon="📕 PDF" if ext=="pdf" else "📊 PPT" if ext in ["pptx","ppt"] else "📝 Word" if ext in ["docx","doc"] else "📗 Excel"
            docs.append({"id":len(docs)+1,"category":dcat,"title":dt,"description":dd,"file_name":df.name,"file_path":fpath,"file_ext":ext,"file_icon":icon,"size":df.size,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(UPLOADED_DOCS_FILE, docs)
            st.success(f"Uploaded {icon} {df.name}"); st.balloons(); st.rerun()
    for doc in reversed(docs):
        with st.container(border=True):
            st.write(f"{doc.get('file_icon')} {doc['title']} - {doc['by']}")
            st.caption(f"{doc['file_name']} | {doc.get('file_ext','').upper()} | {doc.get('size',0)//1024} KB")
            if os.path.exists(doc.get('file_path','')):
                st.download_button(f"Download {doc['file_name']}", open(doc['file_path'],'rb').read(), file_name=doc['file_name'], key=f"dl_doc_{doc['id']}", type="primary")

with tab9:
    st.subheader("Media Gallery")
    mt=st.text_input("Title",key="media_t")
    mf=st.file_uploader("File JPG/PNG/MP4/MP3",type=["jpg","png","mp4","mp3"],key="media_f")
    if st.button("Upload Media",key="media_s"):
        if mt and mf:
            fpath=f"data/media_files/media_{len(st.session_state.media)+1}_{mf.name.replace(' ','_')}"
            with open(fpath,'wb') as out: out.write(mf.getvalue())
            st.session_state.media.append({"id":len(st.session_state.media)+1,"title":mt,"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(MEDIA_FILE, st.session_state.media)
            st.success("Saved"); st.rerun()
    for m in reversed(load_json(MEDIA_FILE, st.session_state.media)):
        with st.container(border=True):
            st.write(f"{m['title']} - {m['by']}")
            if os.path.exists(m['file_path']):
                if "image" in m['file_type']: st.image(m['file_path'])
                elif "video" in m['file_type']: st.video(m['file_path'])
                elif "audio" in m['file_type']: st.audio(m['file_path'])

with tab10:
    st.subheader("Cabinet Archive - For Years")
    cy=st.text_input("Year",key="cab_y")
    cn=st.text_input("Cabinet Name",key="cab_n")
    cm=st.text_area("Members",key="cab_m")
    cp=st.file_uploader("Photo",type=["jpg","png"],key="cab_p")
    if st.button("Save Cabinet",key="cab_s"):
        if cy and cn and cm and cp:
            fpath=f"data/media_files/cab_{len(st.session_state.cabinets)+1}.jpg"
            with open(fpath,'wb') as out: out.write(cp.getvalue())
            st.session_state.cabinets.append({"id":len(st.session_state.cabinets)+1,"year":cy,"name":cn,"members":cm,"photo_path":fpath,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(CABINETS_FILE, st.session_state.cabinets)
            st.success("Saved"); st.rerun()
    for cab in reversed(load_json(CABINETS_FILE, st.session_state.cabinets)):
        with st.container(border=True):
            st.write(f"{cab['name']} - {cab['year']}")
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'])
            st.info(cab['members'])
