import pandas as pd
import xgboost as xgb
import joblib
import os

MODEL_PATH = "model.pkl"

FEATURES = ["price","ema20","ema50","rsi","macd","momentum"]

def train_model():
    df = pd.read_csv("dataset.csv")

    X = df[FEATURES]
    y = df["label"]

    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        objective="multi:softprob"
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    return model


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def predict(model, X):
    prob = model.predict_proba([X])[0]
    pred = model.predict([X])[0]
    return pred, max(prob)
