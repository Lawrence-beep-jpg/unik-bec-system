import streamlit as st, os, json, pandas as pd, time, re, hashlib, base64, secrets
from datetime import datetime as dt, timedelta
import streamlit.components.v1 as components
try:
    from cryptography.fernet import Fernet
except:
    Fernet = None
st.set_page_config(page_title="UNIK BEC UNASNM Governance Portal", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")

os.makedirs("data/media_files", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)
os.makedirs("data/personal", exist_ok=True)

# FIRST PHRASE ONLY. AFTER FIRST LOGIN, BIG FOUR CAN CHANGE IT INSIDE THE PORTAL. TELL NO ONE.
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
            # Only re-encrypt if old phrase really opened it, or file was plain json
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

KEEP_OPTIONS = {"7 Days - then disappears from portal":7, "30 Days":30, "90 Days":90, "1 Year - 365 Days":365, "Forever on Portal":36500}
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
def show_header(subtitle="Friendly, colourful, easy. Tap green, join Meet."):
    c_left, c_mid, c_right = st.columns([2,3,2])
    with c_left:
        show_space("university")
    with c_mid:
        st.markdown("<h1 style='text-align:center;color:#FFFFFF;font-size:48px;line-height:1.1;'>UNIK BEC UNASNM<br>Governance Portal</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#FFFFFF;font-size:26px;font-weight:900;'>{subtitle}</p>", unsafe_allow_html=True)
    with c_right:
        show_space("unasnm")
def office_buttons():
    st.markdown("### MICROSOFT TEAMS AND MICROSOFT OFFICE - UPLOAD DIRECT HERE, NO COPY")
    st.write("Tap one, it opens Teams / Word / Excel / PowerPoint. Work there, save there, then upload the file below direct in this portal. Do not copy files out.")
    b1,b2,b3,b4 = st.columns(4)
    b1.link_button("OPEN MICROSOFT TEAMS", TEAMS_LINK, use_container_width=True)
    b2.link_button("OPEN WORD", WORD_LINK, use_container_width=True)
    b3.link_button("OPEN EXCEL", EXCEL_LINK, use_container_width=True)
    b4.link_button("OPEN POWERPOINT", PPT_LINK, use_container_width=True)
    st.link_button("OPEN MICROSOFT OFFICE - ALL", OFFICE_LINK, use_container_width=True)
def youtube_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{6,})", url or "")
    return m.group(1) if m else ""
def javascript_copy_button():
    components.html(f"""
    <div style="text-align:center;">
      <button onclick="copyLink()" style="background:#075E54;color:white;padding:16px 22px;border-radius:20px;font-size:18px;font-weight:900;border:none;width:100%;">COPY PORTAL LINK - TAP HERE (JavaScript)</button>
      <p id="copiedMsg" style="color:#0B3D1E;font-weight:900;font-size:18px;"></p>
    </div>
    <script>
    function copyLink() {{
      var link = "{PORTAL_LINK}";
      if (navigator.clipboard) {{
        navigator.clipboard.writeText(link).then(function() {{
          document.getElementById("copiedMsg").innerText = "Link Copied! Send it on WhatsApp now.";
        }});
      }} else {{
        document.getElementById("copiedMsg").innerText = link;
      }}
    }}
    </script>
    """, height=110)

MEET_LINK = get_meet_link()
is_public = st.query_params.get("public", "") == "vote"
USERS = {"principal":"Principal - School Head","patron":"Patron","president":"His Excellency President","vice_president":"Vice President","speaker":"Right Hon. Speaker","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
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
            st.write(f"PDF file: {fname} - tap Download to Phone below")
        else:
            st.write(f"File: {fname} - tap Download to Phone below, any file works")
    except:
        st.write(f"File: {fname}")
def download_and_keep(fp, fname, key):
    if fp and os.path.exists(fp):
        st.download_button("DOWNLOAD TO PHONE / LAPTOP - Keep Forever In Your Files", read_decrypted_file(fp), file_name=fname, key=key, type="primary", use_container_width=True)
        st.write("After you download, it stays in your phone Downloads / Files even if it later disappears from this portal. The downloaded copy is decrypted, keep your phone locked.")
def retention_badge(item):
    if item.get("expires"):
        if is_expired(item):
            return "EXPIRED - Download quickly"
        d = days_left(item)
        return f"Keeps on portal: {d} days left | Expires: {item['expires']} | Download to phone to keep forever"
    return "Keeps: Forever"
def do_change_password(target_user, old_pw, new_pw, new_pw2):
    pw_dict = load_json(FILES["passwords"], st.session_state.passwords)
    if not check_password(old_pw, pw_dict.get(target_user, "")):
        st.error("Old password is wrong!")
        return False
    if not new_pw or len(new_pw) < 4:
        st.error("New password must be 4 or more letters / numbers!")
        return False
    if new_pw != new_pw2:
        st.error("New passwords do not match! Type same twice!")
        return False
    pw_dict[target_user] = hash_password(new_pw)
    save_json(FILES["passwords"], pw_dict)
    st.session_state.passwords = pw_dict
    st.success("Saved! Your new password works now. Next time, login with your own new password. Remember it well.")
    st.balloons()
    return True

if is_public:
    show_header("One Email = One Vote")
    st.markdown("<h3 style='text-align:center;color:#FFFFFF;font-size:32px;'>PUBLIC ELECTORAL COMMISSION</h3>", unsafe_allow_html=True)
    t1,t2,t3 = st.tabs(["Apply Candidate","Vote One Email Once","Live Results"])
    with t1:
        rp = st.selectbox("Position", ELECTION_POS, format_func=lambda x: USERS[x], key="pub_pos")
        rn = st.text_input("Full Names *", key="pub_name"); rclass = st.text_input("Class *", key="pub_class")
        remail = st.text_input("Email *", key="pub_email"); rreason = st.text_area("Why vote you? *", key="pub_reason")
        rphoto = st.file_uploader("Passport Photo * JPG/PNG", type=["jpg","png","jpeg"], key="pub_photo")
        if st.button("Submit", type="primary", use_container_width=True):
            if not rn or not rphoto:
                st.error("Full Names + Photo required")
            else:
                nid = int(time.time()); fpath = f"data/media_files/cand_{nid}.jpg"; write_encrypted_file(fpath, rphoto.getvalue())
                st.session_state.pending.append({"id":nid,"position":rp,"name":rn,"class":rclass,"email":remail,"reason":rreason,"photo_path":fpath,"date":str(dt.now())[:16]})
                save_json(FILES["pending"], st.session_state.pending); st.success("Sent!"); st.balloons()
    with t2:
        voter_email = st.text_input("University Email *", key="pub_voter_email")
        if voter_email and "@" in voter_email:
            vp = st.selectbox("Choose Position", ELECTION_POS, format_func=lambda x: USERS[x], key="pub_vote_pos")
            already = [v for v in st.session_state.votes if v.get('voter_email','').lower() == voter_email.lower() and v['position'] == vp]
            if already:
                st.error(f"Already voted for {USERS[vp]}!")
            else:
                email_key = abs(hash(voter_email.lower()))
                for c in [x for x in st.session_state.candidates if x['position'] == vp]:
                    with st.container(border=True):
                        if c.get('photo_path','') and os.path.exists(c.get('photo_path','')):
                            st.image(read_decrypted_file(c.get('photo_path','')), width=140, caption=c['name'])
                        st.write(f"{c['name']} - {c.get('class','')}"); st.info(c.get('reason',''))
                        if st.button(f"VOTE {c['name']}", key=f"pv_{c['id']}_{email_key}", type="primary", use_container_width=True):
                            st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email.lower(),"position":vp,"candidate_name":c['name'],"date":str(dt.now())})
                            save_json(FILES["votes"], st.session_state.votes); st.success(f"Voted {c['name']}!"); st.balloons(); st.rerun()
        else:
            st.warning("Enter valid university email to vote")
    with t3:
        votes = load_json(FILES["votes"], st.session_state.votes); st.success(f"Total Votes: {len(votes)}")
        for pos in ELECTION_POS:
            for cc in [c for c in st.session_state.candidates if c['position'] == pos]:
                st.write(f"{cc['name']} - {USERS[pos]} - {len([v for v in votes if v['candidate_id']==cc['id']])} votes")
    st.stop()

if not st.session_state.logged_in:
    show_header("Welcome, Family! Governance Portal")
    st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#FFFFFF;color:#0B3D1E;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:22px;display:block;text-align:center;'>JOIN GOOGLE MEET NOW - TAP HERE</a>", unsafe_allow_html=True)
    st.info(f"MEET LINK: {MEET_LINK}")
    javascript_copy_button()
    office_buttons()
    PUBLIC_VOTE_LINK = PORTAL_LINK + "?public=vote"
    st.markdown(f"### PUBLIC VOTE FOR ALL STUDENTS\nLink: {PUBLIC_VOTE_LINK}")
    st.markdown("## LOGIN HERE - CHOOSE YOUR OFFICE, TYPE PASSWORD")
    st.write("Every person: choose your office, type password, tap LOGIN. Big Four: choose Your Office, choose Office To Open, type YOUR OWN Big Four password, it will open even if they changed theirs.")
    u = st.selectbox("Your Office - Who Are You? (13)", LOGIN_USERS, format_func=lambda x: USERS[x], key="login")
    target = st.selectbox("Office To Open - Normally Same As Yours. Big Four can choose another office.", LOGIN_USERS, format_func=lambda x: USERS[x], key="login_target")
    p = st.text_input("Password - Your Own Password", type="password", key="pass")
    st.write("First time password is unik2025 for all 13. Change it below at once, use your new one after that.")
    if st.button("LOGIN TO PORTAL", type="primary", use_container_width=True):
        pw_dict = load_json(FILES["passwords"], st.session_state.passwords)
        if u == target and is_blocked(u):
            st.error("You are BLOCKED by Big Four. You cannot enter again. Talk to President / Patron / Speaker / Principal.")
        elif u == target and check_password(p, pw_dict.get(u, "")):
            st.session_state.logged_in = True; st.session_state.user = target; st.session_state.acting_as = ""; st.rerun()
        elif u != target and u in BIG_FOUR and check_password(p, pw_dict.get(u, "")):
            st.session_state.logged_in = True; st.session_state.user = target; st.session_state.acting_as = u; st.rerun()
        elif u != target and u not in BIG_FOUR:
            st.error("Only Big Four can open another office. Choose Office To Open same as Your Office.")
        else:
            st.error("Wrong password! Use your own password. Default unik2025 if you never changed it.")
    st.divider()
    st.markdown("### CHANGE MY PASSWORD HERE - EVERY PERSON, BEFORE YOU LOGIN")
    st.write("You just received the link? Do this first: choose your office, type old password unik2025, type your new password twice, tap SAVE. Then login above with your new password.")
    cu = st.selectbox("My Office - For Password Change", LOGIN_USERS, format_func=lambda x: USERS[x], key="chg_login_user")
    cold = st.text_input("Old Password", type="password", key="chg_login_old")
    cnew = st.text_input("New Password - Your Own", type="password", key="chg_login_new")
    cnew2 = st.text_input("New Password Again", type="password", key="chg_login_new2")
    if st.button("SAVE MY NEW PASSWORD", type="primary", use_container_width=True, key="chg_login_save"):
        do_change_password(cu, cold, cnew, cnew2)
    st.stop()

user = st.session_state.user; user_full = USERS[user]
is_bigfour_viewer = st.session_state.acting_as in BIG_FOUR
reports = load_json(FILES["reports"], st.session_state.reports); media = load_json(FILES["media"], st.session_state.media); docs_uploaded = load_json(FILES["uploaded"], st.session_state.uploaded); votes = load_json(FILES["votes"], st.session_state.votes)
show_header("Organised, colourful, easy. Everything visible on this big screen.")
st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#FFFFFF;color:#0B3D1E;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:22px;display:block;text-align:center;'>JOIN GOOGLE MEET NOW - TAP HERE</a>", unsafe_allow_html=True)
if is_bigfour_viewer:
    st.warning(f"Big Four access: You are {USERS[st.session_state.acting_as]}, you opened {user_full}. You can see everything here, even if they changed their password.")
else:
    st.markdown(f"Hello, {user_full} | All 13 Online Now | Encrypted storage ON")
office_buttons()
PAGES = ["Dashboard","My Personal Portal","Public Portal OPEN","Meeting - GOOGLE MEET DIRECT","Submit Report","Private SUPER 4","Electoral OPEN","Disciplinary OPEN","GP OPEN","Finance - MICROSOFT TEAMS AND OFFICE","Secret OPEN","Documents OPEN","Media Gallery OPEN - ANY FILE","YouTube - TAGGED VIDEOS","Cabinet Archive OPEN","Audit Log"]
if user in BIG_FOUR or is_bigfour_viewer:
    PAGES = ["Big Four Control - Block / Allow"] + PAGES
page = st.selectbox("CHOOSE DEPARTMENT - ALL VISIBLE HERE, TAP ONE", PAGES, key="top_page")
if st.button("Logout", use_container_width=True):
    st.session_state.logged_in = False; st.session_state.user = ""; st.session_state.acting_as = ""; st.rerun()
st.success("ALL 13 CAN: Upload ANY FILE direct, Download to Phone / Laptop, Vote, Join Meet, Join Teams, Use Office, Submit, Open Every Department, See Every Photo. Files are stored encrypted on the portal.")
st.warning("PHONE SPACE: Tap DOWNLOAD TO PHONE, it saves in your phone Downloads / Files and stays forever. Portal copy can expire after 7 days / 30 days / 1 year, your phone copy does not expire.")
st.markdown(f"### {page}  |  13 departments  |  Online now")
st.divider()

if page.startswith("Big Four"):
    st.subheader("Big Four Control - Refuse Access / Give Access Back")
    st.write("Only Big Four sees this. If a person misuses the portal, BLOCK them here. They cannot login again, even with the correct password. Tap ALLOW to give them back.")
    st.divider()
    st.markdown("### CHANGE SECRET PHRASE HERE - INSIDE YOUR OFFICE - BIG FOUR ONLY")
    st.write("This is the secret phrase that locks all files. Change it here, do not change it in the code again. Write the new phrase down in a safe book, tell no one. If you lose it, old files cannot be opened.")
    old_ph = st.text_input("Old Secret Phrase", type="password", key="old_phrase")
    new_ph = st.text_input("New Secret Phrase - Your Own, long", type="password", key="new_phrase")
    new_ph2 = st.text_input("New Secret Phrase Again", type="password", key="new_phrase2")
    if st.button("SAVE NEW SECRET PHRASE AND RE-LOCK ALL FILES", type="primary", use_container_width=True, key="save_phrase"):
        if old_ph != CURRENT_PHRASE:
            st.error("Old secret phrase is wrong!")
        elif not new_ph or len(new_ph) < 8:
            st.error("New phrase must be 8 or more letters / numbers!")
        elif new_ph != new_ph2:
            st.error("New phrases do not match! Type same twice!")
        else:
            migrate_phrase(old_ph, new_ph)
            st.success("Saved! New secret phrase works now. All old files were re-locked with it. Write it down now.")
            st.balloons(); st.rerun()
    st.divider()
    blocked = get_blocked()
    for off in LOGIN_USERS:
        status = "BLOCKED - Cannot enter" if blocked.get(off, False) else "ALLOWED - Can enter"
        with st.container(border=True):
            st.markdown(f"{USERS[off]} - {status}")
            c1, c2, c3 = st.columns(3)
            if c1.button(f"BLOCK {USERS[off]}", key=f"block_{off}"):
                blocked[off] = True; save_json(FILES["blocked"], blocked); st.session_state.blocked = blocked; st.success(f"{USERS[off]} is BLOCKED now."); st.rerun()
            if c2.button(f"ALLOW {USERS[off]}", key=f"allow_{off}"):
                blocked[off] = False; save_json(FILES["blocked"], blocked); st.session_state.blocked = blocked; st.success(f"{USERS[off]} can enter again."); st.rerun()
            if c3.button(f"RESET PASSWORD {USERS[off]}", key=f"reset_{off}"):
                pw_dict = load_json(FILES["passwords"], st.session_state.passwords); pw_dict[off] = hash_password("unik2025"); save_json(FILES["passwords"], pw_dict); st.session_state.passwords = pw_dict; st.success(f"Password for {USERS[off]} is back to unik2025. Tell the new person to change it at once."); st.rerun()
elif page.startswith("Dashboard"):
    st.subheader("Dashboard"); c1,c2,c3,c4 = st.columns(4)
    c1.metric("Reports", len(reports)); c2.metric("Media", len(media)); c3.metric("Docs", len(docs_uploaded)); c4.metric("Votes", len(votes))
    st.info("Tip: Go to Media Gallery, download the Anthem to your phone, then it is yours forever.")
    yt = load_json(FILES["youtube"], st.session_state.youtube)
    st.subheader("YouTube - All You Were Tagged In - Watch Here")
    for y in reversed(yt[-3:]):
        vid = youtube_id(y.get("url",""))
        if vid:
            st.video(f"https://www.youtube.com/watch?v={vid}")
        st.write(y.get("title",""))
elif page.startswith("YouTube"):
    st.subheader("YouTube - TAGGED VIDEOS - Paste Link, Watch Here, No Copy")
    yt = load_json(FILES["youtube"], st.session_state.youtube)
    yt_t = st.text_input("Video Title - type here, what is it about?", key="yt_t")
    yt_u = st.text_input("YouTube Link - paste here", key="yt_u")
    if st.button("SAVE YOUTUBE VIDEO HERE", type="primary", use_container_width=True, key="yt_s"):
        if not yt_u:
            st.error("Paste YouTube link first")
        else:
            yt.append({"id":int(time.time()),"title":yt_t.strip(),"url":yt_u.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["youtube"], yt); st.success("Saved! Watch it below now."); st.balloons(); st.rerun()
    for idx, y in enumerate(reversed(yt)):
        with st.container(border=True):
            st.markdown(f"{y.get('title','YouTube Video')} | by {y.get('by','')} | {y.get('date','')}")
            vid = youtube_id(y.get("url",""))
            if vid:
                st.video(f"https://www.youtube.com/watch?v={vid}")
            st.write(y.get("url",""))
            st.link_button("OPEN ON YOUTUBE", y.get("url",""), use_container_width=True)
elif page.startswith("Media"):
    st.subheader("Media Gallery - ANY FILE - MPEG, MP4, MP3, JPG, PDF, ZIP")
    st.info("Upload here direct, any file from any source. Files are stored encrypted. Everyone can see every photo here after login. Download to phone = keep forever in your phone.")
    office_buttons()
    med = load_json(FILES["media"], st.session_state.media)
    mt = st.text_input("Media Title *", key="media_t")
    keep_label = st.selectbox("Keep on portal for:", list(KEEP_OPTIONS.keys()), key="media_keep")
    mf = st.file_uploader("File * - ANY FILE TYPE - MPEG, MP4, MP3, JPG, PDF, ZIP", key="media_f")
    if st.button("Upload - ALL 13 SEE SAME GALLERY!", type="primary", use_container_width=True, key="media_s"):
        if not mt.strip() or not mf:
            st.error("Title + File required")
        else:
            nid = int(time.time()); fpath = f"data/media_files/media_{nid}_{mf.name.replace(' ','_')}"; write_encrypted_file(fpath, mf.getvalue())
            med.append({"id":nid,"title":mt.strip(),"file_name":mf.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"keep":keep_label,"expires":expiry_str(keep_days(keep_label))}); save_json(FILES["media"], med); st.success("Saved encrypted! Now download it to your phone to keep forever!"); st.balloons(); st.rerun()
    q = st.text_input("Search media by name", key="media_q")
    show_expired = st.checkbox("Show expired files too", key="media_exp")
    cols = st.columns(3)
    shown = [m for m in reversed(med) if (not q or q.lower() in m['title'].lower() + m.get('file_name','').lower())]
    for idx, m in enumerate(shown):
        if is_expired(m) and not show_expired:
            continue
        with cols[idx % 3]:
            with st.container(border=True):
                st.write(f"{m['title']} - {m['by']}")
                st.write(retention_badge(m))
                fp = m.get('file_path','')
                if fp and os.path.exists(fp):
                    show_any_file(fp, m.get('file_name',''))
                    download_and_keep(fp, m.get('file_name',''), key=f"dl_med_{m['id']}_{idx}")
                c1,c2 = st.columns(2)
                if c1.button("Renew +30 Days", key=f"ren_med_{m['id']}_{idx}"):
                    for x in med:
                        if x['id'] == m['id']:
                            x['expires'] = (dt.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M"); x['keep'] = "Renewed +30 Days"
                    save_json(FILES["media"], med); st.success("Renewed!"); st.rerun()
                if c2.button("Delete Forever", key=f"del_med_{m['id']}_{idx}"):
                    med = [x for x in med if x['id'] != m['id']]
                    try:
                        if fp and os.path.exists(fp):
                            os.remove(fp)
                    except:
                        pass
                    save_json(FILES["media"], med); st.success("Deleted from portal. Phone copies stay."); st.rerun()
elif page.startswith("Documents"):
    st.subheader("Documents - ANY FILE + Keep Time")
    office_buttons()
    docs = load_json(FILES["uploaded"], st.session_state.uploaded)
    dcat = st.selectbox("Category", DOC_CATS, key="doc_cat"); dtit = st.text_input("Title *", key="doc_t"); dd = st.text_area("Description", key="doc_d")
    keep2 = st.selectbox("Keep on portal for:", list(KEEP_OPTIONS.keys()), key="doc_keep")
    df = st.file_uploader("Upload File * - ANY FILE - MPEG, MP4, MP3, JPG, PDF, ZIP, Word, Excel", key="doc_f")
    if st.button("Upload Document - ALL 13 SEE SAME!", type="primary", use_container_width=True, key="doc_s"):
        if not dtit.strip() or not df:
            st.error("Title + File required")
        else:
            safe = df.name.replace(" ","_"); fpath = f"data/documents/doc_{int(time.time())}_{safe}"; write_encrypted_file(fpath, df.getvalue())
            docs.append({"id":int(time.time()),"category":dcat,"title":dtit.strip(),"description":dd.strip(),"file_name":df.name,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M"),"keep":keep2,"expires":expiry_str(keep_days(keep2))}); save_json(FILES["uploaded"], docs); st.success("Uploaded encrypted direct! Download to phone to keep forever."); st.balloons(); st.rerun()
    for idx, doc in enumerate(reversed(docs)):
        with st.container(border=True):
            st.markdown(f"{doc['title']} | {doc['category']} | by {doc['by']}"); st.write(retention_badge(doc))
            if doc.get('file_path',''):
                show_any_file(doc['file_path'], doc.get('file_name',''))
                download_and_keep(doc['file_path'], doc.get('file_name',''), key=f"dl_doc_{doc['id']}_{idx}")
            if st.button(f"Renew +30 Days - {doc['title']}", key=f"ren_doc_{doc['id']}_{idx}"):
                for x in docs:
                    if x['id'] == doc['id']:
                        x['expires'] = (dt.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M")
                save_json(FILES["uploaded"], docs); st.success("Renewed!"); st.rerun()
            if st.button(f"Delete Forever - {doc['title']}", key=f"del_doc_{doc['id']}_{idx}"):
                docs = [x for x in docs if x['id'] != doc['id']]; save_json(FILES["uploaded"], docs); st.success("Deleted!"); st.rerun()
elif page.startswith("Public"):
    st.subheader("Public Portal")
    office_buttons()
    anns = load_json(FILES["ann"], st.session_state.ann)
    at = st.text_input("Title *", key="ann_t"); acont = st.text_area("Message *", key="ann_c"); af = st.file_uploader("Attach File - ANY FILE", key="ann_f")
    if st.button("BROADCAST TO ALL 13", type="primary", use_container_width=True):
        fpath = ""; fname = ""
        if af:
            fname = af.name.replace(" ","_"); fpath = f"data/documents/ann_{int(time.time())}_{fname}"; write_encrypted_file(fpath, af.getvalue())
        anns.append({"id":int(time.time()),"title":at.strip(),"content":acont.strip(),"file_name":fname,"file_path":fpath,"from":user,"from_name":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")})
        save_json(FILES["ann"], anns); st.success("Broadcasted!"); st.balloons(); st.rerun()
    for idx, ann in enumerate(reversed(anns)):
        with st.container(border=True):
            st.markdown(f"{ann['title']} | {ann['from_name']} | {ann['date']} | Seen by 13"); st.info(ann['content'])
            if ann.get('file_path',''):
                show_any_file(ann['file_path'], ann.get('file_name',''))
                download_and_keep(ann['file_path'], ann.get('file_name',''), key=f"dl_ann_{ann['id']}_{idx}")
elif page.startswith("Meeting"):
    st.subheader("Meeting - GOOGLE MEET DIRECT + MICROSOFT TEAMS")
    st.success(f"Current Meet Link: {MEET_LINK}")
    st.markdown(f"<a href='{MEET_LINK}' target='_blank' style='background:#075E54;color:#FFFFFF;padding:18px 25px;border-radius:25px;text-decoration:none;font-weight:900;font-size:20px;display:block;text-align:center;'>JOIN GOOGLE MEET NOW</a>", unsafe_allow_html=True)
    st.link_button("JOIN MICROSOFT TEAMS MEETING", TEAMS_LINK, use_container_width=True)
    st.code(MEET_LINK)
    new_link = st.text_input("Paste NEW Google Meet Link", value=MEET_LINK, key="new_meet_link")
    if st.button("SAVE LINK", type="primary", use_container_width=True):
        if "meet.google.com" not in new_link:
            st.error("Not a Meet link!")
        else:
            save_json(FILES["meetlink"], {"link":new_link.strip(),"by":user_full,"date":str(dt.now())}); st.success("Saved!"); st.rerun()
elif page.startswith("My Personal"):
    st.subheader("My Personal Portal - ONLY YOU")
    st.markdown("### CHANGE MY PASSWORD HERE - INSIDE MY PORTAL")
    st.write("You entered with unik2025? Do this now: type old password unik2025, type your new password twice, tap Save. Next time, login with your own new password.")
    old_pw = st.text_input("Old Password", type="password", key="chg_old")
    new_pw = st.text_input("New Password - Your Own", type="password", key="chg_new")
    new_pw2 = st.text_input("New Password Again", type="password", key="chg_new2")
    if st.button("SAVE MY NEW PASSWORD", type="primary", use_container_width=True, key="chg_save"):
        do_change_password(user, old_pw, new_pw, new_pw2)
    st.divider()
    office_buttons()
    personal = load_json(FILES["personal"], st.session_state.personal); my_personal = [p for p in personal if p['owner'] == user]
    pt = st.text_input("Title *", key="pers_t"); pc = st.text_area("Notes *", key="pers_c"); pf = st.file_uploader("File - ANY FILE", key="pers_f")
    if st.button("Save PRIVATE", type="primary", use_container_width=True, key="pers_s"):
        fpath = ""; fname = ""
        if pf:
            fname = pf.name.replace(" ","_"); fpath = f"data/personal/{user}_{int(time.time())}_{fname}"; write_encrypted_file(fpath, pf.getvalue())
        personal.append({"id":int(time.time()),"owner":user,"title":pt.strip(),"content":pc.strip(),"file_name":fname,"file_path":fpath,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["personal"], personal); st.success("Saved only for you, encrypted!"); st.rerun()
    for idx, p in enumerate(reversed(my_personal)):
        with st.container(border=True):
            st.markdown(f"{p['title']} | {p['date']}")
            if p.get('content'):
                st.info(p['content'])
            if p.get('file_path',''):
                show_any_file(p['file_path'], p.get('file_name','')); download_and_keep(p['file_path'], p.get('file_name',''), key=f"dl_pers_{p['id']}_{idx}")
elif page.startswith("Submit"):
    st.subheader("Submit Report - With Microsoft Office and Teams")
    office_buttons()
    rt = st.selectbox("Report Type", REPORT_TYPES, key="rt"); rtitle = st.text_input("Title *", key="rtitle"); rcontent = st.text_area("Details * - type here", key="rcontent")
    rf = st.file_uploader("Attach Report File - Word, Excel, PDF, ANY FILE - upload direct", key="rep_f")
    if st.button("Submit Report", type="primary", use_container_width=True):
        fpath = ""; fname = ""
        if rf:
            fname = rf.name.replace(" ","_"); fpath = f"data/documents/report_{int(time.time())}_{fname}"; write_encrypted_file(fpath, rf.getvalue())
        reports.append({"id":int(time.time()),"date":dt.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":fname,"file_path":fpath}); save_json(FILES["reports"], reports); st.success("Report submitted encrypted!"); st.balloons(); st.rerun()
    for idx, r in enumerate(reversed(reports)):
        with st.container(border=True):
            st.markdown(f"{r['title']} | {r.get('type','')} | {r['from_name']}")
            st.info(r.get('content',''))
            if r.get('file_path',''):
                show_any_file(r['file_path'], r.get('file_name','')); download_and_keep(r['file_path'], r.get('file_name',''), key=f"dl_rep_{r['id']}_{idx}")
elif page.startswith("Private"):
    st.subheader("Private SUPER 4")
    for r in reversed(load_json(FILES["reports"], st.session_state.reports)):
        with st.expander(f"{r['title']} - {r['from_name']}"):
            st.info(r['content'])
elif page.startswith("Electoral"):
    st.subheader("Electoral OPEN")
    pend = load_json(FILES["pending"], st.session_state.pending); cand = load_json(FILES["candidates"], st.session_state.candidates)
    st.write(f"Total Votes: {len(votes)} | Public link: {PORTAL_LINK}?public=vote")
    for pc in reversed(pend):
        with st.container(border=True):
            st.write(f"{pc['name']} - {USERS[pc['position']]}"); st.info(pc.get('reason',''))
            if st.button(f"Approve {pc['name']}", key=f"ap_{pc['id']}"):
                st.session_state.candidates.append(pc); st.session_state.pending = [x for x in st.session_state.pending if x['id'] != pc['id']]; save_json(FILES["candidates"], st.session_state.candidates); save_json(FILES["pending"], st.session_state.pending); st.success("Approved!"); st.rerun()
    for cc in cand:
        st.write(f"{cc['name']} - {USERS[cc['position']]} - {len([v for v in votes if v['candidate_id']==cc['id']])} votes")
elif page.startswith("Disciplinary"):
    st.subheader("Disciplinary"); disc = load_json(FILES["disc"], st.session_state.disc)
    d_t = st.text_input("Case Title *", key="disc_t"); d_c = st.text_area("Details *", key="disc_c")
    if st.button("Save Disciplinary", type="primary", key="disc_s"):
        disc.append({"id":int(time.time()),"title":d_t.strip(),"content":d_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["disc"], disc); st.success("Saved!"); st.rerun()
    for dr in reversed(disc):
        st.info(f"{dr['title']} - {dr['by']} - {dr['content']}")
elif page.startswith("GP"):
    st.subheader("GP"); gp = load_json(FILES["gp"], st.session_state.gp)
    gp_t = st.text_input("GP Title *", key="gp_t"); gp_c = st.text_area("GP Details *", key="gp_c")
    if st.button("Save GP", type="primary", key="gp_s"):
        gp.append({"id":int(time.time()),"title":gp_t.strip(),"content":gp_c.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["gp"], gp); st.success("Saved!"); st.rerun()
    for gpr in reversed(gp):
        st.info(f"{gpr['title']} - {gpr['by']} - {gpr['content']}")
elif page.startswith("Finance"):
    st.subheader("Finance - MICROSOFT TEAMS AND MICROSOFT OFFICE - Finance Can Access All")
    office_buttons()
    fin = load_json(FILES["finance"], st.session_state.finance)
    f_t = st.text_input("Finance Title *", key="fin_t"); f_d = st.text_area("Description", key="fin_d"); f_f = st.file_uploader("Upload ANY FILE - Excel, Word, PDF, ANY FILE - upload direct", key="fin_f"); f_amount = st.number_input("Amount UGX", min_value=0, step=1000, key="fin_amount")
    if st.button("Save Finance Report", type="primary", key="fin_s2"):
        fname = ""; fpath = ""
        if f_f:
            fname = f_f.name.replace(" ","_"); fpath = f"data/documents/finance_{int(time.time())}_{fname}"; write_encrypted_file(fpath, f_f.getvalue())
        fin.append({"id":int(time.time()),"title":f_t.strip(),"description":f_d.strip(),"amount":f_amount,"file_name":fname,"file_path":fpath,"by":user_full,"date":dt.now().strftime("%Y-%m-%d %H:%M")}); save_json(FILES["finance"], fin); st.success("Finance saved encrypted!"); st.balloons(); st.rerun()
    for idx, fd in enumerate(reversed(fin)):
        with st.container(border=True):
            st.markdown(f"{fd['title']} - UGX {fd.get('amount',0):,}")
            if fd.get('file_path',''):
                show_any_file(fd['file_path'], fd.get('file_name','')); download_and_keep(fd['file_path'], fd.get('file_name',''), key=f"dl_fin_{fd['id']}_{idx}")
elif page.startswith("Secret"):
    st.subheader("Secret"); sec = load_json(FILES["docs"], st.session_state.docs)
    dc = st.selectbox("Category", DOC_CATS, key="sec_cat"); dt_ = st.text_input("Title *", key="sec_t"); dd = st.text_area("Description", key="sec_d")
    if st.button("Save Secret", type="primary", key="sec_s"):
        sec.append({"id":int(time.time()),"category":dc,"title":dt_.strip(),"description":dd.strip(),"by":user_full,"date":dt.now().strftime("%Y-%m-%d")}); save_json(FILES["docs"], sec); st.success("Saved!"); st.rerun()
    for d in reversed(sec):
        st.write(f"{d['category']} | {d['title']} - {d['description']}")
elif page.startswith("Cabinet"):
    st.subheader("Cabinet Archive"); cabs = load_json(FILES["cabinets"], st.session_state.cabinets)
    cy = st.text_input("Year *", key="cab_y"); cn = st.text_input("Cabinet Name *", key="cab_n"); cm = st.text_area("Members List *", key="cab_m"); cp = st.file_uploader("Group Photo - ANY FILE", key="cab_p")
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

st.markdown("---"); st.markdown(f"<p style='text-align:center;color:#000000;'>UNIK BEC UNASNM | Friendly and Clear to See | All Rights Reserved To The Maker, Right Hon. Speaker | {dt.now().year}</p>", unsafe_allow_html=True)
