import streamlit as st
import pandas as pd
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Smart Queue System", layout="wide")

DATA_FILE = "queue_data.csv"

# -------------------------------
# LOAD / SAVE DATA
# -------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Token", "Name", "Priority", "Status"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# -------------------------------
# TITLE
# -------------------------------
st.title("📊 Smart Queue Management System")

# -------------------------------
# ADD USER SECTION
# -------------------------------
st.subheader("🎟️ Get Token")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Enter Name")

with col2:
    priority = st.selectbox("Select Priority", ["Normal", "VIP", "Emergency"])

if st.button("Generate Token"):
    if name.strip() == "":
        st.error("Please enter a name")
    else:
        token = len(df) + 1
        new_entry = pd.DataFrame([[token, name, priority, "Waiting"]],
                                 columns=df.columns)
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
        st.success(f"✅ Token {token} generated for {name}")

# -------------------------------
# PRIORITY SORTING
# -------------------------------
priority_order = {"Emergency": 1, "VIP": 2, "Normal": 3}
df["PriorityOrder"] = df["Priority"].map(priority_order)
df = df.sort_values(by=["PriorityOrder", "Token"]).drop(columns=["PriorityOrder"])

# -------------------------------
# DISPLAY QUEUE
# -------------------------------
st.subheader("📋 Current Queue")

waiting_df = df[df["Status"] == "Waiting"]

st.dataframe(waiting_df, use_container_width=True)

# -------------------------------
# WAIT TIME ESTIMATION
# -------------------------------
st.subheader("⏱️ Estimated Wait Time")

if not waiting_df.empty:
    avg_time = 5  # minutes per person
    waiting_df = waiting_df.reset_index(drop=True)
    waiting_df["Estimated Wait (min)"] = waiting_df.index * avg_time
    st.dataframe(waiting_df, use_container_width=True)
else:
    st.info("No one in queue")

# -------------------------------
# ADMIN PANEL
# -------------------------------
st.subheader("🛠️ Admin Panel")

if st.button("Serve Next"):
    waiting = df[df["Status"] == "Waiting"]

    if not waiting.empty:
        next_index = waiting.index[0]
        df.loc[next_index, "Status"] = "Served"
        save_data(df)
        st.success(f"🎯 Serving Token {df.loc[next_index, 'Token']}")
    else:
        st.warning("Queue is empty")

# -------------------------------
# STATS
# -------------------------------
st.subheader("📈 Statistics")

total = len(df)
served = len(df[df["Status"] == "Served"])
waiting = len(df[df["Status"] == "Waiting"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Tokens", total)
col2.metric("Served", served)
col3.metric("Waiting", waiting)
