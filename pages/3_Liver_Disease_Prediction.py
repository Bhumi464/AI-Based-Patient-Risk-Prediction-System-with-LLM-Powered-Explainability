import streamlit as st

from gemini_helper import ask_ai
from doctor_list import append_doctor_request, get_doctor_details
from navigation import render_sidebar_menu

# Check Login
if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.stop()

# Check Patient Info
if "patient_name" not in st.session_state:
    st.warning(
        "Please fill patient information first"
    )

    if st.button("Go to Patient Information"):
        st.switch_page(
            "pages/1_Patient_Information.py"
        )

    st.stop()

st.set_page_config(
    page_title="Liver Disease Prediction"
)

render_sidebar_menu()

st.title("🧪 Liver Disease Prediction")

st.subheader("🧑 Patient Details")

st.write(
    f"Name: {st.session_state['patient_name']}"
)

st.write(
    f"Age: {st.session_state['patient_age']}"
)

st.write(
    f"Gender: {st.session_state['patient_gender']}"
)

st.header("Select Symptoms")

yellow_skin = st.selectbox(
    "Yellow Skin / Eyes",
    ["No", "Yes"]
)

dark_urine = st.selectbox(
    "Dark Urine",
    ["No", "Yes"]
)

fatigue = st.selectbox(
    "Fatigue",
    ["No", "Yes"]
)

abdominal_pain = st.selectbox(
    "Abdominal Pain",
    ["No", "Yes"]
)

nausea = st.selectbox(
    "Nausea",
    ["No", "Yes"]
)

loss_appetite = st.selectbox(
    "Loss of Appetite",
    ["No", "Yes"]
)

swelling = st.selectbox(
    "Swelling in Legs/Abdomen",
    ["No", "Yes"]
)

fever = st.selectbox(
    "Fever",
    ["No", "Yes"]
)


def get_liver_prediction(symptom_values):

    yellow_skin = symptom_values["yellow_skin"]
    dark_urine = symptom_values["dark_urine"]
    fatigue = symptom_values["fatigue"]
    abdominal_pain = symptom_values["abdominal_pain"]
    nausea = symptom_values["nausea"]
    loss_appetite = symptom_values["loss_appetite"]
    swelling = symptom_values["swelling"]
    fever = symptom_values["fever"]

    if yellow_skin and dark_urine and loss_appetite:
        return "Jaundice / Hepatitis"

    if swelling and abdominal_pain and fatigue:
        return "Possible Liver Cirrhosis"

    if fever and fatigue and nausea and abdominal_pain:
        return "Possible Liver Infection / Hepatitis"

    if fatigue and loss_appetite and nausea and abdominal_pain:
        return "Fatty Liver / Hepatitis"

    if yellow_skin or dark_urine:
        return "Possible Liver Dysfunction"

    return "Low Risk"


liver_profiles = {
    "Jaundice / Hepatitis": {
        "status": "⚠️ Likely Jaundice or Hepatitis",
        "precautions": [
            "Avoid alcohol completely",
            "Do not eat oily or heavy food",
            "Drink plenty of water and stay rested",
            "Avoid self-medication and unnecessary painkillers",
            "See a doctor for liver function testing"
        ],
        "medicines": [
            "Medicines only as prescribed by a doctor",
            "Oral rehydration if needed",
            "Vitamin supplements if advised"
        ]
    },
    "Possible Liver Cirrhosis": {
        "status": "⚠️ Possible Liver Cirrhosis",
        "precautions": [
            "Stop alcohol immediately",
            "Limit salt intake to reduce swelling",
            "Follow a liver-friendly diet",
            "Get medical evaluation as soon as possible",
            "Monitor swelling and abdominal discomfort"
        ],
        "medicines": [
            "Medicines only after doctor consultation",
            "Diuretics if prescribed",
            "Liver support medicines as advised"
        ]
    },
    "Possible Liver Infection / Hepatitis": {
        "status": "⚠️ Possible Liver Infection or Hepatitis",
        "precautions": [
            "Take proper rest",
            "Drink enough fluids",
            "Avoid outside or contaminated food",
            "Avoid alcohol and smoking",
            "Visit a doctor if fever persists"
        ],
        "medicines": [
            "Only doctor-prescribed medicines",
            "Fever medicine if prescribed",
            "Supportive treatment based on test results"
        ]
    },
    "Fatty Liver / Hepatitis": {
        "status": "⚠️ Possible Fatty Liver or Hepatitis",
        "precautions": [
            "Reduce oily, fried, and sugary foods",
            "Exercise regularly if advised by doctor",
            "Maintain a healthy weight",
            "Drink enough water",
            "Get liver tests if symptoms continue"
        ],
        "medicines": [
            "Medicines only if prescribed",
            "Vitamin supplements if advised",
            "Liver support medicines as directed"
        ]
    },
    "Possible Liver Dysfunction": {
        "status": "⚠️ Possible Liver Dysfunction",
        "precautions": [
            "Avoid alcohol",
            "Follow a low-fat diet",
            "Stay hydrated",
            "Do not ignore yellow eyes or dark urine",
            "Consult a doctor for further evaluation"
        ],
        "medicines": [
            "Medicines only after diagnosis",
            "Supportive treatment as prescribed"
        ]
    },
    "Low Risk": {
        "status": "✅ Low Risk of Liver Disease",
        "precautions": [
            "Continue healthy eating",
            "Drink plenty of water",
            "Avoid alcohol",
            "Exercise regularly",
            "Monitor symptoms if they appear later"
        ],
        "medicines": [
            "No medicine needed unless prescribed by a doctor"
        ]
    }
}

# Predict
if st.button("Predict Liver Disease"):

    symptom_values = {
        "yellow_skin": yellow_skin == "Yes",
        "dark_urine": dark_urine == "Yes",
        "fatigue": fatigue == "Yes",
        "abdominal_pain": abdominal_pain == "Yes",
        "nausea": nausea == "Yes",
        "loss_appetite": loss_appetite == "Yes",
        "swelling": swelling == "Yes",
        "fever": fever == "Yes"
    }

    disease = get_liver_prediction(symptom_values)
    profile = liver_profiles[disease]

    if disease == "Low Risk":

        st.success(profile["status"])

    else:

        st.warning(profile["status"])

    st.subheader("🩺 Predicted Condition")

    st.info(disease)

    # Save predicted disease/condition so AI assistant can use it automatically
    st.session_state['predicted_disease'] = disease
    st.session_state['prediction_page'] = "Liver Disease Prediction"
    doctor_details = get_doctor_details(disease)

    st.subheader("🛡️ Precautions")

    for precaution in profile["precautions"]:
        st.write("✔️", precaution)

    st.subheader("💊 Suggested Medicines")

    for medicine in profile["medicines"]:
        st.write("💉", medicine)

    st.subheader("🥗 Recommended Diet")

    if disease == "Possible Liver Cirrhosis":
        st.write("🍎 Fruits")
        st.write("🥦 Cooked vegetables")
        st.write("🥛 Low-salt, low-fat foods")
        st.write("🥤 Plenty of water")
    elif disease == "Jaundice / Hepatitis":
        st.write("🍎 Fruits")
        st.write("🥣 Light home-cooked meals")
        st.write("🥛 Plenty of fluids")
        st.write("🥦 Steamed vegetables")
    else:
        st.write("🍎 Fruits")
        st.write("🥦 Green vegetables")
        st.write("🥛 Low-fat foods")
        st.write("🥤 Fresh juices")

    st.warning(
        "This is an AI-based prediction system. "
        "Consult a doctor for proper diagnosis."
    )

    st.session_state['admin_send_ready'] = True

if st.session_state.get('predicted_disease') and st.session_state.get('prediction_page') == "Liver Disease Prediction":

    st.markdown("---")

    if st.button("📨 Send Predicted Disease to Admin", key="send_liver_to_admin"):

        doctor_details = get_doctor_details(st.session_state['predicted_disease'])

        append_doctor_request(
            st.session_state.get('patient_name', ''),
            st.session_state.get('patient_age', ''),
            st.session_state.get('patient_gender', ''),
            "Liver Disease Prediction",
            st.session_state['predicted_disease']
        )

        st.success(
            f"Predicted disease sent to admin. Recommended doctor: {doctor_details['doctor_name']} ({doctor_details['specialty']})"
        )
        st.info(f"Doctor Contact: {doctor_details['contact']}")

st.markdown("---")

st.title("🤖 AI Liver Health Assistant")

with st.form("liver_ai_form"):

    question = st.text_input(
        "Ask About Liver Health"
    )

    submitted = st.form_submit_button("Ask AI")

if submitted:

    prompt = f'''
    Patient Age:
    {st.session_state.get('patient_age','')}

    Predicted Condition:
    {st.session_state.get('predicted_disease','')}

    Symptoms:
    Liver related symptoms

    User Question:
    {question}

    Explain:
    - liver disease risks
    - precautions
    - diet
    - medicines
    '''

    answer = ask_ai(prompt)

    st.success(answer)