import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
import lightgbm as lgb
import pickle


DATA_PROCESSED = "data/processed/spam_clean.csv"
MODEL_SAVE_PATH = Path("models/transformer_model.pkl")


def train_transformer_lightgbm():

    print("📥 Loading clean data...")
    df = pd.read_csv(DATA_PROCESSED)

    X = df["text"].astype(str).values
    y = df["label"].values

    print("✂️ Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("🤖 Loading SentenceTransformer Model (MiniLM)...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔎 Creating text embeddings...")
    X_train_emb = embedder.encode(X_train, show_progress_bar=True)
    X_test_emb = embedder.encode(X_test, show_progress_bar=True)

    print("🌲 Training LightGBM classifier...")
    clf = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=40,
        random_state=42
    )

    clf.fit(X_train_emb, y_train)

    print("📊 Evaluation:")
    y_pred = clf.predict(X_test_emb)
    print(classification_report(y_test, y_pred))

    print("\n💾 Saving Transformer Model + Classifier...")

    # Ensure the directory exists
    MODEL_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save both embedder + classifier
    with open(MODEL_SAVE_PATH, "wb") as f:
        pickle.dump(
            {
                "embedder": embedder,
                "classifier": clf
            },
            f
        )

    print(f"✅ Model saved successfully to: {MODEL_SAVE_PATH.resolve()}")


if __name__ == "__main__":
    train_transformer_lightgbm()
