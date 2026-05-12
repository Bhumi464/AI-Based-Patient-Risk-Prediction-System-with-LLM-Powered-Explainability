import streamlit as st
import pandas as pd
import html

from doctor_list import load_doctor_requests, save_doctor_requests, get_doctor_details
from navigation import render_sidebar_menu

USERS_FILE = "users.csv"
ROLE_OPTIONS = ["admin", "user", "doctor"]

st.set_page_config(page_title="Admin Panel")

render_sidebar_menu()

# Check Login
if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# Check Admin
if st.session_state.get("role") != "admin":
    st.error("Access Denied")
    st.stop()

st.title("🛠️ Admin Dashboard")

st.success("Welcome Admin")

# Load Users
users = pd.read_csv(USERS_FILE)

st.subheader("Registered Users")
st.dataframe(users, use_container_width=True)

st.subheader("Change User Roles")

if users.empty:
    st.info("No users found.")
else:
    editable_users = users.copy()
    user_options = ["Select"] + editable_users["username"].tolist()

    selected_username = st.selectbox("Select user", user_options, index=0, key="admin_role_user")

    if selected_username != "Select":
        selected_user_row = editable_users.loc[editable_users["username"] == selected_username].iloc[0]
        current_role = selected_user_row["role"]
        st.info(f"Selected User: {selected_username} | Current Role: {current_role}")

        role_options = ["Select"] + ROLE_OPTIONS
        default_role_index = role_options.index(current_role) if current_role in role_options else 0
        selected_role = st.selectbox("New role", role_options, index=default_role_index, key="admin_role_value")

        if st.button("Save Role Change"):
            if selected_role == "Select":
                st.warning("Please select a new role")
            else:
                editable_users.loc[editable_users["username"] == selected_username, "role"] = selected_role
                editable_users.to_csv(USERS_FILE, index=False)
                st.success(f"Updated {selected_username} to role '{selected_role}'.")
                st.rerun()
    else:
        st.info("Select a user to view details and change role.")

st.subheader("Patient Requests For Doctor Contact")

requests_df = load_doctor_requests()

if requests_df.empty:
    st.info("No predicted disease requests have been sent yet.")
else:
    cleaned_requests = requests_df.fillna("")
    requests_container = st.container()

    def safe_text(value):
        text = str(value).strip()
        return "NA" if not text else text

    def render_cell(column, value, bold=False):
        weight = "700" if bold else "500"
        column.markdown(
            (
                "<div style='white-space: nowrap; "
                f"font-size: 0.88rem; font-weight: {weight};'>{html.escape(value)}</div>"
            ),
            unsafe_allow_html=True
        )

    with requests_container:
        st.markdown(
            """
            <div id='requests-scroll-anchor'></div>
            <style>
            div[data-testid="stVerticalBlock"]:has(#requests-scroll-anchor) {
                overflow-x: auto;
            }
            div[data-testid="stVerticalBlock"]:has(#requests-scroll-anchor) div[data-testid="stHorizontalBlock"] {
                min-width: 2100px;
                flex-wrap: nowrap;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        header_cols = st.columns([1.2, 1.3, 0.5, 0.8, 0.9, 1.2, 1.4, 1.2, 1.1, 0.5])
        render_cell(header_cols[0], "Time", bold=True)
        render_cell(header_cols[1], "Patient", bold=True)
        render_cell(header_cols[2], "Age", bold=True)
        render_cell(header_cols[3], "Gender", bold=True)
        render_cell(header_cols[4], "Page", bold=True)
        render_cell(header_cols[5], "Disease", bold=True)
        render_cell(header_cols[6], "Doctor", bold=True)
        render_cell(header_cols[7], "Specialty", bold=True)
        render_cell(header_cols[8], "Contact", bold=True)
        render_cell(header_cols[9], "Delete", bold=True)

        for req_index, row in cleaned_requests.iterrows():
            doctor_details = get_doctor_details(str(row.get("predicted_disease", "")))

            row_cols = st.columns([1.2, 1.3, 0.5, 0.8, 0.9, 1.2, 1.4, 1.2, 1.1, 0.5])
            render_cell(row_cols[0], safe_text(row.get("timestamp", "")))
            render_cell(row_cols[1], safe_text(row.get("patient_name", "")))
            render_cell(row_cols[2], safe_text(row.get("patient_age", "")))
            render_cell(row_cols[3], safe_text(row.get("patient_gender", "")))
            render_cell(row_cols[4], safe_text(row.get("page", "")))
            render_cell(row_cols[5], safe_text(row.get("predicted_disease", "")))
            render_cell(row_cols[6], safe_text(doctor_details["doctor_name"]))
            render_cell(row_cols[7], safe_text(doctor_details["specialty"]))
            render_cell(row_cols[8], safe_text(doctor_details["contact"]))

            if row_cols[9].button("🗑️", key=f"admin_delete_row_{req_index}"):
                updated_requests = requests_df.drop(index=req_index).reset_index(drop=True)
                try:
                    save_doctor_requests(updated_requests)
                    st.success("Request deleted successfully.")
                    st.rerun()
                except PermissionError:
                    st.error(
                        "Cannot delete right now because doctor_requests.csv is in use. "
                        "Please close it in Excel/another app and try again."
                    )
