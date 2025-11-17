import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_PATH = "models/transformer_model.pkl"

# Load model + transformer
print("📦 Loading model...")
model_data = pickle.load(open(MODEL_PATH, "rb"))

embedder: SentenceTransformer = model_data["embedder"]
classifier = model_data["classifier"]

print("✅ Model Loaded Successfully!\n")

def predict_email(text: str):
    """Predict spam or ham for a given text."""
    
    # Create embedding
    embedding = embedder.encode([text])

    # Predict class
    pred = classifier.predict(embedding)[0]
    prob = classifier.predict_proba(embedding)[0]

    label = "SPAM" if pred == 1 else "NOT SPAM"

    return {
        "label": label,
        "probability": float(np.max(prob))
    }

# Test
if __name__ == "__main__":
    test = "Congratulations! You have won a free iPhone!"
    result = predict_email(test)
    print("\nTest Email:", test)
    print("Prediction:", result)
