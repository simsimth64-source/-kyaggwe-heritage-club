import streamlit as st
import pandas as pd
from datetime import datetime, date
import uuid

try:
    import gspread
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseUpload
    import io
    GSHEETS_AVAILABLE = True
except:
    GSHEETS_AVAILABLE = False

st.set_page_config(page_title="Kyaggwe Heritage V13", page_icon="♻️", layout="wide")

SHEET_ID = st.secrets.get("SHEET_ID", "")
DRIVE_FOLDER_ID = st.secrets.get("DRIVE_FOLDER_ID", "")
PERMANENT_MODE = False
gc = None
sheet = None
drive_service = None

if GSHEETS_AVAILABLE and "gcp_service_account" in st.secrets and SHEET_ID:
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(SHEET_ID)
        drive_service = build('drive', 'v3', credentials=creds)
        PERMANENT_MODE = True
    except Exception as e:
        st.error(f"Connection failed: {e}")

def get_or_create_ws(name, headers):
    try:
        try:
            ws = sheet.worksheet(name)
        except:
            ws = sheet.add_worksheet(title=name, rows=1000, cols=20)
            ws.append_row(headers)
            return ws
        vals = ws.get_all_values()
        if not vals:
            ws.append_row(headers)
        return ws
    except:
        return None

def load_data(ws_name, cols):
    if not PERMANENT_MODE:
        return pd.DataFrame(columns=cols)
    ws = get_or_create_ws(ws_name, cols)
    if not ws:
        return pd.DataFrame(columns=cols)
    try:
        records = ws.get_all_records()
        df = pd.DataFrame(records)
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        return df
    except:
        return pd.DataFrame(columns=cols)

def append_row(ws_name, row_data, headers):
    if not PERMANENT_MODE:
        return False
    ws = get_or_create_ws(ws_name, headers)
    try:
        ws.append_row([str(x) for x in row_data])
        return True
    except Exception as e:
        st.error(f"Save failed {ws_name}: {e}")
        return False

def clear_and_save(ws_name, df, headers):
    ws = get_or_create_ws(ws_name, headers)
    try:
        ws.clear()
        ws.append_row(headers)
        if not df.empty:
            ws.append_rows(df.astype(str).values.tolist())
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

def upload_to_drive(file_bytes, filename):
    if not PERMANENT_MODE or not drive_service:
        return None
    try:
        file_metadata = {'name': filename, 'parents': [DRIVE_FOLDER_ID] if DRIVE_FOLDER_ID else []}
        media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype='application/octet-stream')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        try:
            drive_service.permissions().create(fileId=file.get('id'), body={'type': 'anyone', 'role': 'reader'}).execute()
        except:
            pass
        return file.get('webViewLink')
    except Exception as e:
        st.error(f"Drive upload failed: {e}")
        return None

MEMBER_COLS = ["Name", "Phone", "Email", "Role", "JoinDate", "Status"]
BOARD_COLS = ["Position", "Name", "Phone", "Email", "StartDate"]
ANNOUNCE_COLS = ["Date", "Title", "Message", "By"]
FILES_COLS = ["Date", "FileName", "Type", "Link", "UploadedBy"]
ATTEND_COLS = ["Date", "MemberName", "Present", "MeetingType"]
FINANCE_COLS = ["Date", "Description", "Income", "Expense", "Balance", "Category", "By"]
RECEIPT_COLS = ["Date", "MemberName", "Amount", "Purpose", "ReceiptNo", "IssuedBy"]

members_df = load_data("members", MEMBER_COLS)
board_df = load_data("board", BOARD_COLS)
announce_df = load_data("announcements", ANNOUNCE_COLS)
files_df = load_data("files", FILES_COLS)
attendance_df = load_data("attendance", ATTEND_COLS)
finances_df = load_data("finances", FINANCE_COLS)
receipts_df = load_data("receipts", RECEIPT_COLS)

if board_df.empty and PERMANENT_MODE:
    defaults = [["President","To be assigned","","",""], ["Secretary","Francis Ssemugonda","","",""], ["Treasurer","To be assigned","","",""]]
    for r in defaults:
        append_row("board", r, BOARD_COLS)
    board_df = load_data("board", BOARD_COLS)

if PERMANENT_MODE:
    st.sidebar.success("✅ PERMANENT MODE V13 ALL PERMANENT")
else:
    st.sidebar.warning("⚠️ TEMP MODE")

st.sidebar.markdown("### Rotary Kyaggwe Heritage")
st.sidebar.markdown("Francis Ssemugonda - Secretary")
menu = st.sidebar.radio("MENU", ["🏠 Dashboard (Permanent)", "👥 Members (Permanent)", "🏛️ Board Officers (Permanent)", "✅ Attendance (Permanent)", "💰 Finances (Permanent)", "📁 Club Records (Permanent)", "📊 Reports (Permanent)", "📸 Gallery (Permanent)", "📢 Club Hub (Permanent)", "🧾 Receipts (Permanent)", "📱 Get APK"])

if "Dashboard" in menu:
    st.markdown("<h1 style='text-align:center;color:#1e3a8a'>Rotary Club of Kyaggwe Heritage</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>V13 - ALL PERMANENT - Nothing Disappears!</h3>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Members", len(members_df))
    c2.metric("Attendance", len(attendance_df))
    c3.metric("Finances", len(finances_df))
    c4.metric("Files", len(files_df))
    st.divider()
    st.dataframe(members_df.tail(5))

elif "Members" in menu:
    st.header("👥 Members - Permanent")
    with st.form("add_member"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        role = st.selectbox("Role", ["Member","President","Secretary","Treasurer","Board"])
        if st.form_submit_button("Add Member (Permanent Save)"):
            if name:
                append_row("members", [name, phone, email, role, str(date.today()), "Active"], MEMBER_COLS)
                st.success(f"Member {name} saved permanently!")
                st.rerun()
    st.dataframe(members_df, use_container_width=True)

elif "Board" in menu:
    st.header("🏛️ Board Officers - Permanent")
    with st.form("board_form"):
        pos = st.selectbox("Position", ["President","Vice President","Secretary","Treasurer","Membership Chair","Service Projects","Public Image","Foundation Chair","SAA"])
        bname = st.text_input("Name")
        bphone = st.text_input("Phone")
        bemail = st.text_input("Email")
        if st.form_submit_button("Save Board Officer Permanently"):
            append_row("board", [pos, bname, bphone, bemail, str(date.today())], BOARD_COLS)
            st.success("Saved!")
            st.rerun()
    st.dataframe(board_df, use_container_width=True)

elif "Attendance" in menu:
    st.header("✅ Attendance - Permanent V13")
    with st.form("attend_form"):
        att_date = st.date_input("Meeting Date", date.today())
        meeting_type = st.selectbox("Meeting Type", ["Weekly Fellowship","Board Meeting","Service Project","Special"])
        member_names = members_df["Name"].tolist() if not members_df.empty else ["Guest"]
        selected_member = st.selectbox("Member", member_names)
        present = st.selectbox("Status", ["Present","Absent","Apology"])
        if st.form_submit_button("Save Attendance Permanently"):
            append_row("attendance", [str(att_date), selected_member, present, meeting_type], ATTEND_COLS)
            st.success(f"Attendance for {selected_member} saved permanently!")
            st.rerun()
    st.dataframe(attendance_df, use_container_width=True)

elif "Finances" in menu:
    st.header("💰 Finances - Permanent V13")
    with st.form("finance_form"):
        f_date = st.date_input("Date", date.today())
        desc = st.text_input("Description")
        income = st.number_input("Income (UGX)", min_value=0, step=1000)
        expense = st.number_input("Expense (UGX)", min_value=0, step=1000)
        category = st.selectbox("Category", ["Membership Fees","Donation","Project","Administration","Fellowship","Other"])
        by = st.text_input("Recorded By", "Francis Ssemugonda")
        if st.form_submit_button("Save Finance Permanently"):
            try:
                prev_income = pd.to_numeric(finances_df["Income"], errors='coerce').sum() if not finances_df.empty else 0
                prev_expense = pd.to_numeric(finances_df["Expense"], errors='coerce').sum() if not finances_df.empty else 0
                new_bal = (prev_income + income) - (prev_expense + expense)
            except:
                new_bal = income - expense
            append_row("finances", [str(f_date), desc, income, expense, new_bal, category, by], FINANCE_COLS)
            st.success(f"Finance saved! Balance: {new_bal}")
            st.rerun()
    st.dataframe(finances_df, use_container_width=True)

elif "Club Records" in menu:
    st.header("📁 Club Records - Permanent")
    uploaded = st.file_uploader("Upload Document", type=["pdf","docx","xlsx","jpg","png"])
    if uploaded and st.button("Upload to Permanent Drive"):
        link = upload_to_drive(uploaded.getvalue(), uploaded.name)
        if link:
            append_row("files", [str(date.today()), uploaded.name, "Document", link, "Secretary"], FILES_COLS)
            st.success(f"Uploaded! {link}")
            st.rerun()
    st.dataframe(files_df, use_container_width=True)

elif "Reports" in menu:
    st.header("📊 Reports - Permanent")
    if not finances_df.empty:
        st.dataframe(finances_df)
        csv = finances_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Finance CSV", csv, "finances_v13.csv", "text/csv")
    if not attendance_df.empty:
        csv2 = attendance_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Attendance CSV", csv2, "attendance_v13.csv", "text/csv")

elif "Gallery" in menu:
    st.header("📸 Gallery - Permanent Drive")
    img = st.file_uploader("Upload Photo", type=["jpg","jpeg","png"])
    if img and st.button("Upload Photo Permanently"):
        link = upload_to_drive(img.getvalue(), img.name)
        if link:
            append_row("files", [str(date.today()), img.name, "Gallery", link, "Secretary"], FILES_COLS)
            st.success("Photo saved permanently!")
            st.rerun()
    gallery = files_df[files_df["Type"] == "Gallery"] if not files_df.empty else pd.DataFrame()
    for _, r in gallery.iterrows():
        st.markdown(f"**{r['FileName']}** - [View]({r['Link']})")

elif "Club Hub" in menu:
    st.header("📢 Club Hub - Permanent")
    with st.form("announce_form"):
        title = st.text_input("Title")
        msg = st.text_area("Message")
        if st.form_submit_button("Post Announcement Permanently"):
            append_row("announcements", [str(datetime.now()), title, msg, "Secretary"], ANNOUNCE_COLS)
            st.success("Posted!")
            st.rerun()
    st.dataframe(announce_df, use_container_width=True)

elif "Receipts" in menu:
    st.header("🧾 Receipts - Permanent V13")
    with st.form("receipt_form"):
        r_date = st.date_input("Date", date.today())
        r_member = st.selectbox("Member", members_df["Name"].tolist() if not members_df.empty else ["Guest"])
        amount = st.number_input("Amount", min_value=0, step=1000)
        purpose = st.text_input("Purpose")
        receipt_no = st.text_input("Receipt No", f"RCP-{uuid.uuid4().hex[:6].upper()}")
        issued_by = st.text_input("Issued By", "Francis Ssemugonda")
        if st.form_submit_button("Issue Receipt Permanently"):
            append_row("receipts", [str(r_date), r_member, amount, purpose, receipt_no, issued_by], RECEIPT_COLS)
            st.success(f"Receipt {receipt_no} saved!")
            st.rerun()
    st.dataframe(receipts_df, use_container_width=True)

else:
    st.header("📱 Get APK")
    st.write("App link: https://kyaggwe-heritage-club.streamlit.app")
    st.info("V13 ALL PERMANENT - All modules save to Google Sheets!")

st.sidebar.divider()
st.sidebar.write(f"V13 | {len(members_df)} Members | {len(finances_df)} Finance | {len(attendance_df)} Attendance")
