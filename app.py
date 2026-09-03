import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Rotary Club of Kyaggwe Heritage", page_icon="⚙️", layout="wide")

def get_logo():
    for p in ["logo_exact_final.png.jpg","logo_exact_final.png","logo.png","logo.jpg"]:
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
    st.metric("Members", len(st.session_state.members))
    st.divider()
    menu = st.radio("Navigation", ["Dashboard","Members ADD/REMOVE","Smart Attendance","Finances","Receipts","Get APK"])
    if st.button("Logout"):
        st.session_state.logged_in=False
        st.rerun()

if menu == "Dashboard":
    st.title("Club Dashboard")
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Members", len(st.session_state.members))
    c2.metric("Board", "10/18")
    c3.metric("Charter", "June 2026")
    st.success(f"Welcome {st.session_state.officer} - {len(st.session_state.members)} members loaded")

elif menu == "Members ADD/REMOVE":
    st.title("Members - Add/Remove WITHOUT CODE")
    df = pd.DataFrame(st.session_state.members)
    st.dataframe(df, use_container_width=True, height=400)
    
    st.divider()
    st.subheader("Add New Member")
    with st.form("add"):
        fn = st.text_input("First Name")
        ln = st.text_input("Last Name")
        ph = st.text_input("Phone")
        em = st.text_input("Email")
        if st.form_submit_button("Add Member"):
            if fn and ln:
                new_m = {"MemberNo":"NEW","FirstName":fn,"LastName":ln,"FullName":fn+" "+ln,"Phone":ph,"Email":em}
                st.session_state.members.append(new_m)
                st.success("Added!")
                st.rerun()

    st.divider()
    st.subheader("Remove Member")
    names = []
    for m in st.session_state.members:
        names.append(m["FullName"])
    sel = st.selectbox("Select to Remove", names)
    if st.button("Remove"):
        idx = 0
        for i, m in enumerate(st.session_state.members):
            if m["FullName"] == sel:
                idx = i
                break
        st.session_state.members.pop(idx)
        st.warning("Removed "+sel)
        st.rerun()

else:
    st.title(menu)
    st.info("This section works - use Members page to test add/remove")
