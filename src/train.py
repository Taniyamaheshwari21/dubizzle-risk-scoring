import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.linear_model import LogisticRegression

from features import make_feature_matrix



BASE_DIR = os.path.dirname(__file__) 
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model.joblib")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.joblib")



def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    # target
    y = df["is_suspicious"].astype(int).values

    # split
    train_df, test_df, y_train, y_test = train_test_split(
        df, y, test_size=0.2, random_state=42, stratify=y
    )

    # features
    X_train, feature_names, vectorizer = make_feature_matrix(
        train_df, vectorizer=None, fit_vectorizer=True
    )
    X_test, _, _ = make_feature_matrix(
        test_df, vectorizer=vectorizer, fit_vectorizer=False
    )

    # model
    model = LogisticRegression(max_iter=2000, n_jobs=-1)
    model.fit(X_train, y_train)

    # evaluation
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))

    print("\n--- ROC AUC ---")
    print(roc_auc_score(y_test, y_prob))

    # save
    joblib.dump(model, os.path.join(MODEL_DIR, "risk_model.joblib"))
    joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))
    joblib.dump(feature_names, os.path.join(MODEL_DIR, "feature_names.joblib"))

    print("\nSaved model + vectorizer into /models")


if __name__ == "__main__":
    main()
