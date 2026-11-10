import streamlit as st, os, json, pandas as pd, time, re, hashlib, base64, secrets, urllib.parse, urllib.request
from datetime import datetime as dt
try:
    from cryptography.fernet import Fernet
except Exception:
    Fernet = None

# ===== ONLY CHANGE THIS ONE LINE - PASTE YOUR KEY HERE, INSIDE THE QUOTES =====
GITHUB_TOKEN = "PASTE_YOUR_KEY_HERE"
GITHUB_REPO = "Lawrence-beep-jpg/unik-bec-system"
GITHUB_BRANCH = "main"
# ===== DO NOT CHANGE ANYTHING ELSE BELOW =====

st.set_page_config(page_title="UNIK BEC UNASNM Portal", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")
os.makedirs("data/media_files", exist_ok=True)
os.makedirs("data/documents", exist_ok=True)

MAKER_NAME = "Right Hon. Speaker - Hon. Lawrence Ssango"
MEET_LINK = "https://meet.google.com/abc-defg-hij"
PUBLIC_VOTE_URL = "https://unik-bec-system-edudyqeshonywrcnjthl8l.streamlit.app/?public=vote"

def _secret(name):
    try:
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""
if GITHUB_TOKEN == "PASTE_YOUR_KEY_HERE" or not GITHUB_TOKEN.strip():
    GITHUB_TOKEN = _secret("GITHUB_TOKEN")
if not GITHUB_REPO.strip():
    GITHUB_REPO = _secret("GITHUB_REPO") or "Lawrence-beep-jpg/unik-bec-system"
GH_ON = bool(GITHUB_TOKEN and GITHUB_TOKEN != "PASTE_YOUR_KEY_HERE" and GITHUB_REPO)

def _gh_req(url, method="GET", data=None):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "unik-bec-portal")
    return urllib.request.urlopen(req, timeout=30)

def gh_get_bytes(path):
    if not GH_ON: return None
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{urllib.parse.quote(path)}?ref={GITHUB_BRANCH}"
        with _gh_req(url) as r:
            j = json.loads(r.read().decode("utf-8"))
        return base64.b64decode(j.get("content", ""))
    except Exception:
        return None

def gh_put_bytes(path, content_bytes, message):
    if not GH_ON: return False
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{urllib.parse.quote(path)}"
        sha = None
        try:
            with _gh_req(url + f"?ref={GITHUB_BRANCH}") as r:
                sha = json.loads(r.read().decode("utf-8")).get("sha")
        except Exception:
            sha = None
        payload = {"message": message, "content": base64.b64encode(content_bytes).decode("utf-8"), "branch": GITHUB_BRANCH}
        if sha: payload["sha"] = sha
        with _gh_req(url, method="PUT", data=json.dumps(payload).encode("utf-8")) as r:
            return r.status in (200, 201)
    except Exception as e:
        st.warning(f"GitHub save failed for {path}: {e}")
        return False

def gh_save_json(name, data):
    return gh_put_bytes(f"data/{name}.json", json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"), f"Save {name} - UNIK BEC Portal")

def gh_load_json(name, default):
    b = gh_get_bytes(f"data/{name}.json")
    if b:
        try: return json.loads(b.decode("utf-8"))
        except Exception: return default
    return default

def _load(name, default):
    if GH_ON:
        v = gh_load_json(name, None)
        if v is not None: return v
    p = f"data/{name}.json"
    try:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: pass
    return default

def _save(name, data):
    p = f"data/{name}.json"
    try:
        with open(p, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception: pass
    if GH_ON: gh_save_json(name, data)
    st.session_state[f"db_{name}"] = data
    return data

def load_all():
    return {
        "reports": _load("reports", []),
        "votes": _load("votes", []),
        "candidates": _load("candidates", [
            {"id": "cand_1", "name": "SSANGO LAWRENCE", "position": "Right Hon. Speaker - Hon. Lawrence Ssango", "votes": 0},
            {"id": "cand_2", "name": "Candidate 2", "position": "Right Hon. Speaker", "votes": 0},
        ]),
        "documents": _load("documents", []),
        "media": _load("media", []),
        "cabinet": _load("cabinet", []),
        "audit": _load("audit", []),
        "finance": _load("finance", []),
        "disciplinary": _load("disciplinary", []),
        "gp": _load("gp", []),
        "secret": _load("secret", []),
        "super4": _load("super4", []),
        "notices": _load("notices", [{"title": "Public Portal OPEN", "body": "Tap Green Button, Go Straight To Google Meet, Meet Direct - No Login, No Waiting", "time": str(dt.now())}]),
        "settings": _load("settings", {"meet_link": MEET_LINK, "password": "unik123", "maker_password": "maker123"}),
        "users": _load("users", [{"name": MAKER_NAME, "role": "Maker", "password": "maker123"}]),
    }

if "DB" not in st.session_state:
    st.session_state.DB = load_all()
DB = st.session_state.DB

def save(name): _save(name, DB[name])
def audit(action, who="System"):
    DB["audit"].append({"time": str(dt.now())[:19], "who": who, "action": action}); save("audit")
def uid(): return f"{int(time.time())}_{secrets.token_hex(3)}"
def safe_name(n): return re.sub(r"[^A-Za-z0-9_.-]", "_", str(n))

def save_file_to_github_and_local(folder, stored_name, content_bytes):
    fp = os.path.join(folder, stored_name)
    open(fp, "wb").write(content_bytes)
    if GH_ON: gh_put_bytes(f"{folder}/{stored_name}", content_bytes, f"Upload file {stored_name} - UNIK BEC Portal")
    return fp

def get_file_bytes(folder, stored_name):
    fp = os.path.join(folder, stored_name)
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        return open(fp, "rb").read(), fp
    if GH_ON:
        b = gh_get_bytes(f"{folder}/{stored_name}")
        if b:
            open(fp, "wb").write(b)
            return b, fp
    return None, fp

if "user" not in st.session_state: st.session_state.user = None
if "maker" not in st.session_state: st.session_state.maker = False
params = st.query_params
is_public_vote = params.get("public", "") == "vote"

st.title("🏛️ UNIK BEC UNASNM")
st.subheader("Governance Portal - FILES KEPT IN GITHUB, THEY COME BACK AFTER REBOOT")
if GH_ON: st.success("✅ GitHub Storage is ON. Your files will come back after reboot / sleep.")
else: st.error("⚠️ GitHub Storage is OFF. Paste your key in the top line of app.py and save again.")
st.markdown(f"**Logged:** {st.session_state.user['name'] if st.session_state.user else 'Guest - Public Portal OPEN'}")
if st.session_state.maker: st.success(f"🔓 MAKER MODE: You Can Make Changes - {MAKER_NAME}")
else: st.info("🔒 ONLY MAKER CAN: Delete, Approve, Change Password, Change Settings, Change Google Meet Link. ALL CAN: Upload, Download, Vote, Join Google Meet Direct, Submit Reports.")

meet = DB["settings"].get("meet_link", MEET_LINK)
st.link_button("📞 JOIN GOOGLE MEET NOW - TAP HERE, GO STRAIGHT TO MEET, NO LOGIN", meet, type="primary", use_container_width=True)
st.markdown(f"📞 **MEET LINK:** {meet}")
st.markdown(f"🗳️ **PUBLIC STUDENT VOTING LINK:** {PUBLIC_VOTE_URL}")

with st.sidebar:
    st.header("Login")
    if not st.session_state.user:
        nm = st.text_input("Your Name", key="login_name")
        pw = st.text_input("Password (leave blank for public)", type="password", key="login_pw")
        if st.button("Enter Portal", key="btn_enter"):
            if nm.strip().lower().startswith("lawrence") or pw == DB["settings"].get("maker_password"):
                st.session_state.user = {"name": MAKER_NAME, "role": "Maker"}; st.session_state.maker = True; audit("Maker logged in", MAKER_NAME)
            elif nm.strip():
                st.session_state.user = {"name": nm.strip(), "role": "Student"}; audit(f"{nm.strip()} entered portal", nm.strip())
            st.rerun()
    else:
        st.write(f"👤 {st.session_state.user['name']}")
        if st.button("Log Out", key="btn_logout"):
            st.session_state.user = None; st.session_state.maker = False; st.rerun()
    st.markdown("---")
    if st.session_state.maker:
        st.subheader("Maker Settings")
        new_meet = st.text_input("Google Meet Link", value=meet, key="set_meet")
        new_pw = st.text_input("Change Portal Password", value=DB["settings"].get("password",""), key="set_pw")
        if st.button("Save Settings", key="btn_save_settings"):
            DB["settings"]["meet_link"] = new_meet; DB["settings"]["password"] = new_pw; save("settings"); audit("Maker changed settings", MAKER_NAME); st.success("Saved. It will stay after reboot."); st.rerun()

who = st.session_state.user["name"] if st.session_state.user else "Guest"
is_maker = st.session_state.maker
tabs = st.tabs(["📊 Dashboard","👤 My Personal Portal","📢 Public Portal","🎥 Meeting","📝 Submit Report","🔒 Private SUPER 4","🗳️ Electoral","⚖️ Disciplinary","📋 GP","💰 Finance 5 ONLY","🔐 Secret","📄 Documents","📸 Media Gallery","🏛️ Cabinet Archive","📜 Audit Log"])

with tabs[0]:
    st.header("📊 Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Reports", len(DB["reports"])); c2.metric("Votes Cast", len(DB["votes"])); c3.metric("Documents", len(DB["documents"])); c4.metric("Media Files", len(DB["media"]))
    for i, n in enumerate(DB["notices"]):
        st.write(f"✅ **{n.get('title','')}** - {n.get('body','')}")
        if is_maker and st.button("Delete notice", key=f"del_notice_{i}"):
            DB["notices"].pop(i); save("notices"); st.rerun()
    if is_maker:
        t = st.text_input("New notice title", key="nt_title"); b = st.text_area("Notice body", key="nt_body")
        if st.button("Add Notice", key="btn_notice"):
            DB["notices"].append({"title": t, "body": b, "time": str(dt.now())}); save("notices"); audit("Added notice", who); st.rerun()

with tabs[1]:
    st.header("👤 My Personal Portal")
    st.write(f"Name: **{who}** | Role: **{'Maker' if is_maker else 'Student / Guest'}**")
    mine = [r for r in DB["reports"] if r.get("who")==who]
    for r in mine: st.write(f"- {r.get('title','')} - {r.get('time','')}")
    if not mine: st.write("No reports yet. Go to Submit Report.")

with tabs[2]:
    st.header("📢 Public Portal OPEN")
    st.link_button("📞 JOIN GOOGLE MEET - GO STRAIGHT", meet, type="primary")

with tabs[3]:
    st.header("🎥 Meeting - GOOGLE MEET DIRECT")
    st.link_button("📞 JOIN GOOGLE MEET NOW", meet, type="primary", use_container_width=True)
    st.code(meet)

with tabs[4]:
    st.header("📝 Submit Report")
    rt = st.text_input("Report Title *", key="rep_title"); rb = st.text_area("Report Body - type, copy paste", key="rep_body")
    rf = st.file_uploader("Upload Word / Excel / PowerPoint / PDF", type=["docx","xlsx","pptx","pdf","txt"], key="rep_file")
    if st.button("Submit Report", key="btn_rep"):
        if not rt.strip(): st.error("Title is needed")
        else:
            item = {"id": uid(), "title": rt, "body": rb, "who": who, "time": str(dt.now())[:19], "file_name": "", "approved": is_maker}
            if rf is not None:
                fn = f"{uid()}_{safe_name(rf.name)}"; save_file_to_github_and_local("data/documents", fn, rf.getbuffer()); item["file_name"] = rf.name; item["stored"] = fn
            DB["reports"].append(item); save("reports"); audit(f"Submitted report: {rt}", who); st.success("Report saved in GitHub. It will stay after reboot."); st.rerun()
    for idx, r in enumerate(DB["reports"]):
        st.markdown(f"**{r.get('title','')}** - {r.get('who','')} - {r.get('time','')}")
        st.write(r.get("body","")[:500])
        if r.get("stored"):
            b, fp = get_file_bytes("data/documents", r["stored"])
            if b: st.download_button(f"⬇️ Download {r.get('file_name','file')}", b, file_name=r.get("file_name","file"), key=f"dl_rep_{r['id']}_{idx}")
        if is_maker and st.button("Delete report", key=f"del_rep_{r['id']}_{idx}"):
            DB["reports"].pop(idx); save("reports"); st.rerun()

with tabs[5]:
    st.header("🔒 Private SUPER 4")
    if not is_maker: st.warning("Only Maker / SUPER 4 can see this.")
    else:
        txt = st.text_area("SUPER 4 Note", key="s4_txt")
        if st.button("Save SUPER 4", key="btn_s4"):
            DB["super4"].append({"id": uid(), "text": txt, "who": who, "time": str(dt.now())[:19]}); save("super4"); st.rerun()
        for s in DB["super4"]: st.write(f"- {s.get('text','')} ({s.get('time','')})")

with tabs[6]:
    st.header("🗳️ Electoral OPEN")
    vname = st.text_input("Your Full Name for Voting", key="vote_name", value=who if who!="Guest" else "")
    for idx, cand in enumerate(DB["candidates"]):
        col1, col2 = st.columns([3,1])
        col1.write(f"**{cand['name']}** - {cand['position']} - Votes: {cand.get('votes',0)}")
        if col2.button(f"Vote {cand['name'][:12]}", key=f"vote_btn_{cand['id']}_{idx}"):
            if not vname.strip(): st.error("Type your name first")
            elif any(v.get("voter")==vname.strip() for v in DB["votes"]): st.error("You already voted. Your vote is saved.")
            else:
                cand["votes"] = cand.get("votes",0)+1; DB["votes"].append({"voter": vname.strip(), "candidate": cand["name"], "time": str(dt.now())[:19]}); save("candidates"); save("votes"); audit(f"Vote for {cand['name']}", vname.strip()); st.success("Vote saved in GitHub."); st.rerun()
    if is_maker:
        cn = st.text_input("New Candidate Name", key="cand_name"); cp = st.text_input("Position", key="cand_pos", value="Right Hon. Speaker")
        if st.button("Add Candidate", key="btn_cand"):
            DB["candidates"].append({"id": uid(), "name": cn, "position": cp, "votes": 0}); save("candidates"); st.rerun()

with tabs[7]:
    st.header("⚖️ Disciplinary OPEN")
    dt_title = st.text_input("Case Title", key="disc_title"); dt_body = st.text_area("Case Details", key="disc_body")
    if st.button("Submit Case", key="btn_disc"):
        DB["disciplinary"].append({"id": uid(), "title": dt_title, "body": dt_body, "who": who, "time": str(dt.now())[:19]}); save("disciplinary"); st.rerun()
    for d in DB["disciplinary"]: st.write(f"- **{d.get('title','')}** by {d.get('who','')} - {d.get('body','')[:200]}")

with tabs[8]:
    st.header("📋 GP OPEN")
    g = st.text_area("GP Entry", key="gp_txt")
    if st.button("Save GP", key="btn_gp"):
        DB["gp"].append({"id": uid(), "text": g, "who": who, "time": str(dt.now())[:19]}); save("gp"); st.rerun()
    for x in DB["gp"]: st.write(f"- {x.get('text','')} ({x.get('who','')})")

with tabs[9]:
    st.header("💰 Finance 5 ONLY")
    if not is_maker: st.warning("Finance is for 5 ONLY / Maker.")
    else:
        fa = st.text_input("Finance Item", key="fin_item"); fam = st.number_input("Amount", min_value=0, key="fin_amt")
        if st.button("Save Finance", key="btn_fin"):
            DB["finance"].append({"id": uid(), "item": fa, "amount": fam, "time": str(dt.now())[:19]}); save("finance"); st.rerun()
        for f in DB["finance"]: st.write(f"- {f.get('item','')} : {f.get('amount','')}")

with tabs[10]:
    st.header("🔐 Secret OPEN")
    s = st.text_area("Secret Entry", key="sec_txt")
    if st.button("Save Secret", key="btn_sec"):
        DB["secret"].append({"id": uid(), "text": s, "who": who, "time": str(dt.now())[:19]}); save("secret"); st.rerun()
    for x in DB["secret"]: st.write(f"- {x.get('text','')[:200]}")

with tabs[11]:
    st.header("📄 Documents OPEN")
    up = st.file_uploader("Upload Document", type=["docx","xlsx","pptx","pdf","txt","png","jpg"], key="doc_up")
    dtitle = st.text_input("Document Title", key="doc_title")
    if st.button("Upload Document", key="btn_doc") and up is not None:
        fn = f"{uid()}_{safe_name(up.name)}"; save_file_to_github_and_local("data/documents", fn, up.getbuffer())
        DB["documents"].append({"id": uid(), "title": dtitle or up.name, "file_name": up.name, "stored": fn, "who": who, "time": str(dt.now())[:19]}); save("documents"); audit(f"Uploaded document {up.name}", who); st.success("Document saved in GitHub."); st.rerun()
    for idx, d in enumerate(DB["documents"]):
        st.write(f"📄 **{d.get('title','')}** - {d.get('who','')} - {d.get('time','')}")
        b, fp = get_file_bytes("data/documents", d.get("stored",""))
        if b: st.download_button(f"⬇️ Download {d['file_name']}", b, file_name=d['file_name'], key=f"dl_doc_{d['id']}_{idx}")
        if is_maker and st.button("Delete document", key=f"del_doc_{d['id']}_{idx}"):
            DB["documents"].pop(idx); save("documents"); st.rerun()

with tabs[12]:
    st.header("📸 Media Gallery - ALL CAN UPLOAD!")
    mt = st.text_input("Media Title *", key="med_title")
    mf = st.file_uploader("File * - photo, audio, video", type=["png","jpg","jpeg","mp3","mp4","wav"], key="med_file")
    if st.button("Upload Media", key="btn_med"):
        if mf is None: st.error("Choose a file first")
        elif not mt.strip(): st.error("Type a title first")
        else:
            fn = f"{uid()}_{safe_name(mf.name)}"; save_file_to_github_and_local("data/media_files", fn, mf.getbuffer())
            DB["media"].append({"id": uid(), "title": mt, "file_name": mf.name, "stored": fn, "who": who, "time": str(dt.now())[:19]}); save("media"); audit(f"Uploaded media {mf.name}", who); st.success("Media saved in GitHub. It will come back after reboot."); st.rerun()
    for idx, m in enumerate(DB["media"]):
        st.markdown(f"**{m.get('title','')}** - {m.get('who','')} - {m.get('time','')}")
        b, fp = get_file_bytes("data/media_files", m.get("stored",""))
        if b:
            low = m["file_name"].lower()
            if low.endswith((".png",".jpg",".jpeg")): st.image(b, width=300)
            elif low.endswith((".mp3",".wav")): st.audio(b)
            elif low.endswith(".mp4"): st.video(b)
            st.download_button(f"⬇️ Download {m['file_name']}", b, file_name=m['file_name'], key=f"dl_med_{m['id']}_{idx}")
        else: st.write("(File not found yet. Paste your key in the top line and save again.)")
        if is_maker and st.button("Delete media", key=f"del_med_{m['id']}_{idx}"):
            DB["media"].pop(idx); save("media"); st.rerun()

with tabs[13]:
    st.header("🏛️ Cabinet Archive OPEN")
    ca = st.text_area("Cabinet Entry", key="cab_txt")
    if st.button("Save Cabinet", key="btn_cab"):
        DB["cabinet"].append({"id": uid(), "text": ca, "who": who, "time": str(dt.now())[:19]}); save("cabinet"); st.rerun()
    for x in DB["cabinet"]: st.write(f"- {x.get('text','')} ({x.get('time','')})")

with tabs[14]:
    st.header("📜 Audit Log")
    for a in reversed(DB["audit"][-100:]):
        st.write(f"{a.get('time','')} - {a.get('who','')} - {a.get('action','')}")

st.markdown("---")
st.markdown(f"🔒 ALL RIGHTS RESERVED TO THE MAKER: {MAKER_NAME}. Everything Stays As Maker Said.")
if is_public_vote: st.info("You came from the Public Voting Link. Go to Electoral tab to vote.")
