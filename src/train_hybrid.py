import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics import classification_report
from catboost import CatBoostClassifier
import pickle
from src.config import DATA_PROCESSED, HYBRID_MODEL_PATH

def train_hybrid():
    print("📥 Loading cleaned dataset...")
    df = pd.read_csv(DATA_PROCESSED)

    # Use cleaned text
    X = df["clean_text"].astype(str)
    y = df["label"]

    print("✂ Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("🔤 Creating TF-IDF features...")
    tfidf = TfidfVectorizer(max_features=4000, ngram_range=(1, 2))
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    print("🤖 Loading SentenceTransformer (MiniLM)...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    X_train_emb = embedder.encode(X_train.tolist(), show_progress_bar=True)
    X_test_emb = embedder.encode(X_test.tolist(), show_progress_bar=True)

    print("🔗 Combining features (TF-IDF + Embeddings)...")
    X_train_combined = np.hstack((X_train_emb, X_train_tfidf.toarray()))
    X_test_combined = np.hstack((X_test_emb, X_test_tfidf.toarray()))

    print("🌲 Training CatBoost hybrid model...")
    model = CatBoostClassifier(
        iterations=700,
        depth=8,
        learning_rate=0.05,
        loss_function="Logloss",
        verbose=0
    )
    model.fit(X_train_combined, y_train)

    print("\n📊 Evaluation:")
    y_pred = model.predict(X_test_combined)
    print(classification_report(y_test, y_pred))

    print("\n💾 Saving hybrid model...")
    HYBRID_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(HYBRID_MODEL_PATH, "wb") as f:
        pickle.dump({
            "embedder": embedder,
            "tfidf": tfidf,
            "classifier": model
        }, f)
    print(f"✅ Saved hybrid model → {HYBRID_MODEL_PATH.resolve()}")

if __name__ == "__main__":
    train_hybrid()
