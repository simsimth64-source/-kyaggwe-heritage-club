import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Kyaggwe Heritage", page_icon="⚙️", layout="wide")

def get_logo():
    for p in ["logo_exact_final.png.jpg","logo_exact_final.png","logo.png","logo.jpg","rotary_logo.png"]:
        if os.path.exists(p):
            return p
    return None
logo_path = get_logo()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: #f0f4ff; }
.welcome-banner { background: linear-gradient(135deg, #0A2A5E 0%, #1746A2 60%, #FDB913 100%); padding: 25px; border-radius: 18px; text-align: center; color: white; margin-bottom: 15px; }
.pro-header { background: linear-gradient(135deg, #0A2A5E 0%, #1746A2 100%); padding: 18px 20px; border-radius: 15px; color: white; margin-bottom: 15px; }
.pro-card { background: white; padding: 18px; border-radius: 14px; box-shadow: 0 3px 15px rgba(0,0,0,0.06); border-left: 5px solid #FDB913; margin-bottom: 12px; }
.icon-card { background: white; padding: 18px; border-radius: 16px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 4px solid #FDB913; height: 130px; }
</style>
""", unsafe_allow_html=True)

ADMIN_PASSWORDS = {
    "Khissa Pamela - President": "President123",
    "Francis Ssemugonda - Secretary": "Secretary123",
    "Ntulume Wilson Ssekulwana - Treasurer": "Treasurer123",
    "Mubeezi Geoffrey - Secretary": "Secretary123",
    "Kasirye Simon Peter - Treasurer": "Treasurer123"
}
ADMINS = ["President","Secretary","Treasurer"]

DEFAULT_MEMBERS = [
    {"MemberNo":"11563120","FirstName":"Muzige","LastName":"Abubaker","FullName":"Muzige Abubaker","Phone":"+256 757447213","Email":"muzigeabubakar@gmail.com","Role":"Club Executive Secretary/Director"},
    {"MemberNo":"11460462","FirstName":"Beatrice","LastName":"Kasirye","FullName":"Beatrice Nannozi Kasirye","Phone":"+256 0782145945","Email":"beatricenanozi@gmail.com","Role":"Club Learning Facilitator"},
    {"MemberNo":"12666632","FirstName":"Simon","LastName":"Katinda","FullName":"Simon Katinda","Phone":"+256 782602035","Email":"katsimon327@gmail.com","Role":"Member"},
    {"MemberNo":"12664746","FirstName":"Twaha","LastName":"Kayondo","FullName":"Twaha William Kayondo","Phone":"+256 782645644","Email":"twahakayondo@gmail.com","Role":"Club Membership Chair"},
    {"MemberNo":"12666762","FirstName":"Jamir","LastName":"Kibirige","FullName":"Jamir Kibirige","Phone":"+256 704797943","Email":"jakibirige1@gmail.com","Role":"Club Young Leaders Contact"},
    {"MemberNo":"12664764","FirstName":"Moses","LastName":"Kizito","FullName":"Moses Kizito","Phone":"+256 702330143","Email":"kizito.moses2@gmail.com","Role":"Club Foundation Chair"},
    {"MemberNo":"12666737","FirstName":"Sarah","LastName":"Laker","FullName":"Sarah Laker","Phone":"+256 705510951","Email":"lakersarah82@gmail.com","Role":"Member"},
    {"MemberNo":"11816050","FirstName":"Samuel","LastName":"Lukondha","FullName":"Samuel Lukondha","Phone":"+256 703998227","Email":"lukondhasa@yahoo.com","Role":"Member"},
    {"MemberNo":"12394274","FirstName":"Bashir","LastName":"Masembe","FullName":"Bashir Masembe","Phone":"+256 771242277","Email":"masembebash@gmail.com","Role":"Member"},
    {"MemberNo":"12666750","FirstName":"Lucky","LastName":"Mugisha","FullName":"Lucky Racheal Mugisha","Phone":"+256 785804292","Email":"humberlacy@gmail.com","Role":"Club Public Image Chair"},
    {"MemberNo":"12666771","FirstName":"Henry","LastName":"Mukalazi","FullName":"Henry Mukalazi","Phone":"+256 701145732","Email":"heronahospital76@gmail.com","Role":"Member"},
    {"MemberNo":"12666597","FirstName":"Annet","LastName":"Nankabirwa","FullName":"Annet Nankabirwa","Phone":"+256 782059870","Email":"annetnank@gmail.com","Role":"Club Service Projects Chair"},
    {"MemberNo":"12666794","FirstName":"Andrew","LastName":"Ndaura","FullName":"Andrew Ndaura","Phone":"+256 775180954","Email":"drea92002@gmail.com","Role":"Member"},
    {"MemberNo":"12666781","FirstName":"Denis","LastName":"Onyama","FullName":"Denis Onyama","Phone":"+256 774337111","Email":"denis.onyama@gmail.com","Role":"Member"},
    {"MemberNo":"12666652","FirstName":"Mariah","LastName":"Owino","FullName":"Mariah Owino","Phone":"+256 772846171","Email":"mariahebenah.mb@gmail.com","Role":"Member"},
    {"MemberNo":"12664727","FirstName":"Khissa","LastName":"Pamela","FullName":"Khissa Pamela","Phone":"+256 781451436","Email":"pamelakhissa4@gmail.com","Role":"Club President"},
    {"MemberNo":"12664757","FirstName":"Ntulume","LastName":"Ssekulwana","FullName":"Ntulume Wilson Ssekulwana","Phone":"+256 752525386","Email":"wilsonntulume97@gmail.com","Role":"Club Treasurer"},
    {"MemberNo":"12664735","FirstName":"Francis","LastName":"Ssemugonda","FullName":"Francis Ssemugonda","Phone":"+256 762736379","Email":"francisssemugonda@gmail.com","Role":"Club Secretary"},
]
DEFAULT_BOARD = [
    {"Position":"Club Executive Secretary/Director","Name":"Muzige Abubaker","Phone":"+256 757447213","Email":"muzigeabubakar@gmail.com"},
    {"Position":"Club Foundation Chair","Name":"Moses Kizito","Phone":"+256 702330143","Email":"kizito.moses2@gmail.com"},
    {"Position":"Club Learning Facilitator","Name":"Beatrice Nannozi Kasirye","Phone":"+256 0782145945","Email":"beatricenanozi@gmail.com"},
    {"Position":"Club Membership Chair","Name":"Twaha William Kayondo","Phone":"+256 782645644","Email":"twahakayondo@gmail.com"},
    {"Position":"Club President","Name":"Khissa Pamela","Phone":"+256 781451436","Email":"pamelakhissa4@gmail.com"},
    {"Position":"Club Public Image Chair","Name":"Lucky Racheal Mugisha","Phone":"+256 785804292","Email":"humberlacy@gmail.com"},
    {"Position":"Club Secretary","Name":"Francis Ssemugonda","Phone":"+256 762736379","Email":"francisssemugonda@gmail.com"},
    {"Position":"Club Treasurer","Name":"Ntulume Wilson Ssekulwana","Phone":"+256 752525386","Email":"wilsonntulume97@gmail.com"},
    {"Position":"Club Service Projects Chair","Name":"Annet Nankabirwa","Phone":"+256 782059870","Email":"annetnank@gmail.com"},
    {"Position":"Club Young Leaders Contact","Name":"Jamir Kibirige","Phone":"+256 704797943","Email":"jakibirige1@gmail.com"},
]

if "members" not in st.session_state: st.session_state.members = DEFAULT_MEMBERS.copy()
if "board" not in st.session_state: st.session_state.board = DEFAULT_BOARD.copy()
if "records" not in st.session_state: st.session_state.records = []
if "reports" not in st.session_state: st.session_state.reports = []
if "gallery" not in st.session_state: st.session_state.gallery = []
if "announcements" not in st.session_state: st.session_state.announcements = [{"title":"Welcome to Kyaggwe Heritage!","msg":"App is live with logo and welcome screen!","date":"2026-05-13","by":"President"}]
if "member_passwords" not in st.session_state: st.session_state.member_passwords = {}
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_role" not in st.session_state: st.session_state.user_role = "Member"

def show_header(icon, title, subtitle):
    st.markdown('<div class="pro-header"><h2>' + icon + ' ' + title + '</h2><p>' + subtitle + '</p></div>', unsafe_allow_html=True)
def is_admin():
    return any(a in st.session_state.user_role for a in ADMINS)

# ---------- LOGIN - SIMPLE NO STOP LOOP ----------
if not st.session_state.logged_in:
    st.markdown('<div class="welcome-banner"><div style="font-size:60px;">⚙️</div><h1>Kyaggwe Heritage</h1><h3>Welcome to Kyaggwe Heritage</h3><p>Rotary Club | District 9213 | Service • Fellowship • Community</p><p>Club ID: 228098</p></div>', unsafe_allow_html=True)
    if logo_path:
        st.image(logo_path, width=180)
    tab1, tab2, tab3, tab4 = st.tabs(["🔐 Admin", "👥 Member", "🆕 Register", "🔑 Reset"])
    with tab1:
        officer = st.selectbox("Admin", list(ADMIN_PASSWORDS.keys()))
        pwd = st.text_input("Password", type="password", key="apwd")
        if st.button("Login as Admin", type="primary", use_container_width=True):
            if ADMIN_PASSWORDS.get(officer) == pwd:
                st.session_state.logged_in = True
                st.session_state.current_user = officer
                st.session_state.user_role = officer.split(" - ")[1]
                st.session_state.officer = officer
                st.rerun()
            else: st.error("Wrong!")
    with tab2:
        phone_login = st.text_input("Phone", placeholder="+256 7...")
        pass_login = st.text_input("Password", type="password", key="mpwd")
        if st.button("Login as Member", type="primary", use_container_width=True):
            found = next((m for m in st.session_state.members if m["Phone"] == phone_login), None)
            if found:
                saved_pwd = st.session_state.member_passwords.get(phone_login, "member123")
                if pass_login == saved_pwd:
                    st.session_state.logged_in = True
                    st.session_state.current_user = found["FullName"]
                    st.session_state.user_role = found.get("Role","Member")
                    st.session_state.officer = found["FullName"]
                    st.rerun()
                else: st.error("Wrong password! Use Reset")
            else: st.error("Phone not found!")
    with tab3:
        with st.form("reg"):
            fn = st.text_input("First Name*"); ln = st.text_input("Last Name*"); phone = st.text_input("Phone*"); email = st.text_input("Email"); new_pass = st.text_input("Password*", type="password"); confirm_pass = st.text_input("Confirm*", type="password")
            if st.form_submit_button("Register", type="primary", use_container_width=True):
                if fn and ln and phone and new_pass and new_pass == confirm_pass:
                    if not any(m["Phone"] == phone for m in st.session_state.members):
                        full = fn + " " + ln
                        st.session_state.members.append({"MemberNo":"NEW-"+datetime.now().strftime("%Y%m%d%H%M"),"FirstName":fn,"LastName":ln,"FullName":full,"Phone":phone,"Email":email,"Role":"Member"})
                        st.session_state.member_passwords[phone] = new_pass
                        st.success("Welcome " + full + "! Now login")
                    else: st.warning("Phone exists!")
                else: st.error("Check fields!")
    with tab4:
        with st.form("reset"):
            reset_phone = st.text_input("Registered Phone*"); verify_name = st.text_input("First Name*"); new_pass2 = st.text_input("New Password*", type="password"); confirm2 = st.text_input("Confirm*", type="password")
            if st.form_submit_button("Reset Password", type="primary", use_container_width=True):
                found = next((m for m in st.session_state.members if m["Phone"] == reset_phone and m["FirstName"].lower() == verify_name.lower()), None)
                if found and new_pass2 and new_pass2 == confirm2:
                    st.session_state.member_passwords[reset_phone] = new_pass2
                    st.success("Reset success! Login with new password")
                else: st.error("Verification failed!")
    st.stop()

# ---------- SIDEBAR ----------
with st.sidebar:
    if logo_path: st.image(logo_path, width=160)
    st.markdown("### ⚙️ KYAGGWE HERITAGE")
    st.write("👤 " + str(st.session_state.current_user))
    st.caption("🏷️ " + str(st.session_state.user_role))
    st.metric("👥 Members", len(st.session_state.members))
    st.divider()
    menu = st.radio("📱 MENU", ["🏠 Dashboard","👥 Members","🏛️ Board Officers","✅ Attendance","💰 Finances","📁 Club Records","📊 Reports","📸 Gallery","📢 Club Hub","🧾 Receipts","📲 Get APK with Logo"])
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------- PAGES ----------
if menu == "🏠 Dashboard":
    st.markdown('<div class="welcome-banner"><h2>Welcome to Kyaggwe Heritage, ' + str(st.session_state.current_user).split(" -")[0] + '!</h2><p>Role: ' + str(st.session_state.user_role) + ' | ' + datetime.now().strftime("%b %d, %Y") + '</p></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown('<div class="icon-card"><div style="font-size:35px;">👥</div><h3>' + str(len(st.session_state.members)) + '</h3><p>Members</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="icon-card"><div style="font-size:35px;">🏛️</div><h3>' + str(len(st.session_state.board)) + '</h3><p>Board</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="icon-card"><div style="font-size:35px;">📸</div><h3>' + str(len(st.session_state.gallery)) + '</h3><p>Photos</p></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="icon-card"><div style="font-size:35px;">📁</div><h3>' + str(len(st.session_state.records)) + '</h3><p>Records</p></div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("🏛️ Board Officers")
    cols = st.columns(2)
    for i,b in enumerate(st.session_state.board):
        with cols[i%2]:
            st.markdown('<div class="pro-card"><b>🏛️ ' + b["Position"] + '</b><br>👤 ' + b["Name"] + '</div>', unsafe_allow_html=True)
    st.subheader("📢 Announcements")
    for ann in reversed(st.session_state.announcements):
        st.markdown('<div class="pro-card"><b>📌 ' + ann["title"] + '</b><br>' + ann["msg"] + '<br><small>' + ann["date"] + ' | By ' + ann["by"] + '</small></div>', unsafe_allow_html=True)

elif menu == "👥 Members":
    show_header("👥","Members Directory","Total: " + str(len(st.session_state.members)))
    st.dataframe(pd.DataFrame(st.session_state.members), use_container_width=True, height=350)
    st.download_button("Download CSV", pd.DataFrame(st.session_state.members).to_csv(index=False), "members.csv", "text/csv", use_container_width=True)
    if is_admin():
        with st.form("add_mem"):
            st.subheader("➕ Add Member (Admin Only)")
            fn = st.text_input("First Name"); ln = st.text_input("Last Name"); ph = st.text_input("Phone"); em = st.text_input("Email"); role = st.selectbox("Role", ["Member","Club President","Club Secretary","Club Treasurer","Club Executive Secretary/Director","Club Foundation Chair","Club Learning Facilitator","Club Membership Chair","Club Public Image Chair","Club Service Projects Chair","Club Young Leaders Contact","Other"])
            if st.form_submit_button("Add Member", type="primary"):
                if fn and ln and ph:
                    st.session_state.members.append({"MemberNo":"NEW","FirstName":fn,"LastName":ln,"FullName":fn+" "+ln,"Phone":ph,"Email":em,"Role":role})
                    if ph not in st.session_state.member_passwords: st.session_state.member_passwords[ph] = "member123"
                    st.success("Added"); st.rerun()

elif menu == "🏛️ Board Officers":
    show_header("🏛️","Board Officers","Add more anytime - Reflects in member account")
    st.dataframe(pd.DataFrame(st.session_state.board), use_container_width=True, height=400)
    if is_admin():
        st.divider()
        st.subheader("➕ Add NEW Board Position")
        with st.form("add_board"):
            pos = st.text_input("New Position e.g. Sergeant at Arms")
            member_names = [m["FullName"] for m in st.session_state.members]
            assign_name = st.selectbox("Assign to Member", member_names)
            selected_member = next((m for m in st.session_state.members if m["FullName"] == assign_name), None)
            ph = st.text_input("Phone", value=selected_member["Phone"] if selected_member else "")
            em = st.text_input("Email", value=selected_member["Email"] if selected_member else "")
            if st.form_submit_button("Add Position", type="primary"):
                if pos and assign_name:
                    if not any(b["Position"] == pos for b in st.session_state.board):
                        st.session_state.board.append({"Position":pos,"Name":assign_name,"Phone":ph,"Email":em})
                        for m in st.session_state.members:
                            if m["FullName"] == assign_name:
                                m["Role"] = pos
                                break
                        st.success("Added " + pos + " = " + assign_name); st.rerun()
                    else: st.warning("Position exists!")

elif menu == "✅ Attendance":
    show_header("✅","Smart Attendance","Upload Excel - Auto matches")
    uploaded = st.file_uploader("Upload Attendance", type=["xlsx","csv"])
    if uploaded:
        att_df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        st.dataframe(att_df.head(), use_container_width=True)
        present = []
        for _, row in att_df.iterrows():
            name_str = str(row.iloc[0]).lower()
            for mem in st.session_state.members:
                if mem["FirstName"].lower() in name_str or mem["LastName"].lower() in name_str:
                    present.append(mem["FullName"]); break
        present = list(set(present))
        c1,c2 = st.columns(2); c1.metric("Present", str(len(present)) + "/" + str(len(st.session_state.members))); c2.metric("Absent", len(st.session_state.members)-len(present))
        st.write(present)

elif menu == "💰 Finances":
    show_header("💰","Finances & Dues","Track payments")
    rows = [{"FullName": m["FullName"], "Phone": m["Phone"], "Dues Paid": 0, "Balance": 50000} for m in st.session_state.members]
    fin_df = pd.DataFrame(rows)
    if is_admin():
        st.data_editor(fin_df, use_container_width=True, height=500)
    else:
        st.dataframe(fin_df, use_container_width=True, height=500)

elif menu == "📁 Club Records":
    show_header("📁","Club Records Vault","Upload & Download")
    if is_admin():
        with st.form("record_form", clear_on_submit=True):
            title = st.text_input("Record Title*"); category = st.selectbox("Category", ["Meeting Minutes","Constitution","Other"]); f = st.file_uploader("Upload File*", type=["pdf","docx","xlsx","csv"])
            if st.form_submit_button("Upload Record", type="primary", use_container_width=True):
                if title and f:
                    st.session_state.records.append({"title":title,"category":category,"filename":f.name,"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"by":str(st.session_state.current_user),"data":f.getvalue()}); st.success("Uploaded"); st.rerun()
    for idx, rec in enumerate(reversed(st.session_state.records)):
        with st.expander("📄 " + rec["title"] + " - " + rec["category"]):
            st.write("File: " + rec["filename"] + " | By: " + rec["by"])
            st.download_button("Download", rec["data"], rec["filename"], key="rec"+str(idx), use_container_width=True)

elif menu == "📊 Reports":
    show_header("📊","Reports Center","Upload & Download")
    if is_admin():
        with st.form("rep_form", clear_on_submit=True):
            rtitle = st.text_input("Title*"); rtype = st.selectbox("Type", ["Monthly","Financial","Project"]); rdesc = st.text_area("Summary"); rfile = st.file_uploader("Upload File*", type=["pdf","docx","xlsx"])
            if st.form_submit_button("Upload Report", type="primary", use_container_width=True):
                if rtitle and rfile:
                    st.session_state.reports.append({"title":rtitle,"type":rtype,"desc":rdesc,"filename":rfile.name,"date":datetime.now().strftime("%Y-%m-%d"),"by":str(st.session_state.current_user),"data":rfile.getvalue()}); st.success("Uploaded"); st.rerun()
    for idx, rep in enumerate(reversed(st.session_state.reports)):
        st.markdown('<div class="pro-card"><b>📊 ' + rep["title"] + '</b> - ' + rep["type"] + '<br>' + rep["desc"] + '</div>', unsafe_allow_html=True)
        st.download_button("Download", rep["data"], rep["filename"], key="rep"+str(idx), use_container_width=True)

elif menu == "📸 Gallery":
    show_header("📸","Photo Gallery","Fellowship, Projects, Events")
    if is_admin():
        with st.form("gal_form", clear_on_submit=True):
            album = st.selectbox("Album", ["Fellowship","Projects","Community Service","Fundraising","Board Meeting","Other"]); caption = st.text_input("Caption"); photos = st.file_uploader("Upload Photos*", type=["jpg","jpeg","png"], accept_multiple_files=True)
            if st.form_submit_button("Upload Photos", type="primary", use_container_width=True):
                if photos:
                    for p in photos: st.session_state.gallery.append({"album":album,"caption":caption,"filename":p.name,"date":datetime.now().strftime("%Y-%m-%d"),"data":p.getvalue()})
                    st.success(str(len(photos)) + " uploaded"); st.rerun()
    filter_album = st.selectbox("Filter by Album", ["All","Fellowship","Projects","Community Service","Fundraising","Board Meeting","Other"])
    filtered = st.session_state.gallery if filter_album == "All" else [g for g in st.session_state.gallery if g["album"] == filter_album]
    cols = st.columns(3)
    for idx, item in enumerate(reversed(filtered)):
        with cols[idx % 3]:
            st.image(item["data"], caption=item["album"] + " - " + item["caption"], use_container_width=True)
            st.download_button("Download", item["data"], item["filename"], key="gal"+str(idx), use_container_width=True)

elif menu == "📢 Club Hub":
    show_header("📢","Club Info Hub","Center of Everything")
    if is_admin():
        with st.form("ann_form", clear_on_submit=True):
            atitle = st.text_input("Title*"); amsg = st.text_area("Message*")
            if st.form_submit_button("Post Announcement", type="primary", use_container_width=True):
                if atitle and amsg:
                    st.session_state.announcements.append({"title":atitle,"msg":amsg,"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"by":str(st.session_state.current_user)}); st.success("Posted!"); st.rerun()
    for ann in reversed(st.session_state.announcements):
        st.markdown('<div class="pro-card"><b>📌 ' + ann["title"] + '</b><br>' + ann["msg"] + '<br><small>' + ann["date"] + ' | By ' + ann["by"] + '</small></div>', unsafe_allow_html=True)

elif menu == "🧾 Receipts":
    show_header("🧾","Receipts","Generate receipts")
    names = [m["FullName"] for m in st.session_state.members]
    member = st.selectbox("Member", names)
    amt = st.number_input("Amount UGX", value=50000, step=1000)
    purp = st.selectbox("Purpose", ["Membership Dues","Donation","Fellowship Fee","Other"])
    if st.button("Generate Receipt", type="primary", use_container_width=True):
        rec_no = "RCKH-" + datetime.now().strftime("%Y%m%d%H%M%S")
        st.success("Receipt Generated!")
        st.code("Receipt No: " + rec_no + "\nMember: " + member + "\nAmount: UGX " + str(amt) + "\nPurpose: " + purp + "\nDate: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\nIssued by: " + str(st.session_state.current_user))

elif menu == "📲 Get APK with Logo":
    show_header("📲","Get APK with Club Logo & Welcome Screen","Logo icon + Welcome to Kyaggwe Heritage")
    st.success("Live URL: https://fmwfp.streamlit.app")
    st.markdown("""
    <div class="pro-card">
    <h3>🎯 How to Make APK with Club Logo Icon + Welcome Screen</h3>
    <b>STEP 1 - Make Square Logo 512x512 PNG:</b><br>
    - Crop your logo_exact_final.png.jpg to square 512x512 using picsart or remove.bg<br>
    - Save as rotary_512.png<br><br>
    <b>STEP 2 - Build APK with Logo (PWABuilder - Best):</b><br>
    1. Go to www.pwabuilder.com<br>
    2. Enter https://fmwfp.streamlit.app -> Start -> Build My PWA<br>
    3. Select Android -> Upload your 512x512 logo as icon<br>
    4. Set Splash Text: Welcome to Kyaggwe Heritage<br>
    5. Download APK -> Icon will be your club logo!<br><br>
    <b>STEP 3 - Quick Method (100% Works Now):</b><br>
    1. Open Chrome -> https://fmwfp.streamlit.app<br>
    2. Tap 3 dots ⋮ -> Add to Home screen -> Install<br>
    3. Icon = Club logo, Tap it -> You see Welcome to Kyaggwe Heritage banner (V10 has it!)<br>
    </div>
    """, unsafe_allow_html=True)
    if logo_path:
        st.image(logo_path, width=200, caption="Your logo - will be APK icon")
    st.link_button("Open App Link", "https://fmwfp.streamlit.app", use_container_width=True)
