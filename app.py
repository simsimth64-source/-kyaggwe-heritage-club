import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Rotary Club of Kyaggwe Heritage", page_icon="⚙️", layout="wide")

def get_logo():
    possible = ["logo_exact_final.png.jpg", "logo_exact_final.png", "logo.png", "logo.jpg", "rotary_logo.png", "logo_exact_final.jpg"]
    for p in possible:
        if os.path.exists(p):
            return p
    return None

logo = get_logo()

PASSWORDS = {
    "Khissa Pamela - President": "President123",
    "Mubeezi Geoffrey - Secretary": "Secretary123",
    "Kasirye Simon Peter - Treasurer": "Treasurer123"
}

MEMBERS = [
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if logo:
            st.image(logo, width=300)
        st.title("ROTARY CLUB OF KYAGGWE HERITAGE")
        st.subheader("Club ID: 228098 | District 9213 | Unite for Good")
        st.divider()
        officer = st.selectbox("Select Officer", list(PASSWORDS.keys()))
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True, type="primary"):
            if PASSWORDS.get(officer) == pwd:
                st.session_state.logged_in = True
                st.session_state.officer = officer
                st.rerun()
            else:
                st.error("Wrong password!")
    st.stop()

with st.sidebar:
    if logo:
        st.image(logo, width=200)
    st.title("KYAGGWE HERITAGE")
    st.caption(f"Logged in: {st.session_state.officer}")
    st.divider()
    menu = st.radio("Navigation", ["📊 Dashboard", "👥 Members (18)", "✅ Smart Attendance", "💰 Finances", "🧾 Receipts", "📱 Get APK"])
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

if menu == "📊 Dashboard":
    st.title("Club Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Members", "18")
    c2.metric("Active", "18")
    c3.metric("Board Filled", "10/18")
    c4.metric("Charter", "June 2026")
    st.divider()
    st.info("Club ID 228098 | District 9213 | P.O. Box 954 Mukono, Uganda | Theme: Unite for Good")
    st.write("**President:** Khissa Pamela | **Secretary:** Mubeezi Geoffrey | **Treasurer:** Kasirye Simon Peter")

elif menu == "👥 Members (18)":
    st.title("Members (18) - Real Roster")
    df = pd.DataFrame(MEMBERS)
    st.dataframe(df, use_container_width=True, height=600)
    st.download_button("Download CSV", df.to_csv(index=False), "kyaggwe_members.csv", "text/csv")

elif menu == "✅ Smart Attendance":
    st.title("Smart Attendance")
    st.write("Upload Excel with Name column - auto matches 18 members")
    uploaded = st.file_uploader("Upload Attendance", type=["xlsx","csv"])
    if uploaded:
        att_df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        st.dataframe(att_df.head())
        present = []
        for _, row in att_df.iterrows():
            name_str = str(row.iloc[0]).lower()
            for mem in MEMBERS:
                if mem["FirstName"].lower() in name_str or mem["LastName"].lower() in name_str:
                    present.append(mem["FullName"])
                    break
        present = list(set(present))
        st.metric("Present", f"{len(present)}/18")
        st.write(present)
        st.download_button("Download Report", pd.DataFrame({"Present":present}).to_csv(index=False), "attendance.csv")

elif menu == "💰 Finances":
    st.title("Finances")
    df = pd.DataFrame(MEMBERS)[["FullName","Phone"]]
    df["Dues Paid"] = 0
    st.data_editor(df, use_container_width=True)

elif menu == "🧾 Receipts":
    st.title("Receipt Generator")
    member = st.selectbox("Select Member", [m["FullName"] for m in MEMBERS])
    amount = st.number_input("Amount UGX", value=50000)
    purpose = st.selectbox("Purpose", ["Membership Dues","Donation","Fellowship Fee"])
    if st.button("Generate Receipt"):
        st.success(f"Receipt for {member} - UGX {amount:,} - {purpose}")
        st.code(f"RCKH-{datetime.now().strftime('%Y%m%d%H%M')} | {member} | UGX {amount:,} | {purpose} | By {st.session_state.officer}")
        if logo:
            st.image(logo, width=150)

elif menu == "📱 Get APK":
    st.title("Install as Android App")
    st.success("Live at: https://fmwfp.streamlit.app")
    st.markdown("""
    **FAST INSTALL (Looks like APK):**
    1. Open https://fmwfp.streamlit.app in Chrome
    2. Tap 3 dots ⋮ -> Add to Home screen -> Install

    **REAL APK FILE:**
    1. Go to appsgeyser.com -> Website to APK
    2. Paste: https://fmwfp.streamlit.app
    3. Name: Kyaggwe Heritage Club
    4. Upload logo
    5. Download APK
    """)
    st.link_button("Open App", "https://fmwfp.streamlit.app", use_container_width=True)
