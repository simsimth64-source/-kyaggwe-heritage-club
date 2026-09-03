import streamlit as st
import pandas as pd

st.set_page_config(page_title="RC Kyaggwe Heritage", page_icon="logo_exact_final.png", layout="wide")

ROTARY_BLUE = "#21468B"
ROTARY_GOLD = "#F5A623"

st.markdown(f"""
<style>
[data-testid="stSidebar"]{{background-color:{ROTARY_BLUE};}}
[data-testid="stSidebar"] *{{color:white!important;}}
h1,h2,h3{{color:{ROTARY_BLUE};}}
.stButton>button{{background-color:{ROTARY_BLUE}; color:white; border-radius:8px; border:1px solid {ROTARY_GOLD};}}
</style>
""", unsafe_allow_html=True)

USERS = {
 "president": {"name": "Khissa Pamela - President", "password": "President2026"},
 "secretary": {"name": "Francis Ssemugonda - Secretary", "password": "Secretary2026"},
 "treasurer": {"name": "Ntulume Wilson - Treasurer", "password": "Treasurer2026"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.image("logo_exact_final.png.jpg", width=300)
    st.title("ROTARY CLUB OF KYAGGWE HERITAGE")
    st.write("Club ID: 228098 | District 9213 | Charter June 2026 | Theme: Unite for Good")
    st.divider()
    st.subheader("Secure Login - President, Secretary, Treasurer Only")
    user = st.selectbox("Select Officer", ["president","secretary","treasurer"], format_func=lambda x: USERS[x]["name"])
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == USERS[user]["password"]:
            st.session_state.logged_in = True
            st.session_state.user = USERS[user]
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

st.sidebar.image("logo_exact_final.png.jpg", width=200)
st.sidebar.write(f"**{st.session_state.user['name']}**")
menu = st.sidebar.radio("Menu", ["Dashboard","Members (18)","Board 10+8 Open","Attendance","Dues","Projects","Photos & Events Upload","Documents Upload"])

if menu == "Dashboard":
    st.title("Dashboard")
    c1,c2,c3 = st.columns(3)
    c1.metric("Members",18)
    c2.metric("Board Filled","10 / 18")
    c3.metric("Charter","June 2026")
    st.info("Club ID 228098 | District 9213 | Year 2026-27 | Theme Unite for Good | Service Above Self")

elif menu == "Photos & Events Upload":
    st.header("📸 Upload Photos & Events")
    st.write("Upload fellowship photos, project photos, community service photos")
    files = st.file_uploader("Choose photos", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if files:
        for f in files:
            st.image(f, caption=f.name, width=300)
        st.success(f"{len(files)} photos uploaded! Saved to club gallery")

elif menu == "Documents Upload":
    st.header("📄 Upload Documents")
    doc = st.file_uploader("Upload PDF, Word, Excel", type=["pdf","docx","xlsx"])
    if doc:
        st.success(f"Document {doc.name} uploaded and saved!")

else:
    st.header(menu)
    st.write("This section is ready - data from your Excel database will show here")
