import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Rotary Club of Kyaggwe Heritage", page_icon="⚙️", layout="wide")

def get_logo():
    for p in ["logo_exact_final.png.jpg","logo_exact_final.png","logo.png","logo.jpg","rotary_logo.png","logo_exact_final.jpg"]:
        if os.path.exists(p):
            return p
    return None
logo = get_logo()

PASSWORDS = {
    "Khissa Pamela - President": "President123",
    "Mubeezi Geoffrey - Secretary": "Secretary123",
    "Kasirye Simon Peter - Treasurer": "Treasurer123"
}

DEFAULT_MEMBERS = [
    {"MemberNo":"11563120","FirstName":"Muzige","LastName":"Abubaker","FullName":"Muzige Abubaker","Phone":"+256 757447213","Email":"muzigeabubakar@gmail.com"},
    {"MemberNo":"11460462","FirstName":"Beatrice","LastName":"Kasirye","FullName":"Beatrice Kasirye","Phone":"+256 0782145945","Email":"beatricenanozi@gmail.com"},
    {"MemberNo":"12666632","FirstName":"Simon","LastName":"Katinda","FullName":"Simon Katinda","Phone":"+256 782602035","Email":"katsimon327@gmail.com"},
    {"MemberNo":"12664746","FirstName":"Twaha","LastName":"Kayondo","FullName":"Twaha Kayondo","Phone":"+256 782645644","Email":"twahakayondo@gmail.com"},
    {"MemberNo":"12666762","FirstName":"Jamir","LastName":"Kibirige","FullName":"Jamir Kibirige","Phone":"+256 704797943","Email":"jakibirige1@gmail.com"},
    {"MemberNo":"12664764","FirstName":"Moses","LastName":"Kizito","FullName":"Moses Kizito","Phone":"+256 702330143","Email":"kizito.moses2@gmail.com"},
    {"MemberNo":"12666737","FirstName":"Sarah","LastName":"Laker","FullName":"Sarah Laker","Phone":"+256 705510951","Email":"lakersarah82@gmail.com"},
    {"MemberNo":"11816050","FirstName":"Samuel","LastName":"Lukondha","FullName":"Samuel Lukondha","Phone":"+256 703998227","Email":"lukondhasa@yahoo.com"},
    {"MemberNo":"12394274","FirstName":"Bashir","LastName":"Masembe","FullName":"Bashir Masembe","Phone":"+256 771242277","Email":"masembebash@gmail.com"},
    {"MemberNo":"12666750","FirstName":"Lucky","LastName":"Mugisha","FullName":"Lucky Mugisha","Phone":"+256 785804292","Email":"humberlacy@gmail.com"},
    {"MemberNo":"12666771","FirstName":"Henry","LastName":"Mukalazi","FullName":"Henry Mukalazi","Phone":"+256 701145732","Email":"heronahospital76@gmail.com"},
    {"MemberNo":"12666597","FirstName":"Annet","LastName":"Nankabirwa","FullName":"Annet Nankabirwa","Phone":"+256 782059870","Email":"annetnank@gmail.com"},
    {"MemberNo":"12666794","FirstName":"Andrew","LastName":"Ndaura","FullName":"Andrew Ndaura","Phone":"+256 775180954","Email":"drea92002@gmail.com"},
    {"MemberNo":"12666781","FirstName":"Denis","LastName":"Onyama","FullName":"Denis Onyama","Phone":"+256 774337111","Email":"denis.onyama@gmail.com"},
    {"MemberNo":"12666652","FirstName":"Mariah","LastName":"Owino","FullName":"Mariah Owino","Phone":"+256 772846171","Email":"mariahebenah.mb@gmail.com"},
    {"MemberNo":"12664727","FirstName":"Khissa","LastName":"Pamela","FullName":"Khissa Pamela","Phone":"+256 781451436","Email":"pamelakhissa4@gmail.com"},
    {"MemberNo":"12664757","FirstName":"Ntulume","LastName":"Ssekulwana","FullName":"Ntulume Ssekulwana","Phone":"+256 752525386","Email":"wilsonntulume97@gmail.com"},
    {"MemberNo":"12664735","FirstName":"Francis","LastName":"Ssemugonda","FullName":"Francis Ssemugonda","Phone":"+256 762736379","Email":"francisssemugonda@gmail.com"},
]

if "members" not in st.session_state:
    st.session_state.members = DEFAULT_MEMBERS.copy()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        if logo: st.image(logo, width=300)
        st.title("ROTARY CLUB OF KYAGGWE HERITAGE")
        st.subheader("Club ID: 228098 | District 9213")
        st.divider()
        officer = st.selectbox("Select Officer", list(PASSWORDS.keys()))
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True, type="primary"):
            if PASSWORDS.get(officer) == pwd:
                st.session_state.logged_in=True
                st.session_state.officer=officer
                st.rerun()
            else:
                st.error("Wrong password!")
    st.stop()

with st.sidebar:
    if logo: st.image(logo, width=200)
    st.title("KYAGGWE HERITAGE")
    st.caption(f"Logged in: {st.session_state.officer}")
    st.metric("Total Members", len(st.session_state.members))
    st.divider()
    menu = st.radio("Navigation", ["📊 Dashboard","👥 Members - ADD/REMOVE","✅ Smart Attendance","💰 Finances","🧾 Receipts","📱 Get APK"])
    if st.button("Logout"):
        st.session_state.logged_in=False
        st.rerun()
    st.divider()
    st.warning("After adding members, download backup CSV!")

if menu == "📊 Dashboard":
    st.title("Club Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Members", len(st.session_state.members))
    c2.metric("Active", len(st.session_state.members))
    c3.metric("Board Filled", "10/18")
    c4.metric("Charter", "June 2026")
    st.divider()
    st.info(f"Club ID 228098 | Members: {len(st.session_state.members)} | Live at fmwfp.streamlit.app")

elif menu == "👥 Members - ADD/REMOVE":
    st.title(f"Members ({len(st.session_state.members)}) - Edit/Add/Remove WITHOUT CODE!")
    st.success("✅ You can add/remove here! No GitHub needed!")
    
    df = pd.DataFrame(st.session_state.members)
    st.subheader("1. View & Edit Directly (click cell to edit)")
    edited_df = st.data_editor(df, use_container_width=True, height=400, num_rows="dynamic", key="edit_members")
    if st.button("💾 Save Table Edits"):
        st.session_state.members = edited_df.to_dict('records')
        st.success("Saved!")
        st.rerun()
    
    st.divider()
    st.subheader("2. ➕ Add New Member")
    with st.form("add_member"):
        c1,c2 = st.columns(2)
        fn = c1.text_input("First Name")
        ln = c2.text_input("Last Name")
        c3,c4 = st.columns(2)
        phone = c3.text_input("Phone e.g. +256 7...")
        email = c4.text_input("Email")
        mno = st.text_input("Member No (optional)")
        submitted = st.form_submit_button("Add Member", type="primary", use_container_width=True)
        if submitted:
            if fn and ln:
                new_mem = {"MemberNo":mno or f"TEMP{len(st.session_state.members)+1}","FirstName":fn,"LastName":ln,"FullName":f"{fn} {ln}","Phone":phone,"Email":email}
                st.session_state.members.append(new_mem)
                st.success(f"Added {fn} {ln}! Total now {len(st.session_state.members)}")
                st.rerun()
            else:
                st.error("First and Last Name required!")
    
    st.divider()
    st.subheader("3. ➖ Remove Member")
        options_list = []
    for m in st.session_state.members:
        options_list.append(m["FullName"])
    to_remove = st.selectbox("Select Member to Remove", options_list)
