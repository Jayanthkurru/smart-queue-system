import hashlib

USER_FILE = "users.csv"

# -------------------------
# LANGUAGE DATA (INDIA)
# -------------------------
languages = {
    "English": {
        "login": "Login",
        "register": "Register",
        "username": "Username",
        "password": "Password",
        "new_user": "New Username",
        "new_pass": "New Password",
        "login_btn": "Login",
        "register_btn": "Register",
        "success_login": "Login successful",
        "error_login": "Invalid username or password",
        "success_register": "Registration successful",
    },
    "Hindi": {
        "login": "लॉगिन",
        "register": "रजिस्टर",
        "username": "यूज़रनेम",
        "password": "पासवर्ड",
        "new_user": "नया यूज़रनेम",
        "new_pass": "नया पासवर्ड",
        "login_btn": "लॉगिन",
        "register_btn": "रजिस्टर",
        "success_login": "सफल लॉगिन",
        "error_login": "गलत जानकारी",
        "success_register": "पंजीकरण सफल",
    },
    "Telugu": {
        "login": "లాగిన్",
        "register": "నమోదు",
        "username": "యూజర్ పేరు",
        "password": "పాస్‌వర్డ్",
        "new_user": "కొత్త యూజర్ పేరు",
        "new_pass": "కొత్త పాస్‌వర్డ్",
        "login_btn": "లాగిన్",
        "register_btn": "నమోదు",
        "success_login": "లాగిన్ విజయవంతం",
        "error_login": "తప్పు వివరాలు",
        "success_register": "నమోదు విజయవంతం",
    },
    "Tamil": {
        "login": "உள்நுழைவு",
        "register": "பதிவு",
        "username": "பயனர் பெயர்",
        "password": "கடவுச்சொல்",
        "new_user": "புதிய பயனர்",
        "new_pass": "புதிய கடவுச்சொல்",
        "login_btn": "உள்நுழைவு",
        "register_btn": "பதிவு",
        "success_login": "வெற்றிகரமான உள்நுழைவு",
        "error_login": "தவறான தகவல்",
        "success_register": "பதிவு வெற்றி",
    },
    "Kannada": {
        "login": "ಲಾಗಿನ್",
        "register": "ನೋಂದಣಿ",
        "username": "ಬಳಕೆದಾರ ಹೆಸರು",
        "password": "ಪಾಸ್ವರ್ಡ್",
        "new_user": "ಹೊಸ ಬಳಕೆದಾರ",
        "new_pass": "ಹೊಸ ಪಾಸ್ವರ್ಡ್",
        "login_btn": "ಲಾಗಿನ್",
        "register_btn": "ನೋಂದಣಿ",
        "success_login": "ಲಾಗಿನ್ ಯಶಸ್ವಿ",
        "error_login": "ತಪ್ಪು ಮಾಹಿತಿ",
        "success_register": "ನೋಂದಣಿ ಯಶಸ್ವಿ",
    },
    "Malayalam": {
        "login": "ലോഗിൻ",
        "register": "രജിസ്റ്റർ",
        "username": "യൂസർനേം",
        "password": "പാസ്‌വേഡ്",
        "new_user": "പുതിയ യൂസർ",
        "new_pass": "പുതിയ പാസ്‌വേഡ്",
        "login_btn": "ലോഗിൻ",
        "register_btn": "രജിസ്റ്റർ",
        "success_login": "ലോഗിൻ വിജയകരം",
        "error_login": "തെറ്റായ വിവരം",
        "success_register": "രജിസ്ട്രേഷൻ വിജയകരം",
    }
}

# -------------------------
# LANGUAGE SELECT
# -------------------------
selected_lang = st.selectbox("🌐 Select Language", list(languages.keys()))
text = languages[selected_lang]

# -------------------------
# USER DB
# -------------------------
def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        return pd.DataFrame(columns=["username", "password"])

def save_users(df):
    df.to_csv(USER_FILE, index=False)

users_df = load_users()

# -------------------------
# HASH
# -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------
# SESSION
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Login"

# -------------------------
# PAGE SWITCH
# -------------------------
col1, col2 = st.columns(2)
with col1:
    if st.button(text["login"]):
        st.session_state.page = "Login"
with col2:
    if st.button(text["register"]):
        st.session_state.page = "Register"

# -------------------------
# REGISTER
# -------------------------
if st.session_state.page == "Register":
    st.subheader(text["register"])

    new_user = st.text_input(text["new_user"])
    new_pass = st.text_input(text["new_pass"], type="password")

    if st.button(text["register_btn"]):
        if new_user == "" or new_pass == "":
            st.warning("Fill all fields")
        elif new_user in users_df["username"].values:
            st.error("User exists")
        else:
            hashed = hash_password(new_pass)
            new_entry = pd.DataFrame([[new_user, hashed]],
                                     columns=["username", "password"])
            users_df = pd.concat([users_df, new_entry], ignore_index=True)
            save_users(users_df)
            st.success(text["success_register"])

# -------------------------
# LOGIN
# -------------------------
elif st.session_state.page == "Login":
    st.subheader(text["login"])

    user = st.text_input(text["username"])
    pwd = st.text_input(text["password"], type="password")

    if st.button(text["login_btn"]):
        hashed = hash_password(pwd)

        match = users_df[
            (users_df["username"] == user) &
            (users_df["password"] == hashed)
        ]

        if not match.empty:
            st.session_state.logged_in = True
            st.success(text["success_login"])
        else:
            st.error(text["error_login"])

# -------------------------
# STOP
# -------------------------
if not st.session_state.logged_in:
    st.stop()
