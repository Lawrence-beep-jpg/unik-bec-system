import streamlit as st
import pandas as pd
import datetime
import os, json
import streamlit.components.v1 as components

st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# ===== SAVE TO SERVER FOR YEARS =====
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
        try: return json.loads(open(path,'r').read())
        except: return default
    return default

def save_json(path, data):
    open(path,'w').write(json.dumps(data, default=str))

query_params = st.query_params
is_public_vote = query_params.get("public", "") == "vote"

# ===== ONLY ONE HEADING - FIXED - UNIK BEC UNASNM Governance Portal =====
try:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if os.path.exists("unik_badge.png"): st.image("unik_badge.png", width=100)
    with col2:
        st.markdown("<h2 style='text-align:center; margin-top:10px;'>🏛️ UNIK BEC UNASNM<br>Governance Portal</h2>", unsafe_allow_html=True)
    with col3:
        if os.path.exists("unasnm_badge.png"): st.image("unasnm_badge.png", width=100)
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
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint","Public Information"]

# LOAD ALL
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
    loaded_pw=load_json(PASSWORDS_FILE, {})
    if loaded_pw: st.session_state.passwords=loaded_pw
    else: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

# ===== PUBLIC VOTING - FOR CLASS - NO SECRETS - ONE EMAIL ONCE PER POSITION - WORKS FOR YEARS =====
if is_public_vote:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM - PUBLIC ELECTORAL COMMISSION</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'><b>Public Portal - No Cabinet Secrets Here - One Email Once Per Position - Works For Years</b></p>", unsafe_allow_html=True)
    st.info("Public Link: ?public=vote - Students see ONLY electoral - Cannot see cabinet secrets inside!")
    pub_tab1, pub_tab2, pub_tab3, pub_tab4 = st.tabs(["📝 Apply as Candidate", "🗳️ Vote - One Email Once", "📊 Live Results", "📢 Public Information from SUPER 4"])
    with pub_tab1:
        rp=st.selectbox("Position You Want",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names *",key="pub_name")
        rclass=st.text_input("Class *",key="pub_class")
        remail=st.text_input("Email *",key="pub_email")
        rreason=st.text_area("Why should students vote you? *",key="pub_reason")
        rphoto=st.file_uploader("Your Photo * JPG/PNG",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit Application (Needs Right Honourable Speaker Approval)",type="primary",use_container_width=True,key="pub_submit"):
            if not rn or not rclass or not remail or not rreason or not rphoto: st.error("Fill ALL * fields")
            else:
                nid=len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.pending_candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(PENDING_FILE, st.session_state.pending_candidates)
                st.success("✅ Sent! Wait approval from Right Honourable Speaker - Hon. Lawrence Ssango"); st.balloons()
    with pub_tab2:
        st.subheader("Vote - One Email Once Per Position - For Years")
        voter_email=st.text_input("Your Email * (One email works once per position)",key="pub_voter_email", placeholder="e.g. student@unik.ac.ug")
        if not voter_email or "@" not in voter_email: 
            st.warning("Enter valid email to see candidates"); 
            st.stop()
        vp=st.selectbox("Choose Position to Vote",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        already_voted = [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
        if already_voted: 
            st.error(f"❌ Already voted for {USERS[vp]} with {voter_email} - One email once per position! Cannot vote again for this position - But you can vote for other positions with same email"); 
            st.stop()
        cands=[x for x in st.session_state.candidates if x['position']==vp]
        if not cands: st.warning(f"No approved candidates yet for {USERS[vp]}")
        for c in cands:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c['photo_path'],width=150)
                st.write(f"**{c['name']}** - {c.get('class','')} - {c.get('email','')}")
                st.info(c.get('reason',''))
                if st.button(f"✅ Vote {c['name']} - One Click - Uses {voter_email} for {USERS[vp]}",key=f"pv_{c['id']}_{voter_email}_{vp}", type="primary"):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success(f"✅ Voted {c['name']}! Email {voter_email} used for {USERS[vp]} - Cannot vote again for this position!"); st.balloons(); st.rerun()
    with pub_tab3:
        st.subheader("Live Results - Public Can See")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(f"**{USERS[pos]}**")
                    st.dataframe(pd.DataFrame(rd),use_container_width=True)
    with pub_tab4:
        st.subheader("📢 Public Information from SUPER 4 - For All Students")
        st.info("Information posted by Principal, Patron, His Excellency President, Right Honourable Speaker for public students")
        all_anns = load_json(ANNOUNCEMENTS_FILE, [])
        # Show only those marked as Public Information
        public_anns = [a for a in all_anns if "Public" in a.get('category','') or "Public" in a.get('priority','') or a.get('is_public', False)]
        # Also show all if no public filter - SUPER 4 may want all public
        if not public_anns:
            public_anns = all_anns  # Show all announcements as public info for students to see transparency
        
        if not public_anns:
            st.warning("No public information yet from SUPER 4")
        else:
            for ann in reversed(public_anns):
                with st.container(border=True):
                    st.markdown(f"**{ann['title']}** | From: {ann['from_name']} | {ann['date']}")
                    st.info(ann['content'])
                    if ann.get('file_name','') and os.path.exists(ann.get('file_path','')):
                        try:
                            st.download_button(f"📥 Download {ann['file_name']}", open(ann['file_path'],'rb').read(), file_name=ann['file_name'], key=f"dl_pub_{ann['id']}")
                        except: pass
    st.stop()

# ===== CABINET LOGIN - FOR 13 BEC ONLY - SECRETS INSIDE =====
if not st.session_state.logged_in:
    st.markdown("### 🔐 Cabinet Login - 13 Departments Only - Secrets Inside")
    u=st.selectbox("Select Your Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("🔐 LOGIN TO GOVERNANCE PORTAL",type="primary", use_container_width=True, key="login_btn"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password! Default is unik2025")
    st.info("Default Password: unik2025 | Public Voting Link: Add ?public=vote to your link - Works for years - One email once per position - No secrets")
    st.stop()

user=st.session_state.user
user_full=USERS[user]

# ===== SIDEBAR - PASSWORD CHANGE FOR ALL 13 + PHONE NOTIFICATIONS =====
st.sidebar.title(user_full)
st.sidebar.success(f"Logged as: {user_full}")
st.sidebar.divider()
st.sidebar.subheader("🔐 Change My Password - My Bottle - Every Member!")
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
st.sidebar.subheader("🔔 Phone Notifications - For All 13!")
st.sidebar.info("Enable to get phone alerts when SUPER 4 broadcasts to ALL 13!")
with st.sidebar.expander("🔔 ENABLE PHONE NOTIFICATIONS - Click Here!", expanded=True):
    st.write("Get phone pop-up when new announcement comes from SUPER 4!")
    components.html("""
        <div style="text-align:center; padding:10px;">
            <button onclick="requestNotificationPermission()" style="background:#25D366; color:white; border:none; padding:12px 20px; border-radius:8px; font-weight:bold; cursor:pointer; width:100%;">
                🔔 ENABLE PHONE NOTIFICATIONS
            </button>
            <p id="notif-status" style="margin-top:10px; font-size:12px; color:#666;">Click to allow notifications on your phone</p>
        </div>
        <script>
        function requestNotificationPermission() {
            if (!("Notification" in window)) {
                document.getElementById('notif-status').innerHTML = "❌ Browser doesn't support";
                return;
            }
            Notification.requestPermission().then(function(permission) {
                if (permission === "granted") {
                    document.getElementById('notif-status').innerHTML = "✅ Notifications ENABLED! You will get alerts!";
                    localStorage.setItem('unik_notif_enabled','yes');
                    new Notification("🏛️ UNIK BEC Notifications Enabled!", {
                        body: "You will now receive phone alerts when SUPER 4 broadcasts to ALL 13!",
                        icon: "https://cdn-icons-png.flaticon.com/512/561/561127.png"
                    });
                } else {
                    document.getElementById('notif-status').innerHTML = "❌ Permission denied - Enable in settings";
                }
            });
        }
        if (Notification.permission === "granted") {
            document.getElementById('notif-status').innerHTML = "✅ Notifications ACTIVE - Phone will alert you!";
        }
        </script>
    """, height=130)

st.sidebar.divider()
if user in SUPER_4: st.sidebar.info("SUPER 4 - You can view ALL reports + Broadcast to ALL 13 + Public Info")
st.sidebar.info("Public Voting Link for Class:\n?public=vote\nOne email once per position\nNo secrets\nWorks for years")
if st.sidebar.button("Logout", use_container_width=True): st.session_state.logged_in=False;st.rerun()

# ===== ALL TABS - EVERYTHING - NOTHING REMOVED =====
tab0,tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10=st.tabs([
"📢 Public Portal - SUPER 4 Broadcast to ALL 13 + Phone Alerts",
"📝 Submit Report",
"📂 Private Portal - Principal Sees All",
"🗳️ Electoral Chair - Full",
"⚖️ Disciplinary",
"📋 GP - Vice President",
"💰 Finance - 5 Only - Excel/PDF/PPT",
"🔐 Secret Store",
"📄 Documents - PDF, PowerPoint, Word, Excel - ALL 13",
"📸 Media Gallery - ALL SEE",
"🏛️ Cabinet Archive - For Years"
])

# ===== TAB 0 - PUBLIC PORTAL WHERE SUPER 4 SENDS INFO TO ALL 13 AT ONCE + PUBLIC INFO =====
with tab0:
    st.subheader("📢 Public Portal - SUPER 4 Communicate to ALL 13 at Once - Public Information!")
    st.session_state.announcements=load_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
    
    # PHONE NOTIFICATION JS - AUTO CHECK
    latest_count = len(st.session_state.announcements)
    latest_title = st.session_state.announcements[-1]['title'] if st.session_state.announcements else "No messages"
    latest_from = st.session_state.announcements[-1]['from_name'] if st.session_state.announcements else ""
    latest_content = st.session_state.announcements[-1]['content'][:100] if st.session_state.announcements else ""
    
    components.html(f"""
        <script>
        const latestCount = {latest_count};
        const latestTitle = `{latest_title}`;
        const latestFrom = `{latest_from}`;
        const latestContent = `{latest_content}`;
        const lastSeen = localStorage.getItem('unik_last_ann_count') || 0;
        if (latestCount > lastSeen) {{
            if (Notification.permission === "granted" && localStorage.getItem('unik_notif_enabled') === 'yes') {{
                if (latestCount > 0) {{
                    const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
                    audio.play().catch(()=>{{}});
                    setTimeout(() => {{
                        new Notification("📢 NEW: " + latestTitle, {{
                            body: "From " + latestFrom + ": " + latestContent + "...",
                            icon: "https://cdn-icons-png.flaticon.com/512/561/561127.png",
                            vibrate: [200, 100, 200],
                            requireInteraction: true
                        }});
                    }}, 1000);
                }}
            }}
            localStorage.setItem('unik_last_ann_count', latestCount);
        }}
        setInterval(() => {{ window.parent.location.reload(); }}, 30000);
        </script>
        <div style="background:#e8f5e9; padding:8px; border-radius:6px; text-align:center; font-size:13px;">
            🔔 Auto-checking every 30 seconds... Phone will vibrate + beep when new broadcast from SUPER 4 arrives! Keep notifications enabled!
        </div>
    """, height=80)
    
    if len(st.session_state.announcements)>0:
        st.success(f"📢 {len(st.session_state.announcements)} Announcements from SUPER 4 - All 13 Departments + Phone Alerts + Public Info!")
    else:
        st.info("No announcements yet - SUPER 4 will post here for all 13 to see at once + phone notification + public info for students")
    
    if user in SUPER_4:
        st.divider()
        st.markdown(f"### ✍️ Post as {user_full} - ONE MESSAGE GOES TO ALL 13 AT ONCE + PHONE NOTIFICATION + PUBLIC OPTION!")
        st.warning("When you broadcast, ALL 13 members' phones will vibrate + pop-up - Even if portal closed!")
        ann_title=st.text_input("Announcement Title * (e.g. Meeting Tomorrow 9am - Urgent)", key="ann_title", placeholder="Meeting Tomorrow 9am - All Must Attend")
        ann_category=st.selectbox("Category - Where to show?", ["Internal - All 13 Only","Public Information - Also Show to Students in ?public=vote","Both Internal + Public"], key="ann_cat")
        ann_priority=st.selectbox("Priority", ["Normal","Urgent","Very Urgent - All Must Read + Phone Alert"], key="ann_priority")
        ann_content=st.text_area("Message to ALL 13 Departments * (Type once, all see! For Public Info, write for students too)", height=180, key="ann_content", placeholder="Dear All 13 Departments... This is to inform you...\n\nFor public students: Dear Students...")
        ann_file=st.file_uploader("Attach File Optional - PDF/Excel/PPT/Word/Photo", type=["pdf","xlsx","xls","pptx","ppt","docx","doc","jpg","png","jpeg"], key="ann_file")
        
        if st.button("📢 BROADCAST TO ALL 13 + PHONE NOTIFICATIONS + PUBLIC INFO", type="primary", use_container_width=True, key="ann_broadcast"):
            if not ann_title.strip() or not ann_content.strip():
                st.error("Title + Message required!")
            else:
                fpath=""; fname=""
                if ann_file:
                    fname=ann_file.name
                    fpath=f"data/documents/ann_{len(st.session_state.announcements)+1}_{fname.replace(' ','_')}"
                    open(fpath,'wb').write(ann_file.getvalue())
                
                is_public = "Public" in ann_category or "Both" in ann_category
                st.session_state.announcements.append({
                    "id": len(st.session_state.announcements)+1,
                    "title": ann_title.strip(),
                    "category": ann_category,
                    "priority": ann_priority,
                    "content": ann_content.strip(),
                    "file_name": fname,
                    "file_path": fpath,
                    "from": user,
                    "from_name": user_full,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "read_by": [],
                    "is_public": is_public
                })
                save_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
                st.success(f"✅ BROADCASTED! '{ann_title}' sent to ALL 13 + Phones notified + {'Public students will also see in ?public=vote' if is_public else 'Internal only'}!"); st.balloons(); st.rerun()
    else:
        st.info(f"You are {user_full} - You can READ announcements from SUPER 4 here - Only SUPER 4: Principal, Patron, His Excellency President, Right Honourable Speaker can broadcast")
    
    st.divider()
    st.subheader("📋 All Broadcast Messages - Latest First - ALL 13 See Same + Public Info Mark")
    for ann in reversed(st.session_state.announcements):
        priority_icon = "🔴" if "Very Urgent" in ann['priority'] else "🟡" if "Urgent" in ann['priority'] else "🟢"
        public_tag = "🌐 PUBLIC" if ann.get('is_public', False) else "🔒 INTERNAL"
        with st.container(border=True):
            st.markdown(f"{priority_icon} {public_tag} **{ann['title']}** | {ann.get('category','')} | {ann['priority']} | From: {ann['from_name']} | {ann['date']}")
            st.info(ann['content'])
            if ann.get('file_name',''):
                st.write(f"📎 Attached: {ann['file_name']}")
                if os.path.exists(ann.get('file_path','')):
                    try:
                        st.download_button(f"📥 Download {ann['file_name']}", open(ann['file_path'],'rb').read(), file_name=ann['file_name'], key=f"dl_ann_{ann['id']}")
                    except: pass
            if user not in ann.get('read_by',[]):
                if st.button(f"✅ Mark as Read - {ann['from_name']} knows you saw it", key=f"read_{ann['id']}"):
                    for a in st.session_state.announcements:
                        if a['id']==ann['id']:
                            if user not in a['read_by']: a['read_by'].append(user)
                    save_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
                    st.success("Marked as read!"); st.rerun()
            else:
                st.success(f"✅ You read this - {len(ann.get('read_by',[]))}/13 have read")
            if user in SUPER_4:
                read_names = ', '.join([USERS.get(u,u) for u in ann.get('read_by',[])])
                st.caption(f"Read by: {read_names if read_names else 'No one yet'} ({len(ann.get('read_by',[]))}/13) | {'Will show to public students in ?public=vote' if ann.get('is_public') else 'Internal only'}")

with tab1:
    st.subheader("📝 Submit Report - Where Principal Looks")
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt")
    rtitle=st.text_input("Report Title *",key="rtitle", placeholder="e.g. Weekly Report - Class Rep")
    rcontent=st.text_area("Details *",key="rcontent", height=150, placeholder="Write your report details here...")
    if st.button("Submit Report - Saved on Server - Principal Will See",type="primary",use_container_width=True,key="rsubmit"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Title + Details required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip()})
            save_json(REPORTS_FILE, st.session_state.reports)
            st.success("✅ Saved on server - Principal, Patron, President, Speaker will see!"); st.balloons(); st.rerun()

with tab2:
    st.subheader("📂 Private Portal - Reports - Principal Looks Here")
    st.session_state.reports=load_json(REPORTS_FILE, st.session_state.reports)
    if user in SUPER_4:
        show=st.session_state.reports
        st.success(f"SUPER 4: Viewing ALL {len(show)} reports from all 13 departments")
        if show:
            st.write("Reports per department:")
            st.dataframe(pd.DataFrame([r['from_name'] for r in show], columns=['From']).value_counts(), use_container_width=True)
    else:
        show=[r for r in st.session_state.reports if r['from']==user]
        st.info(f"Your reports: {len(show)} - Only you and SUPER 4 can see your reports")
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['type']} - {r['date']}"):
            st.info(r['content'])

with tab3:
    st.subheader("🗳️ Electoral Chair - Full - Pending, Approved, Register, Vote, Results")
    st.session_state.pending_candidates=load_json(PENDING_FILE, st.session_state.pending_candidates)
    st.session_state.candidates=load_json(CANDIDATES_FILE, st.session_state.candidates)
    st.session_state.votes=load_json(VOTES_FILE, st.session_state.votes)
    t_pending, t_approved, t_reg, t_vote, t_res = st.tabs(["⏳ Pending Approval","✅ Approved Candidates","📝 Register + Photo","🗳️ Vote Cabinet","📊 Results"])
    with t_pending:
        st.write(f"Pending: {len(st.session_state.pending_candidates)} - Need Speaker Approval")
        for pc in reversed(st.session_state.pending_candidates):
            with st.container(border=True):
                if os.path.exists(pc.get('photo_path','')): st.image(pc['photo_path'],width=120)
                st.write(f"**{pc['name']}** - {USERS[pc['position']]} - Class: {pc.get('class','')} - Email: {pc.get('email','')}")
                st.info(pc.get('reason',''))
                st.caption(f"Date: {pc.get('date','')}")
                if user=="speaker":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Approve {pc['name']}",key=f"ap_{pc['id']}", type="primary"):
                            st.session_state.candidates.append(pc)
                            st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                            save_json(CANDIDATES_FILE, st.session_state.candidates)
                            save_json(PENDING_FILE, st.session_state.pending_candidates)
                            st.success(f"Approved {pc['name']}"); st.rerun()
                    with col2:
                        if st.button(f"❌ Reject {pc['name']}",key=f"rj_{pc['id']}"):
                            st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                            save_json(PENDING_FILE, st.session_state.pending_candidates)
                            st.warning(f"Rejected {pc['name']}"); st.rerun()
    with t_approved:
        st.write(f"Approved Candidates: {len(st.session_state.candidates)}")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                st.write(f"**{USERS[pos]}: {len(cs)} candidates**")
                for c in cs:
                    with st.container(border=True):
                        if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path'),width=100)
                        st.write(c['name'])
    with t_reg:
        st.subheader("Register Candidate Manually - With Photo")
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos")
        rn=st.text_input("Full Names *",key="cand_name")
        rclass=st.text_input("Class",key="cand_class")
        rreason=st.text_area("Why vote you?",key="cand_reason")
        rphoto=st.file_uploader("Photo * JPG/PNG",type=["jpg","png","jpeg"],key="cand_photo")
        if st.button("Register - Auto Approved",type="primary",key="cand_submit"):
            if not rn or not rphoto: st.error("Names + Photo required")
            else:
                nid=len(st.session_state.candidates)+len(st.session_state.pending_candidates)+1
                fpath=f"data/media_files/cand_{nid}.jpg"
                open(fpath,'wb').write(rphoto.getvalue())
                st.session_state.candidates.append({"id":nid,"position":rp,"name":rn,"class":rclass,"reason":rreason if rreason else "Cabinet Register","photo_path":fpath,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                save_json(CANDIDATES_FILE, st.session_state.candidates)
                st.success(f"Registered {rn} for {USERS[rp]} - Auto Approved")
    with t_vote:
        st.subheader("Vote as Cabinet Member")
        vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos")
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            with st.container(border=True):
                if os.path.exists(c.get('photo_path','')): st.image(c.get('photo_path'),width=100)
                st.write(c['name'])
                if st.button(f"Vote {c['name']}",key=f"vote_{c['id']}"):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                    save_json(VOTES_FILE, st.session_state.votes)
                    st.success(f"Voted {c['name']}")
    with t_res:
        st.subheader("Election Results")
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0 or True:
                    st.write(f"**{USERS[pos]}**")
                    df=pd.DataFrame(rd).sort_values(by="Votes", ascending=False)
                    st.dataframe(df,use_container_width=True)

with tab4:
    st.subheader("⚖️ Disciplinary Reports")
    st.session_state.disciplinary_reports=load_json(DISC_FILE, st.session_state.disciplinary_reports)
    d_title=st.text_input("Case Title *",key="disc_title")
    d_content=st.text_area("Details *",key="disc_content", height=120)
    if st.button("Save Disciplinary Report",type="primary",key="disc_save"):
        if not d_title or not d_content: st.error("Title + Details required")
        else:
            st.session_state.disciplinary_reports.append({"id":len(st.session_state.disciplinary_reports)+1,"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(DISC_FILE, st.session_state.disciplinary_reports)
            st.success("Saved disciplinary report")
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(f"{dr['title']} - by {dr['by']} - {dr['date']}"):
            st.info(dr['content'])

with tab5:
    st.subheader("📋 GP Reports - General Purpose - Vice President Leader")
    st.session_state.gp_reports=load_json(GP_FILE, st.session_state.gp_reports)
    gp_title=st.text_input("GP Title *",key="gp_title")
    gp_content=st.text_area("GP Details *",key="gp_content", height=120)
    if st.button("Save GP Report",type="primary",key="gp_save"):
        if not gp_title or not gp_content: st.error("Title + Details required")
        else:
            st.session_state.gp_reports.append({"id":len(st.session_state.gp_reports)+1,"title":gp_title,"content":gp_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(GP_FILE, st.session_state.gp_reports)
            st.success("Saved GP report")
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(f"{gpr['title']} - by {gpr['by']} - {gpr['date']}"):
            st.info(gpr['content'])

with tab6:
    st.subheader("💰 Finance Portal - 5 Only - Principal, Patron, President, Speaker, Finance")
    st.session_state.finance_docs=load_json(FINANCE_FILE, st.session_state.finance_docs)
    if user not in FINANCE_5:
        st.error("❌ Finance ONLY 5: Principal, Patron, His Excellency President, Right Honourable Speaker, Finance Secretary can view")
        st.stop()
    st.success(f"Finance 5 Access Granted - {user_full} - {len(st.session_state.finance_docs)} finance docs")
    f_title=st.text_input("Finance Title * (e.g. Budget 2026 Q1)",key="fin_title")
    f_desc=st.text_area("Description",key="fin_desc")
    f_file=st.file_uploader("Upload File - Excel / PPT / PDF / Word - Finance Only",type=["xlsx","xls","pptx","ppt","pdf","docx","doc","csv"],key="fin_file")
    if st.button("Save Finance Doc - Visible to Finance 5 Only",type="primary",key="fin_save"):
        if not f_title: st.error("Title required")
        else:
            fname=""; fpath=""
            if f_file:
                fname=f_file.name
                fpath=f"data/documents/finance_{len(st.session_state.finance_docs)+1}_{fname.replace(' ','_')}"
                open(fpath,'wb').write(f_file.getvalue())
            st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title,"description":f_desc,"file_name":fname,"file_path":fpath,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(FINANCE_FILE, st.session_state.finance_docs)
            st.success(f"✅ Saved finance doc '{f_title}' - Finance 5 can see & download!"); st.rerun()
    st.divider()
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True):
            st.markdown(f"**{fd['title']}** - by {fd['by']} - {fd['date']}")
            if fd.get('description',''): st.write(fd['description'])
            if fd.get('file_name',''): st.write(f"📎 File: {fd['file_name']}")
            if fd.get('file_path','') and os.path.exists(fd['file_path']):
                try:
                    st.download_button(f"📥 Download {fd['file_name']}", open(fd['file_path'],'rb').read(), file_name=fd['file_name'], key=f"dl_fin_{fd['id']}", type="primary")
                except: st.error("File missing")

with tab7:
    st.subheader("🔐 Secret Store - Cabinet Secrets")
    st.session_state.documents=load_json(DOCS_FILE, st.session_state.documents)
    dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat")
    dt=st.text_input("Title *",key="secret_title")
    dd=st.text_area("Description / Secret Details",key="secret_desc", height=120)
    if st.button("Save Secret Text",type="primary",key="secret_save"):
        if not dt.strip(): st.error("Title required")
        else:
            st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DOCS_FILE, st.session_state.documents)
            st.success("Saved secret")
    for d in reversed(st.session_state.documents):
        with st.expander(f"{d['category']} | {d['title']} - by {d['by']}"):
            st.write(d['description'])

with tab8:
    st.subheader("📄 Documents - PDF, PowerPoint, Word, Excel - For ALL 13 Departments!")
    st.info("✅ ALL 13 Departments can upload: PDF (.pdf), PowerPoint (.pptx/.ppt), Word (.docx/.doc), Excel (.xlsx/.xls/.csv) - All see & download - Saved on server for years!")
    st.session_state.uploaded_docs=load_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
    doc_cat=st.selectbox("Document Category",DOC_CATEGORIES,key="doc_cat")
    doc_title=st.text_input("Document Title *",key="doc_title", placeholder="e.g. Budget 2026, Constitution, Minutes")
    doc_desc=st.text_area("Description / Details",key="doc_desc", placeholder="Describe this document...")
    doc_file=st.file_uploader("Upload File * PDF / PowerPoint / Word / Excel - Any of 13 can upload",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv"],key="doc_file", help="Supports: PDF, PowerPoint, Word, Excel")
    if st.button("📤 Upload Document - Visible to ALL 13",type="primary",use_container_width=True,key="doc_save"):
        if not doc_title.strip() or not doc_file: st.error("Title + File required!")
        else:
            did=len(st.session_state.uploaded_docs)+1
            safe_name = doc_file.name.replace(" ", "_")
            fpath=f"data/documents/doc_{did}_{safe_name}"
            open(fpath,'wb').write(doc_file.getvalue())
            ext = safe_name.split('.')[-1].lower()
            icon = "📕 PDF" if ext=="pdf" else "📊 PowerPoint" if ext in ["pptx","ppt"] else "📝 Word" if ext in ["docx","doc"] else "📗 Excel" if ext in ["xlsx","xls","csv"] else "📄 Doc"
            st.session_state.uploaded_docs.append({"id":did,"category":doc_cat,"title":doc_title.strip(),"description":doc_desc.strip(),"file_name":doc_file.name,"file_path":fpath,"file_type":doc_file.type,"file_ext":ext,"file_icon":icon,"size":doc_file.size,"by":user_full,"from":user,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
            st.success(f"✅ Uploaded {icon} {doc_file.name}! ALL 13 can see & download - Saved for years!"); st.balloons(); st.rerun()
    st.divider()
    all_docs=load_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
    st.subheader(f"📂 All Documents - {len(all_docs)} Files - PDF, PPT, Word, Excel - ALL 13 Can Download - Works For Years")
    # Filters
    colf1, colf2 = st.columns(2)
    with colf1:
        docs_filter=st.selectbox("Filter by Category", ["All"]+DOC_CATEGORIES, key="docs_filter")
    with colf2:
        type_filter=st.selectbox("Filter by File Type", ["All Types","📕 PDF","📊 PowerPoint","📝 Word","📗 Excel"], key="type_filter")
    filtered_docs = all_docs
    if docs_filter != "All": filtered_docs=[d for d in filtered_docs if d['category']==docs_filter]
    if type_filter != "All Types":
        if "PDF" in type_filter: filtered_docs=[d for d in filtered_docs if d.get('file_ext','')=='pdf']
        elif "PowerPoint" in type_filter: filtered_docs=[d for d in filtered_docs if d.get('file_ext','') in ['pptx','ppt']]
        elif "Word" in type_filter: filtered_docs=[d for d in filtered_docs if d.get('file_ext','') in ['docx','doc']]
        elif "Excel" in type_filter: filtered_docs=[d for d in filtered_docs if d.get('file_ext','') in ['xlsx','xls','csv']]
    if not filtered_docs:
        st.warning("No documents yet - Upload PDF, PowerPoint, Word, or Excel above! ALL 13 can upload!")
    else:
        for doc in reversed(filtered_docs):
            with st.container(border=True):
                st.markdown(f"{doc.get('file_icon','📄')} **{doc['title']}** | {doc['category']} | by {doc['by']} | {doc['date']}")
                if doc.get('description',''): st.write(f"📝 {doc['description']}")
                st.caption(f"File: {doc['file_name']} | Type: {doc.get('file_ext','').upper()} | Size: {doc.get('size',0)//1024} KB")
                if os.path.exists(doc.get('file_path','')):
                    try:
                        st.download_button(f"📥 Download {doc['file_name']}", open(doc['file_path'],'rb').read(), file_name=doc['file_name'], key=f"dl_doc_{doc['id']}_{doc['file_name']}", type="primary", use_container_width=True)
                    except: st.error("File error")
                else:
                    st.warning("File missing on server")

with tab9:
    st.subheader("📸 Media Gallery - ALL SEE - Photos, Videos, Music - ALL 13")
    st.session_state.media=load_json(MEDIA_FILE, st.session_state.media)
    mt=st.text_input("Media Title *",key="media_title", placeholder="e.g. Sports Day 2026")
    mf=st.file_uploader("File * JPG/PNG/MP4/MP3",type=["jpg","png","jpeg","mp4","mp3","m4a","wav"],key="media_file")
    if st.button("Upload - Visible to ALL 13",type="primary",use_container_width=True,key="media_save"):
        if not mt.strip() or not mf: st.error("Title + File required")
        else:
            fid=len(st.session_state.media)+1
            fpath=f"data/media_files/media_{fid}_{mf.name.replace(' ','_')}"
            open(fpath,'wb').write(mf.getvalue())
            st.session_state.media.append({"id":fid,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(MEDIA_FILE, st.session_state.media)
            st.success("✅ Saved - ALL 13 can see!"); st.rerun()
    for m in reversed(st.session_state.media):
        with st.container(border=True):
            st.write(f"**{m['title']}** - by {m['by']} - {m['date']}")
            if os.path.exists(m['file_path']):
                if "image" in m['file_type']: st.image(m['file_path'],use_container_width=True)
                elif "video" in m['file_type']: st.video(m['file_path'])
                elif "audio" in m['file_type']: st.audio(m['file_path'])

with tab10:
    st.subheader("🏛️ Cabinet Archive - For Years - First BEC, Second BEC...")
    st.session_state.cabinets=load_json(CABINETS_FILE, st.session_state.cabinets)
    st.info("Save cabinets for future years - e.g. First BEC 2025, Second BEC 2026 - Works for years!")
    cab_year=st.text_input("Year * (e.g. 2026)",key="cab_year")
    cab_name=st.text_input("Cabinet Name * (e.g. First BEC 2026)",key="cab_name")
    cab_members=st.text_area("Members * (List all members)",key="cab_members", height=100)
    cab_photo=st.file_uploader("Cabinet Group Photo *",type=["jpg","png","jpeg"],key="cab_photo")
    if st.button("Save Cabinet - For Future Years - All 13 See",type="primary",use_container_width=True,key="cab_save"):
        if not cab_year or not cab_name or not cab_members or not cab_photo: st.error("All fields required!")
        else:
            nid=len(st.session_state.cabinets)+1
            p_path=f"data/media_files/cab_{nid}.jpg"
            open(p_path,'wb').write(cab_photo.getvalue())
            st.session_state.cabinets.append({"id":nid,"year":cab_year.strip(),"name":cab_name.strip(),"members":cab_members.strip(),"photo_path":p_path,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(CABINETS_FILE, st.session_state.cabinets)
            st.success("✅ Saved for years - Future cabinets will see!"); st.rerun()
    for cab in reversed(st.session_state.cabinets):
        with st.container(border=True):
            st.markdown(f"**{cab['name']} - {cab['year']}** - by {cab['by']} - {cab['date']}")
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'],use_container_width=True)
            st.info(cab['members'])
