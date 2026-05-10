import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_liver_model():

    # Load Dataset
    data = pd.read_csv("liver.csv")

    # Features
    X = data.drop("Dataset", axis=1)

    # Target
    y = data["Dataset"]

    # Convert Gender
    X["Gender"] = X["Gender"].map({
        "Male": 1,
        "Female": 0
    })

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # Model
    model = RandomForestClassifier()

    model.fit(X_train, y_train)

    return model