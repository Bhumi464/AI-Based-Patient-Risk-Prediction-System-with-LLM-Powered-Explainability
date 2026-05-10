import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def train_heart_model():
    df = pd.read_csv("datasets/heart.csv")

    X = df[["age", "trestbps", "chol", "thalach"]]
    y = df["condition"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Accuracy
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("Heart Accuracy:", acc)

    return model