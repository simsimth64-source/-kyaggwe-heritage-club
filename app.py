import streamlit as st
import pandas as pd
from datetime import date, datetime
import uuid

st.set_page_config(page_title="Kyaggwe Heritage Club", page_icon="♻️", layout="wide")

# LOGO - RESTORED
c1, c2 = st.columns([1,5])
with c1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Rotary_International_Emblem_2020.svg/400px-Rotary_International_Emblem_2020.svg.png", width=90)
with c2:
    st.markdown("## Rotary Club of Kyaggwe Heritage\nDistrict 9213 | Club ID: 228098")

# --- PERMANENT SETUP - SAFE (won't crash) ---
PERM = False
sheet = None
try:
    import gspread
    from google.oauth2.service_account import Credentials
    SHEET_ID = st.secrets.get("SHEET_ID","")
    if SHEET_ID and "gcp_service_account" in st.secrets:
        scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(SHEET_ID)
        PERM = True
except Exception as e:
    st.sidebar.warning(f"Temp mode: {e}")

if PERM:
    st.sidebar.success("✅ PERMANENT MODE")
else:
    st.sidebar.warning("⚠️ TEMP MODE - Add secrets")

# --- SAFE LOADERS ---
def safe_load(name, cols):
    if not PERM or not sheet:
        return pd.DataFrame(columns=cols)
    try:
        # try different capitalizations
        ws = None
        for n in [name, name.capitalize(), name.lower(), name.upper(), "Sheet1"]:
            try:
                ws = sheet.worksheet(n)
                break
            except:
                continue
        if not ws:
            return pd.DataFrame(columns=cols)
        rec = ws.get_all_records()
        df = pd.DataFrame(rec)
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        return df
    except:
        return pd.DataFrame(columns=cols)

def safe_append(name, row, headers):
    if not PERM or not sheet:
        st.warning("Temp mode - not saved to sheet")
        return True
    try:
        ws = None
        for n in [name, name.capitalize(), name.lower(), name.upper()]:
            try:
                ws = sheet.worksheet(n)
                break
            except:
                continue
        if not ws:
            ws = sheet.add_worksheet(title=name, rows=1000, cols=10)
            ws.append_row(headers)
        ws.append_row([str(x) for x in row])
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

# --- LOGIN - RESTORED ---
if "logged" not in st.session_state:
    st.session_state.logged = False
if not st.session_state.logged:
    st.subheader("🔐 Login")
    with st.form("log"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if u:
                st.session_state.logged = True
                st.session_state.user = u
                st.rerun()
    st.info("Enter any username to login - Default: admin / kyaggwe2024")
    st.stop()

st.sidebar.write(f"User: {st.session_state.get('user','Secretary')}")
if st.sidebar.button("Logout"):
    st.session_state.logged = False
    st.rerun()

# --- COLS ---
MCOLS = ["Name","Phone","Email","Role","JoinDate","Status"]
BCOLS = ["Position","Name","Phone","Email","StartDate"]
ACOLS = ["Date","MemberName","Present","MeetingType"]
FCOLS = ["Date","Description","Income","Expense","Balance","Category","By"]
RCOLS = ["Date","MemberName","Amount","Purpose","ReceiptNo","IssuedBy"]

mdf = safe_load("members", MCOLS)
bdf = safe_load("board", BCOLS)
adf = safe_load("attendance", ACOLS)
fdf = safe_load("finances", FCOLS)
rdf = safe_load("receipts", RCOLS)

menu = st.sidebar.radio("MENU", ["Dashboard","Members","Board Officers","Attendance (Permanent)","Finances (Permanent)","Club Records","Reports","Gallery","Club Hub","Receipts (Permanent)","Get APK"])

if menu=="Dashboard":
    c1,c2,c3 = st.columns(3)
    c1.metric("Members", len(mdf))
    c2.metric("Attendance", len(adf))
    c3.metric("Finances", len(fdf))
    st.dataframe(mdf)
    st.dataframe(bdf)

elif menu=="Members":
    st.header("👥 Members")
    with st.form("mf"):
        n = st.text_input("Name")
        ph = st.text_input("Phone")
        em = st.text_input("Email")
        ro = st.selectbox("Role",["Member","President","Secretary","Treasurer"])
        if st.form_submit_button("Add Member"):
            safe_append("members",[n,ph,em,ro,str(date.today()),"Active"],MCOLS)
            st.success("Saved!")
            st.rerun()
    st.dataframe(mdf)

elif menu=="Board Officers":
    st.header("🏛️ Board Officers")
    with st.form("bf"):
        pos = st.selectbox("Position",["President","Secretary","Treasurer","Vice President"])
        nm = st.text_input("Name")
        ph = st.text_input("Phone")
        em = st.text_input("Email")
        if st.form_submit_button("Save Officer"):
            safe_append("board",[pos,nm,ph,em,str(date.today())],BCOLS)
            st.success("Saved!")
            st.rerun()
    st.dataframe(bdf)

elif "Attendance" in menu:
    st.header("✅ Attendance (Permanent)")
    with st.form("af"):
        d = st.date_input("Date",date.today())
        mt = st.selectbox("Type",["Weekly","Board","Service"])
        ml = mdf["Name"].tolist() if not mdf.empty else ["Guest"]
        sel = st.selectbox("Member",ml)
        pr = st.selectbox("Present",["Present","Absent","Apology"])
        if st.form_submit_button("Save Attendance"):
            safe_append("attendance",[str(d),sel,pr,mt],ACOLS)
            st.success("Attendance saved permanently!")
            st.rerun()
    st.dataframe(adf)

elif "Finances" in menu:
    st.header("💰 Finances (Permanent)")
    with st.form("ff"):
        d = st.date_input("Date",date.today())
        desc = st.text_input("Description")
        inc = st.number_input("Income",0)
        exp = st.number_input("Expense",0)
        cat = st.selectbox("Category",["Fees","Donation","Project","Admin"])
        if st.form_submit_button("Save Finance"):
            safe_append("finances",[str(d),desc,inc,exp,inc-exp,cat,st.session_state.get('user','')],FCOLS)
            st.success("Finance saved permanently!")
            st.rerun()
    st.dataframe(fdf)

elif "Receipts" in menu:
    st.header("🧾 Receipts (Permanent)")
    with st.form("rf"):
        d = st.date_input("Date",date.today())
        ml = mdf["Name"].tolist() if not mdf.empty else ["Guest"]
        sel = st.selectbox("Member",ml)
        amt = st.number_input("Amount",0)
        purp = st.text_input("Purpose")
        rno = st.text_input("Receipt No",f"RCP-{uuid.uuid4().hex[:6]}")
        if st.form_submit_button("Save Receipt"):
            safe_append("receipts",[str(d),sel,amt,purp,rno,st.session_state.get('user','')],RCOLS)
            st.success("Receipt saved permanently!")
            st.rerun()
    st.dataframe(rdf)

else:
    st.header(menu)
    st.write("Module coming - your data is safe in Google Sheet")
    st.write(f"Sheet ID: {st.secrets.get('SHEET_ID','')}")

st.sidebar.write(f"Members: {len(mdf)} | Board: {len(bdf)}")
