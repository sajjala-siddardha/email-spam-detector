import pickle
import numpy as np
from src.config import HYBRID_MODEL_PATH

def load_hybrid_model():
    with open(HYBRID_MODEL_PATH, "rb") as f:
        data = pickle.load(f)
    return data["embedder"], data["tfidf"], data["classifier"]

embedder, tfidf, model = load_hybrid_model()

def predict_hybrid(text, threshold=0.4):
    emb = embedder.encode([text])
    tfidf_vec = tfidf.transform([text]).toarray()
    combined = np.hstack([emb, tfidf_vec])
    prob = model.predict_proba(combined)[0][1]
    label = 1 if prob >= threshold else 0
    return {"label": "SPAM" if label == 1 else "NOT SPAM", "prob": prob}

if __name__ == "__main__":
    email = "Congratulations! You have won a free iPhone. Claim now!"
    print(predict_hybrid(email))
