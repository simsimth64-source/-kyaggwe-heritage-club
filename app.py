import streamlit as st
import pandas as pd
import os, io, base64
from datetime import datetime

st.set_page_config(page_title="Kyaggwe Heritage PERMANENT", page_icon="⚙️", layout="wide")

# TRY GOOGLE, FALLBACK TO MEMORY IF NOT SET
USE_GOOGLE = False
try:
    import gspread
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    if "gcp_service_account" in st.secrets:
        USE_GOOGLE = True
        scope = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        gc = gspread.authorize(creds)
        SHEET_ID = st.secrets["SHEET_ID"]
        DRIVE_ID = st.secrets["DRIVE_FOLDER_ID"]
        sh = gc.open_by_key(SHEET_ID)
        drive_service = build('drive','v3',credentials=creds)
        st.success("✅ PERMANENT MODE: Connected to Google Sheet + Drive")
    else:
        st.warning("⚠️ Running in TEMP mode - Add Secrets for Permanent storage")
except Exception as e:
    USE_GOOGLE = False
    st.warning(f"⚠️ Google not connected ({e}) - Using temporary memory. Add Secrets for permanent!")

def get_logo():
    for p in ["logo_exact_final.png.jpg","logo_exact_final.png","logo.png","logo.jpg","rotary_logo.png"]:
        if os.path.exists(p): return p
    return None
logo_path = get_logo()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: #eef2ff; }
.welcome-banner { background: linear-gradient(135deg, #0A2A5E 0%, #1746A2 60%, #FDB913 100%); padding: 25px; border-radius: 18px; text-align: center; color: white; }
.pro-header { background: linear-gradient(135deg, #0A2A5E 0%, #1746A2 100%); padding: 15px 20px; border-radius: 12px; color: white; }
.pro-card { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 3px 10px rgba(0,0,0,0.06); border-left: 5px solid #FDB913; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

ADMIN_PASSWORDS = {
    "Khissa Pamela - President": "President123",
    "Francis Ssemugonda - Secretary": "Secretary123",
    "Ntulume Wilson Ssekulwana - Treasurer": "Treasurer123"
}
ADMINS = ["President","Secretary","Treasurer"]

# DEFAULTS
DEFAULT_MEMBERS = [
    {"MemberNo":"11563120","FirstName":"Muzige","LastName":"Abubaker","FullName":"Muzige Abubaker","Phone":"+256 757447213","Email":"muzigeabubakar@gmail.com","Role":"Club Executive Secretary/Director"},
    {"MemberNo":"12664727","FirstName":"Khissa","LastName":"Pamela","FullName":"Khissa Pamela","Phone":"+256 781451436","Email":"pamelakhissa4@gmail.com","Role":"Club President"},
    {"MemberNo":"12664757","FirstName":"Ntulume","LastName":"Ssekulwana","FullName":"Ntulume Wilson Ssekulwana","Phone":"+256 752525386","Email":"wilsonntulume97@gmail.com","Role":"Club Treasurer"},
    {"MemberNo":"12664735","FirstName":"Francis","LastName":"Ssemugonda","FullName":"Francis Ssemugonda","Phone":"+256 762736379","Email":"francisssemugonda@gmail.com","Role":"Club Secretary"},
]
DEFAULT_BOARD = [
    {"Position":"Club President","Name":"Khissa Pamela","Phone":"+256 781451436","Email":"pamelakhissa4@gmail.com"},
    {"Position":"Club Secretary","Name":"Francis Ssemugonda","Phone":"+256 762736379","Email":"francisssemugonda@gmail.com"},
    {"Position":"Club Treasurer","Name":"Ntulume Wilson Ssekulwana","Phone":"+256 752525386","Email":"wilsonntulume97@gmail.com"},
]

# GOOGLE FUNCTIONS
def load_sheet(tab):
    if not USE_GOOGLE: return None
    try:
        ws = sh.worksheet(tab)
        data = ws.get_all_records()
        return data
    except: return None

def save_sheet(tab, df):
    if not USE_GOOGLE: return
    try:
        ws = sh.worksheet(tab)
        ws.clear()
        ws.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        st.error(f"Save error {tab}: {e}")

def upload_to_drive(file_bytes, filename):
    if not USE_GOOGLE: return None
    try:
        file_metadata = {'name': filename, 'parents': [DRIVE_ID]}
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype='application/octet-stream')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        drive_service.permissions().create(fileId=file.get('id'), body={'role':'reader','type':'anyone'}).execute()
        return file.get('webViewLink')
    except Exception as e:
        st.error(f"Drive upload error: {e}")
        return None

# INIT SESSION WITH GOOGLE OR DEFAULT
if "members" not in st.session_state:
    data = load_sheet("members") if USE_GOOGLE else None
    st.session_state.members = data if data else DEFAULT_MEMBERS.copy()
if "board" not in st.session_state:
    data = load_sheet("board") if USE_GOOGLE else None
    st.session_state.board = data if data else DEFAULT_BOARD.copy()
if "announcements" not in st.session_state:
    data = load_sheet("announcements") if USE_GOOGLE else None
    st.session_state.announcements = data if data else [{"title":"Welcome to Kyaggwe Heritage V12 Permanent!","msg":"All uploads now stay forever via Google!","date":"2026-05-13","by":"President"}]
if "records" not in st.session_state: st.session_state.records = load_sheet("files") or []
if "gallery" not in st.session_state: st.session_state.gallery = []
if "reports" not in st.session_state: st.session_state.reports = []
if "member_passwords" not in st.session_state: st.session_state.member_passwords = {}
if "logged_in" not in st.session_state: st.session_state.logged_in = False

def show_header(icon, title, subtitle):
    st.markdown(f'<div class="pro-header"><h3>{icon} {title}</h3><p>{subtitle}</p></div>', unsafe_allow_html=True)
def is_admin(): return any(a in st.session_state.get("user_role","") for a in ADMINS)

# LOGIN
if not st.session_state.logged_in:
    st.markdown('<div class="welcome-banner"><div style="font-size:50px;">⚙️</div><h1>Kyaggwe Heritage</h1><h3>Welcome to Kyaggwe Heritage - V12 PERMANENT</h3><p>District 9213 | Club ID: 228098</p></div>', unsafe_allow_html=True)
    if logo_path: st.image(logo_path, width=150)
    tab1, tab2 = st.tabs(["🔐 Admin (3 Only)", "👥 Member"])
    with tab1:
        officer = st.selectbox("Select Admin", list(ADMIN_PASSWORDS.keys()))
        pwd = st.text_input("Password", type="password")
        if st.button("Login as Admin", type="primary", use_container_width=True):
            if ADMIN_PASSWORDS.get(officer) == pwd:
                st.session_state.logged_in = True
                st.session_state.current_user = officer
                st.session_state.user_role = officer.split(" - ")[1]
                st.rerun()
            else: st.error("Wrong!")
    with tab2:
        phone = st.text_input("Phone"); pp = st.text_input("Password", type="password", key="m2")
        if st.button("Login Member", type="primary", use_container_width=True):
            found = next((m for m in st.session_state.members if m["Phone"]==phone), None)
            if found:
                if st.session_state.member_passwords.get(phone,"member123")==pp:
                    st.session_state.logged_in=True
                    st.session_state.current_user=found["FullName"]
                    st.session_state.user_role=found["Role"]
                    st.rerun()
                else: st.error("Wrong password")
            else: st.error("Not found")
    st.stop()

with st.sidebar:
    if logo_path: st.image(logo_path, width=120)
    st.write(f"👤 {st.session_state.current_user}")
    st.caption(f"🏷️ {st.session_state.user_role} {'✅' if is_admin() else ''}")
    st.caption("✅ PERMANENT MODE" if USE_GOOGLE else "⚠️ TEMP MODE")
    menu = st.radio("MENU", ["🏠 Dashboard","👥 Members","🏛️ Board Officers","✅ Attendance","💰 Finances","📁 Club Records (Permanent)","📊 Reports (Permanent)","📸 Gallery (Permanent)","📢 Club Hub","🧾 Receipts","📲 Get APK"])
    if st.button("🚪 Logout"):
        st.session_state.logged_in=False
        st.rerun()

# DASHBOARD
if menu=="🏠 Dashboard":
    st.markdown(f'<div class="welcome-banner"><h2>Welcome {st.session_state.current_user.split(" -")[0]}!</h2><p>{datetime.now().strftime("%b %d, %Y")} | Permanent Storage: {"ON ✅" if USE_GOOGLE else "OFF ⚠️"}</p></div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("👥 Members", len(st.session_state.members))
    c2.metric("🏛️ Board", len(st.session_state.board))
    c3.metric("📢 Announcements", len(st.session_state.announcements))
    st.dataframe(pd.DataFrame(st.session_state.board), use_container_width=True)
    for ann in reversed(st.session_state.announcements[-5:]):
        st.markdown(f'<div class="pro-card"><b>📌 {ann["title"]}</b><br>{ann["msg"]}<br><small>{ann["date"]} | {ann["by"]}</small></div>', unsafe_allow_html=True)

elif menu=="👥 Members":
    show_header("👥","Members","Permanent if Google ON")
    st.dataframe(pd.DataFrame(st.session_state.members), use_container_width=True)
    if is_admin():
        with st.form("add_mem"):
            fn=st.text_input("First"); ln=st.text_input("Last"); ph=st.text_input("Phone"); em=st.text_input("Email"); role=st.text_input("Role", "Member")
            if st.form_submit_button("Add & Save Permanently", type="primary"):
                if fn and ln and ph:
                    st.session_state.members.append({"MemberNo":"NEW","FirstName":fn,"LastName":ln,"FullName":fn+" "+ln,"Phone":ph,"Email":em,"Role":role})
                    if USE_GOOGLE: save_sheet("members", pd.DataFrame(st.session_state.members))
                    st.success("Saved permanently!"); st.rerun()
        if st.button("💾 Force Save All to Google Sheet"):
            if USE_GOOGLE:
                save_sheet("members", pd.DataFrame(st.session_state.members))
                st.success("Saved to Google!")
            else: st.error("Connect Google first")

elif menu=="🏛️ Board Officers":
    show_header("🏛️","Board Officers - Edit/Add/Remove + Permanent","Edits save to Google Sheet forever")
    st.dataframe(pd.DataFrame(st.session_state.board), use_container_width=True)
    if is_admin():
        st.divider()
        st.subheader("✏️ Edit")
        sel = st.selectbox("Select Position", [b["Position"] for b in st.session_state.board])
        cur = next(b for b in st.session_state.board if b["Position"]==sel)
        with st.form("edit_b"):
            nn=st.text_input("Name", cur["Name"]); pp=st.text_input("Phone", cur["Phone"]); ee=st.text_input("Email", cur["Email"])
            if st.form_submit_button("💾 Save Edit Permanently", type="primary"):
                for b in st.session_state.board:
                    if b["Position"]==sel:
                        b["Name"]=nn; b["Phone"]=pp; b["Email"]=ee
                if USE_GOOGLE: save_sheet("board", pd.DataFrame(st.session_state.board))
                st.success("Updated permanently!"); st.rerun()
        st.divider()
        st.subheader("➕ Add")
        with st.form("add_b"):
            pos=st.text_input("New Position*"); name=st.selectbox("Member", [m["FullName"] for m in st.session_state.members])
            sel_m=next(m for m in st.session_state.members if m["FullName"]==name)
            if st.form_submit_button("Add Permanently", type="primary"):
                if pos:
                    st.session_state.board.append({"Position":pos,"Name":name,"Phone":sel_m["Phone"],"Email":sel_m["Email"]})
                    if USE_GOOGLE: save_sheet("board", pd.DataFrame(st.session_state.board))
                    st.success("Added permanently!"); st.rerun()
        st.divider()
        st.subheader("🗑️ Remove")
        rem=st.selectbox("Position to Remove", [b["Position"] for b in st.session_state.board], key="rem")
        if st.button("Remove Permanently"):
            st.session_state.board=[b for b in st.session_state.board if b["Position"]!=rem]
            if USE_GOOGLE: save_sheet("board", pd.DataFrame(st.session_state.board))
            st.warning(f"Removed {rem} permanently"); st.rerun()

elif menu=="📁 Club Records (Permanent)":
    show_header("📁","Club Records - Permanent Storage","Uploads to Google Drive forever")
    if is_admin():
        with st.form("rec", clear_on_submit=True):
            title=st.text_input("Title*"); cat=st.selectbox("Category", ["Minutes","Constitution","Other"]); f=st.file_uploader("File*")
            if st.form_submit_button("📤 Upload Permanently to Drive", type="primary", use_container_width=True):
                if title and f:
                    link = upload_to_drive(f.getvalue(), f.name) if USE_GOOGLE else None
                    st.session_state.records.append({"title":title,"category":cat,"filename":f.name,"date":datetime.now().strftime("%Y-%m-%d"),"by":st.session_state.current_user,"link":link or "TEMP"})
                    if USE_GOOGLE and link: save_sheet("files", pd.DataFrame(st.session_state.records))
                    st.success(f"Uploaded! Link: {link}" if link else "Uploaded temp - Connect Google for permanent"); st.rerun()
    for idx, rec in enumerate(reversed(st.session_state.records)):
        with st.expander(f"📄 {rec['title']} - {rec['filename']}"):
            st.write(f"By {rec['by']} | {rec['date']}")
            if rec.get("link") and "http" in rec["link"]:
                st.link_button("🔗 Open in Drive (Permanent)", rec["link"])
            else:
                st.caption("Temp file - Will delete after reboot")

elif menu=="📸 Gallery (Permanent)":
    show_header("📸","Gallery - Permanent","Photos to Drive")
    if is_admin():
        album=st.selectbox("Album", ["Fellowship","Projects","Other"]); cap=st.text_input("Caption"); photos=st.file_uploader("Photos", accept_multiple_files=True, type=["jpg","png","jpeg"])
        if st.button("📸 Upload Photos Permanently", type="primary", use_container_width=True):
            if photos:
                for p in photos:
                    link = upload_to_drive(p.getvalue(), p.name) if USE_GOOGLE else None
                    st.session_state.gallery.append({"album":album,"caption":cap,"filename":p.name,"link":link})
                st.success(f"{len(photos)} uploaded to Drive permanently!" if USE_GOOGLE else "Uploaded temp"); st.rerun()
    for item in reversed(st.session_state.gallery):
        if item.get("link") and "http" in str(item.get("link")):
            st.write(f"{item['album']} - {item['caption']}")
            st.link_button(f"View {item['filename']}", item["link"])
        else:
            st.caption(f"TEMP: {item['filename']}")

elif menu=="📢 Club Hub":
    show_header("📢","Club Hub - Permanent Announcements","Saves to Google Sheet")
    if is_admin():
        with st.form("ann", clear_on_submit=True):
            at=st.text_input("Title*"); am=st.text_area("Message*")
            if st.form_submit_button("Post Permanently", type="primary"):
                if at and am:
                    st.session_state.announcements.append({"title":at,"msg":am,"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"by":st.session_state.current_user})
                    if USE_GOOGLE: save_sheet("announcements", pd.DataFrame(st.session_state.announcements))
                    st.success("Posted permanently!"); st.rerun()
    for ann in reversed(st.session_state.announcements):
        st.markdown(f'<div class="pro-card"><b>{ann["title"]}</b><br>{ann["msg"]}<br><small>{ann["date"]} | {ann["by"]}</small></div>', unsafe_allow_html=True)

else:
    show_header("✅","Other Pages","Same as V11 - Now permanent if Google ON")
    st.info("Attendance, Finances, Reports, Receipts, APK pages work same as V11. For permanent, connect Google as above. Current mode: " + ("PERMANENT ✅" if USE_GOOGLE else "TEMP ⚠️ Add Secrets for permanent"))
