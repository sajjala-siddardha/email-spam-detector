# ======================== PATH SETUP ============================
import sys
import os
from pathlib import Path

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)

# ======================== IMPORTS ==============================
import streamlit as st
import pickle
import numpy as np
import re
import ipaddress
from urllib.parse import urlparse
from collections import Counter

import plotly.express as px
import plotly.graph_objects as go
# ========================= PAGE CONFIG =========================
st.set_page_config(page_title="AI Spam Detector", page_icon="⚡", layout="wide")

# ========================= MODEL PATH ==========================
BASELINE_MODEL_PATH = Path(PROJECT_ROOT, "models/baseline_model.pkl")


# ========================= LOAD MODEL ==========================
@st.cache_resource
def load_baseline_model():
    if not BASELINE_MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {BASELINE_MODEL_PATH}")
    with open(BASELINE_MODEL_PATH, "rb") as f:
        data = pickle.load(f)
    vectorizer = data["vectorizer"]
    classifier = data["classifier"]
    return vectorizer, classifier


vectorizer, classifier = load_baseline_model()


# ========================= URL ANALYSIS HELPERS =================

SUSPICIOUS_TLDS = {
    "xyz", "top", "club", "info", "click", "work", "biz", "shop",
    "fit", "loan", "link", "icu", "cyou", "men", "zip", "country"
}

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly",
    "ow.ly", "cutt.ly", "rb.gy", "rebrand.ly"
}

PHISHING_KEYWORDS = [
    "login", "verify", "update", "secure", "account", "bank",
    "wallet", "password", "reset", "payment", "confirm", "support",
    "security", "unlock"
]


def extract_urls(text: str):
    """Find URLs in the email text."""
    if not text:
        return []
    return re.findall(r"https?://[^\s)>\]]+", text)


def analyze_single_url(url: str):
    """Return risk info for a single URL."""
    risk_score = 0
    reasons = []

    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = (parsed.path or "").lower()
    dom_core = domain.split(":", 1)[0]

    # 1) HTTP instead of HTTPS
    if url.startswith("http://"):
        risk_score += 2
        reasons.append("Uses http:// (not secure)")

    # 2) URL shorteners
    if dom_core in URL_SHORTENERS:
        risk_score += 3
        reasons.append("Shortened URL (hidden target)")

    # 3) Suspicious TLD
    if "." in dom_core:
        tld = dom_core.split(".")[-1]
        if tld in SUSPICIOUS_TLDS:
            risk_score += 2
            reasons.append(f"Suspicious domain ending .{tld}")

    # 4) IP-based URL
    try:
        ipaddress.ip_address(dom_core)
        risk_score += 3
        reasons.append("Uses IP instead of domain")
    except ValueError:
        pass

    # 5) Phishing keywords
    combined = domain + path
    for kw in PHISHING_KEYWORDS:
        if kw in combined:
            risk_score += 2
            reasons.append(f"Contains \"{kw}\"")
            break

    if risk_score >= 7:
        level = "HIGH RISK"
        emoji = "🟥"
    elif risk_score >= 3:
        level = "MEDIUM RISK"
        emoji = "🟧"
    else:
        level = "SAFE"
        emoji = "🟩"

    return {
        "url": url,
        "score": risk_score,
        "level": level,
        "emoji": emoji,
        "reasons": reasons or ["No suspicious indicators detected"],
    }


def analyze_urls(urls):
    if not urls:
        return [], 0
    results = [analyze_single_url(u) for u in urls]
    max_score = max(r["score"] for r in results)
    return results, max_score


# ========================= RISK SCORE =========================

def compute_risk_score(spam_prob, url_score):
    """Returns total risk score 0–100."""
    spam_component = spam_prob * 60          # 60% weight
    url_component = (url_score / 10) * 40    # 40% weight
    return int(spam_component + url_component)


def risk_level_label(score):
    if score >= 75:
        return "🟥 HIGH RISK"
    elif score >= 40:
        return "🟧 MEDIUM RISK"
    return "🟩 LOW RISK"





# ========================= CUSTOM CSS ==========================
st.markdown("""
<style>
body { background-color: #0E0F12; }
.main { background-color: #0E0F12; }

.header {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00FFFF, #0088FF);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 20px #00FFFF60;
}
.sub-header {
    font-size: 18px;
    color: #AFAFAF;
    text-align: center;
    margin-bottom: 30px;
}
.glass-box {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(0,255,255,0.20);
    backdrop-filter: blur(12px);
}
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ========================= HEADER ==============================
st.markdown("<h1 class='header'>⚡ AI Spam Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>TF-IDF Spam Classifier • URL Phishing Scanner • Risk Scoring Dashboard</p>", unsafe_allow_html=True)
st.markdown("---")


# ========================= LAYOUT ===============================
col_left, col_right = st.columns([2.3, 1], gap="large")


# ========================= LEFT SIDE ============================
with col_left:

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 📩 Enter Email Content")
    email_text = st.text_area("", height=220, placeholder="Paste email text here...")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Analyze Email", use_container_width=True):

        text = email_text.strip()

        if not text:
            st.warning("Please enter some email content.")
        else:
            # ---------------- SPAM PREDICTION ----------------
            X = vectorizer.transform([text])
            spam_prob = classifier.predict_proba(X)[0][1]
            spam_label = "🛑 SPAM" if spam_prob >= 0.5 else "✅ NOT SPAM"

            st.write(f"### {spam_label}")
            st.write(f"🔢 **Spam Probability:** `{spam_prob:.4f}`")

            # ---------------- URL ANALYSIS ----------------
            urls = extract_urls(text)
            url_info, url_score = analyze_urls(urls)

            st.markdown("### 🔗 URL / Phishing Analysis")

            if urls:
                for u in url_info:
                    st.markdown(f"**{u['emoji']} {u['level']}** — `{u['url']}`")
                    for r in u["reasons"]:
                        st.markdown(f"- {r}")
            else:
                st.info("No URLs detected.")

            # ---------------- TOTAL RISK SCORE ----------------
            total_risk = compute_risk_score(spam_prob, url_score)
            risk_level = risk_level_label(total_risk)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### ⚠️ Total Email Risk Score")
            st.markdown(f"## {risk_level} — **{total_risk}/100**")
            st.progress(total_risk / 100)

            # ===================== 📊 DASHBOARD SECTION =====================
            st.markdown("---")
            st.markdown("## 📊 Email Analysis Dashboard")

            # 1️⃣ Spam vs Not-Spam Probability Bar
            spam_chart = go.Figure(go.Bar(
                x=["Spam Probability", "Not Spam Probability"],
                y=[spam_prob, 1 - spam_prob],
                marker_color=["red", "green"]
            ))
            spam_chart.update_layout(
                height=350,
                title="Spam vs Not-Spam Probability"
            )
            st.plotly_chart(spam_chart, use_container_width=True)

            # 2️⃣ Risk Score Gauge
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=total_risk,
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "orange"},
                    "steps": [
                        {"range": [0, 40], "color": "green"},
                        {"range": [40, 75], "color": "yellow"},
                        {"range": [75, 100], "color": "red"},
                    ],
                },
                title={"text": "Total Risk Score"},
            ))
            gauge.update_layout(height=350)
            st.plotly_chart(gauge, use_container_width=True)

            # 3️⃣ URL Risk Breakdown Donut
            if urls:
                score_counts = Counter([u["level"] for u in url_info])
                labels = list(score_counts.keys())
                values = list(score_counts.values())

                donut = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.5,
                    marker_colors=["#00FF00", "#FFA500", "#FF0000"]
                )])
                donut.update_layout(
                    title="URL Risk Breakdown",
                    height=350
                )
                st.plotly_chart(donut, use_container_width=True)

            # 4️⃣ Suspicious Keyword Frequency
            words = text.lower().split()
            sus_words = [w for w in words if any(k in w for k in PHISHING_KEYWORDS)]

            if sus_words:
                freq = Counter(sus_words)
                df_freq = {
                    "Word": list(freq.keys()),
                    "Count": list(freq.values())
                }
                st.markdown("### 🔍 Suspicious Keyword Frequency")
                freq_chart = px.bar(
                    df_freq,
                    x="Word",
                    y="Count",
                    color="Count",
                    title="Keyword Risk Frequency"
                )
                st.plotly_chart(freq_chart, use_container_width=True)


# ========================= RIGHT SIDE ==========================
with col_right:

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 📊 Model Information")
    st.write("- **Model:** TF–IDF + Logistic Regression")
    st.write("- **Accuracy:** ~98–99% on classic spam datasets")
    st.write("- **Backend:** Pure scikit-learn (no Torch / Transformers)")
    st.write("- **Features:** Spam Detection, URL Phishing, Risk Scoring, Dashboard")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 🧪 URL & Risk Legend")
    st.write("🟩 SAFE / LOW — No major issues")
    st.write("🟧 MEDIUM — Suspicious patterns found")
    st.write("🟥 HIGH — Strong phishing indicators")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- DEVELOPER SECTION ----------------
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 👨‍💻 Developer")
    st.write("**Sajjala Siddardha**")
    st.write("AIML @ SRKR Engineering College")
    st.write("[🌐 Portfolio](https://sajjala-portfolio.vercel.app)")
    st.write("📧 Email: **siddardhagaming@gmail.com**")
    st.markdown("</div>", unsafe_allow_html=True)
