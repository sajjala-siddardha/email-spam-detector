import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os


DATA_PROCESSED = Path("data/processed/spam_clean.csv")
MODEL_PATH = Path("models/baseline_model.pkl")


def train_baseline():
    print("📥 Loading processed dataset...")
    if not DATA_PROCESSED.exists():
        raise FileNotFoundError(f"Processed file not found: {DATA_PROCESSED}")

    df = pd.read_csv(DATA_PROCESSED)

    # Adjust column names if needed:
    # Expecting df["clean_text"] and df["label"]
    text_col = "clean_text" if "clean_text" in df.columns else "text"
    X = df[text_col].astype(str)
    y = df["label"]

    print("✂ Splitting train/test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("🔤 Building TF-IDF vectorizer...")
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words="english"
    )
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)

    print("🤖 Training Logistic Regression classifier...")
    clf = LogisticRegression(
        max_iter=400,
        n_jobs=-1,
        class_weight="balanced"
    )
    clf.fit(X_train_vec, y_train)

    print("\n📊 Evaluation on test set:")
    y_pred = clf.predict(X_test_vec)
    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

    print("\n💾 Saving baseline model...")
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(
            {
                "vectorizer": tfidf,
                "classifier": clf,
            },
            f,
        )
    print(f"✅ Saved baseline model → {MODEL_PATH.resolve()}")


if __name__ == "__main__":
    train_baseline()
