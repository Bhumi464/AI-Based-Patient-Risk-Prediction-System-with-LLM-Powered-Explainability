import streamlit as st


def render_sidebar_menu():
    """Render role-based sidebar navigation for all app pages."""
    logged_in = st.session_state.get("logged_in", False)
    role = st.session_state.get("role", "")

    with st.sidebar:
        st.subheader("Menu")

        st.page_link("Login.py", label="Login")

        if logged_in:
            st.page_link("pages/1_Patient_Information.py", label="Patient Information")
            st.page_link("pages/2_Common_Disease_Prediction.py", label="Common Disease Prediction")
            st.page_link("pages/3_Liver_Disease_Prediction.py", label="Liver Disease Prediction")

            if role == "admin":
                st.page_link("pages/4_Admin_Page.py", label="Admin Page")

            if st.button("Logout", key="sidebar_logout"):
                st.session_state.clear()
                st.switch_page("Login.py")
        else:
            st.page_link("pages/5_Register.py", label="Register")
            st.page_link("pages/6_Forgot_Password.py", label="Forgot Password")
