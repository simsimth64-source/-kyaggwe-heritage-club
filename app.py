import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Rotary Club of Kyaggwe Heritage", page_icon="⚙️", layout="wide")

def get_logo():
    for p in ["logo_exact_final.png.jpg","logo_exact_final.png","logo.png","logo.jpg","rotary_logo.png"]:
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
        st.subheader("Club ID: 228098 | District 9213 | Unite for Good")
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
    st.caption("Logged in: " + str(st.session_state.officer))
    st.metric("Total Members", len(st.session_state.members))
    st.divider()
    menu = st.radio("Navigation", ["Dashboard","Members ADD/REMOVE","Smart Attendance","Finances","Receipts","Get APK"])
    if st.button("Logout"):
        st.session_state.logged_in=False
        st.rerun()

if menu == "Dashboard":
    st.title("Club Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Members", len(st.session_state.members))
    c2.metric("Active", len(st.session_state.members))
    c3.metric("Board Filled", "10/18")
    c4.metric("Charter", "June 2026")
    st.divider()
    st.info("Club ID 228098 | P.O Box 954 Mukono | District 9213 | Theme: Unite for Good")
    st.write("President: Khissa Pamela | Secretary: Mubeezi Geoffrey | Treasurer: Kasirye Simon Peter")

elif menu == "Members ADD/REMOVE":
    st.title("Members - Add/Remove Without Code")
    st.success("Total: " + str(len(st.session_state.members)) + " members")
    df = pd.DataFrame(st.session_state.members)
    st.dataframe(df, use_container_width=True, height=400)
    st.download_button("Download Backup CSV", df.to_csv(index=False), "members.csv", "text/csv")

    st.divider()
    st.subheader("Add New Member")
    with st.form("add"):
        fn = st.text_input("First Name")
        ln = st.text_input("Last Name")
        ph = st.text_input("Phone")
        em = st.text_input("Email")
        mno = st.text_input("Member No")
        if st.form_submit_button("Add Member", type="primary"):
            if fn and ln:
                full = fn + " " + ln
                new_m = {"MemberNo":mno, "FirstName":fn, "LastName":ln, "FullName":full, "Phone":ph, "Email":em}
                st.session_state.members.append(new_m)
                st.success("Added " + full)
                st.rerun()
            else:
                st.error("Need First and Last name")

    st.divider()
    st.subheader("Remove Member")
    names = []
    for m in st.session_state.members:
        names.append(m["FullName"])
    sel = st.selectbox("Select Member to Remove", names)
    if st.button("Remove Selected"):
        for i, m in enumerate(st.session_state.members):
            if m["FullName"] == sel:
                st.session_state.members.pop(i)
                break
        st.warning("Removed " + sel)
        st.rerun()

elif menu == "Smart Attendance":
    st.title("Smart Attendance")
    st.write("Upload Excel list with names - system auto-matches your members")
    uploaded = st.file_uploader("Upload Attendance Excel or CSV", type=["xlsx","csv"])
    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            att_df = pd.read_csv(uploaded)
        else:
            att_df = pd.read_excel(uploaded)
        st.write("File preview:")
        st.dataframe(att_df.head(), use_container_width=True)

        present = []
        for idx, row in att_df.iterrows():
            name_str = str(row.iloc[0]).lower()
            for mem in st.session_state.members:
                first = mem["FirstName"].lower()
                last = mem["LastName"].lower()
                if first in name_str or last in name_str:
                    present.append(mem["FullName"])
                    break
        present_unique = list(set(present))
        st.divider()
        c1,c2 = st.columns(2)
        c1.metric("Present", str(len(present_unique)) + " / " + str(len(st.session_state.members)))
        c2.metric("Absent", len(st.session_state.members) - len(present_unique))
        st.write("Present members:")
        st.write(present_unique)

        all_names = []
        for m in st.session_state.members:
            all_names.append(m["FullName"])
        absent = []
        for n in all_names:
            if n not in present_unique:
                absent.append(n)
        st.write("Absent members:")
        st.write(absent)

        report_df = pd.DataFrame({"FullName": all_names})
        status = []
        for n in all_names:
            if n in present_unique:
                status.append("Present")
            else:
                status.append("Absent")
        report_df["Status"] = status
        st.download_button("Download Attendance Report", report_df.to_csv(index=False), "attendance_report.csv", "text/csv")

elif menu == "Finances":
    st.title("Finances - Dues Tracking")
    base_df = pd.DataFrame(st.session_state.members)
    cols = []
    for m in st.session_state.members:
        cols.append({"FullName": m["FullName"], "Phone": m["Phone"], "Dues Paid": 0, "Balance": 50000})
    fin_df = pd.DataFrame(cols)
    st.data_editor(fin_df, use_container_width=True, height=500)
    st.info("Edit Dues directly in table")

elif menu == "Receipts":
    st.title("Receipt Generator")
    names = []
    for m in st.session_state.members:
        names.append(m["FullName"])
    member = st.selectbox("Select Member", names)
    amount = st.number_input("Amount UGX", value=50000)
    purpose = st.selectbox("Purpose", ["Membership Dues","Donation","Fellowship Fee","Other"])
    if st.button("Generate Receipt", type="primary"):
        receipt_no = "RCKH-" + datetime.now().strftime("%Y%m%d%H%M")
        st.success("Receipt Generated!")
        st.code(receipt_no + " | Member: " + member + " | Amount: UGX " + str(amount) + " | Purpose: " + purpose + " | By: " + str(st.session_state.officer))
        if logo:
            st.image(logo, width=150)

elif menu == "Get APK":
    st.title("Get Android APK")
    st.success("Your app is live at: https://fmwfp.streamlit.app")
    st.markdown("""
    **OPTION 1 - Install as App (30 seconds, like APK):**
    1. Open Chrome: fmwfp.streamlit.app
    2. Tap 3 dots top right -> Add to Home screen
    3. Tap Install - Rotary icon appears on phone!

    **OPTION 2 - Real APK file:**
    1. Go to appsgeyser.com
    2. Create App -> Website -> Paste https://fmwfp.streamlit.app
    3. Name: Kyaggwe Heritage Club - Upload logo
    4. Download APK and share on WhatsApp
    """)
    st.link_button("Open Live App", "https://fmwfp.streamlit.app", use_container_width=True)
