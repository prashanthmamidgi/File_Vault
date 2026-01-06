import streamlit as st
import os
import base64
from Encrypt_Decrypt import encrypt_file, decrypt_file, hash_password
from filepath import save_user_file, get_user_files
from users import load_users

st.set_page_config(page_title="Secure File Vault", layout="centered")

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def add_bg(image):
    with open(image, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        header {{ visibility: hidden; }}
        .stApp {{
            background: url("data:image/jpeg;base64,{encoded}") center/cover no-repeat fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if "user" not in st.session_state:
    st.session_state.user = None

add_bg("images/img1.jpeg" if st.session_state.user is None else "images/img2.jpeg")

st.title("🔐 Secure File Vault")

def register_ui():
    st.subheader("Register")

    u = st.text_input("Username", key="reg_user")
    p = st.text_input("Password", type="password", key="reg_pass")

    if st.button("Register", key="reg_btn"):
        users = load_users()
        if not u or not p:
            st.error("Fields cannot be empty")
        elif u in users:
            st.error("User already exists")
        else:
            with open("users.txt", "a") as f:
                f.write(f"{u}|{hash_password(p)}\n")
            st.success("Registration successful")

def login_ui():
    st.subheader("Login")

    u = st.text_input("Username", key="login_user")
    p = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login", key="login_btn"):
        users = load_users()
        if users.get(u) == hash_password(p):
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Invalid username or password")

def dashboard():
    st.success(f"Logged in as {st.session_state.user}")

    uploaded = st.file_uploader("Upload a text file", type=["txt"], key="upload_file")
    enc_key = st.text_input("Encryption Key", type="password", key="enc_key")

    if uploaded and st.button("Encrypt File", key="encrypt_btn"):
        if not enc_key:
            st.error("Encryption key required")
        else:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded.name)
            with open(file_path, "wb") as f:
                f.write(uploaded.read())

            enc_path = encrypt_file(file_path, enc_key)
            save_user_file(st.session_state.user, enc_path)

            st.success("File encrypted successfully")
            with open(enc_path, "rb") as f:
                st.download_button(
                    "Download Encrypted File",
                    f,
                    file_name=os.path.basename(enc_path),
                    key="download_enc"
                )

    st.subheader("Your Encrypted Files")
    files = get_user_files(st.session_state.user)

    if files:
        for i, f in enumerate(files):
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(os.path.basename(f))

            dec_key = col2.text_input(
                "Decryption Key",
                type="password",
                key=f"dec_key_{i}"
            )

            if col3.button("Decrypt", key=f"dec_btn_{i}"):
                if not dec_key:
                    st.error("Key required for decryption")
                else:
                    dec_path = decrypt_file(f, dec_key)
                    st.success("File decrypted")

                    with open(dec_path, "rb") as df:
                        st.download_button(
                            "Download Decrypted File",
                            df,
                            file_name=os.path.basename(dec_path),
                            key=f"download_dec_{i}"
                        )
    else:
        st.info("No encrypted files found")

    if st.button("Logout", key="logout_btn"):
        st.session_state.user = None
        st.rerun()

if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login_ui()
    with tab2:
        register_ui()
else:
    dashboard()
