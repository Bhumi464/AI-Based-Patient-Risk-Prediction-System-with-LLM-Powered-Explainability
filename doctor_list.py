from __future__ import annotations

from datetime import datetime
from pathlib import Path
import os
import time

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
REQUESTS_FILE = BASE_DIR / "doctor_requests.csv"


DOCTOR_DIRECTORY = {
    "Flu": {
        "doctor_name": "Dr. Ananya Verma",
        "specialty": "General Physician",
        "contact": "+91 98765 43210"
    },
    "Covid-19": {
        "doctor_name": "Dr. Mohit Sharma",
        "specialty": "Internal Medicine",
        "contact": "+91 98765 43211"
    },
    "Heart Disease": {
        "doctor_name": "Dr. Rakesh Mehta",
        "specialty": "Cardiologist",
        "contact": "+91 98765 43212"
    },
    "Diabetes": {
        "doctor_name": "Dr. Priya Nair",
        "specialty": "Endocrinologist",
        "contact": "+91 98765 43213"
    },
    "Jaundice / Hepatitis": {
        "doctor_name": "Dr. Sandeep Rao",
        "specialty": "Gastroenterologist",
        "contact": "+91 98765 43214"
    },
    "Possible Liver Cirrhosis": {
        "doctor_name": "Dr. Sandeep Rao",
        "specialty": "Gastroenterologist",
        "contact": "+91 98765 43214"
    },
    "Possible Liver Infection / Hepatitis": {
        "doctor_name": "Dr. Sandeep Rao",
        "specialty": "Gastroenterologist",
        "contact": "+91 98765 43214"
    },
    "Fatty Liver / Hepatitis": {
        "doctor_name": "Dr. Sandeep Rao",
        "specialty": "Gastroenterologist",
        "contact": "+91 98765 43214"
    },
    "Possible Liver Dysfunction": {
        "doctor_name": "Dr. Sandeep Rao",
        "specialty": "Gastroenterologist",
        "contact": "+91 98765 43214"
    },
    "Low Risk": {
        "doctor_name": "Dr. Kavita Singh",
        "specialty": "General Physician",
        "contact": "+91 98765 43215"
    }
}


def get_doctor_details(disease: str) -> dict:
    default_details = {
        "doctor_name": "Dr. Kavita Singh",
        "specialty": "General Physician",
        "contact": "+91 98765 43215"
    }

    return DOCTOR_DIRECTORY.get(disease, default_details)


def load_doctor_requests() -> pd.DataFrame:
    if REQUESTS_FILE.exists():
        return pd.read_csv(REQUESTS_FILE)

    return pd.DataFrame(
        columns=[
            "timestamp",
            "patient_name",
            "patient_age",
            "patient_gender",
            "page",
            "predicted_disease"
        ]
    )


def save_doctor_requests(requests_df: pd.DataFrame) -> None:
    temp_file = REQUESTS_FILE.with_suffix(".tmp")
    last_error = None

    # Retry helps with short-lived locks on Windows.
    for _ in range(3):
        try:
            requests_df.to_csv(temp_file, index=False)
            os.replace(temp_file, REQUESTS_FILE)
            return
        except PermissionError as exc:
            last_error = exc
            time.sleep(0.2)

    if temp_file.exists():
        try:
            temp_file.unlink()
        except OSError:
            pass

    raise PermissionError(
        f"Could not write to '{REQUESTS_FILE}'. Close it if open in another app and try again."
    ) from last_error


def append_doctor_request(patient_name: str, patient_age, patient_gender: str, page: str, predicted_disease: str) -> None:
    requests_df = load_doctor_requests()
    new_row = pd.DataFrame([
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patient_name": patient_name,
            "patient_age": patient_age,
            "patient_gender": patient_gender,
            "page": page,
            "predicted_disease": predicted_disease
        }
    ])

    requests_df = pd.concat([requests_df, new_row], ignore_index=True)
    save_doctor_requests(requests_df)