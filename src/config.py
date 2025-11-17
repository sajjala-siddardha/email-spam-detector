from pathlib import Path
from pathlib import Path

# Hybrid model paths
HYBRID_MODEL_PATH = Path("models/hybrid_spam_model.pkl")
DATA_PROCESSED = Path("data/processed/spam_clean.csv")


# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
DATA_RAW = BASE_DIR / "data" / "raw" / "spam.csv"
DATA_PROCESSED = BASE_DIR / "data" / "processed" / "spam_clean.csv"

# Model paths
BASELINE_MODEL_PATH = BASE_DIR / "models" / "baseline_model.pkl"
BASELINE_VECTORIZER_PATH = BASE_DIR / "models" / "baseline_vectorizer.pkl"

TRANSFORMER_MODEL_PATH = BASE_DIR / "models" / "transformer_model.pkl"

# ML settings
RANDOM_STATE = 42
TEST_SIZE = 0.2
MAX_FEATURES = 10000

# Transformer model name
TRANSFORMER_NAME = "sentence-transformers/all-MiniLM-L6-v2"
