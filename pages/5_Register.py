import streamlit as st
import pandas as pd
from navigation import render_sidebar_menu

st.set_page_config(page_title="Register")

render_sidebar_menu()

st.title("🆕 New User Registration")

users = pd.read_csv("users.csv")

new_user = st.text_input("Create Username")

new_pass = st.text_input(
    "Create Password",
    type="password"
)

if st.button("Register"):

    if new_user in users["username"].values:

        st.warning("Username already exists")

    else:

        new_data = pd.DataFrame({
            "username": [new_user],
            "password": [new_pass],
            "role": ["user"]
        })

        updated_users = pd.concat(
            [users, new_data],
            ignore_index=True
        )

        updated_users.to_csv(
            "users.csv",
            index=False
        )

        st.success("Registration Successful")

# Back Button
if st.button("⬅ Back to Login"):
    st.switch_page("Login.py")