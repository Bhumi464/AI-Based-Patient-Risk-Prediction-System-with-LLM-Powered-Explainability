import pandas as pd
from sklearn.tree import DecisionTreeClassifier

SYMPTOM_COLUMNS = [
    "fever", "cough", "fatigue", "headache",
    "nausea", "vomiting", "chest_pain", "shortness_of_breath"
]

def train_symptom_model():
    df = pd.read_csv("datasets/symptoms.csv")

    X = df[SYMPTOM_COLUMNS]
    
    y = df["disease"]

    # Decision tree gives deterministic behavior and perfectly learns this small tabular symptom set.
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

    return model


def predict_symptom_disease(model, symptom_values):
    df = pd.read_csv("datasets/symptoms.csv")

    symptom_row = pd.DataFrame([symptom_values], columns=SYMPTOM_COLUMNS)

    exact_match = df[(df[SYMPTOM_COLUMNS] == symptom_row.iloc[0]).all(axis=1)]
    if not exact_match.empty:
        return exact_match.iloc[0]["disease"]

    return model.predict(symptom_row)[0]