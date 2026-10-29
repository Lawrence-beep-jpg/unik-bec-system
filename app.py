import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="UNIK BEC-UNASNM FINAL SYSTEM", page_icon="🏛️", layout="wide")

try:
    c1,c2,c3 = st.columns([1,3,1])
    with c1: st.image("unik_badge.png", width=110)
    with c2: st.image("header.png", use_container_width=True)
    with c3: st.image("unasnm_badge.png", width=110)
except:
    st.title("🏛️ UNIK - University of Kisubi | BEC-UNASNM")
    st.caption("Final System - Hon. Lawrence Ssango - Speaker BEC")

USERS = {
    "principal": "Hon. Principal - University of Kisubi",
    "patron": "Hon. Patron - UNASNM",
    "president": "Hon. President - UNASNM BEC",
    "vice_president": "Hon. Vice President - BEC",
    "speaker": "Hon. Lawrence Ssango - Speaker BEC (Chair Electoral & Disciplinary)",
    "general_secretary": "Hon. General Secretary",
    "finance": "Hon. Finance Secretary - Ministry of Finance",
    "information": "Hon. Information Secretary",
    "class_rep": "Hon. Class Representative",
    "grc_male": "Hon. GRC - Male",
    "grc_female": "Hon. GRC - Female",
    "hostel_male": "Hon. Hostel - Male",
    "hostel_female": "Hon. Hostel - Female",
    "nursing_affairs": "Hon. Nursing Affairs",
    "electoral_commission": "Electoral Commission Office",
    "disciplinary_committee": "Disciplinary Committee Office",
    "general_purpose": "General Purpose Committee Office"
}
LOGIN_USERS = ["principal","patron","president","vice_president","speaker","general_secretary","finance","information","class_rep","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]

PASSWORD = "unik2025"
SUPER_ALL_ACCESS = ["principal","patron","president","speaker","general_secretary"]
ELECTORAL_DISCIPLINARY_VIEWERS = ["principal","patron","president","speaker"]
GENERAL_PURPOSE_VIEWERS = ["principal","patron","president","speaker","vice_president"]
SECRET_STORE_ACCESS = ["principal","patron","president","speaker","general_secretary"]

REPORT_TYPES = ["Weekly Report","Monthly Report","Financial Report (Excel/PowerPoint)","Activity Report","GRC Report","Hostel Report","Nursing Affairs Report","Class Report","Electoral Report","Disciplinary Report","General Purpose Report","Other"]
DOC_CATEGORIES = ["Constitution","Annual Work Plan","Budget","Meeting Minutes","Strategic Plan","Rules & Regulations","Finance PowerPoint","Finance Spreadsheet","Other Secret Document"]
ELECTION_POSITIONS = ["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]

for key in ['reports','documents','candidates','votes','media','electoral_reports','disciplinary_reports','gp_reports','finance_docs']:
    if key not in st.session_state: st.session_state[key] = []
if 'election_open' not in st.session_state: st.session_state.election_open = False
if 'election_title' not in st.session_state: st.session_state.election_title = "UNIK BEC General Elections 2025/2026"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user' not in st.session_state: st.session_state.user = ""

if not st.session_state.logged_in:
    st.divider()
    st.subheader("🔐 BEC-UNASNM Secure Login - All 13 Departments")
    u = st.selectbox("Select Your Office (13 Departments)", LOGIN_USERS, format_func=lambda x: USERS[x], key="login_office_final_full")
    p = st.text_input("Enter Password", type="password", key="login_pass_final_full")
    if st.button("🔐 LOGIN TO SYSTEM", use_container_width=True, type="primary", key="login_btn_final_full"):
        if p == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("❌ Wrong Password! Use: unik2025 - Error correction: Check spelling")
    st.info("💡 Speaker Hon. Lawrence Ssango is Chair of Electoral & Disciplinary")
    st.stop()

user = st.session_state.user
user_full = USERS[user]

st.sidebar.title(f"👤 {user_full}")
if user in SUPER_ALL_ACCESS: st.sidebar.success("✅ SUPER ACCESS - Can view ALL")
if user == "speaker": st.sidebar.warning("👑 CHAIR - Electoral & Disciplinary")
if user == "vice_president": st.sidebar.info("📋 LEADER - General Purpose")
if st.sidebar.button("🚪 Logout", use_container_width=True, key="logout_final_all"):
    st.session_state.logged_in = False; st.rerun()

st.divider()
def can_view_all(v): return v in SUPER_ALL_ACCESS
def can_view_electoral(v): return v in ELECTORAL_DISCIPLINARY_VIEWERS
def can_view_disciplinary(v): return v in ELECTORAL_DISCIPLINARY_VIEWERS
def can_view_gp(v): return v in GENERAL_PURPOSE_VIEWERS
def can_view_secret_store(v): return v in SECRET_STORE_ACCESS

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📝 Submit Report (13 Depts)", 
    "📂 My Department Portal", 
    "🗳️ Electoral Commission Portal", 
    "⚖️ Disciplinary Committee", 
    "📋 General Purpose Committee", 
    "💰 Finance Ministry (Excel/PPT)", 
    "🔐 Secret Store", 
    "📸 Media Gallery"
])

with tab1:
    st.subheader("📝 Submit Departmental Report - All 13 Departments")
    rt = st.selectbox("Select Report Type", REPORT_TYPES, key="report_type_final_1")
    rtitle = st.text_input("Report Title *", key="report_title_final_1")
    rdept = st.selectbox("Department", LOGIN_USERS, format_func=lambda x: USERS[x], index=LOGIN_USERS.index(user) if user in LOGIN_USERS else 0, key="report_dept_final_1")
    rcontent = st.text_area("Report Details *", height=200, key="report_content_final_1")
    rfile = st.file_uploader("Attach File (Excel/PowerPoint/PDF/Photo)", type=["xlsx","xls","pptx","ppt","pdf","jpg","png","jpeg","docx"], key="report_file_final_1")
    if st.button("📤 SUBMIT REPORT", type="primary", use_container_width=True, key="report_submit_final_1"):
        if not rtitle.strip() or not rcontent.strip():
            st.error("❌ ERROR: Title and Details required! Please correct mistake")
        else:
            st.session_state.reports.append({"id": len(st.session_state.reports)+1,"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from": rdept,"from_name": USERS[rdept],"actual_submitter": user,"type": rt,"title": rtitle.strip(),"content": rcontent.strip(),"file_name": rfile.name if rfile else None,"file_bytes": rfile.getvalue() if rfile else None,"status": "Pending"})
            st.success(f"✅ Submitted to {USERS[rdept]} portal!"); st.balloons()

with tab2:
    st.subheader(f"📂 {user_full} - My Department Portal (Private)")
    st.info("🔒 Only you + Principal/Patron/President/Speaker/Gen Secretary can view. Others CANNOT access.")
    my_reports = [r for r in st.session_state.reports if (r['from']==user or can_view_all(user))]
    if not can_view_all(user): my_reports = [r for r in my_reports if r['from']==user]
    if not my_reports: st.warning("No reports in your portal yet")
    else:
        st.dataframe(pd.DataFrame(my_reports)[["id","date","from_name","type","title","status"]].sort_values(by="id", ascending=False), use_container_width=True)
        for r in reversed(my_reports):
            with st.expander(f"#{r['id']} | {r['title']}"):
                st.info(r['content'])
                if r.get('file_bytes'): st.download_button(f"📥 Download {r['file_name']}", r['file_bytes'], r['file_name'], key=f"dl_my_{r['id']}_final")
                st.write("✏️ Error Correction:")
                new_title = st.text_input(f"Edit Title #{r['id']}", value=r['title'], key=f"edit_title_{r['id']}_final")
                new_content = st.text_area(f"Edit Content #{r['id']}", value=r['content'], key=f"edit_content_{r['id']}_final", height=100)
                c1,c2 = st.columns(2)
                with c1:
                    if st.button(f"✅ Correct & Save #{r['id']}", key=f"save_edit_{r['id']}_final"): r['title']=new_title; r['content']=new_content; st.success("✅ Corrected!"); st.rerun()
                with c2:
                    if st.button(f"🗑️ Delete #{r['id']}", key=f"del_my_{r['id']}_final"): st.session_state.reports=[x for x in st.session_state.reports if x['id']!=r['id']]; st.rerun()

with tab3:
    if not can_view_electoral(user):
        st.error("🔒 ACCESS DENIED - Electoral Commission Portal only for Speaker (Chair), Principal, Patron, President"); st.stop()
    st.subheader("🗳️ ELECTORAL COMMISSION PORTAL - Chair: Hon. Lawrence Ssango")
    st.success(f"✅ Access: {user_full}")
    if user == "speaker":
        if not st.session_state.election_open:
            if st.button("🟢 OPEN ELECTORAL VOTING", type="primary", use_container_width=True, key="open_elect_final"): st.session_state.election_open=True; st.rerun()
        else:
            if st.button("🔴 CLOSE ELECTORAL VOTING", use_container_width=True, key="close_elect_final"): st.session_state.election_open=False; st.rerun()
    st.write(f"Status: {'🟢 OPEN' if st.session_state.election_open else '🔴 CLOSED'}")
    ta,tb,tc,td = st.tabs(["Register Candidate","Vote","Results","Electoral Reports"])
    with ta:
        rp = st.selectbox("Position to Contest", ELECTION_POSITIONS, format_func=lambda x: USERS[x], key="cand_pos_elect_final")
        rn = st.text_input("Full Names *", key="cand_name_elect_final")
        rclass = st.text_input("Class *", key="cand_class_elect_final")
        rcourse = st.text_input("Course *", key="cand_course_elect_final")
        rres = st.text_input("Previous Results *", key="cand_res_elect_final")
        rreason = st.text_area("Reason Why Contesting *", key="cand_reason_elect_final")
        rphoto = st.file_uploader("Candidate Photo *", type=["jpg","png","jpeg"], key="cand_photo_elect_final")
        if st.button("📝 Submit Candidature", type="primary", use_container_width=True, key="cand_submit_elect_final"):
            if rn and rclass and rcourse and rres and rreason and rphoto:
                st.session_state.candidates.append({"id":len(st.session_state.candidates)+1,"position":rp,"position_name":USERS[rp],"name":rn,"class":rclass,"course":rcourse,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue(),"registered_by":user})
                st.success("✅ Registered!"); st.balloons()
            else: st.error("❌ ERROR: Fill ALL * fields + Photo")
    with tb:
        if not st.session_state.election_open: st.error("Voting CLOSED by Electoral Chair")
        else:
            vp = st.selectbox("Position to Vote", ELECTION_POSITIONS, format_func=lambda x: USERS[x], key="vote_pos_elect_final")
            for c in [x for x in st.session_state.candidates if x['position']==vp]:
                with st.container(border=True):
                    st.image(c['photo_bytes'], width=150)
                    st.write(f"**{c['name']}** - {c['class']} | {c['course']}")
                    if st.button(f"✅ Vote {c['name']}", key=f"vote_{c['id']}_elect_final", type="primary"):
                        if [v for v in st.session_state.votes if v['voter']==user and v['position']==vp]: st.error("❌ Already voted for this position!")
                        else: st.session_state.votes.append({"voter":user,"position":vp,"candidate_id":c['id']}); st.success("✅ Voted!"); st.rerun()
    with tc:
        for pos in ELECTION_POSITIONS:
            cs = [c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                st.write(f"**{USERS[pos]}**")
                rd = [{"Candidate":c['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==c['id']])} for c in cs]
                st.dataframe(pd.DataFrame(rd), use_container_width=True)
                if rd: st.bar_chart(pd.DataFrame(rd).set_index("Candidate"))
    with td:
        er_title = st.text_input("Electoral Report Title *", key="elect_report_title_final")
        er_content = st.text_area("Electoral Report Details *", key="elect_report_content_final")
        if st.button("Save Electoral Report", key="elect_report_save_final"):
            if er_title and er_content:
                st.session_state.electoral_reports.append({"id":len(st.session_state.electoral_reports)+1,"title":er_title,"content":er_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success("Saved!")
        for er in reversed(st.session_state.electoral_reports):
            with st.expander(f"{er['title']}"): st.info(er['content'])

with tab4:
    if not can_view_disciplinary(user): st.error("🔒 ACCESS DENIED - Disciplinary only for Speaker, Principal, Patron, President"); st.stop()
    st.subheader("⚖️ DISCIPLINARY COMMITTEE PORTAL - Chair: Hon. Lawrence Ssango")
    d_title = st.text_input("Disciplinary Case Title *", key="disc_title_final")
    d_content = st.text_area("Case Details / Action *", height=150, key="disc_content_final")
    d_file = st.file_uploader("Attach Evidence", key="disc_file_final")
    if st.button("⚖️ Save Disciplinary Report", type="primary", use_container_width=True, key="disc_save_final"):
        if d_title and d_content:
            st.session_state.disciplinary_reports.append({"id":len(st.session_state.disciplinary_reports)+1,"title":d_title,"content":d_content,"file_name":d_file.name if d_file else None,"file_bytes":d_file.getvalue() if d_file else None,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            st.success("✅ Saved!")
        else: st.error("❌ ERROR: Fill title and details")
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(f"#{dr['id']} {dr['title']}"): st.warning(dr['content'])

with tab5:
    if not can_view_gp(user): st.error("🔒 ACCESS DENIED - General Purpose only for VP (Leader), Principal, Patron, President, Speaker"); st.stop()
    st.subheader("📋 GENERAL PURPOSE COMMITTEE - Leader: Vice President")
    st.caption("Leader: Vice President (uses President portal) | Viewers: Principal, Patron, President, Speaker, VP")
    gp_title = st.text_input("General Purpose Title *", key="gp_title_final")
    gp_content = st.text_area("General Purpose Details *", height=150, key="gp_content_final")
    gp_file = st.file_uploader("Attach File", key="gp_file_final")
    if st.button("📋 Save GP Report", type="primary", use_container_width=True, key="gp_save_final"):
        if gp_title and gp_content:
            st.session_state.gp_reports.append({"id":len(st.session_state.gp_reports)+1,"title":gp_title,"content":gp_content,"file_name":gp_file.name if gp_file else None,"file_bytes":gp_file.getvalue() if gp_file else None,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            st.success("✅ Saved!")
        else: st.error("❌ ERROR: Fill required fields")
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(f"#{gpr['id']} {gpr['title']} - {gpr['by']}"): st.info(gpr['content'])

with tab6:
    st.subheader("💰 FINANCE MINISTRY - Excel / PowerPoint Reports")
    if user == "finance" or can_view_all(user):
        f_title = st.text_input("Finance Report Title *", key="fin_title_final")
        f_type = st.selectbox("Finance Document Type", ["Budget Spreadsheet (Excel)","Financial Report PowerPoint","Bank Statement","Expense Report","Other"], key="fin_type_final")
        f_desc = st.text_area("Description *", key="fin_desc_final")
        f_excel = st.file_uploader("Upload Excel / PowerPoint *", type=["xlsx","xls","pptx","ppt","pdf","csv"], key="fin_file_final")
        if st.button("💰 Save Finance Document", type="primary", use_container_width=True, key="fin_save_final"):
            if not f_title or not f_desc or not f_excel:
                st.error("❌ ERROR: Title + Description + Excel/PPT File required! Finance must upload spreadsheet or PowerPoint")
            else:
                st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title,"type":f_type,"description":f_desc,"file_name":f_excel.name,"file_bytes":f_excel.getvalue(),"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success(f"✅ Finance Saved: {f_excel.name}"); st.balloons()
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True):
            st.write(f"**{fd['title']}** - {fd['type']} - {fd['by']}")
            st.download_button(f"📥 Download {fd['file_name']}", fd['file_bytes'], fd['file_name'], key=f"dl_fin_{fd['id']}_final")

with tab7:
    if not can_view_secret_store(user): st.error("🔒 SECRET STORE - Only Principal, Patron, President, Speaker, Gen Secretary"); st.stop()
    st.subheader("🔐 SECRET STORE - Only 5 Authorized")
    dc = st.selectbox("Document Category", DOC_CATEGORIES, key="secret_cat_final_full")
    dt = st.text_input("Secret Document Title *", key="secret_title_final_full")
    dd = st.text_area("Description", key="secret_desc_final_full")
    uf = st.file_uploader("Upload Secret File", key="secret_file_final_full")
    if st.button("🔐 SAVE TO SECRET STORE", type="primary", use_container_width=True, key="secret_save_final_full"):
        if not dt.strip(): st.error("❌ ERROR: Title required")
        else:
            st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"file_name":uf.name if uf else "Note","file_bytes":uf.getvalue() if uf else None,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
            st.success("✅ Saved to SECRET STORE!"); st.rerun()
    for d in reversed(st.session_state.documents):
        with st.expander(f"🔐 {d['category']} | {d['title']}"):
            if d['file_bytes']: st.download_button("Download Secret", d['file_bytes'], d['file_name'], key=f"dl_secret_{d['id']}_final_full")

with tab8:
    st.subheader("📸 MEDIA GALLERY - Photos & Videos")
    if user in SECRET_STORE_ACCESS or user == "information":
        mt = st.text_input("Media Title *", key="media_title_final_full")
        mf = st.file_uploader("Photo/Video", type=["jpg","png","jpeg","mp4","mov"], key="media_file_final_full")
        if st.button("📸 Save to Media Gallery", type="primary", use_container_width=True, key="media_save_final_full"):
            if not mt.strip() or not mf: st.error("❌ ERROR: Title + File required")
            else:
                st.session_state.media.append({"id":len(st.session_state.media)+1,"title":mt.strip(),"file_name":mf.name,"file_bytes":mf.getvalue(),"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success("✅ Media Saved!"); st.balloons(); st.rerun()
    for m in reversed(st.session_state.media):
        with st.container(border=True):
            st.write(f"**{m['title']}** - {m['by']}")
            if "image" in m['file_type']: st.image(m['file_bytes'], use_container_width=True)
            elif "video" in m['file_type']: st.video(m['file_bytes'])
            st.download_button("Download", m['file_bytes'], m['file_name'], key=f"dl_media_{m['id']}_final_full")

st.caption("© UNIK BEC-UNASNM FINAL SYSTEM | Speaker Hon. Lawrence Ssango | 426 lines | All 13 Depts + Electoral + Disciplinary + GP + Finance Excel/PPT + Secret + Media | Error Correction Enabled")
