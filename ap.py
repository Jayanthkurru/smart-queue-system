import streamlit as st
import pandas as pd
import os

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Smart Queue System", layout="wide")

DATA_FILE = "queue_data.csv"

# -------------------------
# LANGUAGE SUPPORT
# -------------------------
lang_dict = {
    "English": {
        "login": "Login",
        "username": "Username",
        "password": "Password",
        "select_city": "Select City",
        "select_office": "Select Office",
        "get_token": "Get Token",
        "queue": "Current Queue",
        "wait_time": "Estimated Wait Time",
    },
    "Telugu": {
        "login": "లాగిన్",
        "username": "యూజర్ పేరు",
        "password": "పాస్‌వర్డ్",
        "select_city": "నగరం ఎంచుకోండి",
        "select_office": "ఆఫీస్ ఎంచుకోండి",
        "get_token": "టోకెన్ పొందండి",
        "queue": "ప్రస్తుత క్యూలైన్",
        "wait_time": "అంచనా వేచి సమయం",
    }
}

# -------------------------
# LOGIN SYSTEM
# -------------------------
def login():
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# -------------------------
# LANGUAGE SELECT
# -------------------------
language = st.selectbox("🌐 Select Language", ["English", "Telugu"])
text = lang_dict[language]

# -------------------------
# DATA LOAD
# -------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Token", "City", "Office", "Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# -------------------------
# CITY & OFFICE
# -------------------------
cities = {
    "Hyderabad": ["Aadhar Center", "Passport Office"],
    "Vijayawada": ["Municipal Office", "RTO Office"],
    "Visakhapatnam": ["Collector Office", "Bank"]
}

st.subheader("📍 Location Selection")

city = st.selectbox(text["select_city"], list(cities.keys()))
office = st.selectbox(text["select_office"], cities[city])

# -------------------------
# TOKEN GENERATION
# -------------------------
st.subheader("🎟️ Token Generation")

if st.button(text["get_token"]):
    token = len(df) + 1
    new_row = pd.DataFrame([[token, city, office, "Waiting"]],
                           columns=df.columns)
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    st.success(f"Token {token} generated")

# -------------------------
# FILTER BY LOCATION
# -------------------------
filtered_df = df[(df["City"] == city) & (df["Office"] == office)]
waiting_df = filtered_df[filtered_df["Status"] == "Waiting"]

# -------------------------
# DISPLAY QUEUE
# -------------------------
st.subheader(text["queue"])
st.dataframe(waiting_df, use_container_width=True)

# -------------------------
# WAIT TIME CALCULATION
# -------------------------
st.subheader(text["wait_time"])

if not waiting_df.empty:
    waiting_df = waiting_df.reset_index(drop=True)
    waiting_df["Estimated Time (min)"] = waiting_df.index * 15
    st.dataframe(waiting_df, use_container_width=True)
else:
    st.info("No queue")

# -------------------------
# ADMIN PANEL
# -------------------------
st.subheader("🛠️ Admin Panel")

if st.button("Serve Next"):
    if not waiting_df.empty:
        next_token = waiting_df.iloc[0]["Token"]
        df.loc[df["Token"] == next_token, "Status"] = "Served"
        save_data(df)
        st.success(f"Serving Token {next_token}")
    else:
        st.warning("No one in queue")

# -------------------------
# STATS
# -------------------------
st.subheader("📊 Stats")

total = len(df)
served = len(df[df["Status"] == "Served"])
waiting = len(df[df["Status"] == "Waiting"])

col1, col2, col3 = st.columns(3)

col1.metric("Total", total)
col2.metric("Served", served)
col3.metric("Waiting", waiting)
