import streamlit as st, os, json, pandas as pd, time
from datetime import datetime as dt, timedelta
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

os.makedirs("data/media_files", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)
os.makedirs("data/personal", exist_ok=True)

MAKER = "speaker"
LOCK_MSG = "LOCKED - Only The Maker, Right Hon. Speaker Hon. Lawrence Ssango, Can Make Changes / Delete / Change Settings. You Can Upload, Download, Vote, Join Calls, Submit Reports, Type And Copy Paste."
DEFAULT_MEET_LINK = "https://meet.google.com/abc-defg-hij"

FILES = {"reports":"data/reports.json","media":"data/media.json","candidates":"data/candidates.json","pending":"data/pending.json","votes":"data/votes.json","cabinets":"data/cabinets.json","docs":"data/docs.json","finance":"data/finance.json","disc":"data/disc.json","gp":"data/gp.json","passwords":"data/passwords.json","uploaded":"data/uploaded_docs.json","ann":"data/announcements.json","meet":"data/meetings.json","personal":"data/personal.json","audit":"data/audit.json","notif":"data/notifications.json","meetlink":"data/meet_link.json"}

def load_json(p,d):
    if os.path.exists(p):
        try:
            with open(p,'r') as f: return json.load(f)
        except: return d
    return d
def save_json(p,data):
    with open(p,'w') as f: json.dump(data,f,default=str,indent=2)
def get_meet_link():
    d=load_json(FILES["meetlink"],{})
    link=d.get("link","") if isinstance(d,dict) else ""
    return link.strip() if link else DEFAULT_MEET_LINK
def add_notify(title,body,sender="System"):
    try:
        nlist=load_json(FILES["notif"],[])
        nlist.append({"id":len(nlist)+1,"title":title,"body":body,"from":sender,"date":dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["notif"],nlist); st.session_state.notif=nlist
    except: pass
    st.toast(f"🔔 {title}: {body}",icon="🔔")

KEEP_OPTIONS={"7 Days - then disappears from portal":7,"30 Days":30,"90 Days":90,"1 Year - 365 Days":365,"Forever on Portal":36500}
def keep_days(label):
    return KEEP_OPTIONS.get(label,30)
def expiry_str(days):
    return (dt.now()+timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
def is_expired(item):
    try:
        exp=item.get("expires","")
        if not exp: return False
        return dt.now() > dt.strptime(exp,"%Y-%m-%d %H:%M")
    except: return False
def days_left(item):
    try:
        exp=dt.strptime(item.get("expires",""),"%Y-%m-%d %H:%M")
        return max(0,(exp-dt.now()).days)
    except: return 9999

# HEADER WITH YOUR 2 GROUP ICONS - LEFT UNASNM, RIGHT UNIVERSITY OF KISUBI, WAY THEY ARE
def show_header(subtitle="Friendly, colourful, easy. Tap green, join Meet."):
    c_left, c_mid, c_right = st.columns([1,3,1])
    with c_left:
        if os.path.exists("unasnm.jpg"): st.image("unasnm.jpg", width=110)
        elif os.path.exists("unasnm.png"): st.image("unasnm.png", width=110)
        elif os.path.exists("unasnm.jpeg"): st.image("unasnm.jpeg", width=110)
        else: st.image("https://via.placeholder.com/110", width=110)
    with c_mid:
        st.markdown("<h2 style='text-align:center;color:#0B3D1E;'>UNIK BEC UNASNM<br>Governance Portal</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#000000;'>{subtitle}</p>", unsafe_allow_html=True)
    with c_right:
        if os.path.exists("university.jpg"): st.image("university.jpg", width=110)
        elif os.path.exists("university.png"): st.image("university.png", width=110)
        elif os.path.exists("university.jpeg"): st.image("university.jpeg", width=110)
        else: st.image("https://via.placeholder.com/110", width=110)

MEET_LINK=get_meet_link()
is_public=st.query_params.get("public","")=="vote"
USERS={"principal":"Principal - School Head","patron":"Hon. Patron","president":"His Excellency President","vice_president":"Hon. Vice President","speaker":"Right Hon. Speaker - Hon. Lawrence Ssango","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys()); SUPER_4=["principal","patron","president","speaker"]; FINANCE_5=["principal","patron","president","speaker","finance"]
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

# CLEAR COLOURS FOR WEAK EYES - DARK TEXT ON LIGHT, WHITE TEXT ONLY ON DARK GREEN
st.markdown("""
<style>
.stApp{background-color:#FFF8E1 !important; color:#000000 !important;}
.stApp p, .stApp div, .stApp label, .stApp span{color:#000000 !important; font-size:18px !important; font-weight:600 !important;}
h1,h2,h3{color:#0B3D1E !important; font-weight:900 !important;}
input, textarea, select{color:#000000 !important; background-color:#FFFFFF !important; font-size:18px !important; font-weight:700 !important; border:2px solid #0B3D1E !important;}
div[data-testid="stSidebar"]{background-color:#075E54 !important;}
div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] div, div[data-testid="stSidebar"] label, div[data-testid="stSidebar"] span, div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h2, div[data-testid="stSidebar"] h3{color:#FFFFFF !important; font-size:18px !important; font-weight:700 !important;}
div[data-testid="stSidebar"] input{color:#000000 !important; background-color:#FFFFFF !important;}
div[data-testid="stSidebar"] a{color:#FFFF00 !important; font-weight:900 !important;}
button[kind="primary"]{background-color:#075E54 !important; color:#FFFFFF !important; border-radius:20px !important; font-size:18px !important; font-weight:900 !important;}
button[kind="primary"] p, button[kind="primary"] span{color:#FFFFFF !important;}
button[kind="secondary"]{background-color:#FFFFFF !important; color:#000000 !important; border:2px solid #075E54 !important; font-size:18px !important; font-weight:900 !important;}
button[kind="secondary"] p, button[kind="secondary"] span{color:#000000 !important;}
div[data-testid="stAlert"]{color:#000000 !important;}
div[data-testid="stAlert"] p{color:#000000 !important; font-size:18px !important; font-weight:700 !important;}
</style>
""",unsafe_allow_html=True)

def show_any_file(fp,fname):
    if not fp or not os.path.exists(fp): return
    low=fp.lower()
    try:
        if low.endswith(('.jpg','.jpeg','.png','.gif','.webp','.bmp')): st.image(fp,use_container_width=True)
        elif low.endswith(('.mp4','.mov','.mpeg','.mpg','.avi','.mkv','.webm')): st.video(fp)
        elif low.endswith(('.mp3','.m4a','.wav','.ogg','.opus','.aac','.flac')): st.audio(fp)
        elif low.endswith(('.pdf',)): st.write(f"PDF file: {fname} - tap Download to Phone below")
        else: st.write(f"File: {fname} - tap Download to Phone below, any file works")
    except: st.write(f"File: {fname}")

def download_and_keep(fp,fname,key):
    if fp and os.path.exists(fp):
        st.download_button("DOWNLOAD TO PHONE / LAPTOP - Keep Forever In Your Files",open(fp,'rb').read(),file_name=fname,key=key,type="primary",use_container_width=True)
        st.write("After you download, it stays in your phone Downloads / Files even if it later disappears from this portal.")

def retention_badge(item):
    if item.get("expires"):
        if is_expired(item): return "EXPIRED - Download quickly, Maker can Renew"
        d=days_left(item)
        return f"Keeps on portal: {d} days left | Expires: {item['expires']} | Download to phone to keep forever"
    return "Keeps: Forever"

if is_public:
    show_header("One Email = One Vote")
    st.markdown("<h3 style='text-align:center;color:#0B3D1E;'>PUBLIC ELECTORAL COMMISSION</h3>",unsafe_allow_html=True)
    t1,t2,t3=st.tabs(["Apply Candidate","Vote One Email Once","Live Results"])
    with t1:
        rp=st.selectbox("Position",ELECTION_POS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names *",key="pub_name"); rclass=st.text_input("Class *",key="pub_class")
        remail=st.text_input("Email *",key="pub_email"); rreason=st.text_area("Why vote you? *",key="pub_reason")
        rphoto=st.file_uploader("Passport Photo * JPG/PNG",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit (Speaker Approves)",type="primary",use_container_width=True):
            if not rn or not rphoto: st.error("Full Names + Photo required")
            else:
                nid=int(time.time()); fpath=f"data/media_files/cand_{nid}.jpg"; open(fpath,'wb').write(rphoto.getvalue())
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
                        if c.get('photo_path','') and os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path',''),width=140,caption=c['name'])
                        st.write(f"{c['name']} - {c.get('class','')}"); st.info(c.get('reason',''))
                        if st.button(f"VOTE {c['name']}",key=f"pv_{c['id']}_{voter_email}",type="primary",use_container_width=True):
                            st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email.lower(),"position":vp,"candidate_name":c['name'],"date":str(dt.now())})
                            save_json(FILES["votes"],st.session_state.votes); st.success(f"Voted {c['name']}!"); st.balloons(); st.rerun()
        else: st.warning("Enter valid university email to vote")
    with t3:
        votes=load_json(FILES["votes"],st.session_state.votes); st.success(f"Total Votes: {len(votes)}")
        for pos in ELECTION_POS:
            for cc in [c for c in st.session_state.candidates if c['position']==pos]:
                st.write(f"{cc['name']} - {USERS[pos]} - {len([v for v in votes if v['candidate_id']==cc['id']])} votes")
    st.stop()

if not st.session_state.logged_in:
    show_header("Welcome, Family! Governance Portal")
    st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#075E54;color:#FFFFFF;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:22px;display:block;text-align:center;'>JOIN GOOGLE MEET NOW - TAP HERE</a>", unsafe_allow_html=True)
    st.info(f"MEET LINK: {MEET_LINK}")
    PUBLIC_VOTE_LINK="https://unik-bec-system-edudyqeshonywrcnjthl8l.streamlit.app/?public=vote"
    st.markdown(f"### PUBLIC VOTE FOR ALL STUDENTS\nLink: {PUBLIC_VOTE_LINK}")
    u=st.selectbox("Select Office (13)",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password - My Portal",type="password",key="pass")
    if st.button("LOGIN TO PORTAL",type="primary",use_container_width=True):
        if p==st.session_state.passwords.get(u,"unik2025"): st.session_state.logged_in=True; st.session_state.user=u; st.rerun()
        else: st.error("Wrong password! Default unik2025")
    st.stop()

user=st.session_state.user; user_full=USERS[user]; CAN_CHANGE=(user==MAKER)
reports=load_json(FILES["reports"],st.session_state.reports); media=load_json(FILES["media"],st.session_state.media); docs_uploaded=load_json(FILES["uploaded"],st.session_state.uploaded); votes=load_json(FILES["votes"],st.session_state.votes)
notifs_now=load_json(FILES["notif"],[])

with st.sidebar:
    st.markdown("### UNIK BEC - Chats")
    st.markdown(f"Hello, {user_full}")
    if CAN_CHANGE: st.success("MAKER MODE - Hon. Lawrence Ssango")
    else: st.success("YOU CAN: Upload ANY FILE, Download to Phone, Vote, Join, Submit")
    st.markdown(f"[JOIN GOOGLE MEET]({MEET_LINK})")
    search=st.text_input("Search departments",key="wa_search",placeholder="Search...")
    st.markdown("All | Unread | Favourites | Groups  Notifications: "+str(len(notifs_now))+"  13 Online")
    st.markdown("STATUS - All 13 Online Now")
    for _u in LOGIN_USERS: st.markdown(f"Online: {USERS[_u]}")
    st.markdown("---")
    PAGES=["Dashboard","My Personal Portal","Public Portal OPEN","Meeting - GOOGLE MEET DIRECT","Submit Report","Private SUPER 4","Electoral OPEN","Disciplinary OPEN","GP OPEN","Finance 5 ONLY","Secret OPEN","Documents OPEN","Media Gallery OPEN - ANY FILE","Cabinet Archive OPEN","Audit Log"]
    if search: PAGES=[p for p in PAGES if search.lower() in p.lower()] or PAGES
    page=st.radio("Departments",PAGES,key="wa_page",label_visibility="collapsed")
    st.markdown("---")
    st.markdown("YOUR PHONE SPACE")
    st.markdown("Download any file, it stays in your phone / laptop Files forever, even after portal time ends.")
    for _n in reversed(notifs_now[-5:]): st.info(f"{_n['title']} - {_n['body'][:60]}")
    if CAN_CHANGE:
        with st.expander("Change My Password - Maker Only"):
            cur=st.text_input("Current",type="password",key="cur_pw"); new=st.text_input("New",type="password",key="new_pw"); conf=st.text_input("Confirm",type="password",key="conf_pw")
            if st.button("Save My Portal",key="save_pw"):
                if cur!=st.session_state.passwords.get(user,"unik2025"): st.error("Wrong current")
                elif new!=conf: st.error("Don't match")
                else: st.session_state.passwords[user]=new; save_json(FILES["passwords"],st.session_state.passwords); st.success("Changed!")
    if st.button("Logout",use_container_width=True): st.session_state.logged_in=False; st.session_state.user=""; st.rerun()

show_header("Organised like WhatsApp. Colourful. Easy. Clear to see.")
st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#075E54;color:#FFFFFF;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:22px;display:block;text-align:center;'>JOIN GOOGLE MEET NOW - TAP HERE</a>", unsafe_allow_html=True)
st.success("ALL 13 CAN: Upload ANY FILE, Download to Phone / Laptop, Vote, Join Meet, Submit. ONLY MAKER CAN: Delete, Renew, Approve, Change Settings.")
st.warning("PHONE SPACE: Portal cannot write straight into your phone. Tap DOWNLOAD TO PHONE, it saves in your phone Downloads / Files and stays forever. Portal copy can expire after 7 days / 30 days / 1 year, your phone copy does not expire.")
st.markdown(f"### {page}  |  13 departments  |  Online now")
st.divider()

if page.startswith("Dashboard"):
    st.subheader("Dashboard"); c1,c2,c3,c4=st.columns(4)
    c1.metric("Reports",len(reports)); c2.metric("Media",len(media)); c3.metric("Docs",len(docs_uploaded)); c4.metric("Votes",len(votes))
    st.info("Tip: Go to Media Gallery, download the Anthem to your phone, then it is yours forever.")
    for _n in reversed(load_json(FILES["notif"],[])[-10:]): st.info(f"{_n['title']} - {_n['body']}")

elif page.startswith("Media"):
    st.subheader("Media Gallery - ANY FILE - MPEG, MP4, MP3, JPG, PDF, ZIP")
    st.info("Upload here, choose how long to keep on portal. Download to phone = keep forever in your phone.")
    med=load_json(FILES["media"],st.session_state.media)
    mt=st.text_input("Media Title *",key="media_t")
    keep_label=st.selectbox("Keep on portal for:",list(KEEP_OPTIONS.keys()),key="media_keep")
    mf=st.file_uploader("File * - ANY FILE TYPE",key="media_f")
    if st.button("Upload - ALL 13 SEE SAME GALLERY!",type="primary",use_container_width=True,key="media_s"):
        if not mt.strip() or not mf: st.error("Title + File required")
        else:
            nid=int(time.time()); fpath=f"data/media_files/media_{nid}_{mf.name.replace(' ','_')}"; open(fpath,'wb').write(mf.getvalue())
            med.append({"id":nid,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"keep":keep_label,"expires":expiry_str(keep_days(keep_label))}); save_json(FILES["media"],med); st.success("Saved! Now download it to your phone to keep forever!"); st.balloons(); st.rerun()
    q=st.text_input("Search media by name",key="media_q")
    show_expired=st.checkbox("Show expired files too (so Maker can Renew)",key="media_exp")
    cols=st.columns(3)
    shown=[m for m in reversed(med) if (not q or q.lower() in m['title'].lower()+m.get('file_name','').lower())]
    for idx,m in enumerate(shown):
        if is_expired(m) and not show_expired and not CAN_CHANGE: continue
        with cols[idx%3]:
            with st.container(border=True):
                st.write(f"{m['title']} - {m['by']}")
                st.write(retention_badge(m))
                fp=m.get('file_path','')
                if fp and os.path.exists(fp):
                    show_any_file(fp,m.get('file_name',''))
                    download_and_keep(fp,m.get('file_name',''),key=f"dl_med_{m['id']}_{idx}")
                if CAN_CHANGE:
                    c1,c2=st.columns(2)
                    if c1.button("Renew +30 Days",key=f"ren_med_{m['id']}_{idx}"):
                        for x in med:
                            if x['id']==m['id']: x['expires']=(dt.now()+timedelta(days=30)).strftime("%Y-%m-%d %H:%M"); x['keep']="Renewed +30 Days"
                        save_json(FILES["media"],med); st.success("Renewed! Keeps 30 more days."); st.rerun()
                    if c2.button("Delete Forever",key=f"del_med_{m['id']}_{idx}"):
                        med=[x for x in med if x['id']!=m['id']]
                        try:
                            if fp and os.path.exists(fp): os.remove(fp)
                        except: pass
                        save_json(FILES["media"],med); st.success("Deleted Forever from portal. Phone copies stay."); st.rerun()

elif page.startswith("Documents"):
    st.subheader("Documents - ANY FILE + Keep Time")
    docs=load_json(FILES["uploaded"],st.session_state.uploaded)
    dcat=st.selectbox("Category",DOC_CATS,key="doc_cat"); dtit=st.text_input("Title *",key="doc_t"); dd=st.text_area("Description",key="doc_d")
    keep2=st.selectbox("Keep on portal for:",list(KEEP_OPTIONS.keys()),key="doc_keep")
    df=st.file_uploader("Upload File * - ANY FILE",key="doc_f")
    if st.button("Upload Document - ALL 13 SEE SAME!",type="primary",use_container_width=True,key="doc_s"):
        if not dtit.strip() or not df: st.error("Title + File required")
        else:
            safe=df.name.replace(" ","_"); fpath=f"data/documents/doc_{int(time.time())}_{safe}"; open(fpath,'wb').write(df.getvalue())
            docs.append({"id":int(time.time()),"category":dcat,"title":dtit.strip(),"description":dd.strip(),"file_name":df.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"keep":keep2,"expires":expiry_str(keep_days(keep2))}); save_json(FILES["uploaded"],docs); st.success("Uploaded! Download to phone to keep forever."); st.balloons(); st.rerun()
    for idx,doc in enumerate(reversed(docs)):
        with st.container(border=True):
            st.markdown(f"{doc['title']} | {doc['category']} | by {doc['by']}"); st.write(retention_badge(doc))
            if doc.get('file_path',''):
                show_any_file(doc['file_path'],doc.get('file_name',''))
                download_and_keep(doc['file_path'],doc.get('file_name',''),key=f"dl_doc_{doc['id']}_{idx}")
            if CAN_CHANGE:
                if st.button(f"Renew +30 Days - {doc['title']}",key=f"ren_doc_{doc['id']}_{idx}"):
                    for x in docs:
                        if x['id']==doc['id']: x['expires']=(dt.now()+timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
                    save_json(FILES["uploaded"],docs); st.success("Renewed!"); st.rerun()
                if st.button(f"Delete Forever - {doc['title']} - Maker Only",key=f"del_doc_{doc['id']}_{idx}"): docs=[x for x in docs if x['id']!=doc['id']]; save_json(FILES["uploaded"],docs); st.success("Deleted!"); st.rerun()

elif page.startswith("Public"):
    st.subheader("Public Portal - WhatsApp Group Chat")
    anns=load_json(FILES["ann"],st.session_state.ann)
    at=st.text_input("Title *",key="ann_t"); acont=st.text_area("Message *",key="ann_c"); af=st.file_uploader("Attach File - ANY FILE",key="ann_f")
    if st.button("BROADCAST TO ALL 13",type="primary",use_container_width=True):
        fpath=""; fname=""
        if af: fname=af.name.replace(" ","_"); fpath=f"data/documents/ann_{int(time.time())}_{fname}"; open(fpath,'wb').write(af.getvalue())
        anns.append({"id":int(time.time()),"title":at.strip(),"content":acont.strip(),"file_name":fname,"file_path":fpath,"from":user,"from_name":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["ann"],anns); add_notify("New Public Message",f"{at.strip()}",user_full); st.success("Broadcasted!"); st.balloons(); st.rerun()
    for idx,ann in enumerate(reversed(anns)):
        with st.container(border=True):
            st.markdown(f"{ann['title']} | {ann['from_name']} | {ann['date']} | Seen by 13"); st.info(ann['content'])
            if ann.get('file_path',''):
                show_any_file(ann['file_path'],ann.get('file_name',''))
                download_and_keep(ann['file_path'],ann.get('file_name',''),key=f"dl_ann_{ann['id']}_{idx}")

elif page.startswith("Meeting"):
    st.subheader("Meeting - GOOGLE MEET DIRECT")
    st.success(f"Current Link: {MEET_LINK}")
    st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#075E54;color:#FFFFFF;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:20px;display:block;text-align:center;'>JOIN GOOGLE MEET NOW</a>", unsafe_allow_html=True)
    st.code(MEET_LINK)
    if CAN_CHANGE:
        new_link=st.text_input("Paste NEW Google Meet Link",value=MEET_LINK,key="new_meet_link")
        if st.button("SAVE LINK - MAKER ONLY",type="primary",use_container_width=True):
            if "meet.google.com" not in new_link: st.error("Not a Meet link!")
            else: save_json(FILES["meetlink"],{"link":new_link.strip(),"by":user_full,"date":str(dt.now())}); st.success("Saved!"); st.rerun()
    else: st.error(LOCK_MSG)

elif page.startswith("My Personal"):
    st.subheader("My Personal Portal - ONLY YOU")
    personal=load_json(FILES["personal"],st.session_state.personal); my_personal=[p for p in personal if p['owner']==user]
    pt=st.text_input("Title *",key="pers_t"); pc=st.text_area("Notes *",key="pers_c"); pf=st.file_uploader("File - ANY FILE",key="pers_f")
    if st.button("Save PRIVATE",type="primary",use_container_width=True,key="pers_s"):
        fpath=""; fname=""
        if pf: fname=pf.name.replace(" ","_"); fpath=f"data/personal/{user}_{int(time.time())}_{fname}"; open(fpath,'wb').write(pf.getvalue())
        personal.append({"id":int(time.time()),"owner":user,"title":pt.strip(),"content":pc.strip(),"file_name":fname,"file_path":fpath,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["personal"],personal); st.success("Saved only for you!"); st.rerun()
    for idx,p in enumerate(reversed(my_personal)):
        with st.container(border=True):
            st.markdown(f"{p['title']} | {p['date']}")
            if p.get('content'): st.info(p['content'])
            if p.get('file_path',''): show_any_file(p['file_path'],p.get('file_name','')); download_and_keep(p['file_path'],p.get('file_name',''),key=f"dl_pers_{p['id']}_{idx}")

elif page.startswith("Submit"):
    st.subheader("Submit Report")
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt"); rtitle=st.text_input("Title *",key="rtitle"); rcontent=st.text_area("Details *",key="rcontent")
    if st.button("Submit Report",type="primary",use_container_width=True):
        reports.append({"id":int(time.time()),"date":dt.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip()}); save_json(FILES["reports"],reports); st.success("Saved!"); st.balloons()

elif page.startswith("Private"):
    st.subheader("Private SUPER 4 ONLY")
    if user in SUPER_4:
        for r in reversed(load_json(FILES["reports"],st.session_state.reports)):
            with st.expander(f"{r['title']} - {r['from_name']}"): st.info(r['content'])
    else: st.error("SUPER 4 ONLY")

elif page.startswith("Electoral"):
    st.subheader("Electoral OPEN")
    pend=load_json(FILES["pending"],st.session_state.pending); cand=load_json(FILES["candidates"],st.session_state.candidates)
    st.write(f"Total Votes: {len(votes)} | Public link: https://unik-bec-system-edudyqeshonywrcnjthl8l.streamlit.app/?public=vote")
    for pc in reversed(pend):
        with st.container(border=True):
            st.write(f"{pc['name']} - {USERS[pc['position']]}"); st.info(pc.get('reason',''))
            if CAN_CHANGE and st.button(f"Approve {pc['name']}",key=f"ap_{pc['id']}"):
                st.session_state.candidates.append(pc); st.session_state.pending=[x for x in st.session_state.pending if x['id']!=pc['id']]; save_json(FILES["candidates"],st.session_state.candidates); save_json(FILES["pending"],st.session_state.pending); st.success("Approved!"); st.rerun()
    for cc in cand: st.write(f"{cc['name']} - {USERS[cc['position']]} - {len([v for v in votes if v['candidate_id']==cc['id']])} votes")

elif page.startswith("Disciplinary"):
    st.subheader("Disciplinary"); disc=load_json(FILES["disc"],st.session_state.disc)
    d_t=st.text_input("Case Title *",key="disc_t"); d_c=st.text_area("Details *",key="disc_c")
    if st.button("Save Disciplinary",type="primary",key="disc_s"): disc.append({"id":int(time.time()),"title":d_t.strip(),"content":d_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["disc"],disc); st.success("Saved!"); st.rerun()
    for dr in reversed(disc): st.info(f"{dr['title']} - {dr['by']} - {dr['content']}")

elif page.startswith("GP"):
    st.subheader("GP"); gp=load_json(FILES["gp"],st.session_state.gp)
    gp_t=st.text_input("GP Title *",key="gp_t"); gp_c=st.text_area("GP Details *",key="gp_c")
    if st.button("Save GP",type="primary",key="gp_s"): gp.append({"id":int(time.time()),"title":gp_t.strip(),"content":gp_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["gp"],gp); st.success("Saved!"); st.rerun()
    for gpr in reversed(gp): st.info(f"{gpr['title']} - {gpr['by']} - {gpr['content']}")

elif page.startswith("Finance"):
    st.subheader("Finance - 5 ONLY")
    if user in FINANCE_5:
        fin=load_json(FILES["finance"],st.session_state.finance)
        f_t=st.text_input("Finance Title *",key="fin_t"); f_d=st.text_area("Description",key="fin_d"); f_f=st.file_uploader("Upload ANY FILE",key="fin_f"); f_amount=st.number_input("Amount UGX",min_value=0,step=1000,key="fin_amount")
        if st.button("Save Finance",type="primary",key="fin_s2"):
            fname=""; fpath=""
            if f_f: fname=f_f.name.replace(" ","_"); fpath=f"data/documents/finance_{int(time.time())}_{fname}"; open(fpath,'wb').write(f_f.getvalue())
            fin.append({"id":int(time.time()),"title":f_t.strip(),"description":f_d.strip(),"amount":f_amount,"file_name":fname,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["finance"],fin); st.success("Saved!"); st.rerun()
        for idx,fd in enumerate(reversed(fin)):
            with st.container(border=True):
                st.markdown(f"{fd['title']} - UGX {fd.get('amount',0):,}")
                if fd.get('file_path',''): show_any_file(fd['file_path'],fd.get('file_name','')); download_and_keep(fd['file_path'],fd.get('file_name',''),key=f"dl_fin_{fd['id']}_{idx}")
    else: st.error("Finance is 5 ONLY")

elif page.startswith("Secret"):
    st.subheader("Secret"); sec=load_json(FILES["docs"],st.session_state.docs)
    dc=st.selectbox("Category",DOC_CATS,key="sec_cat"); dt_=st.text_input("Title *",key="sec_t"); dd=st.text_area("Description",key="sec_d")
    if st.button("Save Secret",type="primary",key="sec_s"): sec.append({"id":int(time.time()),"category":dc,"title":dt_.strip(),"description":dd.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d")}); save_json(FILES["docs"],sec); st.success("Saved!"); st.rerun()
    for d in reversed(sec): st.write(f"{d['category']} | {d['title']} - {d['description']}")

elif page.startswith("Cabinet"):
    st.subheader("Cabinet Archive"); cabs=load_json(FILES["cabinets"],st.session_state.cabinets)
    cy=st.text_input("Year *",key="cab_y"); cn=st.text_input("Cabinet Name *",key="cab_n"); cm=st.text_area("Members List *",key="cab_m"); cp=st.file_uploader("Group Photo - ANY FILE",key="cab_p")
    if st.button("Save Cabinet",type="primary",use_container_width=True,key="cab_s"):
        if not cy or not cn or not cm or not cp: st.error("All required")
        else: fpath=f"data/media_files/cab_{int(time.time())}.jpg"; open(fpath,'wb').write(cp.getvalue()); cabs.append({"id":int(time.time()),"year":cy.strip(),"name":cn.strip(),"members":cm.strip(),"photo_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d")}); save_json(FILES["cabinets"],cabs); st.success("Saved!"); st.rerun()
    for cab in reversed(cabs):
        with st.container(border=True):
            st.markdown(f"{cab['name']} - {cab['year']}"); show_any_file(cab['photo_path'],cab['name']); st.info(cab['members'])

elif page.startswith("Audit"):
    st.subheader("Audit Log"); audit=load_json(FILES["audit"],st.session_state.audit)
    if audit: st.dataframe(pd.DataFrame(reversed(audit)),use_container_width=True)

st.markdown("---"); st.markdown(f"<p style='text-align:center;color:#000000;'>UNIK BEC UNASNM | Friendly and Clear to See | Only Maker Can Delete / Renew | All Rights Reserved To The Maker, Right Hon. Speaker Hon. Lawrence Ssango | {dt.now().year}</p>",unsafe_allow_html=True)
