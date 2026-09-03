import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Kyaggwe Heritage Pro", page_icon="⚙️", layout="wide")

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
.stApp { background: linear-gradient(180deg, #f7f9ff 0%, #eef2ff 100%); }
.pro-header { background: linear-gradient(135deg, #0A2A5E 0%, #1746A2 50%, #0A2A5E 100%); padding: 25px 30px; border-radius: 20px; color: white; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(10,42,94,0.3); }
.pro-card { background: white; padding: 20px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border-left: 5px solid #FDB913; margin-bottom: 15px; }
.pro-stat { background: white; padding: 20px; border-radius: 16px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 4px solid #FDB913; }
.announcement-card { background: white; border-radius: 14px; padding: 18px; border-left: 5px solid #0A2A5E; box-shadow: 0 2px 12px rgba(0,0,0,0.05); margin-bottom: 12px; }
.admin-badge { background: #FDB913; color: #0A2A5E; padding: 3px 10px; border-radius: 20px; font-weight: 700; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ADMIN - ONLY THESE 3 CAN EDIT/UPLOAD - UPDATED WITH YOUR NEW BOARD
ADMIN_PASSWORDS = {
    "Khissa Pamela - President": "President123",
    "Francis Ssemugonda - Secretary": "Secretary123",
    "Ntulume Wilson Ssekulwana - Treasurer": "Treasurer123",
    # Keep old for transition
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

# YOUR EXACT BOARD FROM IMAGE
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
if "announcements" not in st.session_state: st.session_state.announcements = [{"title":"Board Updated - Welcome New Leadership!","msg":"Your real Board Officers from My Rotary are now in app. Admins can add more positions anytime from Board Officers page, and member sees it reflected instantly in his account!","date":"2026-05-13","by":"President"}]
if "member_passwords" not in st.session_state: st.session_state.member_passwords = {}
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_role" not in st.session_state: st.session_state.user_role = "Member"

def show_header(t,s): st.markdown('<div class="pro-header"><h2>' + t + '</h2><p>' + s + '</p></div>', unsafe_allow_html=True)
def is_admin(): return any(a in st.session_state.user_role for a in ADMINS)
def sync_member_role(board_name, board_position):
    # When board assigned, update that member's Role so it reflects in his account
    for m in st.session_state.members:
        if board_name.lower() in m["FullName"].lower() or m["FullName"].lower() in board_name.lower():
            m["Role"] = board_position
            break

# ---------- LOGIN WITH SELF-RESET ----------
if not st.session_state.logged_in:
    show_header("ROTARY CLUB OF KYAGGWE HERITAGE", "Club ID 228098 | District 9213 | Board Officers Synced from My Rotary")
    tab1, tab2, tab3, tab4 = st.tabs(["🔐 Admin Login", "👥 Member Login", "🆕 Register", "🔑 Forgot/Reset Password"])

    with tab1:
        if logo_path: st.image(logo_path, width=250)
        st.markdown('<div class="pro-card"><h3>Admin - Only President/Secretary/Treasurer Can Upload/Edit</h3><span class="admin-badge">ADMIN ONLY</span></div>', unsafe_allow_html=True)
        officer = st.selectbox("Select Admin", list(ADMIN_PASSWORDS.keys()))
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
        st.markdown('<div class="pro-card"><h3>Member Login - View Only</h3><p>Your account shows your Board Position automatically when admin assigns you!</p></div>', unsafe_allow_html=True)
        phone_login = st.text_input("Phone Number", placeholder="+256 7...")
        pass_login = st.text_input("Password", type="password", key="mpwd")
        if st.button("Login as Member", type="primary", use_container_width=True):
            found = next((m for m in st.session_state.members if m["Phone"] == phone_login), None)
            if found:
                saved_pwd = st.session_state.member_passwords.get(phone_login, "member123")
                if pass_login == saved_pwd:
                    st.session_state.logged_in = True
                    st.session_state.current_user = found["FullName"]
                    st.session_state.user_role = found.get("Role","Member")
                    st.session_state.officer = found["FullName"] + " - " + found.get("Role","Member")
                    st.rerun()
                else: st.error("Wrong password! Use Forgot tab to reset yourself - no admin needed.")
            else: st.error("Phone not found! Register first.")

    with tab3:
        st.markdown('<div class="pro-card"><h3>New Member Self-Registration</h3></div>', unsafe_allow_html=True)
        with st.form("reg"):
            fn = st.text_input("First Name*"); ln = st.text_input("Last Name*"); phone = st.text_input("Phone*"); email = st.text_input("Email"); new_pass = st.text_input("Create Password*", type="password"); confirm_pass = st.text_input("Confirm*", type="password")
            if st.form_submit_button("🚀 Register & Join", type="primary", use_container_width=True):
                if fn and ln and phone and new_pass and new_pass == confirm_pass:
                    if not any(m["Phone"] == phone for m in st.session_state.members):
                        full = fn + " " + ln
                        st.session_state.members.append({"MemberNo":"NEW-"+datetime.now().strftime("%Y%m%d%H%M"),"FirstName":fn,"LastName":ln,"FullName":full,"Phone":phone,"Email":email,"Role":"Member"})
                        st.session_state.member_passwords[phone] = new_pass
                        st.success("Welcome " + full + "! Now login via Member Login")
                    else: st.warning("Phone already exists!")
                else: st.error("Check fields!")

    with tab4:
        st.markdown('<div class="pro-card"><h3>🔑 Self-Reset - No Calling Admin!</h3></div>', unsafe_allow_html=True)
        with st.form("reset"):
            reset_phone = st.text_input("Registered Phone*"); verify_name = st.text_input("First Name to Verify*"); new_pass2 = st.text_input("New Password*", type="password"); confirm2 = st.text_input("Confirm*", type="password")
            if st.form_submit_button("🔄 Reset My Password", type="primary", use_container_width=True):
                found = next((m for m in st.session_state.members if m["Phone"] == reset_phone and m["FirstName"].lower() == verify_name.lower()), None)
                if found and new_pass2 and new_pass2 == confirm2:
                    st.session_state.member_passwords[reset_phone] = new_pass2
                    st.success("Reset success for " + found["FullName"] + "! Login with new password. No admin call needed!")
                else: st.error("Verification failed!")
    st.stop()

# ---------- SIDEBAR ----------
with st.sidebar:
    if logo_path: st.image(logo_path, width=180)
    st.markdown("### ⚙️ KYAGGWE HERITAGE PRO")
    st.write("User: " + str(st.session_state.current_user))
    st.markdown("Role: <b>" + str(st.session_state.user_role) + "</b> " + ("<span class='admin-badge'>ADMIN - CAN EDIT/UPLOAD</span>" if is_admin() else "<span style='background:#ddd;padding:3px 10px;border-radius:20px;font-size:12px;'>VIEW ONLY</span>"), unsafe_allow_html=True)
    st.metric("Members", len(st.session_state.members))
    st.divider()
    menu = st.radio("📱 NAVIGATION", ["🏠 Dashboard Pro","👥 Members","🏛️ Board Officers","✅ Attendance","💰 Finances","📁 Club Records","📊 Reports","📸 Gallery & Albums","📢 Club Hub","🧾 Receipts","📲 Get APK"])
    if st.button("Logout"):
        st.session_state.logged_in = False; st.session_state.user_role = "Member"; st.rerun()
    if not is_admin():
        st.error("🔒 View Only")
    else:
        st.success("✅ Admin: Can Upload/Edit")

# ---------- PAGES ----------
if menu == "🏠 Dashboard Pro":
    show_header("Welcome, " + str(st.session_state.current_user) + "!", "Role: " + str(st.session_state.user_role) + " | " + ("ADMIN - Full Access" if is_admin() else "Member - View Only"))
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown('<div class="pro-stat"><h1>👥</h1><h2>' + str(len(st.session_state.members)) + '</h2><p>Members</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="pro-stat"><h1>🏛️</h1><h2>' + str(len(st.session_state.board)) + '</h2><p>Board Officers</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="pro-stat"><h1>📸</h1><h2>' + str(len(st.session_state.gallery)) + '</h2><p>Photos</p></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="pro-stat"><h1>📁</h1><h2>' + str(len(st.session_state.records)) + '</h2><p>Records</p></div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("🏛️ Current Board")
    cols = st.columns(2)
    for i,b in enumerate(st.session_state.board):
        with cols[i%2]:
            st.markdown('<div class="pro-card"><b>' + b["Position"] + '</b><br>👤 ' + b["Name"] + '<br><small>📞 ' + b["Phone"] + ' | ✉️ ' + b["Email"] + '</small></div>', unsafe_allow_html=True)
    st.divider()
    st.subheader("📢 Announcements")
    for ann in reversed(st.session_state.announcements):
        st.markdown('<div class="announcement-card"><b>📌 ' + ann["title"] + '</b><br>' + ann["msg"] + '<br><small>📅 ' + ann["date"] + ' | By ' + ann["by"] + '</small></div>', unsafe_allow_html=True)

elif menu == "👥 Members":
    show_header("Members Directory", "Total: " + str(len(st.session_state.members)) + " | Board Position shows in account automatically")
    st.dataframe(pd.DataFrame(st.session_state.members), use_container_width=True, height=350)
    if is_admin():
        c1,c2 = st.columns(2)
        with c1:
            st.subheader("➕ Add Member (Admin Only)")
            with st.form("add_mem"):
                fn = st.text_input("First Name"); ln = st.text_input("Last Name"); ph = st.text_input("Phone"); em = st.text_input("Email"); role = st.selectbox("Role", ["Member","Club President","Club Secretary","Club Treasurer","Club Executive Secretary/Director","Club Foundation Chair","Club Learning Facilitator","Club Membership Chair","Club Public Image Chair","Club Service Projects Chair","Club Young Leaders Contact","Sergeant at Arms","Other Board Position"])
                if st.form_submit_button("Add Member", type="primary"):
                    if fn and ln and ph:
                        st.session_state.members.append({"MemberNo":"NEW","FirstName":fn,"LastName":ln,"FullName":fn+" "+ln,"Phone":ph,"Email":em,"Role":role})
                        if ph not in st.session_state.member_passwords: st.session_state.member_passwords[ph] = "member123"
                        st.success("Added " + fn + " " + ln + " as " + role); st.rerun()
        with c2:
            st.subheader("➖ Remove (Admin Only)")
            names = [m["FullName"] for m in st.session_state.members]
            sel = st.selectbox("Select", names)
            if st.button("Remove", type="primary"):
                for i,m in enumerate(st.session_state.members):
                    if m["FullName"] == sel:
                        st.session_state.members.pop(i); break
                st.warning("Removed " + sel); st.rerun()

elif menu == "🏛️ Board Officers":
    show_header("Board Officers - Add More Positions Anytime!", "When you assign member, it reflects in his account instantly")
    st.dataframe(pd.DataFrame(st.session_state.board), use_container_width=True, height=400)
    if is_admin():
        st.divider()
        st.subheader("✏️ Edit Existing Officer")
        with st.form("edit_board"):
            positions = [b["Position"] for b in st.session_state.board]
            sel_pos = st.selectbox("Select Position to Edit", positions)
            cur = next((b for b in st.session_state.board if b["Position"] == sel_pos), None)
            new_name = st.text_input("Officer Name", value=cur["Name"] if cur else "")
            new_phone = st.text_input("Phone", value=cur["Phone"] if cur else "")
            new_email = st.text_input("Email", value=cur["Email"] if cur else "")
            if st.form_submit_button("💾 Save Change & Update Member Account", type="primary"):
                for b in st.session_state.board:
                    if b["Position"] == sel_pos:
                        b["Name"]=new_name; b["Phone"]=new_phone; b["Email"]=new_email; break
                sync_member_role(new_name, sel_pos)
                st.success("Updated " + sel_pos + " = " + new_name + " - Member account now shows new position!")
                st.rerun()

        st.divider()
        st.subheader("➕ Add NEW Board Position (Provision for Future)")
        st.info("Soon you will add more officers - Use this form! Example: Sergeant at Arms, Vocational Service Chair, etc")
        with st.form("add_board"):
            pos = st.text_input("New Position Title* e.g. Sergeant at Arms")
            # Dropdown of members to assign
            member_names = [m["FullName"] for m in st.session_state.members]
            assign_name = st.selectbox("Assign to Member", member_names)
            # Auto-fill phone/email from member
            selected_member = next((m for m in st.session_state.members if m["FullName"] == assign_name), None)
            ph = st.text_input("Phone", value=selected_member["Phone"] if selected_member else "")
            em = st.text_input("Email", value=selected_member["Email"] if selected_member else "")
            if st.form_submit_button("➕ Add Board Position", type="primary"):
                if pos and assign_name:
                    # Check if position already exists
                    exists = any(b["Position"] == pos for b in st.session_state.board)
                    if not exists:
                        st.session_state.board.append({"Position":pos,"Name":assign_name,"Phone":ph,"Email":em})
                        sync_member_role(assign_name, pos)
                        st.success("Added " + pos + " = " + assign_name + " - Now reflected in " + assign_name + "'s account!")
                        st.rerun()
                    else:
                        st.warning("Position already exists! Use Edit instead.")
                else:
                    st.error("Need position and member!")

        st.divider()
        st.subheader("🗑️ Remove Board Position")
        pos_to_remove = st.selectbox("Select Position to Remove", [b["Position"] for b in st.session_state.board], key="rem")
        if st.button("Remove Position"):
            st.session_state.board = [b for b in st.session_state.board if b["Position"]!= pos_to_remove]
            st.warning("Removed " + pos_to_remove); st.rerun()
    else:
        st.info("🔒 View Only - Only President, Secretary, Treasurer can add/edit Board. Your role: " + str(st.session_state.user_role))

elif menu == "📁 Club Records":
    show_header("Club Records", "Admin Only Upload")
    if is_admin():
        with st.form("record_form"):
            title = st.text_input("Title"); category = st.selectbox("Category", ["Meeting Minutes","Constitution","Board Resolution","Other"]); f = st.file_uploader("File", type=["pdf","docx","xlsx","csv"])
            if st.form_submit_button("Upload (Admin Only)", type="primary"):
                if title and f:
                    st.session_state.records.append({"title":title,"category":category,"filename":f.name,"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"by":str(st.session_state.current_user),"data":f.getvalue()}); st.success("Uploaded"); st.rerun()
    for idx, rec in enumerate(reversed(st.session_state.records)):
        with st.expander("📄 " + rec["title"] + " - " + rec["category"]):
            st.write("File: " + rec["filename"] + " | By: " + rec["by"]); st.download_button("Download", rec["data"], rec["filename"], key="rec"+str(idx), use_container_width=True)

elif menu == "📊 Reports":
    show_header("Reports", "Admin Only Upload")
    if is_admin():
        with st.form("rep_form"):
            rtitle = st.text_input("Title"); rtype = st.selectbox("Type", ["Monthly","Financial","Project","Attendance"]); rdesc = st.text_area("Summary"); rfile = st.file_uploader("File", type=["pdf","docx","xlsx"])
            if st.form_submit_button("Upload (Admin Only)", type="primary"):
                if rtitle and rfile:
                    st.session_state.reports.append({"title":rtitle,"type":rtype,"desc":rdesc,"filename":rfile.name,"date":datetime.now().strftime("%Y-%m-%d"),"by":str(st.session_state.current_user),"data":rfile.getvalue()}); st.success("Uploaded"); st.rerun()
    for idx, rep in enumerate(reversed(st.session_state.reports)):
        st.markdown('<div class="pro-card"><b>📊 ' + rep["title"] + '</b> - ' + rep["type"] + '<br>' + rep["desc"] + '</div>', unsafe_allow_html=True)
        st.download_button("Download", rep["data"], rep["filename"], key="rep"+str(idx))

elif menu == "📸 Gallery & Albums":
    show_header("Gallery", "Admin Only Upload")
    if is_admin():
        with st.form("gal_form"):
            album = st.selectbox("Album", ["Fellowship","Projects","Community Service","Fundraising","Board Meeting","Other"]); caption = st.text_input("Caption"); photos = st.file_uploader("Photos", type=["jpg","jpeg","png"], accept_multiple_files=True)
            if st.form_submit_button("Upload (Admin Only)", type="primary"):
                if photos:
                    for p in photos: st.session_state.gallery.append({"album":album,"caption":caption,"filename":p.name,"date":datetime.now().strftime("%Y-%m-%d"),"data":p.getvalue()})
                    st.success(str(len(photos)) + " uploaded"); st.rerun()
    cols = st.columns(3)
    for idx, item in enumerate(reversed(st.session_state.gallery)):
        with cols[idx % 3]:
            st.image(item["data"], caption=item["album"] + " - " + item["caption"], use_container_width=True)
            st.download_button("Download", item["data"], item["filename"], key="gal"+str(idx))

elif menu == "📢 Club Hub":
    show_header("Club Hub - Center of Everything", "Official Info")
    if is_admin():
        with st.form("ann_form"):
            atitle = st.text_input("Announcement Title"); amsg = st.text_area("Message")
            if st.form_submit_button("Post to All Members (Admin Only)", type="primary"):
                if atitle and amsg:
                    st.session_state.announcements.append({"title":atitle,"msg":amsg,"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"by":str(st.session_state.current_user)}); st.success("Posted!"); st.rerun()
    for ann in reversed(st.session_state.announcements):
        st.markdown('<div class="announcement-card"><b>📌 ' + ann["title"] + '</b><br>' + ann["msg"] + '<br><small>📅 ' + ann["date"] + ' | By ' + ann["by"] + '</small></div>', unsafe_allow_html=True)

elif menu == "📲 Get APK":
    show_header("Share APK - Self Registration + Self Reset", "All members install and manage own password!")
    st.success("Live: https://fmwfp.streamlit.app")
    st.markdown("""
    <div class="pro-card">
    <h3>✅ Admin Powers (Only President/Secretary/Treasurer):</h3>
    - Upload/Edit Records, Reports, Gallery<br>
    - Add/Remove Members<br>
    - Add NEW Board Positions anytime (e.g. Sergeant at Arms) - Member account updates instantly!<br>
    - Edit Board Officers<br>
    - Post Announcements<br><br>
    <h3>👥 Member Powers (View Only):</h3>
    - View everything, download files, see gallery<br>
    - Cannot upload/edit - Protected!<br>
    - Can reset own password via Forgot tab - No admin call!<br>
    - Board position automatically shows in Dashboard when admin assigns them<br><br>
    <h3>➕ How to Add New Board Officer Later:</h3>
    1. Login as Admin -> Board Officers page<br>
    2. Scroll to 'Add NEW Board Position'<br>
    3. Enter Position Title e.g. Sergeant at Arms<br>
    4. Select Member from list<br>
    5. Save -> That member's Role updates everywhere instantly!
    </div>
    """, unsafe_allow_html=True)
    st.link_button("Open App Link to Share", "https://fmwfp.streamlit.app", use_container_width=True)
else:
    show_header(menu, "Coming soon")
