import shap
import numpy as np

def shap_explain_hybrid(model, embed, tfidf, text):
    """
    Generate SHAP values for the hybrid model (MiniLM + TF-IDF + CatBoost)
    """

    # Encode text → embedding
    emb = embed.encode([text])

    # TF-IDF vector
    tfidf_vec = tfidf.transform([text]).toarray()

    # Combine both
    combined = np.hstack([emb, tfidf_vec])

    # Build SHAP explainer
    explainer = shap.TreeExplainer(model)

    # SHAP values
    shap_values = explainer.shap_values(combined)

    # For CatBoost binary → sometimes list
    if isinstance(shap_values, list):
        shap_values = shap_values[0]

    # Base value (required for SHAP v0.20+)
    base_value = explainer.expected_value

    return shap_values, combined, base_value


def highlight_spam_words(text):
    """
    Add a red highlight around risky spam keywords.
    """
    spam_keywords = [
        "free", "win", "offer", "click", "buy", "credit", "loan", "urgent",
        "money", "claim", "gift", "prize", "winner", "cash", "bitcoin", "crypto"
    ]

    highlighted = text.lower()
    for word in spam_keywords:
        highlighted = highlighted.replace(
            word,
            f"<mark style='background-color:#ff4b4b55;color:red;padding:2px;border-radius:4px;'>{word}</mark>"
        )

    return highlighted
