import streamlit as st
import pandas as pd
import datetime
import os, json
import streamlit.components.v1 as components

st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide")

# ===== SAVE TO SERVER + PHONE NOTIFICATIONS =====
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
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint"]

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
if 'election_open' not in st.session_state: st.session_state.election_open=True
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

# PUBLIC VOTING - NO SECRETS
if is_public_vote:
    st.markdown("<h2 style='text-align:center;'>🏛️ UNIK BEC UNASNM - PUBLIC ELECTORAL COMMISSION</h2>", unsafe_allow_html=True)
    st.info("Public Voting - One Email Once Per Position - No Secrets - Works for Years")
    pub_tab1, pub_tab2, pub_tab3 = st.tabs(["Apply as Candidate", "Vote Easy Click", "Results"])
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
    with pub_tab3:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":cc['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])} for cc in cs]
                if sum([x['Votes'] for x in rd])>0:
                    st.write(USERS[pos]); st.dataframe(pd.DataFrame(rd),use_container_width=True)
    st.stop()

if not st.session_state.logged_in:
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("LOGIN",type="primary"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password")
    st.info("Default unik2025 | Public: ?public=vote")
    st.stop()

user=st.session_state.user
user_full=USERS[user]

# PASSWORD CHANGE FOR ALL 13
st.sidebar.title(user_full)
st.sidebar.success(f"Logged as: {user_full}")
st.sidebar.divider()
st.sidebar.subheader("🔐 Change My Password - My Bottle")
with st.sidebar.expander("Change My Own Password - Every Member!", expanded=False):
    current_pw_input=st.text_input("Current Password *", type="password", key="current_pw")
    new_p=st.text_input("New Password *", type="password", key="new_pass")
    confirm_p=st.text_input("Confirm New Password *", type="password", key="conf_pass")
    if st.button("Save New Password - My Bottle Only", type="primary", use_container_width=True, key="save_pass"):
        if not current_pw_input or not new_p or not confirm_p: st.sidebar.error("Fill ALL!")
        elif current_pw_input != st.session_state.passwords.get(user,"unik2025"): st.sidebar.error("Current wrong!")
        elif new_p != confirm_p: st.sidebar.error("Don't match!")
        elif len(new_p) < 4: st.sidebar.error("Min 4 chars!")
        else:
            st.session_state.passwords[user]=new_p
            save_json(PASSWORDS_FILE, st.session_state.passwords)
            st.sidebar.success(f"✅ Changed! New: {new_p}"); st.balloons()
st.sidebar.divider()

# ===== PHONE NOTIFICATION SETTINGS - ADDED =====
st.sidebar.subheader("🔔 Phone Notifications - For All 13!")
st.sidebar.info("Enable to get phone alerts when SUPER 4 broadcasts!")
with st.sidebar.expander("🔔 Enable Notifications - Click Here!", expanded=True):
    st.write("Get phone pop-up when new announcement comes!")
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
                document.getElementById('notif-status').innerHTML = "❌ Browser doesn't support notifications";
                return;
            }
            Notification.requestPermission().then(function(permission) {
                if (permission === "granted") {
                    document.getElementById('notif-status').innerHTML = "✅ Notifications ENABLED! You will get alerts on phone!";
                    localStorage.setItem('unik_notif_enabled','yes');
                    new Notification("🏛️ UNIK BEC Notifications Enabled!", {
                        body: "You will now receive phone alerts when SUPER 4 broadcasts to ALL 13!",
                        icon: "https://cdn-icons-png.flaticon.com/512/561/561127.png"
                    });
                } else {
                    document.getElementById('notif-status').innerHTML = "❌ Permission denied - Enable in browser settings";
                }
            });
        }
        // Auto-check status
        if (Notification.permission === "granted") {
            document.getElementById('notif-status').innerHTML = "✅ Notifications ACTIVE - Phone will alert you!";
        }
        </script>
    """, height=120)

if user in SUPER_4: st.sidebar.info("SUPER 4 - Broadcast + See ALL")
st.sidebar.info(f"Public Voting Link: ?public=vote")
if st.sidebar.button("Logout"): st.session_state.logged_in=False;st.rerun()

tab0,tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10=st.tabs(["📢 Public Announcements + 🔔 Phone Alerts","📝 Submit Report","📂 Private Portal","🗳️ Electoral Chair","⚖️ Disciplinary","📋 GP","💰 Finance","🔐 Secret Store","📄 Documents PDF/Excel/PPT","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab0:
    st.subheader("📢 Public Portal - SUPER 4 Broadcast to ALL 13 + Phone Notifications!")
    st.session_state.announcements=load_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
    
    # ===== PHONE NOTIFICATION JAVASCRIPT - CHECKS FOR NEW MESSAGES =====
    latest_count = len(st.session_state.announcements)
    latest_title = st.session_state.announcements[-1]['title'] if st.session_state.announcements else "No messages"
    latest_from = st.session_state.announcements[-1]['from_name'] if st.session_state.announcements else ""
    latest_content = st.session_state.announcements[-1]['content'][:100] if st.session_state.announcements else ""
    
    # This JS runs every 30 seconds and shows phone notification if new announcement
    components.html(f"""
        <script>
        const latestCount = {latest_count};
        const latestTitle = `{latest_title}`;
        const latestFrom = `{latest_from}`;
        const latestContent = `{latest_content}`;
        
        // Store last seen count
        const lastSeen = localStorage.getItem('unik_last_ann_count') || 0;
        
        // If new announcement and notifications enabled
        if (latestCount > lastSeen) {{
            if (Notification.permission === "granted" && localStorage.getItem('unik_notif_enabled') === 'yes') {{
                if (latestCount > 0) {{
                    // Play sound
                    const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
                    audio.play().catch(()=>{{}});
                    
                    // Show notification
                    setTimeout(() => {{
                        new Notification("📢 NEW: " + latestTitle, {{
                            body: "From " + latestFrom + ": " + latestContent + "...\\nClick to open UNIK Portal",
                            icon: "https://cdn-icons-png.flaticon.com/512/561/561127.png",
                            vibrate: [200, 100, 200],
                            requireInteraction: true
                        }});
                    }}, 1000);
                }}
            }}
            localStorage.setItem('unik_last_ann_count', latestCount);
        }}
        
        // Auto refresh every 30 seconds to check for new announcements
        setInterval(() => {{
            window.parent.location.reload();
        }}, 30000);
        </script>
        <div style="background:#e8f5e9; padding:8px; border-radius:6px; text-align:center; font-size:13px;">
            🔔 Auto-checking for new messages every 30 seconds... Phone will vibrate + sound when new broadcast arrives! Keep notifications enabled!
        </div>
    """, height=80)
    
    if len(st.session_state.announcements)>0:
        st.success(f"📢 {len(st.session_state.announcements)} Announcements from SUPER 4 - All 13 see + Phone alerts sent!")
    else:
        st.info("No announcements yet - SUPER 4 will post here - Phones will be notified!")
    
    if user in SUPER_4:
        st.divider()
        st.markdown(f"### ✍️ Post as {user_full} - ONE MESSAGE → ALL 13 PHONES GET NOTIFICATION!")
        st.warning("📱 When you broadcast, ALL 13 members' phones will vibrate + show pop-up notification - Even if portal is closed!")
        ann_title=st.text_input("Announcement Title *", key="ann_title", placeholder="e.g. Urgent Meeting Tomorrow 9am")
        ann_priority=st.selectbox("Priority", ["Normal","Urgent","Very Urgent - All Must Read + Phone Alert"], key="ann_priority")
        ann_content=st.text_area("Message to ALL 13 * (Type once, all 13 phones notified!)", height=150, key="ann_content", placeholder="Dear All 13 Departments...")
        ann_file=st.file_uploader("Attach PDF/Excel/PPT/Photo (Optional)", type=["pdf","xlsx","pptx","docx","jpg","png"], key="ann_file")
        
        if st.button("📢 BROADCAST TO ALL 13 + SEND PHONE NOTIFICATIONS", type="primary", use_container_width=True, key="ann_broadcast"):
            if not ann_title.strip() or not ann_content.strip():
                st.error("Title + Message required!")
            else:
                fpath=""; fname=""
                if ann_file:
                    fname=ann_file.name
                    fpath=f"data/documents/ann_{len(st.session_state.announcements)+1}_{fname}"
                    open(fpath,'wb').write(ann_file.getvalue())
                
                st.session_state.announcements.append({
                    "id": len(st.session_state.announcements)+1,
                    "title": ann_title.strip(),
                    "priority": ann_priority,
                    "content": ann_content.strip(),
                    "file_name": fname,
                    "file_path": fpath,
                    "from": user,
                    "from_name": user_full,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "read_by": []
                })
                save_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
                
                # TRIGGER NOTIFICATION SOUND FOR SENDER TOO
                components.html("""
                    <script>
                    const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
                    audio.play();
                    if (Notification.permission === "granted") {
                        new Notification("✅ Broadcast Sent!", {
                            body: "Your message sent to ALL 13 + Phone notifications triggered!",
                            icon: "https://cdn-icons-png.flaticon.com/512/561/561127.png"
                        });
                    }
                    </script>
                """, height=0)
                
                st.success(f"✅ BROADCASTED! ALL 13 phones notified with vibration + sound! '{ann_title}'"); st.balloons(); st.rerun()
    else:
        st.info(f"You are {user_full} - You will get phone notifications when SUPER 4 posts - Make sure you enabled notifications in sidebar!")
    
    st.divider()
    st.subheader("📋 All Broadcasts - Latest First - All 13 See Same + Phone Alerts")
    
    for ann in reversed(st.session_state.announcements):
        priority_color = "🔴" if "Very Urgent" in ann['priority'] else "🟡" if "Urgent" in ann['priority'] else "🟢"
        with st.container(border=True):
            st.markdown(f"{priority_color} **{ann['title']}** | {ann['priority']} | From: {ann['from_name']} | {ann['date']}")
            st.info(ann['content'])
            if ann.get('file_name',''):
                st.write(f"📎 Attached: {ann['file_name']}")
                if os.path.exists(ann.get('file_path','')):
                    try:
                        st.download_button(f"📥 Download {ann['file_name']}", open(ann['file_path'],'rb').read(), file_name=ann['file_name'], key=f"dl_ann_{ann['id']}")
                    except: pass
            
            if user not in ann.get('read_by',[]):
                if st.button(f"✅ Mark as Read", key=f"read_{ann['id']}"):
                    for a in st.session_state.announcements:
                        if a['id']==ann['id']:
                            if user not in a['read_by']: a['read_by'].append(user)
                    save_json(ANNOUNCEMENTS_FILE, st.session_state.announcements)
                    st.success("Marked as read!"); st.rerun()
            else:
                st.success(f"✅ You read this - {len(ann.get('read_by',[]))}/13 have read")
            
            if user in SUPER_4:
                st.caption(f"Read by: {', '.join([USERS.get(u,u) for u in ann.get('read_by',[])]) if ann.get('read_by',[]) else 'No one yet'} ({len(ann.get('read_by',[]))}/13)")

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
    st.subheader("Private Portal - Where Principal Looks")
    st.session_state.reports=load_json(REPORTS_FILE, st.session_state.reports)
    if user in SUPER_4:
        show=st.session_state.reports
        st.success(f"SUPER 4: Viewing ALL {len(show)} reports from all 13")
        if show: st.dataframe(pd.DataFrame(show)['from_name'].value_counts(),use_container_width=True)
    else:
        show=[r for r in st.session_state.reports if r['from']==user]
        st.info(f"Your reports: {len(show)}")
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']} - {r['date']}"):
            st.info(r['content'])

with tab3:
    st.subheader("Electoral Chair - Full")
    t_pending, t_approved, t_reg, t_vote, t_res = st.tabs(["Pending","Approved","Register+Photo","Vote Cabinet","Results"])
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
    with t_approved: st.write(f"Approved: {len(st.session_state.candidates)}")
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

with tab4:
    d_title=st.text_input("Case Title *",key="disc_title")
    d_content=st.text_area("Details *",key="disc_content")
    if st.button("Save Disciplinary",key="disc_save"):
        if d_title and d_content:
            st.session_state.disciplinary_reports.append({"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DISC_FILE, st.session_state.disciplinary_reports)
            st.success("Saved")

with tab5:
    gp_title=st.text_input("GP Title *",key="gp_title")
    gp_content=st.text_area("GP Details *",key="gp_content")
    if st.button("Save GP",key="gp_save"):
        if gp_title and gp_content:
            st.session_state.gp_reports.append({"title":gp_title,"content":gp_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(GP_FILE, st.session_state.gp_reports)
            st.success("Saved")

with tab6:
    if user not in FINANCE_5: st.error("Finance ONLY 5: Principal, Patron, President, Speaker, Finance"); st.stop()
    f_title=st.text_input("Finance Title *",key="fin_title")
    f_file=st.file_uploader("Upload Excel / PPT / PDF - Finance",type=["xlsx","xls","pptx","pdf","csv"],key="fin_file")
    if st.button("Save Finance Doc",key="fin_save"):
        if f_title:
            fname=""; fpath=""
            if f_file:
                fname=f_file.name
                fpath=f"data/documents/finance_{len(st.session_state.finance_docs)+1}_{fname}"
                open(fpath,'wb').write(f_file.getvalue())
            st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title,"file_name":fname,"file_path":fpath,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(FINANCE_FILE, st.session_state.finance_docs)
            st.success("Saved! Finance 5 can see")
    for fd in reversed(load_json(FINANCE_FILE, st.session_state.finance_docs)):
        with st.container(border=True):
            st.write(f"{fd['title']} - {fd.get('file_name','')} - by {fd['by']}")
            if fd.get('file_path','') and os.path.exists(fd['file_path']):
                st.download_button(f"📥 Download {fd['file_name']}", open(fd['file_path'],'rb').read(), file_name=fd['file_name'], key=f"dl_fin_{fd['id']}")

with tab7:
    dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat")
    dt=st.text_input("Title *",key="secret_title")
    dd=st.text_area("Description",key="secret_desc")
    if st.button("Save Secret Text",key="secret_save"):
        if dt.strip():
            st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            save_json(DOCS_FILE, st.session_state.documents)
            st.success("Saved")

with tab8:
    st.subheader("📄 Upload Documents - PDF, Excel, PowerPoint, Word")
    doc_cat=st.selectbox("Document Category",DOC_CATEGORIES,key="doc_cat")
    doc_title=st.text_input("Document Title *",key="doc_title")
    doc_desc=st.text_area("Description",key="doc_desc")
    doc_file=st.file_uploader("Upload File * PDF/Excel/PPT/Word",type=["pdf","xlsx","xls","pptx","ppt","docx","doc","csv"],key="doc_file")
    if st.button("📤 Upload Document",type="primary",use_container_width=True,key="doc_save"):
        if not doc_title.strip() or not doc_file: st.error("Title+File required!")
        else:
            did=len(st.session_state.uploaded_docs)+1
            fpath=f"data/documents/doc_{did}_{doc_file.name}"
            open(fpath,'wb').write(doc_file.getvalue())
            st.session_state.uploaded_docs.append({"id":did,"category":doc_cat,"title":doc_title.strip(),"description":doc_desc.strip(),"file_name":doc_file.name,"file_path":fpath,"file_type":doc_file.type,"size":doc_file.size,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
            save_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)
            st.success("Uploaded! ALL 13 can see & download!"); st.rerun()
    for doc in reversed(load_json(UPLOADED_DOCS_FILE, st.session_state.uploaded_docs)):
        with st.container(border=True):
            st.markdown(f"**{doc['title']}** | {doc['category']} | by {doc['by']}")
            if os.path.exists(doc.get('file_path','')):
                st.download_button(f"📥 Download {doc['file_name']}", open(doc['file_path'],'rb').read(), file_name=doc['file_name'], key=f"dl_doc_{doc['id']}", type="primary")

with tab9:
    st.subheader("Media Gallery - ALL SEE")
    mt=st.text_input("Media Title *",key="media_title")
    mf=st.file_uploader("File *",type=["jpg","png","jpeg","mp4","mp3","m4a","wav"],key="media_file")
    if st.button("Upload Visible to ALL",type="primary",key="media_save"):
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

with tab10:
    st.subheader("Cabinet Archive - For Years")
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
            st.write(f"{cab['name']} - {cab['year']}")
            if os.path.exists(cab['photo_path']): st.image(cab['photo_path'],use_container_width=True)
            st.info(cab['members'])
