import streamlit as st
import pandas as pd


from diabetes_model import train_diabetes_model
from heart_model import train_heart_model
from symptom_model import train_symptom_model, predict_symptom_disease
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

render_sidebar_menu()

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

# Load Models
diabetes_model = train_diabetes_model()
heart_model = train_heart_model()
symptom_model = train_symptom_model()

st.header("Patient Information")

age = st.session_state["patient_age"]
glucose = st.number_input("Glucose", key="cd_glucose")
bp = st.number_input("Blood Pressure", key="cd_bp")
bmi = st.number_input("BMI", key="cd_bmi")
chol = st.number_input("Cholesterol", key="cd_chol")
thalach = st.number_input("Max Heart Rate", key="cd_thalach")

st.header("Symptoms")

fever = st.selectbox("Fever", ["No", "Yes"], key="cd_fever")
cough = st.selectbox("Cough", ["No", "Yes"], key="cd_cough")
fatigue = st.selectbox("Fatigue", ["No", "Yes"], key="cd_fatigue")
headache = st.selectbox("Headache", ["No", "Yes"], key="cd_headache")
nausea = st.selectbox("Nausea", ["No", "Yes"], key="cd_nausea")
vomiting = st.selectbox("Vomiting", ["No", "Yes"], key="cd_vomiting")
chest_pain = st.selectbox("Chest Pain", ["No", "Yes"], key="cd_chest_pain")
breath = st.selectbox("Shortness of Breath", ["No", "Yes"], key="cd_breath")

disease_info = {

    "Flu": {
        "precautions": [
            "Take proper rest",
            "Drink warm fluids",
            "Avoid cold food",
            "Wear a mask"
        ],
        "medicines": [
            "Paracetamol",
            "Cetirizine",
            "Cough Syrup"
        ],
        "diet": [
            "Soup",
            "Vitamin C fruits",
            "Warm water"
        ]
    },

    "Covid-19": {
        "precautions": [
            "Isolate yourself",
            "Wear mask",
            "Monitor oxygen level",
            "Stay hydrated"
        ],
        "medicines": [
            "Paracetamol",
            "Vitamin C",
            "Zinc Tablets"
        ],
        "diet": [
            "Protein rich food",
            "Warm liquids",
            "Fruits"
        ]
    },

    "Cold": {
        "precautions": [
            "Take adequate rest",
            "Stay hydrated",
            "Avoid sudden temperature changes",
            "Use steam inhalation"
        ],
        "medicines": [
            "Paracetamol",
            "Antihistamine",
            "Nasal decongestant"
        ],
        "diet": [
            "Warm soups",
            "Herbal tea",
            "Vitamin C rich fruits"
        ]
    },

    "Migraine": {
        "precautions": [
            "Rest in a dark and quiet room",
            "Avoid loud noise and bright lights",
            "Keep a regular sleep schedule",
            "Manage stress"
        ],
        "medicines": [
            "Paracetamol",
            "Ibuprofen",
            "Triptans (if prescribed)"
        ],
        "diet": [
            "Hydrating fluids",
            "Magnesium rich foods",
            "Avoid known trigger foods"
        ]
    },

    "Malaria": {
        "precautions": [
            "Consult doctor immediately",
            "Complete prescribed treatment",
            "Use mosquito nets",
            "Prevent mosquito breeding around home"
        ],
        "medicines": [
            "Antimalarial drugs as prescribed",
            "Paracetamol for fever",
            "Oral rehydration"
        ],
        "diet": [
            "Light meals",
            "Coconut water",
            "Protein rich soft foods"
        ]
    },

    "Allergy": {
        "precautions": [
            "Avoid known allergens",
            "Keep surroundings dust-free",
            "Use mask in dusty environments",
            "Maintain hydration"
        ],
        "medicines": [
            "Cetirizine",
            "Loratadine",
            "Nasal saline spray"
        ],
        "diet": [
            "Fresh fruits",
            "Warm fluids",
            "Avoid trigger foods"
        ]
    },

    "Heart Disease": {
        "precautions": [
            "Avoid oily foods",
            "Reduce stress",
            "Daily exercise",
            "Monitor BP"
        ],
        "medicines": [
            "Aspirin",
            "Atorvastatin"
        ],
        "diet": [
            "Low salt diet",
            "Green vegetables",
            "Oats"
        ]
    },

    "Diabetes": {
        "precautions": [
            "Reduce sugar intake",
            "Exercise regularly",
            "Monitor glucose level"
        ],
        "medicines": [
            "Metformin",
            "Insulin"
        ],
        "diet": [
            "High fiber foods",
            "Vegetables",
            "Low carb diet"
        ]
    }
}

if st.button("Predict Disease"):

    fever = 1 if fever == "Yes" else 0
    cough = 1 if cough == "Yes" else 0
    fatigue = 1 if fatigue == "Yes" else 0
    headache = 1 if headache == "Yes" else 0
    nausea = 1 if nausea == "Yes" else 0
    vomiting = 1 if vomiting == "Yes" else 0
    chest_pain = 1 if chest_pain == "Yes" else 0
    breath = 1 if breath == "Yes" else 0

    # Input Data
    diabetes_input = pd.DataFrame(
        [[glucose, bp, bmi, age]],
        columns=["Glucose", "BloodPressure", "BMI", "Age"]
    )

    heart_input = pd.DataFrame(
        [[age, bp, chol, thalach]],
        columns=["age", "trestbps", "chol", "thalach"]
    )

    symptom_input = [[
        fever, cough, fatigue, headache,
        nausea, vomiting, chest_pain, breath
    ]]

    # Predictions
    diabetes_prob = diabetes_model.predict_proba(diabetes_input)[0][1]

    heart_prob = heart_model.predict_proba(heart_input)[0][1]

    disease = predict_symptom_disease(symptom_model, symptom_input[0])

    # Results
    st.success(f"Diabetes Risk: {round(diabetes_prob*100,2)}%")

    st.warning(f"Heart Disease Risk: {round(heart_prob*100,2)}%")

    st.info(f"Predicted Disease: {disease}")

    # Save predicted disease to session so AI assistant can use it automatically
    st.session_state['predicted_disease'] = disease
    st.session_state['prediction_page'] = "Common Disease Prediction"

    doctor_details = get_doctor_details(disease)

    # ==========================
    # Disease Suggestions
    # ==========================

    if disease in disease_info:

        st.subheader("🛡️ Precautions")

        for p in disease_info[disease]["precautions"]:
            st.write("✔️", p)

        st.subheader("💊 Suggested Medicines")

        for m in disease_info[disease]["medicines"]:
            st.write("💉", m)

        st.subheader("🥗 Recommended Diet")

        for d in disease_info[disease]["diet"]:
            st.write("🍎", d)

    else:
        # Fallback: generate recommendations via AI when disease not in mapping
        st.subheader("🛡️ Precautions")

        with st.spinner("Generating recommendations..."):

            prompt = f'''
            You are a medical assistant. Provide concise, practical information in bullet points.

            Patient Name: {st.session_state['patient_name']}
            Age: {st.session_state['patient_age']}
            Gender: {st.session_state['patient_gender']}

            Symptoms: fever={fever}, cough={cough}, fatigue={fatigue}, headache={headache}, nausea={nausea}, vomiting={vomiting}, chest_pain={chest_pain}, breath={breath}

            Predicted Disease: {disease}

            Return:
            1) Precautions (bullet list)
            2) Suggested medicines (bullet list)
            3) Recommended diet (bullet list)
            '''

            ai_answer = ask_ai(prompt)

        st.info("AI-generated recommendations")
        st.write(ai_answer)

        st.warning(
            "This is an AI-based prediction system. "
            "Please consult a doctor for medical advice."
        )

        # Clear the input widgets so numbers reset automatically after prediction
        try:
            st.session_state['cd_glucose'] = 0
            st.session_state['cd_bp'] = 0
            st.session_state['cd_bmi'] = 0
            st.session_state['cd_chol'] = 0
            st.session_state['cd_thalach'] = 0

            st.session_state['cd_fever'] = "No"
            st.session_state['cd_cough'] = "No"
            st.session_state['cd_fatigue'] = "No"
            st.session_state['cd_headache'] = "No"
            st.session_state['cd_nausea'] = "No"
            st.session_state['cd_vomiting'] = "No"
            st.session_state['cd_chest_pain'] = "No"
            st.session_state['cd_breath'] = "No"
        except Exception:
            pass

    st.session_state['admin_send_ready'] = True

if st.session_state.get('predicted_disease') and st.session_state.get('prediction_page') == "Common Disease Prediction":

    st.markdown("---")

    if st.button("📨 Send Predicted Disease to Admin", key="send_common_to_admin"):

        doctor_details = get_doctor_details(st.session_state['predicted_disease'])

        append_doctor_request(
            st.session_state.get('patient_name', ''),
            st.session_state.get('patient_age', ''),
            st.session_state.get('patient_gender', ''),
            "Common Disease Prediction",
            st.session_state['predicted_disease']
        )

        st.success(
            f"Predicted disease sent to admin. Recommended doctor: {doctor_details['doctor_name']} ({doctor_details['specialty']})"
        )
        st.info(f"Doctor Contact: {doctor_details['contact']}")

st.markdown("---")

st.title("🤖 AI Medical Assistant")

with st.form("cd_ai_form"):

    user_question = st.text_input(
        "Ask Health Questions"
    )

    submitted = st.form_submit_button("Ask AI Doctor")

if submitted:

    with st.spinner("AI is analyzing..."):

        predicted = st.session_state.get('predicted_disease', 'Not specified')

        prompt = f'''
        You are a medical assistant.

        Patient Name:
        {st.session_state.get('patient_name','')}

        Age:
        {st.session_state.get('patient_age','')}

        Gender:
        {st.session_state.get('patient_gender','')}

        Predicted Disease:
        {predicted}

        User Question:
        {user_question}

        Give:
        1. Possible explanation
        2. Precautions
        3. Diet suggestions
        4. Whether doctor consultation is needed
        '''

        answer = ask_ai(prompt)

        st.success(answer)