import os
import joblib
import pandas as pd
from .features import make_feature_matrix

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT_DIR, "dubizzle_synthetic_listings.csv")

MODEL_PATH = os.path.join(ROOT_DIR, "src", "models", "risk_model.joblib")
VECTORIZER_PATH = os.path.join(ROOT_DIR, "src", "models", "tfidf_vectorizer.joblib")


def predict_risk(df: pd.DataFrame):
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    X, feature_names, _ = make_feature_matrix(df, vectorizer=vectorizer, fit_vectorizer=False)
    risk_scores = model.predict_proba(X)[:, 1]

    out = df.copy()
    out["risk_score"] = risk_scores
    out["predicted_suspicious"] = (out["risk_score"] >= 0.5).astype(int)

    return out.sort_values("risk_score", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH).head(30)
    preds = predict_risk(df)
    print(preds[["listing_id", "title", "price_aed", "risk_score", "predicted_suspicious"]].head(10))
