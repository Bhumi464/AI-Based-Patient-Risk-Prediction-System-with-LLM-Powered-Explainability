# AI-Based Patient Risk Prediction System with LLM-Powered Explainability

## Overview

AI-Based Patient Risk Prediction System with LLM-Powered Explainability is an intelligent healthcare application developed using Python and Streamlit. The system predicts various diseases such as diabetes, heart disease, liver disease, and symptom-based diseases using machine learning models.

The application also integrates Large Language Model (LLM)-powered explainability to provide understandable health insights and improve user interaction.

---

# Features

* User Login and Registration System
* Patient Information Management
* Diabetes Disease Prediction
* Heart Disease Prediction
* Liver Disease Prediction
* Symptom-Based Disease Prediction
* Admin Dashboard
* Doctor Request Management
* LLM-Powered Medical Explanation
* Streamlit-Based Interactive Interface

---

# Technologies Used

## Frontend

* Streamlit

## Backend

* Python

## Machine Learning

* Scikit-learn
* Pandas
* NumPy

## AI Integration

* Gemini API / LLM Integration

---

# Project Structure

```text
AI_Healthcare_Project/
│
├── .streamlit/
├── pages/
│   ├── 1_Patient_Information.py
│   ├── 2_Common_Disease_Prediction.py
│   ├── 3_Liver_Disease_Prediction.py
│   ├── 4_Admin_Page.py
│   ├── 5_Register.py
│   └── 6_Forgot_Password.py
│
├── datasets/
├── Login.py
├── navigation.py
├── gemini_helper.py
├── diabetes_model.py
├── heart_model.py
├── liver_model.py
├── symptom_model.py
├── doctor_list.py
├── users.csv
├── doctor_requests.csv
└── README.md
```

---

# Installation

## Step 1: Clone the Repository

```bash
git clone https://github.com/Bhumi464/AI-Based-Patient-Risk-Prediction-System-with-LLM-Powered-Explainability.git
```

## Step 2: Navigate to Project Folder

```bash
cd AI-Based-Patient-Risk-Prediction-System-with-LLM-Powered-Explainability
```

## Step 3: Create Virtual Environment

```bash
python -m venv .venv
```

## Step 4: Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

# Install Required Libraries

```bash
pip install streamlit pandas numpy scikit-learn google-generativeai
```

---

# Run the Application

```bash
streamlit run Login.py
```

---

# Modules Description

## Login Module

Provides secure login access for users and administrators.

## Registration Module

Allows new users to create accounts.

## Disease Prediction Module

Predicts diseases using trained machine learning models.

## LLM Explainability Module

Generates understandable medical explanations and recommendations.

## Admin Module

Manages doctor requests and user information.

---

# Machine Learning Models

The project uses machine learning algorithms trained on healthcare datasets for disease prediction.

Models Included:

* Diabetes Prediction Model
* Heart Disease Prediction Model
* Liver Disease Prediction Model
* Symptom-Based Disease Prediction Model

---

# Future Enhancements

* Real-time doctor consultation
* Cloud database integration
* Mobile application support
* Advanced AI chatbot integration
* Voice-based symptom input
* Secure authentication system

---

# Applications

* Smart Healthcare Systems
* Hospital Assistance Systems
* Patient Risk Monitoring
* AI-Based Medical Guidance
* Health Screening Applications

---

# Author

Bhumika G

---

# License

This project is developed for educational and research purposes.
