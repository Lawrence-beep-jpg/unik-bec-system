import streamlit as st
import pandas as pd
import datetime
st.set_page_config(page_title="UNIK BEC FINAL - Password Change", page_icon="🏛️", layout="wide")
try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
except:
    st.title("🏛️ UNIK - BEC-UNASNM FINAL SYSTEM")
    st.caption("Hon. Lawrence Ssango - Speaker BEC")
USERS={"principal":"Hon. Principal","patron":"Hon. Patron","president":"Hon. President","vice_president":"Hon. Vice President - Leader GP","speaker":"Hon. Lawrence Ssango - Speaker BEC","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys())
SUPER_4=["principal","patron","president","speaker"]
FINANCE_5=["principal","patron","president","speaker","finance"]
REPORT_TYPES=["Weekly","Monthly","Financial Excel/PPT","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Other"]
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret"]
ELECTION_POSITIONS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]
for k in ['reports','documents','candidates','votes','media','electoral_reports','disciplinary_reports','gp_reports','finance_docs']:
    if k not in st.session_state: st.session_state[k]=[]
if 'passwords' not in st.session_state: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=False
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

if not st.session_state.logged_in:
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login_office_pw")
    p=st.text_input("Password",type="password",key="login_pass_pw")
    if st.button("🔐 LOGIN",use_container_width=True,type="primary",key="login_btn_pw"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password!")
    st.info("Default: unik2025 | After change, use YOUR OWN password | SUPER 4: Principal, Patron, President, Speaker | Finance 5: + Finance")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
if user in SUPER_4: st.sidebar.success("✅ SUPER 4 - View ALL private")
if user in FINANCE_5: st.sidebar.success("💰 FINANCE 5")
if user=="speaker": st.sidebar.warning("👑 CHAIR Electoral & Disciplinary")

with st.sidebar.expander("🔑 Change My Password - Own Password"):
    st.write(f"Current user: {user_full}")
    new_p=st.text_input("New Password",type="password",key="new_pass_final")
    confirm_p=st.text_input("Confirm New Password",type="password",key="confirm_pass_final")
    if st.button("Save New Password",key="save_pass_final"):
        if not new_p: st.error("Enter new password")
        elif new_p!=confirm_p: st.error("❌ Passwords don't match - Correct!")
        else:
            st.session_state.passwords[user]=new_p
            st.success(f"✅ Password changed! Your NEW password is: {new_p} - Use it next login, not unik2025 again!")
            st.balloons()

if st.sidebar.button("Logout",key="logout_pw"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8=st.tabs(["📝 Submit","📂 My Private Portal","🗳️ Electoral","⚖️ Disciplinary","📋 GP Committee","💰 Finance (5 Only)","🔐 Secret Store","📸 Media Gallery - Photo/Video/Music"])

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt_pw_1")
    rtitle=st.text_input("Report Title *",key="rtitle_pw_2")
    rcontent=st.text_area("Details *",height=150,key="rcontent_pw_3")
    rfile=st.file_uploader("Attach File",type=["xlsx","xls","pptx","ppt","pdf","jpg","png","docx","mp4","mp3"],key="rfile_pw_4")
    if st.button("📤 Submit Report",type="primary",use_container_width=True,key="rsubmit_pw_5"):
        if not rtitle.strip() or not rcontent.strip(): st.error("❌ ERROR: Title + Details required")
        else:
            st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":rfile.name if rfile else None,"file_bytes":rfile.getvalue() if rfile else None})
            st.success("✅ Submitted to your private portal!");st.balloons()

with tab2:
    st.subheader(f"📂 PRIVATE - {user_full} Portal")
    st.warning("🔒 PRIVATE: Only YOU + SUPER 4 can view")
    if user in SUPER_4: show_reports=st.session_state.reports;st.info(f"SUPER 4: Viewing ALL {len(show_reports)} reports")
    else: show_reports=[r for r in st.session_state.reports if r['from']==user];st.info(f"Private: You have {len(show_reports)} reports")
    if show_reports:
        st.dataframe(pd.DataFrame(show_reports)[["id","date","from_name","type","title"]].sort_values(by="id",ascending=False),use_container_width=True)
        for r in reversed(show_reports):
            with st.expander(f"#{r['id']} {r['title']} - {r['from_name']}"):
                st.info(r['content'])
                if r.get('file_bytes'): st.download_button(f"Download {r['file_name']}",r['file_bytes'],r['file_name'],key=f"dl_priv_{r['id']}_pw")

with tab3:
    st.subheader("🗳️ Electoral Commission - ALL 13 ACCESS")
    if user=="speaker":
        if not st.session_state.election_open:
            if st.button("🟢 OPEN VOTING",type="primary",key="open_pw"): st.session_state.election_open=True;st.rerun()
        else:
            if st.button("🔴 CLOSE VOTING",key="close_pw"): st.session_state.election_open=False;st.rerun()
    st.write(f"Status: {'🟢 OPEN' if st.session_state.election_open else '🔴 CLOSED'}")
    ta,tb,tc=st.tabs(["Register Candidate","Vote","Results"])
    with ta:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos_pw")
        rn=st.text_input("Full Names *",key="cand_name_pw")
        rclass=st.text_input("Class *",key="cand_class_pw")
        rcourse=st.text_input("Course *",key="cand_course_pw")
        rres=st.text_input("Results *",key="cand_res_pw")
        rreason=st.text_area("Reason *",key="cand_reason_pw")
        rphoto=st.file_uploader("Candidate Photo *",type=["jpg","png","jpeg"],key="cand_photo_pw")
        if st.button("Register Candidate",type="primary",key="cand_submit_pw"):
            if rn and rclass and rcourse and rres and rreason and rphoto:
                st.session_state.candidates.append({"id":len(st.session_state.candidates)+1,"position":rp,"name":rn,"class":rclass,"course":rcourse,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue()})
                st.success("✅ Registered!");st.balloons()
            else: st.error("❌ Fill ALL *")
    with tb:
        if not st.session_state.election_open: st.error("Voting Closed")
        else:
            vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos_pw")
            for c in [x for x in st.session_state.candidates if x['position']==vp]:
                with st.container(border=True):
                    st.image(c['photo_bytes'],width=120)
                    st.write(f"**{c['name']}** - {c['class']}")
                    if st.button(f"Vote {c['name']}",key=f"vote_{c['id']}_pw"): st.session_state.votes.append({"candidate_id":c['id'],"voter":user,"position":vp});st.success("Voted!");st.rerun()
    with tc:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                rd=[{"Candidate":c['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==c['id']])} for c in cs]
                st.write(f"**{USERS[pos]}**");st.dataframe(pd.DataFrame(rd),use_container_width=True)

with tab4:
    st.subheader("⚖️ Disciplinary - ALL 13")
    d_title=st.text_input("Case Title *",key="disc_title_pw")
    d_content=st.text_area("Case Details *",key="disc_content_pw")
    if st.button("Save Disciplinary",type="primary",key="disc_save_pw"):
        if d_title and d_content: st.session_state.disciplinary_reports.append({"id":len(st.session_state.disciplinary_reports)+1,"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")});st.success("✅ Saved!");st.balloons()
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(f"{dr['title']} - {dr['by']}"): st.warning(dr['content'])

with tab5:
    st.subheader("📋 GP Committee - ALL 13")
    gp_title=st.text_input("GP Title *",key="gp_title_pw")
    gp_content=st.text_area("GP Details *",key="gp_content_pw")
    if st.button("Save GP Report",type="primary",key="gp_save_pw"):
        if gp_title and gp_content: st.session_state.gp_reports.append({"id":len(st.session_state.gp_reports)+1,"title":gp_title,"content":gp_content,"by":user_full});st.success("✅ Saved!");st.balloons()
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(f"{gpr['title']} - {gpr['by']}"): st.info(gpr['content'])

with tab6:
    if user not in FINANCE_5: st.error("🔒 ACCESS DENIED - Finance only 5: Finance Secretary + Speaker + President + Patron + Principal");st.stop()
    st.subheader("💰 Finance - PRIVATE for 5 Only")
    st.success(f"✅ Authorized: {user_full} - Viewers: Finance + Speaker + President + Patron + Principal")
    f_title=st.text_input("Finance Title *",key="fin_title_pw")
    f_type=st.selectbox("Type",["Budget Excel","Financial Report PPT","Expense","Bank Statement","Other"],key="fin_type_pw")
    f_desc=st.text_area("Description *",key="fin_desc_pw")
    f_file=st.file_uploader("Upload Excel xlsx / PPT pptx *",type=["xlsx","xls","pptx","ppt","pdf","csv"],key="fin_file_pw")
    if st.button("💰 Save Finance",type="primary",use_container_width=True,key="fin_save_pw"):
        if not f_title.strip() or not f_file: st.error("❌ ERROR: Title + File required")
        else: st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title.strip(),"type":f_type,"description":f_desc,"file_name":f_file.name,"file_bytes":f_file.getvalue(),"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")});st.success(f"✅ Saved: {f_file.name}!");st.balloons();st.rerun()
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True):
            st.write(f"**{fd['title']}** | {fd['file_name']} | by {fd['by']}")
            st.download_button(f"📥 Download {fd['file_name']}",fd['file_bytes'],fd['file_name'],key=f"dl_fin_{fd['id']}_pw")

with tab7:
    st.subheader("🔐 Secret Store - ALL 13")
    dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat_pw")
    dt=st.text_input("Secret Title *",key="secret_title_pw")
    dd=st.text_area("Description",key="secret_desc_pw")
    uf=st.file_uploader("Upload File",key="secret_file_pw")
    if st.button("Save to Secret Store",type="primary",key="secret_save_pw"):
        if not dt.strip(): st.error("❌ Title required")
        else: st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"file_name":uf.name if uf else "Note","file_bytes":uf.getvalue() if uf else None,"by":user_full});st.success("✅ Saved!");st.rerun()
    for d in reversed(st.session_state.documents):
        with st.expander(f"{d['category']} | {d['title']} - {d['by']}"):
            if d['file_bytes']: st.download_button("Download",d['file_bytes'],d['file_name'],key=f"dl_sec_{d['id']}_pw")

with tab8:
    st.subheader("📸 MEDIA GALLERY - ALL 13 - Photos, Videos, Music!")
    st.success("✅ Upload Photos, Videos, Music here!")
    mt=st.text_input("Media Title *",key="media_title_pw")
    mf=st.file_uploader("Photo / Video / Music File *",type=["jpg","png","jpeg","mp4","mov","avi","mp3","m4a","wav","ogg"],key="media_file_pw")
    if st.button("📸 Save to Media Gallery",type="primary",use_container_width=True,key="media_save_pw"):
        if not mt.strip() or not mf: st.error("❌ ERROR: Title + File required")
        else: st.session_state.media.append({"id":len(st.session_state.media)+1,"title":mt.strip(),"file_name":mf.name,"file_bytes":mf.getvalue(),"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")});st.success(f"✅ Media Saved: {mf.name}!");st.balloons();st.rerun()
    st.divider()
    for m in reversed(st.session_state.media):
        with st.container(border=True):
            st.write(f"**{m['title']}** - {m['file_name']} - by {m['by']}")
            if "image" in m['file_type']: st.image(m['file_bytes'],use_container_width=True)
            elif "video" in m['file_type']: st.video(m['file_bytes'])
            elif "audio" in m['file_type']: st.audio(m['file_bytes'])
            st.download_button(f"📥 Download {m['file_name']}",m['file_bytes'],m['file_name'],key=f"dl_med_{m['id']}_pw")
