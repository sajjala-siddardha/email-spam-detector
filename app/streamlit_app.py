# ======================== IMPORTS ============================
import os
from pathlib import Path
import sqlite3
from datetime import datetime

import streamlit as st
import pickle
import numpy as np
import re
import ipaddress
from urllib.parse import urlparse
from collections import Counter

import plotly.express as px
import plotly.graph_objects as go

from pyzbar.pyzbar import decode
from PIL import Image

# ========================= PAGE CONFIG =========================
st.set_page_config(
    page_title="AI Spam Detector",
    page_icon="⚡",
    layout="wide"
)

# ========================= PATH SETUP ============================
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
BASELINE_MODEL_PATH = Path(PROJECT_ROOT, "models/baseline_model.pkl")
DB_PATH = Path(PROJECT_ROOT, "spam_history.db")

# ========================= DB SETUP =============================

@st.cache_resource
def get_db_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT,
            label TEXT,
            spam_prob REAL,
            risk_score INTEGER,
            url_count INTEGER,
            has_qr INTEGER,
            snippet TEXT
        )
    """)
    conn.commit()
    return conn

def log_prediction(conn, label, spam_prob, risk_score, url_count, has_qr, text):
    snippet = (text[:120] + "...") if len(text) > 120 else text
    conn.execute(
        "INSERT INTO history (ts, label, spam_prob, risk_score, url_count, has_qr, snippet) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (datetime.utcnow().isoformat(), label, float(spam_prob), int(risk_score), int(url_count), int(has_qr), snippet)
    )
    conn.commit()

def load_history(conn, limit=20):
    cur = conn.cursor()
    cur.execute("""
        SELECT ts, label, spam_prob, risk_score, url_count, has_qr, snippet
        FROM history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    return rows

db_conn = get_db_conn()

# ========================= LOAD MODEL ============================

@st.cache_resource
def load_model():
    with open(Baseline_MODEL_PATH, "rb") as f:
        m = pickle.load(f)
    return m["vectorizer"], m["classifier"]

vectorizer, classifier = load_model()

# ========================= URL PHISHING UTILS =====================

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
    "wallet", "password", "reset", "payment", "confirm",
    "support", "security", "unlock"
]

def extract_urls(text):
    return re.findall(r"https?://[^\s)>\]]+", text)

def analyze_single_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = (parsed.path or "").lower()
    dom = domain.split(":", 1)[0]

    score = 0
    reasons = []

    if url.startswith("http://"):
        score += 2
        reasons.append("Uses http:// (not secure)")

    if dom in URL_SHORTENERS:
        score += 3
        reasons.append("Shortened URL (hidden target)")

    if "." in dom:
        tld = dom.split(".")[-1]
        if tld in SUSPICIOUS_TLDS:
            score += 2
            reasons.append(f"Suspicious domain '.{tld}'")

    try:
        ipaddress.ip_address(dom)
        score += 3
        reasons.append("IP-based URL")
    except:
        pass

    for kw in PHISHING_KEYWORDS:
        if kw in (domain + path):
            score += 2
            reasons.append(f"Contains '{kw}'")
            break

    if score >= 7:
        lvl, emoji = "HIGH RISK", "🟥"
    elif score >= 3:
        lvl, emoji = "MEDIUM RISK", "🟧"
    else:
        lvl, emoji = "SAFE", "🟩"

    return {"url": url, "score": score, "level": lvl, "emoji": emoji, "reasons": reasons or ["No suspicious indicators"]}

def analyze_urls(urls):
    if not urls:
        return [], 0
    items = [analyze_single_url(u) for u in urls]
    max_score = max(x["score"] for x in items)
    return items, max_score

# ========================= RISK SCORE ===============================

def compute_risk(spam_prob, url_score):
    return int((spam_prob * 60) + (url_score * 4))

def risk_label(score):
    if score >= 75:
        return "🟥 HIGH RISK"
    elif score >= 40:
        return "🟧 MEDIUM RISK"
    return "🟩 LOW RISK"

# ========================= CUSTOM CSS ==========================
st.markdown("""
<style>
body { background-color:#0E0F12; }
.header {
    font-size:48px;
    font-weight:900;
    text-align:center;
    background:linear-gradient(90deg,#00FFFF,#0088FF);
    -webkit-background-clip:text;
    color:transparent;
    text-shadow:0 0 20px #00FFFF60;
}
.sub-header {
    font-size:18px;
    color:#AFAFAF;
    text-align:center;
}
.glass-box {
    background:rgba(255,255,255,0.05);
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(0,255,255,0.2);
    backdrop-filter:blur(10px);
}
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ========================= HEADER ==============================
st.markdown("<h1 class='header'>⚡ AI Spam Detector</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Spam Classifier • URL Scanner • QR Decoder • Risk & History Dashboard</p>", unsafe_allow_html=True)
st.markdown("---")

# ========================= LAYOUT ===============================
left, right = st.columns([2.4, 1])

# ========================= LEFT SIDE ============================
with left:

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 📩 Enter Email Content")
    email_text = st.text_area(
        "Email Content",
        height=200,
        placeholder="Paste email here...",
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 📷 QR Scanner (Upload Image)")
    qr_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    extracted_qr_text = ""
    has_qr = 0

    if qr_file:
        img = Image.open(qr_file)
        decoded = decode(img)
        if decoded:
            extracted_qr_text = decoded[0].data.decode("utf-8")
            has_qr = 1
            st.success("QR Code Decoded!")
            st.write(extracted_qr_text)
        else:
            st.error("No QR code detected.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Analyze Email", use_container_width=True):
        text = (email_text + " " + extracted_qr_text).strip()

        if not text:
            st.warning("Please enter or upload something.")
            st.stop()

        # SPAM
        X = vectorizer.transform([text])
        spam_prob = classifier.predict_proba(X)[0][1]
        label = "SPAM" if spam_prob >= 0.5 else "NOT SPAM"
        pretty_label = "🛑 SPAM" if label == "SPAM" else "✅ NOT SPAM"

        st.write(f"### {pretty_label}")
        st.write(f"Spam Probability: `{spam_prob:.4f}`")

        # URL Analysis
        urls = extract_urls(text)
        url_info, url_score = analyze_urls(urls)

        st.markdown("### 🔗 URL Analysis")
        if urls:
            for u in url_info:
                st.markdown(f"**{u['emoji']} {u['level']}** — `{u['url']}`")
                for r in u["reasons"]:
                    st.markdown(f"- {r}")
        else:
            st.info("No URLs detected.")

        # TOTAL RISK
        total = compute_risk(spam_prob, url_score)
        lvl = risk_label(total)

        st.markdown(f"### ⚠ Total Risk Score: **{total}/100**")
        st.markdown(f"## {lvl}")
        st.progress(total / 100)

        # LOG TO DB
        log_prediction(
            db_conn,
            label=label,
            spam_prob=spam_prob,
            risk_score=total,
            url_count=len(urls),
            has_qr=has_qr,
            text=text
        )

        # DASHBOARD
        st.markdown("---")
        st.markdown("## 📊 Email Analysis Dashboard")

        bar_fig = go.Figure(go.Bar(
            x=["Spam", "Not Spam"],
            y=[spam_prob, 1 - spam_prob],
            marker_color=["red", "green"]
        ))
        bar_fig.update_layout(title="Spam vs Not Spam")
        st.plotly_chart(bar_fig, use_container_width=True)

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total,
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 40], "color": "green"},
                    {"range": [40, 75], "color": "yellow"},
                    {"range": [75, 100], "color": "red"}
                ],
                "bar": {"color": "cyan"}
            },
            title={"text": "Total Risk Score"}
        ))
        st.plotly_chart(gauge, use_container_width=True)

        if urls:
            counts = Counter([u["level"] for u in url_info])
            donut = go.Figure(go.Pie(
                labels=list(counts.keys()),
                values=list(counts.values()),
                hole=0.5
            ))
            donut.update_layout(title="URL Risk Breakdown")
            st.plotly_chart(donut, use_container_width=True)

# ========================= RIGHT SIDE ==========================
with right:

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 👨‍💻 Developer")
    st.write("**Sajjala Siddardha**")
    st.write("AIML @ SRKR Engineering College")
    st.write("[🌐 Portfolio](https://sajjala-portfolio.vercel.app)")
    st.write("📧 **siddardhagaming@gmail.com**")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.markdown("### 📜 Recent Scan History")

    rows = load_history(db_conn, limit=20)
    if rows:
        import pandas as pd
        df = pd.DataFrame(rows, columns=[
            "Timestamp (UTC)", "Label", "Spam Prob", "Risk Score",
            "URL Count", "Has QR", "Snippet"
        ])
        df["Spam Prob"] = df["Spam Prob"].round(4)
        st.dataframe(df, use_container_width=True, height=350)
    else:
        st.info("No scans logged yet. Run an analysis to populate history.")
    st.markdown("</div>", unsafe_allow_html=True)
