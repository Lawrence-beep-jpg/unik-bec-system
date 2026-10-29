import streamlit as st
import pandas as pd
import datetime
st.set_page_config(page_title="UNIK BEC FINAL FINAL - Cabinet Archive", page_icon="🏛️", layout="wide")
try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
except:
    st.title("🏛️ UNIK - BEC-UNASNM FINAL FINAL SYSTEM")
    st.caption("Hon. Lawrence Ssango - Speaker BEC - Chair Electoral & Disciplinary")

USERS={"principal":"Hon. Principal","patron":"Hon. Patron","president":"Hon. President","vice_president":"Hon. Vice President - Leader GP","speaker":"Hon. Lawrence Ssango - Speaker BEC","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys())
SUPER_4=["principal","patron","president","speaker"]
FINANCE_5=["principal","patron","president","speaker","finance"]
REPORT_TYPES=["Weekly","Monthly","Financial Excel/PPT","Activity","GRC","Hostel","Class","Electoral","Disciplinary","GP","Other"]
DOC_CATEGORIES=["Constitution","Budget","Minutes","Finance Excel","Finance PPT","Other Secret"]
ELECTION_POSITIONS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]

for k in ['reports','documents','candidates','votes','media','electoral_reports','disciplinary_reports','gp_reports','finance_docs','cabinets']:
    if k not in st.session_state: st.session_state[k]=[]
if 'passwords' not in st.session_state: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=False
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

if not st.session_state.logged_in:
    u=st.selectbox("Select Office - 13 Departments",LOGIN_USERS,format_func=lambda x:USERS[x],key="login_finalfinal")
    p=st.text_input("Password",type="password",key="pass_finalfinal")
    if st.button("🔐 LOGIN",use_container_width=True,type="primary",key="login_btn_finalfinal"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password!")
    st.info("Default: unik2025 | After change, use YOUR OWN password")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
if user in SUPER_4: st.sidebar.success("✅ SUPER 4")
if user in FINANCE_5: st.sidebar.success("💰 FINANCE 5")
with st.sidebar.expander("🔑 Change My Password"):
    new_p=st.text_input("New Password",type="password",key="new_pass_ff")
    confirm_p=st.text_input("Confirm",type="password",key="confirm_pass_ff")
    if st.button("Save Password",key="save_pass_ff"):
        if not new_p: st.error("Enter password")
        elif new_p!=confirm_p: st.error("❌ Don't match - Correct!")
        else: st.session_state.passwords[user]=new_p; st.success(f"✅ New password: {new_p}"); st.balloons()
if st.sidebar.button("Logout",key="logout_ff"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9=st.tabs(["📝 Submit","📂 Private Portal","🗳️ Electoral","⚖️ Disciplinary","📋 GP","💰 Finance (5 Only)","🔐 Secret Store","📸 Media Gallery","🏛️ Cabinet Archive"])

with tab1:
    rt=st.selectbox("Report Type",REPORT_TYPES,key="rt_ff1")
    rtitle=st.text_input("Report Title *",key="rtitle_ff2")
    rcontent=st.text_area("Details *",height=150,key="rcontent_ff3")
    rfile=st.file_uploader("Attach File",type=["xlsx","xls","pptx","ppt","pdf","jpg","png","docx","mp4","mp3"],key="rfile_ff4")
    if st.button("📤 Submit",type="primary",use_container_width=True,key="rsubmit_ff"):
        if not rtitle.strip() or not rcontent.strip(): st.error("❌ Title + Details required")
        else: st.session_state.reports.append({"id":len(st.session_state.reports)+1,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),"from":user,"from_name":user_full,"type":rt,"title":rtitle.strip(),"content":rcontent.strip(),"file_name":rfile.name if rfile else None,"file_bytes":rfile.getvalue() if rfile else None}); st.success("✅ Submitted!"); st.balloons()

with tab2:
    st.subheader(f"📂 PRIVATE - {user_full}")
    if user in SUPER_4: show=st.session_state.reports
    else: show=[r for r in st.session_state.reports if r['from']==user]
    st.dataframe(pd.DataFrame(show)[["id","date","from_name","type","title"]].sort_values(by="id",ascending=False) if show else pd.DataFrame(),use_container_width=True)
    for r in reversed(show):
        with st.expander(f"#{r['id']} {r['title']} - {r['from_name']}"):
            st.info(r['content'])
            if r.get('file_bytes'): st.download_button(f"Download {r['file_name']}",r['file_bytes'],r['file_name'],key=f"dl_priv_{r['id']}_ff")

with tab3:
    st.subheader("🗳️ Electoral - ALL 13")
    if user=="speaker":
        if not st.session_state.election_open:
            if st.button("🟢 OPEN VOTING",type="primary",key="open_ff"): st.session_state.election_open=True;st.rerun()
        else:
            if st.button("🔴 CLOSE VOTING",key="close_ff"): st.session_state.election_open=False;st.rerun()
    st.write(f"Status: {'🟢 OPEN' if st.session_state.election_open else '🔴 CLOSED'}")
    ta,tb,tc=st.tabs(["Register","Vote","Results"])
    with ta:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="cand_pos_ff")
        rn=st.text_input("Full Names *",key="cand_name_ff"); rclass=st.text_input("Class *",key="cand_class_ff"); rcourse=st.text_input("Course *",key="cand_course_ff"); rres=st.text_input("Results *",key="cand_res_ff"); rreason=st.text_area("Reason *",key="cand_reason_ff"); rphoto=st.file_uploader("Photo *",type=["jpg","png","jpeg"],key="cand_photo_ff")
        if st.button("Register",type="primary",key="cand_submit_ff"):
            if rn and rclass and rcourse and rres and rreason and rphoto: st.session_state.candidates.append({"id":len(st.session_state.candidates)+1,"position":rp,"name":rn,"class":rclass,"course":rcourse,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue()}); st.success("✅ Registered!"); st.balloons()
            else: st.error("❌ Fill ALL *")
    with tb:
        if not st.session_state.election_open: st.error("Voting Closed")
        else:
            vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vote_pos_ff")
            for c in [x for x in st.session_state.candidates if x['position']==vp]:
                with st.container(border=True): st.image(c['photo_bytes'],width=120); st.write(f"**{c['name']}**"); 
                if st.button(f"Vote {c['name']}",key=f"vote_{c['id']}_ff"): st.session_state.votes.append({"candidate_id":c['id'],"voter":user,"position":vp}); st.success("Voted!"); st.rerun()
    with tc:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs: rd=[{"Candidate":c['name'],"Votes":len([v for v in st.session_state.votes if v['candidate_id']==c['id']])} for c in cs]; st.write(f"**{USERS[pos]}**"); st.dataframe(pd.DataFrame(rd),use_container_width=True)

with tab4:
    st.subheader("⚖️ Disciplinary - ALL 13"); d_title=st.text_input("Case Title *",key="disc_title_ff"); d_content=st.text_area("Details *",key="disc_content_ff")
    if st.button("Save",type="primary",key="disc_save_ff"):
        if d_title and d_content: st.session_state.disciplinary_reports.append({"id":len(st.session_state.disciplinary_reports)+1,"title":d_title,"content":d_content,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success("✅ Saved!"); st.balloons()
    for dr in reversed(st.session_state.disciplinary_reports):
        with st.expander(f"{dr['title']} - {dr['by']}"): st.warning(dr['content'])

with tab5:
    st.subheader("📋 GP - ALL 13"); gp_title=st.text_input("GP Title *",key="gp_title_ff"); gp_content=st.text_area("Details *",key="gp_content_ff")
    if st.button("Save GP",type="primary",key="gp_save_ff"):
        if gp_title and gp_content: st.session_state.gp_reports.append({"id":len(st.session_state.gp_reports)+1,"title":gp_title,"content":gp_content,"by":user_full}); st.success("✅ Saved!"); st.balloons()
    for gpr in reversed(st.session_state.gp_reports):
        with st.expander(f"{gpr['title']} - {gpr['by']}"): st.info(gpr['content'])

with tab6:
    if user not in FINANCE_5: st.error("🔒 Finance only 5: Finance + Speaker + President + Patron + Principal"); st.stop()
    st.subheader("💰 Finance - 5 Only"); f_title=st.text_input("Title *",key="fin_title_ff"); f_type=st.selectbox("Type",["Budget Excel","PPT Report","Expense","Other"],key="fin_type_ff"); f_desc=st.text_area("Description",key="fin_desc_ff"); f_file=st.file_uploader("Excel/PPT *",type=["xlsx","xls","pptx","ppt","pdf","csv"],key="fin_file_ff")
    if st.button("Save Finance",type="primary",use_container_width=True,key="fin_save_ff"):
        if not f_title.strip() or not f_file: st.error("❌ Title + File required")
        else: st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title.strip(),"type":f_type,"description":f_desc,"file_name":f_file.name,"file_bytes":f_file.getvalue(),"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")}); st.success(f"✅ Saved: {f_file.name}!"); st.balloons(); st.rerun()
    for fd in reversed(st.session_state.finance_docs):
        with st.container(border=True): st.write(f"**{fd['title']}** | {fd['file_name']} | by {fd['by']}"); st.download_button(f"Download {fd['file_name']}",fd['file_bytes'],fd['file_name'],key=f"dl_fin_{fd['id']}_ff")

with tab7:
    st.subheader("🔐 Secret Store - ALL 13"); dc=st.selectbox("Category",DOC_CATEGORIES,key="secret_cat_ff"); dt=st.text_input("Title *",key="secret_title_ff"); dd=st.text_area("Description",key="secret_desc_ff"); uf=st.file_uploader("File",key="secret_file_ff")
    if st.button("Save Secret",type="primary",key="secret_save_ff"):
        if not dt.strip(): st.error("❌ Title required")
        else: st.session_state.documents.append({"id":len(st.session_state.documents)+1,"category":dc,"title":dt.strip(),"description":dd,"file_name":uf.name if uf else "Note","file_bytes":uf.getvalue() if uf else None,"by":user_full}); st.success("✅ Saved!"); st.rerun()
    for d in reversed(st.session_state.documents):
        with st.expander(f"{d['category']} | {d['title']} - {d['by']}"):
            if d['file_bytes']: st.download_button("Download",d['file_bytes'],d['file_name'],key=f"dl_sec_{d['id']}_ff")

with tab8:
    st.subheader("📸 MEDIA GALLERY - ALL 13 - EVERY MEMBER can upload Photo/Video/Music!")
    st.success("✅ EVERY MEMBER can upload + EVERY MEMBER can view everything!")
    filter_type=st.selectbox("Filter Media", ["All","Photos Only","Videos Only","Music Only"], key="media_filter_ff")
    c1,c2=st.columns([2,1])
    with c1: mt=st.text_input("Media Title * e.g. Sports Day 2025",key="media_title_ff")
    with c2: st.write("Supported: JPG, PNG, MP4, MOV, MP3, M4A, WAV, OGG")
    mf=st.file_uploader("Choose Photo / Video / Music File *",type=["jpg","png","jpeg","mp4","mov","avi","mp3","m4a","wav","ogg"],key="media_file_ff")
    if st.button("📸 Upload to Media Gallery",type="primary",use_container_width=True,key="media_save_ff"):
        if not mt.strip() or not mf: st.error("❌ ERROR: Title + File required - Type title + choose file first!")
        else: st.session_state.media.append({"id":len(st.session_state.media)+1,"title":mt.strip(),"file_name":mf.name,"file_bytes":mf.getvalue(),"file_type":mf.type,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}); st.success(f"✅ Media Saved: {mf.name}! Everyone can see it!"); st.balloons(); st.rerun()
    st.divider()
    st.write(f"📸 Total Media: {len(st.session_state.media)} - Visible to ALL 13 members")
    for m in reversed(st.session_state.media):
        ftype=m['file_type']
        if filter_type=="Photos Only" and "image" not in ftype: continue
        if filter_type=="Videos Only" and "video" not in ftype: continue
        if filter_type=="Music Only" and "audio" not in ftype: continue
        with st.container(border=True):
            st.write(f"**{m['title']}** - {m['file_name']} - by {m['by']} - {m['date']}")
            if "image" in ftype: st.image(m['file_bytes'],use_container_width=True)
            elif "video" in ftype: st.video(m['file_bytes'])
            elif "audio" in ftype: st.audio(m['file_bytes'])
            st.download_button(f"📥 Download {m['file_name']}",m['file_bytes'],m['file_name'],key=f"dl_med_{m['id']}_ff")

with tab9:
    st.subheader("🏛️ Leadership Cabinet Archive - Different Years - ALL 13 can view & upload!")
    st.success("✅ EVERY MEMBER can view all cabinets yearly + upload new cabinet!")
    st.info("Examples: First BEC Leadership Cabinet 2024/2025, Second BEC Cabinet 2025/2026")
    with st.container(border=True):
        st.write("**➕ Add New Yearly Cabinet**")
        cab_year=st.text_input("Year * e.g. 2024/2025", key="cab_year_ff")
        cab_name=st.text_input("Cabinet Name * e.g. First BEC Leadership Cabinet", key="cab_name_ff")
        cab_members=st.text_area("List Members in Cabinet * e.g. President: John, Speaker: Lawrence Ssango...", height=100, key="cab_members_ff")
        cab_desc=st.text_area("Achievements / Description", key="cab_desc_ff")
        cab_photo=st.file_uploader("Cabinet Group Photo * JPG/PNG", type=["jpg","png","jpeg"], key="cab_photo_ff")
        cab_video=st.file_uploader("Cabinet Video (Optional) MP4/MOV", type=["mp4","mov","avi"], key="cab_video_ff")
        if st.button("🏛️ Save Cabinet to Archive", type="primary", use_container_width=True, key="cab_save_ff"):
            if not cab_year.strip() or not cab_name.strip() or not cab_members.strip() or not cab_photo:
                st.error("❌ ERROR: Year + Cabinet Name + Members + Photo required!")
            else:
                st.session_state.cabinets.append({"id":len(st.session_state.cabinets)+1,"year":cab_year.strip(),"name":cab_name.strip(),"members":cab_members.strip(),"desc":cab_desc,"photo_bytes":cab_photo.getvalue(),"photo_name":cab_photo.name,"video_bytes":cab_video.getvalue() if cab_video else None,"video_name":cab_video.name if cab_video else None,"by":user_full,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success(f"✅ Cabinet Saved: {cab_name} - {cab_year}! Visible to ALL!"); st.balloons(); st.rerun()
    st.divider()
    st.write(f"🏛️ Total Cabinets Archived: {len(st.session_state.cabinets)}")
    # Year filter
    years = sorted(list(set([c['year'] for c in st.session_state.cabinets])), reverse=True) if st.session_state.cabinets else []
    if years:
        selected_year=st.selectbox("Filter by Year", ["All Years"] + years, key="cab_filter_year_ff")
    else:
        selected_year="All Years"
    for cab in reversed(st.session_state.cabinets):
        if selected_year!="All Years" and cab['year']!=selected_year: continue
        with st.container(border=True):
            st.subheader(f"{cab['name']} - {cab['year']}")
            st.write(f"📅 Archived: {cab['date']} | By: {cab['by']}")
            col1,col2=st.columns([1,1])
            with col1: st.image(cab['photo_bytes'], caption=f"{cab['name']} Photo", use_container_width=True)
            with col2:
                st.write("**👥 Members:**")
                st.info(cab['members'])
                if cab.get('desc'): st.write("**Achievements:**"); st.success(cab['desc'])
            if cab.get('video_bytes'): st.write("**🎥 Cabinet Video:**"); st.video(cab['video_bytes'])
            cA,cB=st.columns(2)
            with cA: st.download_button(f"📥 Download Photo {cab['photo_name']}", cab['photo_bytes'], cab['photo_name'], key=f"dl_cab_photo_{cab['id']}_ff")
            with cB:
                if cab.get('video_bytes'): st.download_button(f"📥 Download Video {cab['video_name']}", cab['video_bytes'], cab['video_name'], key=f"dl_cab_video_{cab['id']}_ff")
            if st.button(f"🗑️ Delete Cabinet #{cab['id']}", key=f"del_cab_{cab['id']}_ff"): st.session_state.cabinets=[x for x in st.session_state.cabinets if x['id']!=cab['id']]; st.rerun()
