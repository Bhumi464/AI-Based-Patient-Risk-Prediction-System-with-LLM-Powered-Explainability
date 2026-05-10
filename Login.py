import streamlit as st
import pandas as pd
from navigation import render_sidebar_menu

st.set_page_config(page_title="Login")

st.title("🔐 AI Healthcare Login")

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

render_sidebar_menu()

# Load Users
users = pd.read_csv("users.csv")

# Login Inputs
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login Button
if st.button("Login"):

    user_found = users[
        (users["username"] == username) &
        (users["password"] == password)
    ]

    if not user_found.empty:

        role = user_found.iloc[0]["role"]

        st.session_state.logged_in = True
        st.session_state.role = role

        st.success("Login Successful")

        st.switch_page("pages/1_Patient_Information.py")

    else:
        st.error("Invalid Username or Password")

st.markdown("---")

# Navigation Buttons
if not st.session_state.logged_in:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🆕 New User"):
            st.switch_page("pages/5_Register.py")

    with col2:
        if st.button("🔑 Forgot Password"):
            st.switch_page("pages/6_Forgot_Password.py")