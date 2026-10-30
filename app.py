import streamlit as st, os, json, pandas as pd
from datetime import datetime as dt
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

os.makedirs("data/media_files", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)
os.makedirs("data/personal", exist_ok=True)

FILES = {
    "reports": "data/reports.json", "media": "data/media.json", "candidates": "data/candidates.json",
    "pending": "data/pending.json", "votes": "data/votes.json", "cabinets": "data/cabinets.json",
    "docs": "data/docs.json", "finance": "data/finance.json", "disc": "data/disc.json", "gp": "data/gp.json",
    "passwords": "data/passwords.json", "uploaded": "data/uploaded_docs.json", "ann": "data/announcements.json",
    "meet": "data/meetings.json", "personal": "data/personal.json", "audit": "data/audit.json"
}

def load_json(p,d):
    if os.path.exists(p):
        try:
            with open(p,'r') as f: return json.load(f)
        except: return d
    return d
def save_json(p,data):
    with open(p,'w') as f: json.dump(data,f,default=str,indent=2)
def add_audit(action,user_full,details=""):
    audit=load_json(FILES["audit"],[]); audit.append({"id":len(audit)+1,"time":dt.now().strftime("%Y-%m-%d %H:%M:%S"),"user":user_full,"action":action,"details":details}); save_json(FILES["audit"],audit)

is_public = st.query_params.get("public","")=="vote"
st.markdown("<h2 style='text-align:center;color:#1a5c2a;'>🏛️ UNIK BEC UNASNM<br>Governance Portal - 800+ FIXED OPEN EDITION</h2><p style='text-align:center;'>All Portals Open - No Red - Bishop Cipriano Kihangire</p>",unsafe_allow_html=True)

# === PUBLIC VOTE LINK FOR STUDENTS - NO CABINET SECRETS - ADDED AS REQUESTED - DON'T REMOVE ANYTHING ELSE ===
PUBLIC_VOTE_LINK = "https://unik-bec-system-edudyqeshonywrcnjthl8l.streamlit.app/?public=vote"
# Show public link banner for all visitors - Safe for students, no secrets
st.info(f"🗳️ PUBLIC STUDENT VOTING LINK (Share to all students - No Cabinet Secrets): {PUBLIC_VOTE_LINK}")
st.markdown(f"<div style='text-align:center; background:#e8f5e9; padding:10px; border-radius:8px; border:2px solid #1a5c2a;'><b>🗳️ FOR ALL UNIK STUDENTS - VOTE HERE - NO LOGIN NEEDED:</b><br><a href='{PUBLIC_VOTE_LINK}' target='_blank' style='font-size:18px; font-weight:bold; color:#1a5c2a;'>{PUBLIC_VOTE_LINK}</a><br><small>One Email = One Vote | Cannot see Cabinet Secrets | Only Voting</small></div>", unsafe_allow_html=True)

USERS={"principal":"Principal - School Head","patron":"Hon. Patron","president":"His Excellency President","vice_president":"Hon. Vice President","speaker":"Right Hon. Speaker - Hon. Lawrence Ssango","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys())
SUPER_4=["principal","patron","president","speaker"]
FINANCE_5=["principal","patron","president","speaker","finance"]
ELECTION_POS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]
REPORT_TYPES=["Weekly","Monthly","Financial","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Audit","Budget","Other"]
DOC_CATS=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint","Public Information","Meeting Minutes","Academic","Welfare","Nursing Affairs"]

for k,f in FILES.items():
    if k not in st.session_state:
        if k=="passwords":
            pw=load_json(f,{}); st.session_state[k]=pw if pw else {u:"unik2025" for u in LOGIN_USERS}
        else: st.session_state[k]=load_json(f,[])
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

if is_public:
    st.markdown("<h3 style='text-align:center;'>🗳️ PUBLIC ELECTORAL COMMISSION</h3>",unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["Apply Candidate","Vote One Email Once","Live Results"])
    with t1:
        rp=st.selectbox("Position",ELECTION_POS,format_func=lambda x:USERS[x],key="pub_pos")
        c1,c2=st.columns(2); rn=c1.text_input("Full Names *",key="pub_name"); rclass=c2.text_input("Class *",key="pub_class")
        remail=st.text_input("Email *",key="pub_email"); rreason=st.text_area("Why vote you? *",key="pub_reason")
        rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit",type="primary",use_container_width=True):
            if not rn or not rphoto: st.error("Fill required")
            else:
                nid=len(st.session_state.pending)+len(st.session_state.candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"; open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.pending.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":str(dt.now())[:16]})
                save_json(FILES["pending"],st.session_state.pending); st.success("Sent to Speaker!"); st.balloons()
    with t2:
        voter_email=st.text_input("University Email *",key="pub_voter_email")
        if voter_email and "@" in voter_email:
            vp=st.selectbox("Choose Position",ELECTION_POS,format_func=lambda x:USERS[x],key="pub_vote_pos")
            already=[v for v in st.session_state.votes if v.get('voter_email','').lower()==voter_email.lower() and v['position']==vp]
            if already: st.error(f"Already voted for {USERS[vp]}!")
            else:
                for c in [x for x in st.session_state.candidates if x['position']==vp]:
                    with st.container(border=True):
                        col1,col2=st.columns([1,3])
                        if os.path.exists(c.get('photo_path','')): col1.image(c.get('photo_path',''),width=130)
                        col2.write(f"**{c['name']}**"); col2.info(c.get('reason',''))
                        if col2.button(f"VOTE {c['name']}",key=f"pv_{c['id']}_{voter_email}",type="primary",use_container_width=True):
                            st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email.lower(),"position":vp,"candidate_name":c['name'],"date":str(dt.now())})
                            save_json(FILES["votes"],st.session_state.votes); st.success("Voted!"); st.balloons(); st.rerun()
    with t3:
        votes=load_json(FILES["votes"],st.session_state.votes); st.success(f"Total Votes: {len(votes)}")
        for pos in ELECTION_POS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0: st.bar_chart(pd.DataFrame(rd).set_index("Candidate"))
    st.stop()

if not st.session_state.logged_in:
    st.markdown(f"### 🗳️ PUBLIC VOTE FOR ALL STUDENTS\n**Link:** {PUBLIC_VOTE_LINK}\nShare this link - Students cannot see Cabinet Secrets!")
    st.markdown(f"<a href='{PUBLIC_VOTE_LINK}' target='_blank' style='background:#1a5c2a;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:bold;'>🗳️ CLICK HERE - STUDENT VOTING - NO LOGIN</a>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🔐 Cabinet Login - 13 Departments - UNIK BEC")
    u=st.selectbox("Select Office (13)",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password - My Bottle",type="password",key="pass")
    if st.button("LOGIN TO PORTAL",type="primary",use_container_width=True):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True; st.session_state.user=u; st.rerun()
        else: st.error("Wrong password! Default unik2025")
    st.stop()

user=st.session_state.user; user_full=USERS[user]
st.sidebar.title(user_full); st.sidebar.success(f"Logged: {user_full}")
with st.sidebar.expander("🔑 Change My Password"):
    cur=st.text_input("Current",type="password",key="cur_pw"); new=st.text_input("New",type="password",key="new_pw"); conf=st.text_input("Confirm",type="password",key="conf_pw")
    if st.button("Save My Bottle",key="save_pw"):
        if cur!=st.session_state.passwords.get(user,"unik2025"): st.sidebar.error("Wrong current")
        elif new!=conf: st.sidebar.error("Don't match")
        else: st.session_state.passwords[user]=new; save_json(FILES["passwords"],st.session_state.passwords); st.sidebar.success(f"Changed! New: {new}")
if st.sidebar.button("🚪 Logout",use_container_width=True): st.session_state.logged_in=False; st.session_state.user=""; st.rerun()

reports=load_json(FILES["reports"],st.session_state.reports); media=load_json(FILES["media"],st.session_state.media); candidates=load_json(FILES["candidates"],st.session_state.candidates); votes=load_json(FILES["votes"],st.session_state.votes); docs_uploaded=load_json(FILES["uploaded"],st.session_state.uploaded)

tabs=st.tabs(["📊 Dashboard","👤 My Personal Portal","📢 Public Portal OPEN","🎥 Meeting OPEN","📝 Submit Report","🔒 Private SUPER 4","🗳️ Electoral OPEN","⚖️ Disciplinary OPEN","📋 GP OPEN","💰 Finance 5 ONLY","🔐 Secret OPEN","📄 Documents OPEN","📸 Media Gallery OPEN","🏛️ Cabinet Archive OPEN","📜 Audit Log"])

with tabs[0]:
    st.subheader(f"📊 Dashboard - {user_full}"); c1,c2,c3,c4=st.columns(4)
    c1.metric("Reports",len(reports)); c2.metric("Media",len(media)); c3.metric("Docs",len(docs_uploaded)); c4.metric("Votes",len(votes))
    st.success("✅ ALL TABS NOW OPEN - No more red!")

with tabs[1]:
    st.subheader(f"👤 My Personal Portal - ONLY YOU - {user_full}")
    st.warning("🔐 Only you can see files here! Other 12 CANNOT!")
    personal=load_json(FILES["personal"],st.session_state.personal); my_personal=[p for p in personal if p['owner']==user]
    st.success(f"Your Personal Files: {len(my_personal)}")
    pt=st.text_input("Title *",key="pers_t"); pc=st.text_area("Notes *",key="pers_c"); pf=st.file_uploader("File - ONLY YOU",type=["pdf","xlsx","pptx","docx","jpg","png","jpeg","mp4","mp3"],key="pers_f")
    if st.button("Save To My Personal Portal - PRIVATE",type="primary",use_container_width=True,key="pers_s"):
        fpath=""; fname=""
        if pf: fname=pf.name.replace(" ","_"); fpath=f"data/personal/{user}_{len(personal)+1}_{fname}"; open(fpath,'wb').write(pf.getvalue())
        personal.append({"id":len(personal)+1,"owner":user,"owner_name":user_full,"title":pt.strip(),"content":pc.strip(),"file_name":fname,"file_path":fpath,"date":dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["personal"],personal); st.success("Saved only for you!"); st.balloons(); st.rerun()
    for p in reversed(my_personal):
        with st.container(border=True):
            st.markdown(f"**{p['title']}** | {p['date']}")
            if p.get('content'): st.info(p['content'])
            if p.get('file_path','') and os.path.exists(p['file_path']):
                st.download_button(f"Download {p['file_name']}",open(p['file_path'],'rb').read(),file_name=p['file_name'],key=f"dl_pers_{p['id']}",type="primary")

with tabs[2]:
    st.subheader("📢 Public Portal - OPEN TO ALL 13 - NOW OPENS!")
    anns=load_json(FILES["ann"],st.session_state.ann)
    at=st.text_input("Title *",key="ann_t"); acont=st.text_area("Message *",key="ann_c"); af=st.file_uploader("Attach File",type=["pdf","xlsx","pptx","docx","jpg","png"],key="ann_f")
    if st.button("📢 BROADCAST TO ALL 13",type="primary",use_container_width=True):
        fpath=""; fname=""
        if af: fname=af.name.replace(" ","_"); fpath=f"data/documents/ann_{len(anns)+1}_{fname}"; open(fpath,'wb').write(af.getvalue())
        anns.append({"id":len(anns)+1,"title":at.strip(),"content":acont.strip(),"file_name":fname,"file_path":fpath,"from":user,"from_name":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["ann"],anns); st.success("Broadcasted to ALL 13!"); st.balloons(); st.rerun()
    for ann in reversed(anns):
        with st.container(border=True):
            st.markdown(f"**{ann['title']}** | {ann['from_name']} | {ann['date']}"); st.info(ann['content'])
            if ann.get('file_path','') and os.path.exists(ann['file_path']): st.download_button(f"Download {ann['file_name']}",open(ann['file_path'],'rb').read(),file_name=ann['file_name'],key=f"dl_ann_{ann['id']}")

with tabs[3]:
    st.subheader("🎥 Online Meeting - OPEN TO ALL 13 - NOW OPENS!")
    meetings=load_json(FILES["meet"],st.session_state.meet); active=[m for m in meetings if m.get('is_active')]
    if active:
        am=active[-1]; st.success(f"🔴 LIVE NOW: {am['title']} by {am['from_name']}")
        mid=am['meeting_id']
        st.markdown(f"<a href='https://meet.jit.si/{mid}' target='_blank' style='background:#25D366;color:white;padding:12px 25px;border-radius:8px;text-decoration:none;font-weight:bold;'>🎥 JOIN MEETING NOW</a>",unsafe_allow_html=True)
        st.components.v1.html(f"<iframe src='https://meet.jit.si/{mid}' style='width:100%;height:600px;border:0;' allow='camera; microphone; fullscreen'></iframe>",height=650)
        if st.button("🔴 END MEETING",key="end_meet"):
            for m in meetings:
                if m['meeting_id']==mid: m['is_active']=False
            save_json(FILES["meet"],meetings); st.success("Ended"); st.rerun()
    mt=st.text_input("Meeting Title *",key="m_title"); mtop=st.text_area("Topic *",key="m_topic")
    if st.button("🎥 START MEETING - ALL 13 CAN JOIN",type="primary",use_container_width=True):
        mid=f"UNIK-BEC-{dt.now().strftime('%Y%m%d-%H%M')}-{mt.replace(' ','')[:8]}"
        meetings.append({"id":len(meetings)+1,"meeting_id":mid,"title":mt.strip(),"topic":mtop.strip(),"from":user,"from_name":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"is_active":True})
        save_json(FILES["meet"],meetings); st.success(f"Started! {mid}"); st.balloons(); st.rerun()

with tabs[4]:
    st.subheader("📝 Submit Report - OPEN - NOW OPENS!")
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt"); rtitle=st.text_input("Title *",key="rtitle"); rcontent=st.text_area("Details *",key="rcontent")
    if st.button("📤 Submit Report",type="primary",use_container_width=True):
        reports.append({"id":len(reports)+1,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip()})
        save_json(FILES["reports"],reports); st.success("Saved! SUPER 4 will see!"); st.balloons()

with tabs[5]:
    st.subheader("🔒 Private Portal - SUPER 4 ONLY - NOW OPENS (No Red)!")
    if user in SUPER_4:
        st.success(f"✅ ACCESS GRANTED - You are SUPER 4: {user_full} - Total Reports: {len(reports)}")
        reports_data=load_json(FILES["reports"],st.session_state.reports)
        ftype=st.selectbox("Filter", ["All"]+REPORT_TYPES, key="filter_type")
        filtered=reports_data if ftype=="All" else [r for r in reports_data if r['type']==ftype]
        for r in reversed(filtered):
            with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']}"): st.info(r['content'])
    else:
        st.error(f"🚫 RESTRICTED: Private is SUPER 4 ONLY (Principal, Patron, President, Speaker). You are {user_full} - Not SUPER 4. But tab is OPEN - No red!")
        st.info("Contact SUPER 4 to access Private reports. This tab is working - It just shows restriction message instead of killing all tabs!")

with tabs[6]:
    st.subheader("🗳️ Electoral - OPEN TO ALL 13 - NOW OPENS!")
    pend=load_json(FILES["pending"],st.session_state.pending); cand=load_json(FILES["candidates"],st.session_state.candidates); votes=load_json(FILES["votes"],st.session_state.votes)
    t_a,t_b,t_c=st.tabs(["Pending - Speaker Approves","Register","Results"])
    with t_a:
        st.write(f"Pending: {len(pend)}")
        for pc in reversed(pend):
            with st.container(border=True):
                col1,col2=st.columns([1,3])
                if os.path.exists(pc.get('photo_path','')): col1.image(pc.get('photo_path',''),width=120)
                col2.write(f"**{pc['name']}** - {USERS[pc['position']]}"); col2.info(pc.get('reason',''))
                if user=="speaker":
                    if col2.button(f"Approve {pc['name']}",key=f"ap_{pc['id']}",type="primary"): st.session_state.candidates.append(pc); st.session_state.pending=[x for x in st.session_state.pending if x['id']!=pc['id']]; save_json(FILES["candidates"],st.session_state.candidates); save_json(FILES["pending"],st.session_state.pending); st.success("Approved!"); st.rerun()
    with t_b:
        rp=st.selectbox("Position",ELECTION_POS,format_func=lambda x:USERS[x],key="cand_pos"); rn=st.text_input("Names *",key="cand_name"); rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="cand_photo")
        if st.button("Register Candidate",type="primary"):
            if not rn or not rphoto: st.error("Required")
            else:
                nid=len(cand)+len(pend)+1; fpath=f"data/media_files/cand_{nid}.jpg"; open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.candidates.append({"id":nid,"position":rp,"name":rn,"class":"","reason":"Cabinet Member","photo_path":fpath,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["candidates"],st.session_state.candidates); st.success(f"Registered {rn}!")
    with t_c:
        st.write(f"Total Votes: {len(votes)}")
        for pos in ELECTION_POS:
            cs=[c for c in cand if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in votes if v['candidate_id']==cc['id']])} for cc in cs]
                st.dataframe(pd.DataFrame(rd).sort_values("Votes",ascending=False),use_container_width=True)

with tabs[7]:
    st.subheader("⚖️ Disciplinary - OPEN TO ALL 13 - NOW OPENS!")
    disc=load_json(FILES["disc"],st.session_state.disc)
    d_t=st.text_input("Case Title *",key="disc_t"); d_c=st.text_area("Details *",key="disc_c")
    if st.button("Save Disciplinary - ALL 13 CAN OPEN!",type="primary",key="disc_s"): disc.append({"id":len(disc)+1,"title":d_t.strip(),"content":d_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["disc"],disc); st.success("Saved! ALL 13 can see!"); st.rerun()
    for dr in reversed(disc):
        with st.expander(f"#{dr['id']} {dr['title']} - {dr['by']}"): st.info(dr['content'])

with tabs[8]:
    st.subheader("📋 GP - OPEN TO ALL 13 - NOW OPENS!")
    gp=load_json(FILES["gp"],st.session_state.gp)
    gp_t=st.text_input("GP Title *",key="gp_t"); gp_c=st.text_area("GP Details *",key="gp_c")
    if st.button("Save GP - ALL 13 CAN OPEN!",type="primary",key="gp_s"): gp.append({"id":len(gp)+1,"title":gp_t.strip(),"content":gp_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["gp"],gp); st.success("Saved! ALL 13 can see!"); st.rerun()
    for gpr in reversed(gp):
        with st.expander(f"{gpr['title']} - {gpr['by']}"): st.info(gpr['content'])

with tabs[9]:
    st.subheader("💰 Finance - 5 ONLY - NOW OPENS (No Red)!")
    if user in FINANCE_5:
        st.success(f"✅ ACCESS GRANTED - Finance 5: {user_full}")
        fin=load_json(FILES["finance"],st.session_state.finance)
        f_t=st.text_input("Finance Title *",key="fin_t"); f_d=st.text_area("Description",key="fin_d"); f_f=st.file_uploader("Upload Excel / PPT / PDF",type=["xlsx","xls","pptx","ppt","pdf","docx","doc"],key="fin_f"); f_amount=st.number_input("Amount UGX",min_value=0,step=1000,key="fin_amount")
        if st.button("Save Finance - 5 ONLY",type="primary",key="fin_s2"):
            fname=""; fpath=""
            if f_f: fname=f_f.name.replace(" ","_"); fpath=f"data/documents/finance_{len(fin)+1}_{fname}"; open(fpath,'wb').write(f_f.getvalue())
            fin.append({"id":len(fin)+1,"title":f_t.strip(),"description":f_d.strip(),"amount":f_amount,"file_name":fname,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["finance"],fin); st.success("Saved! 5 Only can see!"); st.rerun()
        for fd in reversed(fin):
            with st.container(border=True):
                st.markdown(f"**{fd['title']}** - {fd['by']} - UGX {fd.get('amount',0):,}")
                if fd.get('file_path','') and os.path.exists(fd['file_path']): st.download_button(f"Download {fd['file_name']}",open(fd['file_path'],'rb').read(),file_name=fd['file_name'],key=f"dl_fin_{fd['id']}",type="primary")
    else:
        st.error(f"🚫 RESTRICTED: Finance is 5 ONLY (Principal, Patron, President, Speaker, Finance). You are {user_full}. Tab is OPEN - No red - Just shows restriction!")

with tabs[10]:
    st.subheader("🔐 Secret - OPEN TO ALL 13 - NOW OPENS!")
    sec=load_json(FILES["docs"],st.session_state.docs)
    dc=st.selectbox("Category",DOC_CATS,key="sec_cat"); dt_=st.text_input("Title *",key="sec_t"); dd=st.text_area("Description",key="sec_d")
    if st.button("Save Secret - ALL 13 OPEN!",type="primary",key="sec_s"): sec.append({"id":len(sec)+1,"category":dc,"title":dt_.strip(),"description":dd.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d")}); save_json(FILES["docs"],sec); st.success("Saved! ALL 13 can open!"); st.rerun()
    for d in reversed(sec):
        with st.expander(f"{d['category']} | {d['title']} - {d['by']}"): st.write(d['description'])

with tabs[11]:
    st.subheader("📄 Documents - OPEN TO ALL 13 - NOW OPENS!")
    docs=load_json(FILES["uploaded"],st.session_state.uploaded)
    st.success(f"OPEN: ALL 13 can upload & see same! Total: {len(docs)} - Now opens!")
    dcat=st.selectbox("Category",DOC_CATS,key="doc_cat"); dtit=st.text_input("Title *",key="doc_t"); dd=st.text_area("Description",key="doc_d"); df=st.file_uploader("Upload File *",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv","jpg","png"],key="doc_f")
    if st.button("Upload Document - ALL 13 SEE SAME!",type="primary",use_container_width=True,key="doc_s"):
        if not dtit.strip() or not df: st.error("Title + File required")
        else:
            safe=df.name.replace(" ","_"); fpath=f"data/documents/doc_{len(docs)+1}_{safe}"; open(fpath,'wb').write(df.getvalue())
            docs.append({"id":len(docs)+1,"category":dcat,"title":dtit.strip(),"description":dd.strip(),"file_name":df.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["uploaded"],docs); st.success("Uploaded! ALL 13 SEE SAME!"); st.balloons(); st.rerun()
    for doc in reversed(docs):
        with st.container(border=True):
            st.markdown(f"**{doc['title']}** | {doc['category']} | by {doc['by']}")
            if os.path.exists(doc.get('file_path','')): st.download_button(f"Download {doc['file_name']}",open(doc['file_path'],'rb').read(),file_name=doc['file_name'],key=f"dl_doc_{doc['id']}",type="primary")

with tabs[12]:
    st.subheader("📸 Media Gallery - OPEN TO ALL 13 - NOW OPENS - FIXED!")
    med=load_json(FILES["media"],st.session_state.media)
    st.success(f"FIXED! ALL 13 can post! Total: {len(med)} - Class Rep posts, President sees same! Now opens!")
    mt=st.text_input("Media Title *",key="media_t"); mf=st.file_uploader("File *",type=["jpg","png","jpeg","mp4","mp3","m4a","wav","mov"],key="media_f")
    if st.button("Upload - ALL 13 SEE SAME GALLERY! - NOW OPENS!",type="primary",use_container_width=True,key="media_s"):
        if not mt.strip() or not mf: st.error("Required")
        else:
            fpath=f"data/media_files/media_{len(med)+1}_{mf.name.replace(' ','_')}"; open(fpath,'wb').write(mf.getvalue())
            med.append({"id":len(med)+1,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["media"],med); st.success("Saved! NOW ALL 13 SEE SAME!"); st.balloons(); st.rerun()
    cols=st.columns(3)
    for idx,m in enumerate(reversed(med)):
        with cols[idx%3]:
            with st.container(border=True):
                st.write(f"**{m['title']}** - {m['by']}")
                if os.path.exists(m['file_path']):
                    if "image" in m['file_type']: st.image(m['file_path'],use_container_width=True)
                    elif "video" in m['file_type']: st.video(m['file_path'])
                    elif "audio" in m['file_type']: st.audio(m['file_path'])
                if os.path.exists(m['file_path']): st.download_button(f"Download {m['file_name']}",open(m['file_path'],'rb').read(),file_name=m['file_name'],key=f"dl_med_{m['id']}")

with tabs[13]:
    st.subheader("🏛️ Cabinet Archive - OPEN TO ALL 13 - NOW OPENS!")
    cabs=load_json(FILES["cabinets"],st.session_state.cabinets)
    cy=st.text_input("Year *",key="cab_y"); cn=st.text_input("Cabinet Name *",key="cab_n"); cm=st.text_area("Members List *",key="cab_m"); cp=st.file_uploader("Group Photo *",type=["jpg","png","jpeg"],key="cab_p")
    if st.button("Save Cabinet - ALL 13 OPEN!",type="primary",use_container_width=True,key="cab_s"):
        if not cy or not cn or not cm or not cp: st.error("All required")
        else: fpath=f"data/media_files/cab_{len(cabs)+1}.jpg"; open(fpath,'wb').write(cp.getvalue()); cabs.append({"id":len(cabs)+1,"year":cy.strip(),"name":cn.strip(),"members":cm.strip(),"photo_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d")}); save_json(FILES["cabinets"],cabs); st.success("Saved! ALL 13 can see!"); st.rerun()
    for cab in reversed(cabs):
        with st.container(border=True):
            st.markdown(f"**{cab['name']} - {cab['year']}**")
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'],use_container_width=True)
            st.info(cab['members'])

with tabs[14]:
    st.subheader("📜 Audit Log - OPEN - NOW OPENS!"); audit=load_json(FILES["audit"],st.session_state.audit); st.success(f"Total Actions: {len(audit)}"); 
    if audit: st.dataframe(pd.DataFrame(reversed(audit)),use_container_width=True)

st.markdown("---"); st.markdown(f"<p style='text-align:center;color:gray;'>UNIK BEC UNASNM | 800+ FIXED OPEN EDITION | All Tabs Open - No Red - Fixed st.stop() Bug | Speaker Hon. Lawrence Ssango | {dt.now().year} | Public Link: {PUBLIC_VOTE_LINK}</p>",unsafe_allow_html=True)
