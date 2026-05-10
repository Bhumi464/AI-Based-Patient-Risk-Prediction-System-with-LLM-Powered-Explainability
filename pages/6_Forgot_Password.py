import streamlit as st
import pandas as pd
from navigation import render_sidebar_menu

st.set_page_config(page_title="Forgot Password")

render_sidebar_menu()

st.title("🔑 Forgot Password")

users = pd.read_csv("users.csv")

forgot_user = st.text_input("Enter Username")

if forgot_user:

    user_data = users[
        users["username"] == forgot_user
    ]

    if not user_data.empty:
        st.success("Username found. Enter a new password.")

        new_password = st.text_input(
            "Enter New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )

        if st.button("Update Password"):

            if not new_password or not confirm_password:
                st.warning("Please fill both password fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                users.loc[
                    users["username"] == forgot_user,
                    "password"
                ] = new_password

                users.to_csv(
                    "users.csv",
                    index=False
                )

                st.success("Password updated successfully")
    else:
        st.error("Username not found")

# Back Button
if st.button("⬅ Back to Login"):
    st.switch_page("Login.py")