import streamlit as st
from navigation import render_sidebar_menu

st.set_page_config(
    page_title="Patient Information"
)

render_sidebar_menu()

# Check Login
if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.title("🧑 Patient Information")

# ==========================
# PATIENT DETAILS
# ==========================

st.header("Enter Patient Details")

name = st.text_input("Patient Name", key="pi_name")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    key="pi_age"
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female", "Other"],
    key="pi_gender"
)

phone = st.text_input(
    "Phone Number",
    max_chars=10,
    key="pi_phone"
)

weight = st.number_input(
    "Weight (kg)",
    key="pi_weight"
)

height = st.number_input(
    "Height (cm)",
    key="pi_height"
)

# ==========================
# SAVE BUTTON
# ==========================

if st.button("💾 Save & Continue"):

    cleaned_phone = phone.strip()

    if not cleaned_phone.isdigit() or len(cleaned_phone) != 10:
        st.error("Invalid phone number. Please enter exactly 10 digits.")
        st.stop()

    # Save in session
    st.session_state["patient_name"] = name

    st.session_state["patient_age"] = age

    st.session_state["patient_gender"] = gender

    st.session_state["patient_phone"] = cleaned_phone

    st.session_state["patient_weight"] = weight

    st.session_state["patient_height"] = height

    st.success(
        "Patient Information Saved"
    )
    # Clear the input widgets (reset numeric fields and text inputs)
    try:
        st.session_state['pi_age'] = 1
        st.session_state['pi_weight'] = 0
        st.session_state['pi_height'] = 0
        st.session_state['pi_phone'] = ""
        st.session_state['pi_name'] = ""
        st.session_state['pi_gender'] = "Male"
    except Exception:
        pass

    # Go to next page
    st.switch_page(
        "pages/2_Common_Disease_Prediction.py"
    )