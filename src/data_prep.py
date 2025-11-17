import pandas as pd
import re
from sklearn.model_selection import train_test_split
from .config import DATA_RAW, DATA_PROCESSED, RANDOM_STATE, TEST_SIZE

# Basic cleaner
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def prepare_data():
    print("📥 Loading raw data from:", DATA_RAW)

    # Load spam.csv from correct location
    df = pd.read_csv(DATA_RAW, encoding="latin-1")

    # spam.csv uses these column names:
    df = df[['v1', 'v2']]
    df.columns = ['label', 'text']

    # Encode labels
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})

    # Clean text
    print("🧹 Cleaning text...")
    df['clean_text'] = df['text'].apply(clean_text)

    # Save processed file
    DATA_PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PROCESSED, index=False)

    print("✅ Saved processed file:", DATA_PROCESSED)
    return df

def get_split():
    # This function only works AFTER prepare_data()
    df = pd.read_csv(DATA_PROCESSED)
    return train_test_split(
        df['clean_text'],
        df['label'],
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df['label']
    )

if __name__ == "__main__":
    prepare_data()
