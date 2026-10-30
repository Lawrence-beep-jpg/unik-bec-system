import streamlit as st, os, json, datetime, pandas as pd
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")
os.makedirs("data/media_files",exist_ok=True); os.makedirs("data/documents",exist_ok=True)
FILES={"reports":"data/reports.json","media":"data/media.json","candidates":"data/candidates.json","pending":"data/pending.json","votes":"data/votes.json","cabinets":"data/cabinets.json","docs":"data/docs.json","finance":"data/finance.json","disc":"data/disc.json","gp":"data/gp.json","passwords":"data/passwords.json","uploaded":"data/uploaded_docs.json","ann":"data/announcements.json","meet":"data/meetings.json"}
def load_json(p,d):
    if os.path.exists(p):
        try:
            with open(p,'r') as f: return json.load(f)
        except: return d
    return d
def save_json(p,data):
    with open(p,'w') as f: json.dump(data,f,default=str)
is_public=st.query_params.get("public","")=="vote"
st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM<br>Governance Portal</h2>",unsafe_allow_html=True)
USERS={"principal":"Principal","patron":"Hon. Patron","president":"His Excellency President","vice_president":"Hon. Vice President - Leader GP","speaker":"Right Honourable Speaker - Hon. Lawrence Ssango","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys()); SUPER_4=["principal","patron","president","speaker"]; FINANCE_5=["principal","patron","president","speaker","finance"]
ELECTION_POS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]
REPORT_TYPES=["Weekly","Monthly","Financial","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Other"]
DOC_CATS=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint","Public Information","Meeting Minutes"]
for k,f in FILES.items():
    if k not in st.session_state:
        if k=="passwords":
            pw=load_json(f,{}); st.session_state[k]=pw if pw else {u:"unik2025" for u in LOGIN_USERS}
        else: st.session_state[k]=load_json(f,[])
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""
if is_public:
    st.markdown("<h3 style='text-align:center;'>PUBLIC ELECTORAL COMMISSION</h3>",unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["Apply Candidate","Vote One Email Once","Live Results"])
    with t1:
        rp=st.selectbox("Position",ELECTION_POS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names *",key="pub_name"); rclass=st.text_input("Class *",key="pub_class"); remail=st.text_input("Email *",key="pub_email"); rreason=st.text_area("Why vote you? *",key="pub_reason"); rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit (Needs Speaker Approval)",type="primary",use_container_width=True):
            if not rn or not rclass or not remail or not rreason or not rphoto: st.error("Fill ALL")
            else:
                nid=len(st.session_state.pending)+len(st.session_state.candidates)+1; fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue()); st.session_state.pending.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":str(datetime.datetime.now())[:10]}); save_json(FILES["pending"],st.session_state.pending); st.success("Sent!"); st.balloons()
    with t2:
        voter_email=st.text_input("Your Email *",key="pub_voter_email")
        if voter_email and "@" in voter_email:
            vp=st.selectbox("Choose Position",ELECTION_POS,format_func=lambda x:USERS[x],key="pub_vote_pos")
            already=[v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
            if already: st.error(f"Already voted for {USERS[vp]}")
            else:
                for c in [x for x in st.session_state.candidates if x['position']==vp]:
                    with st.container(border=True):
                        if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=150)
                        st.write(f"**{c['name']}**"); st.info(c.get('reason',''))
                        if st.button(f"Vote {c['name']}",key=f"pv_{c['id']}_{voter_email}",type="primary"):
                            st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":str(datetime.datetime.now())}); save_json(FILES["votes"],st.session_state.votes); st.success("Voted!"); st.rerun()
        else: st.warning("Enter valid email")
    with t3:
        for pos in ELECTION_POS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0: st.write(f"**{USERS[pos]}**"); st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()
if not st.session_state.logged_in:
    st.markdown("### Cabinet Login - 13 Departments Only")
    u=st.selectbox("Select Office",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("LOGIN",type="primary",use_container_width=True):
        if p==st.session_state.passwords.get(u,"unik2025"): st.session_state.logged_in=True; st.session_state.user=u; st.rerun()
        else: st.error("Wrong! Default unik2025")
    st.info("Default: unik2025 | Public: ?public=vote"); st.stop()
user=st.session_state.user; user_full=USERS[user]
st.sidebar.title(user_full); st.sidebar.success(f"Logged: {user_full}")
with st.sidebar.expander("Change My Password - My Bottle"):
    cur=st.text_input("Current",type="password",key="cur_pw"); new=st.text_input("New",type="password",key="new_pw"); conf=st.text_input("Confirm",type="password",key="conf_pw")
    if st.button("Save Password",key="save_pw"):
        if cur!=st.session_state.passwords.get(user,"unik2025"): st.sidebar.error("Wrong current")
        elif new!=conf: st.sidebar.error("Don't match")
        else: st.session_state.passwords[user]=new; save_json(FILES["passwords"],st.session_state.passwords); st.sidebar.success(f"Changed to {new}")
if st.sidebar.button("Logout"): st.session_state.logged_in=False; st.rerun()
tab0,tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11=st.tabs(["📢 Public Portal","🎥 Meeting","📝 Submit Report","🔒 Private Portal SUPER 4 ONLY","🗳️ Electoral OPEN ALL 13","⚖️ Disciplinary OPEN","📋 GP OPEN","💰 Finance 5 ONLY","🔐 Secret OPEN ALL 13","📄 Documents OPEN ALL 13","📸 Media Gallery OPEN ALL 13","🏛️ Cabinet Archive OPEN ALL 13"])
with tab0:
    st.subheader("Public Portal - SUPER 4 posts, ALL 13 read")
    anns=load_json(FILES["ann"],st.session_state.ann)
    if user in SUPER_4:
        at=st.text_input("Title *",key="ann_t"); acont=st.text_area("Message to ALL 13 *",key="ann_c",height=120); af=st.file_uploader("Attach File",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","jpg","png","jpeg"],key="ann_f")
        if st.button("BROADCAST TO ALL 13",type="primary",use_container_width=True):
            if not at.strip() or not acont.strip(): st.error("Title + Message required")
            else:
                fpath=""; fname=""
                if af: fname=af.name.replace(" ","_"); fpath=f"data/documents/ann_{len(anns)+1}_{fname}"; open(fpath,'wb').write(af.getvalue())
                anns.append({"id":len(anns)+1,"title":at.strip(),"content":acont.strip(),"file_name":fname,"file_path":fpath,"from":user,"from_name":user_full,"date":str(datetime.datetime.now())[:16]}); save_json(FILES["ann"],anns); st.success("Broadcasted to ALL 13!"); st.balloons(); st.rerun()
    for ann in reversed(anns):
        with st.container(border=True):
            st.markdown(f"**{ann['title']}** | {ann['from_name']} | {ann['date']}"); st.info(ann['content'])
            if ann.get('file_path','') and os.path.exists(ann['file_path']): st.download_button(f"Download {ann['file_name']}",open(ann['file_path'],'rb').read(),file_name=ann['file_name'],key=f"dl_ann_{ann['id']}")
with tab1:
    st.subheader("Online Meeting - Audio/Video - ALL 13 can join")
    meetings=load_json(FILES["meet"],st.session_state.meet); active=[m for m in meetings if m.get('is_active')]
    if active:
        am=active[-1]; st.success(f"LIVE NOW: {am['title']} by {am['from_name']}"); st.warning(f"Topic: {am['topic']}"); mid=am['meeting_id']
        st.markdown(f"<a href='https://meet.jit.si/{mid}' target='_blank' style='background:#25D366;color:white;padding:12px 25px;border-radius:8px;text-decoration:none;font-weight:bold;display:inline-block;'>JOIN MEETING NOW</a>",unsafe_allow_html=True)
        st.components.v1.html(f"<iframe src='https://meet.jit.si/{mid}#userInfo.displayName='{user_full}'' style='width:100%;height:600px;border:0;border-radius:10px;' allow='camera; microphone; fullscreen; display-capture'></iframe>",height=650)
        if user in SUPER_4:
            if st.button("END MEETING FOR ALL",key="end_meet"): 
                for m in meetings:
                    if m['meeting_id']==mid: m['is_active']=False
                save_json(FILES["meet"],meetings); st.success("Ended"); st.rerun()
    else: st.warning("No active meeting")
    if user in SUPER_4:
        st.divider(); mt=st.text_input("Meeting Title *",key="m_title"); mtop=st.text_area("Topic *",key="m_topic")
        if st.button("START MEETING - ALL 13 CAN JOIN",type="primary",use_container_width=True):
            if not mt.strip() or not mtop.strip(): st.error("Required")
            else: mid=f"UNIK-BEC-{datetime.datetime.now().strftime('%Y%m%d-%H%M')}-{mt.replace(' ','')[:8]}"; meetings.append({"id":len(meetings)+1,"meeting_id":mid,"title":mt.strip(),"topic":mtop.strip(),"from":user,"from_name":user_full,"date":str(datetime.datetime.now())[:16],"is_active":True}); save_json(FILES["meet"],meetings); st.success(f"Started ID: {mid}"); st.balloons(); st.rerun()
with tab2:
    st.subheader("Submit Report - Principal Sees")
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt"); rtitle=st.text_input("Report Title *",key="rtitle"); rcontent=st.text_area("Details *",key="rcontent",height=120)
    if st.button("Submit Report",type="primary",use_container_width=True):
        if not rtitle.strip() or not rcontent.strip(): st.error("Required")
        else: st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":str(datetime.datetime.now())[:16],"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip()}); save_json(FILES["reports"],st.session_state.reports); st.success("Saved - Principal will see!"); st.balloons()
with tab3:
    st.subheader("🔒 Private Portal - SUPER 4 ONLY")
    if user not in SUPER_4:
        st.error("RESTRICTED: Only SUPER 4 (Principal, Patron, President, Speaker) can access Private Portal")
        st.stop()
    reports=load_json(FILES["reports"],st.session_state.reports)
    st.success(f"SUPER 4 ACCESS: Total Reports from All 13 Departments: {len(reports)}")
    for r in reversed(reports):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']}"): st.info(r['content'])
with tab4:
    st.subheader("🗳️ Electoral - OPEN TO ALL 13")
    pend=load_json(FILES["pending"],st.session_state.pending); cand=load_json(FILES["candidates"],st.session_state.candidates); votes=load_json(FILES["votes"],st.session_state.votes)
    t_a,t_b,t_c=st.tabs(["Pending Approval - Speaker Only","Register OPEN ALL","Results OPEN ALL"])
    with t_a:
        st.write(f"Pending: {len(pend)}")
        for pc in reversed(pend):
            with st.container(border=True):
                if os.path.exists(pc.get('photo_path','')): st.image(pc.get('photo_path',''),width=120)
                st.write(f"**{pc['name']}** - {USERS[pc['position']]}"); st.info(pc.get('reason',''))
                if user=="speaker":
                    if st.button(f"Approve {pc['name']}",key=f"ap_{pc['id']}",type="primary"):
                        st.session_state.candidates.append(pc); st.session_state.pending=[x for x in st.session_state.pending if x['id']!=pc['id']]; save_json(FILES["candidates"],st.session_state.candidates); save_json(FILES["pending"],st.session_state.pending); st.success("Approved"); st.rerun()
    with t_b:
        rp=st.selectbox("Position",ELECTION_POS,format_func=lambda x:USERS[x],key="cand_pos"); rn=st.text_input("Names *",key="cand_name"); rclass=st.text_input("Class",key="cand_class"); rreason=st.text_area("Why vote you?",key="cand_reason"); rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="cand_photo")
        if st.button("Register",type="primary"):
            if not rn or not rphoto: st.error("Names+Photo required")
            else: nid=len(cand)+len(pend)+1; fpath=f"data/media_files/cand_{nid}.jpg"; open(fpath,'wb').write(rphoto.getvalue()); st.session_state.candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"reason":rreason if rreason else "Cabinet","photo_path":fpath,"date":str(datetime.datetime.now())[:10]}); save_json(FILES["candidates"],st.session_state.candidates); st.success(f"Registered {rn}")
    with t_c:
        for pos in ELECTION_POS:
            cs=[c for c in cand if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in votes if v['candidate_id']==cc['id']])} for cc in cs]
                st.write(f"**{USERS[pos]}**"); st.dataframe(pd.DataFrame(rd),use_container_width=True)
with tab5:
    st.subheader("⚖️ Disciplinary - OPEN TO ALL 13")
    disc=load_json(FILES["disc"],st.session_state.disc); st.success("OPEN: All 13 can access this department - Necessary!")
    d_t=st.text_input("Case Title *",key="disc_t"); d_c=st.text_area("Details *",key="disc_c",height=100)
    if st.button("Save Disciplinary",type="primary",key="disc_s"):
        if not d_t or not d_c: st.error("Required")
        else: disc.append({"id":len(disc)+1,"title":d_t,"content":d_c,"by":user_full,"date":str(datetime.datetime.now())[:16]}); save_json(FILES["disc"],disc); st.success("Saved - ALL 13 can see!"); st.rerun()
    for dr in reversed(disc):
        with st.expander(f"{dr['title']} - {dr['by']} - {dr['date']}"): st.info(dr['content'])
with tab6:
    st.subheader("📋 GP - OPEN TO ALL 13")
    gp=load_json(FILES["gp"],st.session_state.gp); st.success("OPEN: All 13 can access GP reports - Necessary!")
    gp_t=st.text_input("GP Title *",key="gp_t"); gp_c=st.text_area("GP Details *",key="gp_c",height=100)
    if st.button("Save GP",type="primary",key="gp_s"):
        if not gp_t or not gp_c: st.error("Required")
        else: gp.append({"id":len(gp)+1,"title":gp_t,"content":gp_c,"by":user_full,"date":str(datetime.datetime.now())[:16]}); save_json(FILES["gp"],gp); st.success("Saved - ALL 13 can see!"); st.rerun()
    for gpr in reversed(gp):
        with st.expander(f"{gpr['title']} - {gpr['by']} - {gpr['date']}"): st.info(gpr['content'])
with tab7:
    st.subheader("💰 Finance Portal - 5 ONLY")
    if user not in FINANCE_5:
        st.error("RESTRICTED: Finance is ONLY for 5: Principal, Patron, President, Speaker, Finance")
        st.stop()
    fin=load_json(FILES["finance"],st.session_state.finance); st.success(f"FINANCE 5 ACCESS: Welcome {user_full}!")
    f_t=st.text_input("Finance Title *",key="fin_t"); f_d=st.text_area("Description",key="fin_d"); f_f=st.file_uploader("Upload Excel / PPT / PDF / Word",type=["xlsx","xls","pptx","ppt","pdf","docx","doc","csv"],key="fin_f")
    if st.button("Save Finance Doc",type="primary",key="fin_s2"):
        if not f_t: st.error("Title required")
        else:
            fname=""; fpath=""
            if f_f: fname=f_f.name.replace(" ","_"); fpath=f"data/documents/finance_{len(fin)+1}_{fname}"; open(fpath,'wb').write(f_f.getvalue())
            fin.append({"id":len(fin)+1,"title":f_t,"description":f_d,"file_name":fname,"file_path":fpath,"by":user_full,"date":str(datetime.datetime.now())[:16]}); save_json(FILES["finance"],fin); st.success("Saved - 5 Only can see & download!"); st.rerun()
    for fd in reversed(fin):
        with st.container(border=True):
            st.write(f"**{fd['title']}** - {fd['by']} - {fd['date']}")
            if fd.get('file_path','') and os.path.exists(fd['file_path']): st.download_button(f"Download {fd['file_name']}",open(fd['file_path'],'rb').read(),file_name=fd['file_name'],key=f"dl_fin_{fd['id']}",type="primary")
with tab8:
    st.subheader("🔐 Secret Store - OPEN TO ALL 13")
    sec=load_json(FILES["docs"],st.session_state.docs); st.success("OPEN: All 13 can access Secret Store!")
    dc=st.selectbox("Category",DOC_CATS,key="sec_cat"); dt=st.text_input("Title *",key="sec_t"); dd=st.text_area("Description",key="sec_d",height=100)
    if st.button("Save Secret Text",type="primary",key="sec_s"):
        if not dt.strip(): st.error("Title required")
        else: sec.append({"id":len(sec)+1,"category":dc,"title":dt.strip(),"description":dd,"by":user_full,"date":str(datetime.datetime.now())[:10]}); save_json(FILES["docs"],sec); st.success("Saved - ALL 13 can see!")
    for d in reversed(sec):
        with st.expander(f"{d['category']} | {d['title']} - {d['by']}"): st.write(d['description'])
with tab9:
    st.subheader("📄 Documents - OPEN TO ALL 13 - EVERYONE CAN UPLOAD & SEE SAME!")
    docs=load_json(FILES["uploaded"],st.session_state.uploaded); st.success(f"OPEN: ALL 13 can upload & see same! Total: {len(docs)} - No hiding!")
    dcat=st.selectbox("Category",DOC_CATS,key="doc_cat"); dt=st.text_input("Title *",key="doc_t"); dd=st.text_area("Description",key="doc_d"); df=st.file_uploader("Upload File * PDF/PPT/Word/Excel - ALL 13 can upload!",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv"],key="doc_f")
    if st.button("Upload Document - Visible to ALL 13!",type="primary",use_container_width=True,key="doc_s"):
        if not dt.strip() or not df: st.error("Title+File required")
        else:
            safe=df.name.replace(" ","_"); fpath=f"data/documents/doc_{len(docs)+1}_{safe}"; open(fpath,'wb').write(df.getvalue())
            docs.append({"id":len(docs)+1,"category":dcat,"title":dt.strip(),"description":dd.strip(),"file_name":df.name,"file_path":fpath,"by":user_full,"date":str(datetime.datetime.now())[:16]}); save_json(FILES["uploaded"],docs); st.success(f"Uploaded {df.name}! NOW ALL 13 SEE SAME!"); st.balloons(); st.rerun()
    for doc in reversed(docs):
        with st.container(border=True):
            st.markdown(f"**{doc['title']}** | {doc['category']} | by {doc['by']} | {doc['date']}")
            if doc.get('description',''): st.write(doc['description'])
            if os.path.exists(doc.get('file_path','')): st.download_button(f"Download {doc['file_name']} - ALL 13 can download!",open(doc['file_path'],'rb').read(),file_name=doc['file_name'],key=f"dl_doc_{doc['id']}",type="primary",use_container_width=True)
with tab10:
    st.subheader("📸 Media Gallery - OPEN TO ALL 13 - EVERYONE POSTS, EVERYONE SEES SAME!")
    med=load_json(FILES["media"],st.session_state.media); st.success(f"FIXED! ALL 13 can post! Total: {len(med)} - If you post, ALL 13 see same gallery! No hiding!")
    mt=st.text_input("Media Title * - Everyone will see!",key="media_t"); mf=st.file_uploader("File * JPG/PNG/MP4/MP3 - Upload - ALL 13 WILL SEE SAME!",type=["jpg","png","jpeg","mp4","mp3","m4a","wav"],key="media_f")
    if st.button("Upload - Visible to ALL 13 - EVERYONE SEES SAME GALLERY!",type="primary",use_container_width=True,key="media_s"):
        if not mt.strip() or not mf: st.error("Title+File required")
        else:
            fpath=f"data/media_files/media_{len(med)+1}_{mf.name.replace(' ','_')}"; open(fpath,'wb').write(mf.getvalue())
            med.append({"id":len(med)+1,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":str(datetime.datetime.now())[:16]}); save_json(FILES["media"],med); st.success(f"Saved! NOW ALL 13 SEE: {mt.strip()} by {user_full}!"); st.balloons(); st.rerun()
    st.divider()
    for m in reversed(med):
        with st.container(border=True):
            st.write(f"**{m['title']}** - Posted by {m['by']} - {m['date']} - Visible to ALL 13!")
            if os.path.exists(m['file_path']):
                if "image" in m['file_type']: st.image(m['file_path'],use_container_width=True)
                elif "video" in m['file_type']: st.video(m['file_path'])
                elif "audio" in m['file_type']: st.audio(m['file_path'])
with tab11:
    st.subheader("🏛️ Cabinet Archive - OPEN TO ALL 13!")
    cabs=load_json(FILES["cabinets"],st.session_state.cabinets); st.success(f"OPEN: ALL 13 can post & see same! Total: {len(cabs)} - Saved for years!")
    cy=st.text_input("Year *",key="cab_y"); cn=st.text_input("Cabinet Name * (e.g. First BEC 2026)",key="cab_n"); cm=st.text_area("Members *",key="cab_m"); cp=st.file_uploader("Cabinet Photo *",type=["jpg","png","jpeg"],key="cab_p")
    if st.button("Save Cabinet - Visible to ALL 13!",type="primary",use_container_width=True,key="cab_s"):
        if not cy or not cn or not cm or not cp: st.error("All fields required")
        else: fpath=f"data/media_files/cab_{len(cabs)+1}.jpg"; open(fpath,'wb').write(cp.getvalue()); cabs.append({"id":len(cabs)+1,"year":cy.strip(),"name":cn.strip(),"members":cm.strip(),"photo_path":fpath,"by":user_full,"date":str(datetime.datetime.now())[:10]}); save_json(FILES["cabinets"],cabs); st.success("Saved for years! NOW ALL 13 CAN SEE!"); st.rerun()
    for cab in reversed(cabs):
        with st.container(border=True):
            st.markdown(f"**{cab['name']} - {cab['year']}** - Posted by {cab['by']} - Visible to ALL 13!")
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'],use_container_width=True)
            st.info(cab['members'])
