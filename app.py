import streamlit as st, os, json, pandas as pd, time, re, hashlib, base64, secrets
from datetime import datetime as dt, timedelta
import streamlit.components.v1 as components
try:
    from cryptography.fernet import Fernet
except:
    Fernet = None
st.set_page_config(page_title="UNIK BEC UNASNM Portal", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")
os.makedirs("data/media_files", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)
os.makedirs("data/personal", exist_ok=True)
DEFAULT_PHRASE = "CHANGE-THIS-PHRASE-AT-ONCE-UNIK-2026"
PHRASE_FILE = "data/phrase.txt"
def load_phrase():
    try:
        if os.path.exists(PHRASE_FILE):
            with open(PHRASE_FILE, 'r') as f:
                v = f.read().strip()
                if v:
                    return v
    except:
        pass
    return DEFAULT_PHRASE
CURRENT_PHRASE = load_phrase()
def make_fernet(phrase):
    if Fernet is None:
        return None
    key = base64.urlsafe_b64encode(hashlib.sha256(str(phrase).encode()).digest())
    return Fernet(key)
def encrypt_with(phrase, data):
    f = make_fernet(phrase)
    if f is None or data is None:
        return data
    return f.encrypt(data)
def decrypt_with(phrase, data):
    f = make_fernet(phrase)
    if f is None or data is None:
        return data
    try:
        return f.decrypt(data)
    except Exception:
        return data
def encrypt_bytes(data):
    return encrypt_with(CURRENT_PHRASE, data)
def decrypt_bytes(data):
    return decrypt_with(CURRENT_PHRASE, data)
def write_encrypted_file(path, data):
    with open(path, 'wb') as f:
        f.write(encrypt_bytes(data))
def read_decrypted_file(path):
    with open(path, 'rb') as f:
        return decrypt_bytes(f.read())
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + str(password)).encode()).hexdigest()
    return salt + ":" + h
def check_password(password, stored):
    try:
        if ":" not in str(stored):
            return str(password) == str(stored)
        salt, h = str(stored).split(":", 1)
        return hashlib.sha256((salt + str(password)).encode()).hexdigest() == h
    except:
        return False
def migrate_phrase(old_phrase, new_phrase):
    global CURRENT_PHRASE
    paths = []
    for _v in FILES.values():
        paths.append(_v)
    for _root in ["data/media_files", "data/documents", "data/personal"]:
        if os.path.exists(_root):
            for _fn in os.listdir(_root):
                paths.append(os.path.join(_root, _fn))
    for _p in paths:
        if not os.path.exists(_p) or not os.path.isfile(_p):
            continue
        try:
            with open(_p, 'rb') as f:
                raw = f.read()
            if not raw:
                continue
            dec = decrypt_with(old_phrase, raw)
            if dec == raw and raw[:1] != b'{':
                continue
            with open(_p, 'wb') as f:
                f.write(encrypt_with(new_phrase, dec))
        except:
            pass
    CURRENT_PHRASE = new_phrase
    with open(PHRASE_FILE, 'w') as f:
        f.write(new_phrase)
DEFAULT_MEET_LINK = "https://meet.google.com/abc-defg-hij"
TEAMS_LINK = "https://teams.microsoft.com"
OFFICE_LINK = "https://www.office.com"
WORD_LINK = "https://word.cloud.microsoft"
EXCEL_LINK = "https://excel.cloud.microsoft"
PPT_LINK = "https://powerpoint.cloud.microsoft"
BIG_FOUR = ["president","patron","speaker","principal"]
PORTAL_LINK = "https://unik-bec-system-edudyqeshonywrcnjthl8l.streamlit.app/"
FILES = {"reports":"data/reports.json","media":"data/media.json","candidates":"data/candidates.json","pending":"data/pending.json","votes":"data/votes.json","cabinets":"data/cabinets.json","docs":"data/docs.json","finance":"data/finance.json","disc":"data/disc.json","gp":"data/gp.json","passwords":"data/passwords.json","uploaded":"data/uploaded_docs.json","ann":"data/announcements.json","meet":"data/meetings.json","personal":"data/personal.json","audit":"data/audit.json","notif":"data/notifications.json","meetlink":"data/meet_link.json","youtube":"data/youtube.json","blocked":"data/blocked.json"}
def load_json(p, d):
    if os.path.exists(p):
        try:
            with open(p, 'rb') as f:
                raw = f.read()
            if not raw:
                return d
            dec = decrypt_bytes(raw)
            return json.loads(dec.decode())
        except:
            return d
    return d
def save_json(p, data):
    raw = json.dumps(data, default=str, indent=2).encode()
    with open(p, 'wb') as f:
        f.write(encrypt_bytes(raw))
def get_meet_link():
    d = load_json(FILES["meetlink"], {})
    link = d.get("link", "") if isinstance(d, dict) else ""
    return link.strip() if link else DEFAULT_MEET_LINK
def get_blocked():
    d = load_json(FILES["blocked"], {})
    return d if isinstance(d, dict) else {}
def is_blocked(u):
    return bool(get_blocked().get(u, False))
KEEP_OPTIONS = {"7 Days":7, "30 Days":30, "90 Days":90, "1 Year":365, "Forever":36500}
def keep_days(label):
    return KEEP_OPTIONS.get(label, 30)
def expiry_str(days):
    return (dt.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
def is_expired(item):
    try:
        exp = item.get("expires", "")
        if not exp:
            return False
        return dt.now() > dt.strptime(exp, "%Y-%m-%d %H:%M")
    except:
        return False
def days_left(item):
    try:
        exp = dt.strptime(item.get("expires", ""), "%Y-%m-%d %H:%M")
        return max(0, (exp - dt.now()).days)
    except:
        return 9999
def badge_html(kind):
    if kind == "university":
        return """<div style='height:220px;border:4px solid #FFD700;border-radius:20px;background:#0B3D1E;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px;'><div style='font-size:52px;'>✚</div><div style='color:#FFD700;font-weight:900;font-size:22px;line-height:1.1;'>UNIVERSITY<br>OF KISUBI</div><div style='color:#FFFFFF;font-weight:900;font-size:18px;'>UniK</div><div style='color:#FFFFFF;font-size:15px;font-weight:700;'>📖 In Virtue We Educate</div><div style='color:#FFD700;font-size:14px;font-weight:700;'>EST. 2004</div></div>"""
    return """<div style='height:220px;border:4px solid #FFD700;border-radius:20px;background:#075E54;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:10px;'><div style='font-size:52px;'>🩺</div><div style='color:#FFD700;font-weight:900;font-size:24px;line-height:1.1;'>UNASNM</div><div style='color:#FFFFFF;font-weight:900;font-size:16px;line-height:1.2;'>UGANDA NATIONAL<br>ASSOCIATION OF<br>STUDENT NURSES<br>AND MIDWIVES</div><div style='color:#FFD700;font-size:15px;font-weight:700;'>✚ Nursing Cap • Care • Unity</div></div>"""
def find_badge(name):
    for f in [name+".jpg", name+".png", name+".jpeg", name+".JPG", name+".PNG"]:
        if os.path.exists(f):
            return f
    return ""
def show_space(name):
    f = find_badge(name)
    if f:
        st.image(f, use_container_width=True)
    else:
        st.markdown(badge_html(name), unsafe_allow_html=True)
def show_header(subtitle="Tap green, join Meet."):
    c_left, c_mid, c_right = st.columns([2,3,2])
    with c_left:
        show_space("university")
    with c_mid:
        st.markdown("<h1 style='text-align:center;color:#FFFFFF;font-size:48px;line-height:1.1;'>UNIK BEC UNASNM<br>Governance Portal</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#FFFFFF;font-size:26px;font-weight:900;'>{subtitle}</p>", unsafe_allow_html=True)
    with c_right:
        show_space("unasnm")
def office_buttons():
    b1,b2,b3,b4 = st.columns(4)
    b1.link_button("TEAMS", TEAMS_LINK, use_container_width=True)
    b2.link_button("WORD", WORD_LINK, use_container_width=True)
    b3.link_button("EXCEL", EXCEL_LINK, use_container_width=True)
    b4.link_button("POWERPOINT", PPT_LINK, use_container_width=True)
    st.link_button("OFFICE - ALL", OFFICE_LINK, use_container_width=True)
def youtube_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{6,})", url or "")
    return m.group(1) if m else ""
def javascript_copy_button():
    components.html(f"""
    <div style="text-align:center;">
      <button onclick="copyLink()" style="background:#075E54;color:white;padding:16px 22px;border-radius:20px;font-size:18px;font-weight:900;border:none;width:100%;">COPY PORTAL LINK</button>
      <p id="copiedMsg" style="color:#0B3D1E;font-weight:900;font-size:18px;"></p>
    </div>
    <script>
    function copyLink() {{
      var link = "{PORTAL_LINK}";
      if (navigator.clipboard) {{
        navigator.clipboard.writeText(link).then(function() {{
          document.getElementById("copiedMsg").innerText = "Link Copied!";
        }});
      }} else {{
        document.getElementById("copiedMsg").innerText = link;
      }}
    }}
    </script>
    """, height=110)
MEET_LINK = get_meet_link()
is_public = st.query_params.get("public", "") == "vote"
USERS = {"principal":"Principal","patron":"Patron","president":"President","vice_president":"Vice President","speaker":"Speaker","general_secretary":"General Secretary","finance":"Finance Secretary","information":"Information Secretary","class_rep":"Class Rep","grc_male":"GRC Male","grc_female":"GRC Female","hostel_male":"Hostel Male","hostel_female":"Hostel Female","nursing_affairs":"Nursing Affairs"}
LOGIN_USERS = list(USERS.keys())
ELECTION_POS = ["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]
REPORT_TYPES = ["Weekly","Monthly","Financial","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Audit","Budget","Other"]
DOC_CATS = ["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret","PDF Documents","Excel Sheets","PowerPoint","Public Information","Meeting Minutes","Academic","Welfare","Nursing Affairs"]
for k, f in FILES.items():
    if k not in st.session_state:
        if k == "passwords":
            pw = load_json(f, {})
            if isinstance(pw, dict) and pw:
                st.session_state[k] = pw
            else:
                st.session_state[k] = {u: hash_password("unik2025") for u in LOGIN_USERS}
                save_json(f, st.session_state[k])
        elif k == "blocked":
            st.session_state[k] = load_json(f, {})
        else:
            loaded = load_json(f, [])
            st.session_state[k] = loaded if isinstance(loaded, list) else []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""
if 'acting_as' not in st.session_state:
    st.session_state.acting_as = ""
st.markdown("""
<style>
.stApp{background: linear-gradient(180deg, #0B3D1E 0%, #075E54 260px, #FFF8E1 261px, #E8F5E9 100%) !important; color:#000000 !important;}
section[data-testid="stSidebar"]{display:none !important;}
button[data-testid="collapsedControl"]{display:none !important;}
.stApp p, .stApp div, .stApp label, .stApp span{color:#000000 !important; font-size:18px !important; font-weight:600 !important;}
h1,h2,h3{color:#0B3D1E !important; font-weight:900 !important;}
input, textarea, select{color:#000000 !important; background-color:#FFFFFF !important; font-size:18px !important; font-weight:700 !important; border:2px solid #0B3D1E !important;}
button[kind="primary"]{background-color:#075E54 !important; color:#FFFFFF !important; border-radius:20px !important; font-size:18px !important; font-weight:900 !important;}
button[kind="primary"] p, button[kind="primary"] span{color:#FFFFFF !important;}
button[kind="secondary"]{background-color:#FFFFFF !important; color:#000000 !important; border:2px solid #075E54 !important; font-size:18px !important; font-weight:900 !important;}
button[kind="secondary"] p, button[kind="secondary"] span{color:#000000 !important;}
div[data-testid="stAlert"]{color:#000000 !important; background-color:#FFFFFF !important;}
div[data-testid="stAlert"] p{color:#000000 !important; font-size:18px !important; font-weight:700 !important;}
a{color:#0B6B3A !important; font-weight:900 !important;}
</style>
""", unsafe_allow_html=True)
def show_any_file(fp, fname):
    if not fp or not os.path.exists(fp):
        return
    low = fp.lower()
    try:
        data = read_decrypted_file(fp)
        if low.endswith(('.jpg','.jpeg','.png','.gif','.webp','.bmp')):
            st.image(data, use_container_width=True)
        elif low.endswith(('.mp4','.mov','.mpeg','.mpg','.avi','.mkv','.webm')):
            st.video(data, format="video/mp4")
        elif low.endswith(('.mp3','.m4a','.wav','.ogg','.opus','.aac','.flac')):
            st.audio(data, format="audio/mp3")
        elif low.endswith(('.pdf',)):
            st.write(f"PDF: {fname}")
        else:
            st.write(f"File: {fname}")
    except:
        st.write(f"File: {fname}")
def download_and_keep(fp, fname, key):
    if fp and os.path.exists(fp):
        st.download_button("DOWNLOAD TO PHONE", read_decrypted_file(fp), file_name=fname, key=key, type="primary", use_container_width=True)
def retention_badge(item):
    if item.get("expires"):
        if is_expired(item):
            return "EXPIRED"
        return f"{days_left(item)} days left | Expires: {item['expires']}"
    return "Forever"
def do_change_password(target_user, old_pw, new_pw, new_pw2):
    pw_dict = load_json(FILES["passwords"], st.session_state.passwords)
    if not check_password(old_pw, pw_dict.get(target_user, "")):
        st.error("Old password is wrong!")
        return False
    if not new_pw or len(new_pw) < 4:
        st.error("New password must be 4 or more!")
        return False
    if new_pw != new_pw2:
        st.error("New passwords do not match!")
        return False
    pw_dict[target_user] = hash_password(new_pw)
    save_json(FILES["passwords"], pw_dict)
    st.session_state.passwords = pw_dict
    st.success("Saved! Login with your new password.")
    st.balloons()
    return True
if is_public:
    show_header("One Email = One Vote")
    st.markdown("<h3 style='text-align:center;color:#FFFFFF;font-size:32px;'>PUBLIC ELECTION</h3>", unsafe_allow_html=True)
    t1,t2,t3 = st.tabs(["Apply","Vote","Results"])
    with t1:
        rp = st.selectbox("Position", ELECTION_POS, format_func=lambda x: USERS[x], key="pub_pos")
        rn = st.text_input("Full Names *", key="pub_name"); rclass = st.text_input("Class *", key="pub_class")
        remail = st.text_input("Email *", key="pub_email"); rreason = st.text_area("Why vote you? *", key="pub_reason")
        rphoto = st.file_uploader("Photo * JPG/PNG", type=["jpg","png","jpeg"], key="pub_photo")
        st.info("Speaker must approve first. No voting before approval.")
        if st.button("Submit", type="primary", use_container_width=True):
            if not rn or not rphoto:
                st.error("Names + Photo required")
            else:
                nid = int(time.time()); fpath = f"data/media_files/cand_{nid}.jpg"; write_encrypted_file(fpath, rphoto.getvalue())
                st.session_state.pending.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":str(dt.now())[:16]})
                save_json(FILES["pending"], st.session_state.pending); st.success("Sent! Wait for Speaker approval."); st.balloons()
    with t2:
        voter_email = st.text_input("University Email *", key="pub_voter_email")
        if voter_email and "@" in voter_email:
            vp = st.selectbox("Position", ELECTION_POS, format_func=lambda x: USERS[x], key="pub_vote_pos")
            approved = [x for x in st.session_state.candidates if x['position'] == vp]
            if not approved:
                st.warning("No approved candidate yet for this post. Speaker must approve first.")
            else:
                already = [v for v in st.session_state.votes if v.get('voter_email','').lower() == voter_email.lower() and v['position'] == vp]
                if already:
                    st.error(f"Already voted for {USERS[vp]}!")
                else:
                    st.write("Tick ONE person, then tap VOTE:")
                    for c in approved:
                        with st.container(border=True):
                            if c.get('photo_path','') and os.path.exists(c.get('photo_path','')):
                                st.image(read_decrypted_file(c.get('photo_path','')), width=140, caption=c['name'])
                            st.write(f"{c['name']} - {c.get('class','')}"); st.info(c.get('reason',''))
                    choice = st.radio("Choose one:", [f"{c['name']} - {c.get('class','')}" for c in approved], key=f"vote_choice_{vp}")
                    if st.button("VOTE", type="primary", use_container_width=True, key=f"vote_btn_{vp}"):
                        sel = approved[[f"{c['name']} - {c.get('class','')}" for c in approved].index(choice)]
                        st.session_state.votes.append({"candidate_id":sel['id'],"voter_email":voter_email.lower(),"position":vp,"candidate_name":sel['name'],"date":str(dt.now())})
                        save_json(FILES["votes"], st.session_state.votes); st.success(f"Voted {sel['name']}!"); st.balloons(); st.rerun()
        else:
            st.warning("Enter valid email to vote")
    with t3:
        votes = load_json(FILES["votes"], st.session_state.votes); st.success(f"Total Votes: {len(votes)}")
        for pos in ELECTION_POS:
            for cc in [c for c in st.session_state.candidates if c['position'] == pos]:
                st.write(f"{cc['name']} - {USERS[pos]} - {len([v for v in votes if v['candidate_id']==cc['id']])} votes")
    st.stop()
if not st.session_state.logged_in:
    show_header("Welcome, Family!")
    st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#FFFFFF;color:#0B3D1E;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:22px;display:block;text-align:center;'>JOIN MEET NOW</a>", unsafe_allow_html=True)
    javascript_copy_button()
    office_buttons()
    PUBLIC_VOTE_LINK = PORTAL_LINK + "?public=vote"
    st.markdown(f"### PUBLIC VOTE\nLink: {PUBLIC_VOTE_LINK}")
    st.markdown("## LOGIN")
    u = st.selectbox("Your Office", LOGIN_USERS, format_func=lambda x: USERS[x], key="login")
    target = st.selectbox("Office To Open", LOGIN_USERS, format_func=lambda x: USERS[x], key="login_target")
    p = st.text_input("Password", type="password", key="pass")
    st.write("First password: unik2025 for all. Change it below.")
    if st.button("LOGIN", type="primary", use_container_width=True):
        pw_dict = load_json(FILES["passwords"], st.session_state.passwords)
        if u == target and is_blocked(u):
            st.error("You are BLOCKED. Talk to Big Four.")
        elif u == target and check_password(p, pw_dict.get(u, "")):
            st.session_state.logged_in = True; st.session_state.user = target; st.session_state.acting_as = ""; st.rerun()
        elif u != target and u in BIG_FOUR and check_password(p, pw_dict.get(u, "")):
            st.session_state.logged_in = True; st.session_state.user = target; st.session_state.acting_as = u; st.rerun()
        elif u != target and u not in BIG_FOUR:
            st.error("Only Big Four can open another office.")
        else:
            st.error("Wrong password! Default unik2025 if never changed.")
    st.divider()
    st.markdown("### CHANGE MY PASSWORD")
    cu = st.selectbox("My Office", LOGIN_USERS, format_func=lambda x: USERS[x], key="chg_login_user")
    cold = st.text_input("Old Password", type="password", key="chg_login_old")
    cnew = st.text_input("New Password", type="password", key="chg_login_new")
    cnew2 = st.text_input("New Password Again", type="password", key="chg_login_new2")
    if st.button("SAVE PASSWORD", type="primary", use_container_width=True, key="chg_login_save"):
        do_change_password(cu, cold, cnew, cnew2)
    st.stop()
user = st.session_state.user; user_full = USERS[user]
is_bigfour_viewer = st.session_state.acting_as in BIG_FOUR
is_bigfour = user in BIG_FOUR or is_bigfour_viewer
is_speaker = user == "speaker" or st.session_state.acting_as == "speaker"
reports = load_json(FILES["reports"], st.session_state.reports); media = load_json(FILES["media"], st.session_state.media); docs_uploaded = load_json(FILES["uploaded"], st.session_state.uploaded); votes = load_json(FILES["votes"], st.session_state.votes)
show_header("Everything on one screen.")
st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#FFFFFF;color:#0B3D1E;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:22px;display:block;text-align:center;'>JOIN MEET NOW</a>", unsafe_allow_html=True)
if is_bigfour_viewer:
    st.warning(f"Big Four: {USERS[st.session_state.acting_as]} opened {user_full}.")
else:
    st.markdown(f"Hello, {user_full} | Encrypted ON")
office_buttons()
PAGES = ["Dashboard","Personal","Public","Meeting","Reports","Super 4","Electoral","Disciplinary","GP","Finance","Secret Docs","Documents","Media","YouTube","Cabinet","Audit"]
if is_bigfour:
    PAGES = ["Big Four"] + PAGES
page = st.selectbox("CHOOSE DEPARTMENT", PAGES, key="top_page")
if st.button("Logout", use_container_width=True):
    st.session_state.logged_in = False; st.session_state.user = ""; st.session_state.acting_as = ""; st.rerun()
st.markdown(f"### {page}")
st.divider()
if page.startswith("Big Four"):
    st.subheader("Big Four Control")
    st.divider()
    st.markdown("### CHANGE SECRET PHRASE - BIG FOUR ONLY")
    st.success("Old phrase is filled by itself. Only type new phrase twice.")
    old_ph = CURRENT_PHRASE
    st.text_input("Old Secret Phrase - Filled By Itself", value=CURRENT_PHRASE, type="password", disabled=True, key="old_phrase")
    new_ph = st.text_input("New Secret Phrase", type="password", key="new_phrase")
    new_ph2 = st.text_input("New Secret Phrase Again", type="password", key="new_phrase2")
    if st.button("SAVE NEW PHRASE", type="primary", use_container_width=True, key="save_phrase"):
        if old_ph != CURRENT_PHRASE:
            st.error("Old phrase is wrong!")
        elif not new_ph or len(new_ph) < 8:
            st.error("New phrase must be 8 or more!")
        elif new_ph != new_ph2:
            st.error("New phrases do not match!")
        else:
            migrate_phrase(old_ph, new_ph)
            st.success("Saved! All files re-locked. Write it down.")
            st.balloons(); st.rerun()
    st.divider()
    blocked = get_blocked()
    for off in LOGIN_USERS:
        status = "BLOCKED" if blocked.get(off, False) else "ALLOWED"
        with st.container(border=True):
            st.markdown(f"{USERS[off]} - {status}")
            c1, c2, c3 = st.columns(3)
            if c1.button(f"BLOCK {USERS[off]}", key=f"block_{off}"):
                blocked[off] = True; save_json(FILES["blocked"], blocked); st.session_state.blocked = blocked; st.rerun()
            if c2.button(f"ALLOW {USERS[off]}", key=f"allow_{off}"):
                blocked[off] = False; save_json(FILES["blocked"], blocked); st.session_state.blocked = blocked; st.rerun()
            if c3.button(f"RESET {USERS[off]}", key=f"reset_{off}"):
                pw_dict = load_json(FILES["passwords"], st.session_state.passwords); pw_dict[off] = hash_password("unik2025"); save_json(FILES["passwords"], pw_dict); st.session_state.passwords = pw_dict; st.success(f"{USERS[off]} back to unik2025."); st.rerun()
elif page.startswith("Dashboard"):
    st.subheader("Dashboard"); c1,c2,c3,c4 = st.columns(4)
    c1.metric("Reports", len(reports)); c2.metric("Media", len(media)); c3.metric("Docs", len(docs_uploaded)); c4.metric("Votes", len(votes))
    yt = load_json(FILES["youtube"], st.session_state.youtube)
    st.subheader("YouTube - Latest")
    for y in reversed(yt[-3:]):
        vid = youtube_id(y.get("url",""))
        if vid:
            st.video(f"https://www.youtube.com/watch?v={vid}")
        st.write(y.get("title",""))
elif page.startswith("YouTube"):
    st.subheader("YouTube")
    yt = load_json(FILES["youtube"], st.session_state.youtube)
    yt_t = st.text_input("Title", key="yt_t")
    yt_u = st.text_input("YouTube Link", key="yt_u")
    if st.button("SAVE VIDEO", type="primary", use_container_width=True, key="yt_s"):
        if not yt_u:
            st.error("Paste link first")
        else:
            yt.append({"id":int(time.time()),"title":yt_t.strip(),"url":yt_u.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["youtube"], yt); st.success("Saved!"); st.balloons(); st.rerun()
    for idx, y in enumerate(reversed(yt)):
        with st.container(border=True):
            st.markdown(f"{y.get('title','Video')} | {y.get('by','')} | {y.get('date','')}")
            vid = youtube_id(y.get("url",""))
            if vid:
                st.video(f"https://www.youtube.com/watch?v={vid}")
            st.link_button("OPEN ON YOUTUBE", y.get("url",""), use_container_width=True)
elif page.startswith("Media"):
    st.subheader("Media - Any File")
    med = load_json(FILES["media"], st.session_state.media)
    mt = st.text_input("Title *", key="media_t")
    keep_label = st.selectbox("Keep for:", list(KEEP_OPTIONS.keys()), key="media_keep")
    mf = st.file_uploader("File *", key="media_f")
    if st.button("Upload", type="primary", use_container_width=True, key="media_s"):
        if not mt.strip() or not mf:
            st.error("Title + File required")
        else:
            nid = int(time.time()); fpath = f"data/media_files/media_{nid}_{mf.name.replace(' ','_')}"; write_encrypted_file(fpath, mf.getvalue())
            med.append({"id":nid,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"keep":keep_label,"expires":expiry_str(keep_days(keep_label))}); save_json(FILES["media"], med); st.success("Saved! Download to phone to keep forever."); st.balloons(); st.rerun()
    q = st.text_input("Search", key="media_q")
    cols = st.columns(3)
    shown = [m for m in reversed(med) if (not q or q.lower() in m['title'].lower() + m.get('file_name','').lower())]
    for idx, m in enumerate(shown):
        if is_expired(m):
            continue
        with cols[idx % 3]:
            with st.container(border=True):
                st.write(f"{m['title']} - {m['by']}"); st.write(retention_badge(m))
                fp = m.get('file_path','')
                if fp and os.path.exists(fp):
                    show_any_file(fp, m.get('file_name',''))
                    download_and_keep(fp, m.get('file_name',''), key=f"dl_med_{m['id']}_{idx}")
                c1,c2 = st.columns(2)
                if c1.button("Renew +30", key=f"ren_med_{m['id']}_{idx}"):
                    for x in med:
                        if x['id'] == m['id']:
                            x['expires'] = (dt.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
                    save_json(FILES["media"], med); st.rerun()
                if c2.button("Delete", key=f"del_med_{m['id']}_{idx}"):
                    med = [x for x in med if x['id'] != m['id']]
                    try:
                        if fp and os.path.exists(fp):
                            os.remove(fp)
                    except:
                        pass
                    save_json(FILES["media"], med); st.rerun()
elif page.startswith("Documents"):
    st.subheader("Documents - Any File")
    docs = load_json(FILES["uploaded"], st.session_state.uploaded)
    dcat = st.selectbox("Category", DOC_CATS, key="doc_cat"); dtit = st.text_input("Title *", key="doc_t"); dd = st.text_area("Description", key="doc_d")
    keep2 = st.selectbox("Keep for:", list(KEEP_OPTIONS.keys()), key="doc_keep")
    df = st.file_uploader("File *", key="doc_f")
    if st.button("Upload", type="primary", use_container_width=True, key="doc_s"):
        if not dtit.strip() or not df:
            st.error("Title + File required")
        else:
            safe = df.name.replace(" ","_"); fpath = f"data/documents/doc_{int(time.time())}_{safe}"; write_encrypted_file(fpath, df.getvalue())
            docs.append({"id":int(time.time()),"category":dcat,"title":dtit.strip(),"description":dd.strip(),"file_name":df.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"keep":keep2,"expires":expiry_str(keep_days(keep2))}); save_json(FILES["uploaded"], docs); st.success("Uploaded!"); st.balloons(); st.rerun()
    for idx, doc in enumerate(reversed(docs)):
        with st.container(border=True):
            st.markdown(f"{doc['title']} | {doc['category']} | {doc['by']}"); st.write(retention_badge(doc))
            if doc.get('file_path',''):
                show_any_file(doc['file_path'], doc.get('file_name',''))
                download_and_keep(doc['file_path'], doc.get('file_name',''), key=f"dl_doc_{doc['id']}_{idx}")
            if st.button(f"Renew +30 - {doc['title']}", key=f"ren_doc_{doc['id']}_{idx}"):
                for x in docs:
                    if x['id'] == doc['id']:
                        x['expires'] = (dt.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
                save_json(FILES["uploaded"], docs); st.rerun()
            if st.button(f"Delete - {doc['title']}", key=f"del_doc_{doc['id']}_{idx}"):
                docs = [x for x in docs if x['id'] != doc['id']]; save_json(FILES["uploaded"], docs); st.rerun()
elif page.startswith("Public"):
    st.subheader("Public Portal")
    anns = load_json(FILES["ann"], st.session_state.ann)
    at = st.text_input("Title *", key="ann_t"); acont = st.text_area("Message *", key="ann_c"); af = st.file_uploader("File", key="ann_f")
    if st.button("BROADCAST", type="primary", use_container_width=True):
        fpath = ""; fname = ""
        if af:
            fname = af.name.replace(" ","_"); fpath = f"data/documents/ann_{int(time.time())}_{fname}"; write_encrypted_file(fpath, af.getvalue())
        anns.append({"id":int(time.time()),"title":at.strip(),"content":acont.strip(),"file_name":fname,"file_path":fpath,"from":user,"from_name":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["ann"], anns); st.success("Broadcasted!"); st.balloons(); st.rerun()
    for idx, ann in enumerate(reversed(anns)):
        with st.container(border=True):
            st.markdown(f"{ann['title']} | {ann['from_name']} | {ann['date']}"); st.info(ann['content'])
            if ann.get('file_path',''):
                show_any_file(ann['file_path'], ann.get('file_name',''))
                download_and_keep(ann['file_path'], ann.get('file_name',''), key=f"dl_ann_{ann['id']}_{idx}")
elif page.startswith("Meeting"):
    st.subheader("Meeting")
    st.success(f"Meet: {MEET_LINK}")
    st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#075E54;color:#FFFFFF;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:20px;display:block;text-align:center;'>JOIN MEET NOW</a>", unsafe_allow_html=True)
    st.link_button("JOIN TEAMS", TEAMS_LINK, use_container_width=True)
    new_link = st.text_input("New Meet Link", value=MEET_LINK, key="new_meet_link")
    if st.button("SAVE LINK", type="primary", use_container_width=True):
        if "meet.google.com" not in new_link:
            st.error("Not a Meet link!")
        else:
            save_json(FILES["meetlink"], {"link":new_link.strip(),"by":user_full,"date":str(dt.now())}); st.success("Saved!"); st.rerun()
elif page.startswith("Personal"):
    st.subheader("My Personal Portal - Only You")
    st.markdown("### CHANGE MY PASSWORD")
    old_pw = st.text_input("Old Password", type="password", key="chg_old")
    new_pw = st.text_input("New Password", type="password", key="chg_new")
    new_pw2 = st.text_input("New Password Again", type="password", key="chg_new2")
    if st.button("SAVE PASSWORD", type="primary", use_container_width=True, key="chg_save"):
        do_change_password(user, old_pw, new_pw, new_pw2)
    st.divider()
    personal = load_json(FILES["personal"], st.session_state.personal); my_personal = [p for p in personal if p['owner'] == user]
    pt = st.text_input("Title *", key="pers_t"); pc = st.text_area("Notes *", key="pers_c"); pf = st.file_uploader("File", key="pers_f")
    if st.button("Save PRIVATE", type="primary", use_container_width=True, key="pers_s"):
        fpath = ""; fname = ""
        if pf:
            fname = pf.name.replace(" ","_"); fpath = f"data/personal/{user}_{int(time.time())}_{fname}"; write_encrypted_file(fpath, pf.getvalue())
        personal.append({"id":int(time.time()),"owner":user,"title":pt.strip(),"content":pc.strip(),"file_name":fname,"file_path":fpath,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["personal"], personal); st.success("Saved only for you!"); st.rerun()
    for idx, p in enumerate(reversed(my_personal)):
        with st.container(border=True):
            st.markdown(f"{p['title']} | {p['date']}")
            if p.get('content'):
                st.info(p['content'])
            if p.get('file_path',''):
                show_any_file(p['file_path'], p.get('file_name','')); download_and_keep(p['file_path'], p.get('file_name',''), key=f"dl_pers_{p['id']}_{idx}")
elif page.startswith("Reports"):
    st.subheader("Submit Report")
    rt = st.selectbox("Type", REPORT_TYPES, key="rt"); rtitle = st.text_input("Title *", key="rtitle"); rcontent = st.text_area("Details *", key="rcontent")
    rf = st.file_uploader("File", key="rep_f")
    if st.button("Submit", type="primary", use_container_width=True):
        fpath = ""; fname = ""
        if rf:
            fname = rf.name.replace(" ","_"); fpath = f"data/documents/report_{int(time.time())}_{fname}"; write_encrypted_file(fpath, rf.getvalue())
        reports.append({"id":int(time.time()),"date":dt.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":fname,"file_path":fpath}); save_json(FILES["reports"], reports); st.success("Submitted!"); st.balloons(); st.rerun()
    for idx, r in enumerate(reversed(reports)):
        with st.container(border=True):
            st.markdown(f"{r['title']} | {r.get('type','')} | {r['from_name']}")
            st.info(r.get('content',''))
            if r.get('file_path',''):
                show_any_file(r['file_path'], r.get('file_name','')); download_and_keep(r['file_path'], r.get('file_name',''), key=f"dl_rep_{r['id']}_{idx}")
elif page.startswith("Super"):
    st.subheader("Private Super 4")
    for r in reversed(load_json(FILES["reports"], st.session_state.reports)):
        with st.expander(f"{r['title']} - {r['from_name']}"):
            st.info(r['content'])
elif page.startswith("Electoral"):
    st.subheader("Electoral")
    st.write(f"Total Votes: {len(votes)} | Public: {PORTAL_LINK}?public=vote")
    pend = load_json(FILES["pending"], st.session_state.pending); cand = load_json(FILES["candidates"], st.session_state.candidates)
    st.markdown("### Waiting for Speaker")
    if not pend:
        st.write("No one waiting.")
    for pc in reversed(pend):
        with st.container(border=True):
            st.write(f"{pc['name']} - {USERS[pc['position']]} - {pc.get('class','')}"); st.info(pc.get('reason',''))
            if is_speaker:
                if st.button(f"APPROVE {pc['name']}", key=f"ap_{pc['id']}", type="primary"):
                    st.session_state.candidates.append(pc); st.session_state.pending = [x for x in st.session_state.pending if x['id'] != pc['id']]; save_json(FILES["candidates"], st.session_state.candidates); save_json(FILES["pending"], st.session_state.pending); st.success("Approved! Now people can vote."); st.rerun()
                if st.button(f"REJECT {pc['name']}", key=f"rj_{pc['id']}"):
                    st.session_state.pending = [x for x in st.session_state.pending if x['id'] != pc['id']]; save_json(FILES["pending"], st.session_state.pending); st.rerun()
            else:
                st.write("Only Speaker can approve.")
    st.markdown("### Approved - Can Be Voted")
    for pos in ELECTION_POS:
        group = [c for c in cand if c['position'] == pos]
        if not group:
            continue
        st.markdown(f"**{USERS[pos]}**")
        for cc in group:
            st.write(f"{cc['name']} - {cc.get('class','')} - {len([v for v in votes if v['candidate_id']==cc['id']])} votes")
elif page.startswith("Disciplinary"):
    st.subheader("Disciplinary"); disc = load_json(FILES["disc"], st.session_state.disc)
    d_t = st.text_input("Title *", key="disc_t"); d_c = st.text_area("Details *", key="disc_c")
    if st.button("Save", type="primary", key="disc_s"):
        disc.append({"id":int(time.time()),"title":d_t.strip(),"content":d_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["disc"], disc); st.success("Saved!"); st.rerun()
    for dr in reversed(disc):
        st.info(f"{dr['title']} - {dr['by']} - {dr['content']}")
elif page.startswith("GP"):
    st.subheader("GP"); gp = load_json(FILES["gp"], st.session_state.gp)
    gp_t = st.text_input("Title *", key="gp_t"); gp_c = st.text_area("Details *", key="gp_c")
    if st.button("Save", type="primary", key="gp_s"):
        gp.append({"id":int(time.time()),"title":gp_t.strip(),"content":gp_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["gp"], gp); st.success("Saved!"); st.rerun()
    for gpr in reversed(gp):
        st.info(f"{gpr['title']} - {gpr['by']} - {gpr['content']}")
elif page.startswith("Finance"):
    st.subheader("Finance")
    fin = load_json(FILES["finance"], st.session_state.finance)
    f_t = st.text_input("Title *", key="fin_t"); f_d = st.text_area("Description", key="fin_d"); f_f = st.file_uploader("File", key="fin_f"); f_amount = st.number_input("Amount UGX", min_value=0, step=1000, key="fin_amount")
    if st.button("Save", type="primary", key="fin_s2"):
        fname = ""; fpath = ""
        if f_f:
            fname = f_f.name.replace(" ","_"); fpath = f"data/documents/finance_{int(time.time())}_{fname}"; write_encrypted_file(fpath, f_f.getvalue())
        fin.append({"id":int(time.time()),"title":f_t.strip(),"description":f_d.strip(),"amount":f_amount,"file_name":fname,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["finance"], fin); st.success("Saved!"); st.balloons(); st.rerun()
    for idx, fd in enumerate(reversed(fin)):
        with st.container(border=True):
            st.markdown(f"{fd['title']} - UGX {fd.get('amount',0):,}")
            if fd.get('file_path',''):
                show_any_file(fd['file_path'], fd.get('file_name','')); download_and_keep(fd['file_path'], fd.get('file_name',''), key=f"dl_fin_{fd['id']}_{idx}")
elif page.startswith("Secret"):
    st.subheader("Secret Docs - Documents Only")
    sec = load_json(FILES["docs"], st.session_state.docs)
    if not isinstance(sec, list):
        sec = []
    dt_ = st.text_input("Title *", key="sec_t"); dd = st.text_area("Note", key="sec_d")
    if is_bigfour:
        keep_sec = st.selectbox("Keep for:", list(KEEP_OPTIONS.keys()), key="sec_keep")
    else:
        keep_sec = "30 Days"
        st.write("Stays 30 days. Big Four decide Forever or remove.")
    sf = st.file_uploader("Document * - PDF, Word, Excel, PowerPoint, Text", type=["pdf","doc","docx","xls","xlsx","ppt","pptx","txt","csv"], key="sec_f")
    if st.button("Save Secret Doc", type="primary", use_container_width=True, key="sec_s"):
        if not dt_.strip() or not sf:
            st.error("Title + Document required")
        else:
            fname = sf.name.replace(" ","_"); fpath = f"data/documents/secret_{int(time.time())}_{fname}"; write_encrypted_file(fpath, sf.getvalue())
            sec.append({"id":int(time.time()),"title":dt_.strip(),"description":dd.strip(),"file_name":sf.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d"),"keep":keep_sec,"expires":expiry_str(keep_days(keep_sec))}); save_json(FILES["docs"], sec); st.success("Saved!"); st.rerun()
    for idx, d in enumerate(reversed(sec)):
        if is_expired(d) and not is_bigfour:
            continue
        with st.container(border=True):
            st.markdown(f"{d.get('title','')} | {d.get('by','')} | {retention_badge(d)}")
            if d.get('description'):
                st.write(d.get('description',''))
            if d.get('file_path','') and os.path.exists(d.get('file_path','')):
                show_any_file(d['file_path'], d.get('file_name',''))
                download_and_keep(d['file_path'], d.get('file_name',''), key=f"dl_sec_{d['id']}_{idx}")
            if is_bigfour:
                c1,c2 = st.columns(2)
                if c1.button("Keep Forever", key=f"sec_forever_{d['id']}_{idx}"):
                    for x in sec:
                        if x['id'] == d['id']:
                            x['expires'] = expiry_str(36500); x['keep'] = "Forever"
                    save_json(FILES["docs"], sec); st.rerun()
                if c2.button("Remove", key=f"sec_del_{d['id']}_{idx}"):
                    sec = [x for x in sec if x['id'] != d['id']]; save_json(FILES["docs"], sec); st.rerun()
elif page.startswith("Cabinet"):
    st.subheader("Cabinet Archive"); cabs = load_json(FILES["cabinets"], st.session_state.cabinets)
    cy = st.text_input("Year *", key="cab_y"); cn = st.text_input("Name *", key="cab_n"); cm = st.text_area("Members *", key="cab_m"); cp = st.file_uploader("Photo", key="cab_p")
    if st.button("Save Cabinet", type="primary", use_container_width=True, key="cab_s"):
        if not cy or not cn or not cm or not cp:
            st.error("All required")
        else:
            fpath = f"data/media_files/cab_{int(time.time())}.jpg"; write_encrypted_file(fpath, cp.getvalue()); cabs.append({"id":int(time.time()),"year":cy.strip(),"name":cn.strip(),"members":cm.strip(),"photo_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d")}); save_json(FILES["cabinets"], cabs); st.success("Saved!"); st.rerun()
    for cab in reversed(cabs):
        with st.container(border=True):
            st.markdown(f"{cab['name']} - {cab['year']}"); show_any_file(cab['photo_path'], cab['name']); st.info(cab['members'])
elif page.startswith("Audit"):
    st.subheader("Audit Log"); audit = load_json(FILES["audit"], st.session_state.audit)
    if audit:
        st.dataframe(pd.DataFrame(list(reversed(audit))), use_container_width=True)
st.markdown("---"); st.markdown(f"<p style='text-align:center;color:#000000;'>UNIK BEC UNASNM | {dt.now().year}</p>", unsafe_allow_html=True)
