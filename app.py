import streamlit as st
from datetime import date
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="UNIK BEC-UNASNM Official Letter System", layout="centered")

st.markdown("""
<style>
.letter-box {background:white; color:black; padding:40px; border:1px solid #ccc; font-family: 'Times New Roman', serif; line-height:1.6}
.header {text-align:center; border-bottom:3px double black; padding-bottom:15px; margin-bottom:20px}
.header h2 {margin:0; color:#0a4a2a}
.header h4 {margin:5px 0; font-weight:normal}
.footer {margin-top:40px; text-align:center; font-size:12px; color:#555; border-top:1px solid #ccc; padding-top:10px}
</style>
""", unsafe_allow_html=True)

st.title("🇺🇬 UNIK BEC-UNASNM")
st.subheader("Official Letter Generation System")

with st.sidebar:
    st.header("Letter Settings")
    letter_type = st.selectbox("Letter Type", ["Appointment Letter", "Invitation Letter", "Official Communication", "Recommendation Letter", "Meeting Notice"])
    ref_no = st.text_input("Ref No.", "UNIK/BEC/UNASNM/2025/")
    letter_date = st.date_input("Date", date.today())
    recipient_name = st.text_input("To (Name/Title)", "The Dean of Students")
    recipient_org = st.text_input("Organization/Office", "Uganda National Institute")
    subject = st.text_input("Subject / Re:", "RE: OFFICIAL APPOINTMENT")
    sender_name = st.text_input("From (Your Name)", "Lawrence")
    sender_title = st.text_input("Your Title", "Speaker, UNIK BEC-UNASNM")
    st.divider()
    signature_name = st.text_input("Signature Name", "Lawrence - Speaker")
    
st.markdown("### Letter Content")
salutation = st.text_input("Salutation", "Dear Sir/Madam,")
body = st.text_area("Main Body", """With great honor, the Office of the Speaker, UNIK BEC-UNASNM, writes to officially communicate...

This letter serves to confirm/appoint/invite you as part of our commitment to student leadership and development in UNIK.

We look forward to your positive response and continued collaboration.

Thank you for your service to UNIK.""", height=250)
closing = st.text_input("Closing", "Yours faithfully,")
include_signature = st.checkbox("Show Signature Line", True)

if st.button("Generate Official Letter Preview"):
    st.markdown("---")
    st.markdown('<div class="letter-box">', unsafe_allow_html=True)
    st.markdown(f'''
    <div class="header">
        <h2>UGANDA NATIONAL KICKBOXING - BUSINESS & ECONOMICS CLUB</h2>
        <h4>UNIK BEC-UNASNM Official Secretariat</h4>
        <p style="font-size:13px">Email: unikbec@example.com | Tel: +256 XXX XXX XXX | Kampala, Uganda</p>
    </div>
    <p><strong>Ref:</strong> {ref_no}<br><strong>Date:</strong> {letter_date.strftime("%d %B, %Y")}</p>
    <p><strong>{recipient_name}</strong><br>{recipient_org}</p>
    <p><strong>{subject}</strong></p>
    <p>{salutation}</p>
    <p style="white-space: pre-wrap;">{body}</p>
    <p>{closing}</p>
    <br><br>
    <p><strong>{signature_name}</strong><br>{sender_title}<br><em>UNIK BEC-UNASNM</em></p>
    <div class="footer">This is an official system generated document for UNIK BEC-UNASNM | Generated via unik-bec-system</div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.success("Letter generated! You can now Print (Ctrl+P) and Save as PDF")
else:
    st.info("Fill the sidebar and content above, then click 'Generate Official Letter Preview'")

st.divider()
st.caption("Built for Speaker Lawrence | UNIK BEC-UNASNM | Deploy on Streamlit Cloud")
