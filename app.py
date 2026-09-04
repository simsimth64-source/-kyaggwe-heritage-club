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

st.set_page_config(page_title="Kyaggwe Heritage V13.1", page_icon="♻️", layout="wide")
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

def get_ws_safe(name, headers):
    if not PERMANENT_MODE or not sheet:
        return None
    try:
        for try_name in [name, name.lower(), name.capitalize(), name.upper(), "Sheet1"]:
            try:
                ws = sheet.worksheet(try_name)
                return ws
            except:
                continue
        ws = sheet.add_worksheet(title=name, rows=1000, cols=len(headers)+5)
        ws.append_row(headers)
        return ws
    except Exception as e:
        st.error(f"Sheet error {name}: {e}")
        return None

def load_data(ws_name, cols):
    if not PERMANENT_MODE:
        return pd.DataFrame(columns=cols)
    ws = get_ws_safe(ws_name, cols)
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
        return True
    ws = get_ws_safe(ws_name, headers)
    if not ws:
        try:
            ws = sheet.add_worksheet(title=ws_name, rows=1000, cols=20)
            ws.append_row(headers)
        except:
            return False
    try:
        ws.append_row([str(x) for x in row_data])
        return True
    except Exception as e:
        st.error(f"Save failed {ws_name}: {e}")
        return False
