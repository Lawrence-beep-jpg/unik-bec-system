import streamlit as st
import pandas as pd
import datetime
st.set_page_config(page_title="UNIK BEC Governance Portal System", page_icon="🏛️", layout="wide")

query_params = st.query_params
is_public_vote = query_params.get("public", "") == "vote"

try:
    c1,c2,c3=st.columns([1,3,1])
    with c1: st.image("unik_badge.png",width=100)
    with c2: st.image("header.png",use_container_width=True)
    with c3: st.image("unasnm_badge.png",width=100)
except:
    st.title("UNIK BEC GOVERNANCE PORTAL SYSTEM")

USERS={"principal":"Hon. Principal","patron":"Hon. Patron","president":"Hon. President","vice_president":"Hon. Vice President","speaker":"Hon. Lawrence Ssango - Speaker BEC","general_secretary":"Hon. General Secretary","finance":"Hon. Finance Secretary","information":"Hon. Information Secretary","class_rep":"Hon. Class Rep","grc_male":"Hon. GRC Male","grc_female":"Hon. GRC Female","hostel_male":"Hon. Hostel Male","hostel_female":"Hon. Hostel Female","nursing_affairs":"Hon. Nursing Affairs"}
LOGIN_USERS=list(USERS.keys())
SUPER_4=["principal","patron","president","speaker"]
FINANCE_5=["principal","patron","president","speaker","finance"]
ELECTION_POSITIONS=["president","vice_president","speaker","finance","general_secretary","information","grc_male","grc_female","hostel_male","hostel_female","nursing_affairs"]

for k in ['reports','documents','candidates','votes','media','finance_docs','cabinets','pending_candidates']:
    if k not in st.session_state: st.session_state[k]=[]
if 'passwords' not in st.session_state: st.session_state.passwords={u:"unik2025" for u in LOGIN_USERS}
if 'election_open' not in st.session_state: st.session_state.election_open=False
if 'logged_in' not in st.session_state: st.session_state.logged_in=False
if 'user' not in st.session_state: st.session_state.user=""

if is_public_vote:
    st.success("UNIK BEC GOVERNANCE PORTAL - PUBLIC VOTING")
    st.info("Public Link: Students can Apply and Vote. No cabinet secrets here.")
    if st.session_state.election_open: st.success("Voting OPEN")
    else: st.error("Voting CLOSED by Chair")
    pub_tab1, pub_tab2 = st.tabs(["Apply as Candidate", "Vote Leaders"])
    with pub_tab1:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_pos")
        rn=st.text_input("Full Names",key="pub_name")
        rclass=st.text_input("Class",key="pub_class")
        rcourse=st.text_input("Course",key="pub_course")
        remail=st.text_input("Email",key="pub_email")
        rres=st.text_input("Results",key="pub_res")
        rreason=st.text_area("Why vote you?",key="pub_reason")
        rphoto=st.file_uploader("Photo",type=["jpg","png","jpeg"],key="pub_photo")
        if st.button("Submit Application",type="primary",key="pub_submit"):
            if not rn or not rclass or not rcourse or not remail or not rres or not rreason or not rphoto:
                st.error("Fill ALL fields")
            else:
                st.session_state.pending_candidates.append({"id":len(st.session_state.pending_candidates)+len(st.session_state.candidates)+1,"position":rp,"name":rn,"class":rclass,"course":rcourse,"email":remail,"results":rres,"reason":rreason,"photo_bytes":rphoto.getvalue(),"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                st.success("Application Sent! Wait for Chair approval.")
                st.balloons()
    with pub_tab2:
        if not st.session_state.election_open:
            st.error("Voting CLOSED")
            st.stop()
        voter_email=st.text_input("Your Email",key="pub_voter_email")
        if not voter_email or "@" not in voter_email:
            st.warning("Enter valid email")
            st.stop()
        vp=st.selectbox("Choose Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="pub_vote_pos")
        already_voted = [v for v in st.session_state.votes if v.get('voter_email','')==voter_email and v['position']==vp]
        if already_voted:
            st.error("You already voted for this position!")
            st.stop()
        approved_for_pos = [c for c in st.session_state.candidates if c['position']==vp]
        for c in approved_for_pos:
            with st.container(border=True):
                st.image(c['photo_bytes'],width=150)
                st.write(c['name'])
                st.info(c['reason'])
                if st.button("Vote " + c['name'],key="pv_"+str(c['id'])+"_"+voter_email):
                    st.session_state.votes.append({"candidate_id":c['id'],"voter_email":voter_email,"position":vp,"date":datetime.datetime.now().strftime("%Y-%m-%d")})
                    st.success("Voted!")
                    st.rerun()
    st.stop()

if not st.session_state.logged_in:
    u=st.selectbox("Select Office",LOGIN_USERS,format_func=lambda x:USERS[x],key="login")
    p=st.text_input("Password",type="password",key="pass")
    if st.button("LOGIN",use_container_width=True,type="primary",key="login_btn"):
        if p==st.session_state.passwords.get(u,"unik2025"):
            st.session_state.logged_in=True;st.session_state.user=u;st.rerun()
        else: st.error("Wrong Password")
    st.info("Default unik2025 | Public link: add ?public=vote to URL")
    st.stop()

user=st.session_state.user
user_full=USERS[user]
st.sidebar.title(user_full)
with st.sidebar.expander("Change My Password"):
    new_p=st.text_input("New Password",type="password",key="new_pass")
    confirm_p=st.text_input("Confirm",type="password",key="conf_pass")
    if st.button("Save Password",key="save_pass"):
        if not new_p: st.error("Enter password")
        elif new_p!=confirm_p: st.error("Dont match")
        else: st.session_state.passwords[user]=new_p; st.success("Saved: " + new_p)
if st.sidebar.button("Logout"): st.session_state.logged_in=False;st.rerun()

tab1,tab2,tab3,tab6,tab7,tab8,tab9=st.tabs(["Submit","Private","Electoral","Finance 5 Only","Secret Store","Media","Cabinet Archive"])

with tab1:
    rtitle=st.text_input("Title",key="t1")
    rcontent=st.text_area("Details",key="c1")
    if st.button("Submit",key="b1"):
        if not rtitle.strip() or not rcontent.strip(): st.error("Required")
        else: st.session_state.reports.append({"id":len(st.session_state.reports)+1,"from":user,"from_name":user_full,"title":rtitle,"content":rcontent}); st.success("Submitted")

with tab2:
    st.subheader("Private - " + user_full)
    show = st.session_state.reports if user in SUPER_4 else [r for r in st.session_state.reports if r['from']==user]
    st.write("Total reports: " + str(len(show)))

with tab3:
    st.subheader("Electoral Commission - Governance Portal")
    pending_count = len(st.session_state.pending_candidates)
    st.write("Pending approvals: " + str(pending_count))
    if user=="speaker":
        if not st.session_state.election_open:
            if st.button("OPEN VOTING",key="open"): st.session_state.election_open=True;st.rerun()
        else:
            if st.button("CLOSE VOTING",key="close"): st.session_state.election_open=False;st.rerun()
    t_pending, t_approved, t_reg, t_vote, t_res = st.tabs(["Pending Approval","Approved","Register","Vote","Results"])
    with t_pending:
        st.subheader("Pending Candidates Need Chair Approval")
        for pc in reversed(st.session_state.pending_candidates):
            with st.container(border=True):
                st.image(pc['photo_bytes'],width=120)
                st.write(pc['name'] + " - " + USERS[pc['position']])
                st.write("Email: " + pc['email'])
                st.info(pc['reason'])
                if st.button("Approve " + pc['name'],key="ap_"+str(pc['id'])):
                    st.session_state.candidates.append({"id":pc['id'],"position":pc['position'],"name":pc['name'],"class":pc['class'],"course":pc['course'],"results":pc['results'],"reason":pc['reason'],"photo_bytes":pc['photo_bytes']})
                    st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                    st.success("Approved"); st.rerun()
                if st.button("Reject " + pc['name'],key="rj_"+str(pc['id'])):
                    st.session_state.pending_candidates=[x for x in st.session_state.pending_candidates if x['id']!=pc['id']]
                    st.rerun()
    with t_approved:
        for c in st.session_state.candidates:
            st.write(c['name'] + " - " + USERS[c['position']])
    with t_reg:
        rp=st.selectbox("Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="rp")
        rn=st.text_input("Names",key="rn")
        rphoto=st.file_uploader("Photo",type=["jpg","png"],key="rph")
        if st.button("Register",key="reg"):
            if rn and rphoto: st.session_state.candidates.append({"id":len(st.session_state.candidates)+1,"position":rp,"name":rn,"class":"BEC","course":"Nursing","results":"A","reason":"Cabinet","photo_bytes":rphoto.getvalue()}); st.success("Registered")
    with t_vote:
        vp=st.selectbox("Vote Position",ELECTION_POSITIONS,format_func=lambda x:USERS[x],key="vp")
        for c in [x for x in st.session_state.candidates if x['position']==vp]:
            if st.button("Vote " + c['name'],key="v_"+str(c['id'])): st.session_state.votes.append({"candidate_id":c['id'],"voter_email":user+"@cabinet","position":vp}); st.success("Voted")
    with t_res:
        for pos in ELECTION_POSITIONS:
            cs=[c for c in st.session_state.candidates if c['position']==pos]
            if cs:
                for cc in cs:
                    vcount=len([v for v in st.session_state.votes if v['candidate_id']==cc['id']])
                    st.write(cc['name'] + ": " + str(vcount) + " votes")

with tab6:
    if user not in FINANCE_5: st.error("Finance only 5: Finance + Speaker + President + Patron + Principal"); st.stop()
    st.subheader("Finance - 5 Only")
    f_title=st.text_input("Title",key="ft")
    f_file=st.file_uploader("Excel PPT",type=["xlsx","pptx","pdf"],key="ff")
    if st.button("Save Finance",key="sf"):
        if not f_title or not f_file: st.error("Required")
        else: st.session_state.finance_docs.append({"id":len(st.session_state.finance_docs)+1,"title":f_title,"file_name":f_file.name,"file_bytes":f_file.getvalue(),"by":user_full}); st.success("Saved")

with tab7:
    st.subheader("Secret Store ALL 13")
    dt=st.text_input("Title",key="st")
    if st.button("Save",key="ss"): st.session_state.documents.append({"title":dt}); st.success("Saved")

with tab8:
    st.subheader("Media Gallery ALL 13")
    mt=st.text_input("Title",key="mt")
    mf=st.file_uploader("Photo Video Music",type=["jpg","png","mp4","mp3"],key="mf")
    if st.button("Upload",key="mu"):
        if not mt or not mf: st.error("Required")
        else: st.session_state.media.append({"title":mt,"file_name":mf.name,"file_bytes":mf.getvalue(),"file_type":mf.type,"by":user_full}); st.success("Saved"); st.balloons()
    for m in reversed(st.session_state.media):
        st.write(m['title'] + " by " + m['by'])
        if "image" in m['file_type']: st.image(m['file_bytes'])
        elif "video" in m['file_type']: st.video(m['file_bytes'])
        elif "audio" in m['file_type']: st.audio(m['file_bytes'])

with tab9:
    st.subheader("Cabinet Archive Different Years")
    cy=st.text_input("Year e.g. 2024/2025",key="cy")
    cn=st.text_input("Cabinet Name",key="cn")
    cm=st.text_area("Members",key="cm")
    cp=st.file_uploader("Photo",type=["jpg","png"],key="cp")
    if st.button("Save Cabinet",key="sc"):
        if not cy or not cn or not cm or not cp: st.error("Required")
        else: st.session_state.cabinets.append({"year":cy,"name":cn,"members":cm,"photo_bytes":cp.getvalue(),"by":user_full}); st.success("Saved")
    for cab in reversed(st.session_state.cabinets):
        with st.container(border=True):
            st.write(cab['name'] + " - " + cab['year'])
            st.image(cab['photo_bytes'])
            st.info(cab['members'])
