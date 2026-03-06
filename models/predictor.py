import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib


def train_model():

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "../data/E0.csv")

    df = pd.read_csv(csv_path)

    if df.empty:
        print("❌ Dataset empty")
        return

    # Premium Feature Set
    features = [
        "FTHG",
        "FTAG",
        "HS",
        "AS",
        "HST",
        "AST",
        "HC",
        "AC",
        "HY",
        "AY"
    ]

    features = [f for f in features if f in df.columns]

    if "FTR" not in df.columns:
        print("❌ FTR target not found")
        return

    X = df[features]
    y = df["FTR"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        random_state=42
    )

    model.fit(X_train, y_train)

    model_path = os.path.join(base_dir, "model.pkl")

    joblib.dump(model, model_path)

    print("🔥 Premium AI Model Trained")