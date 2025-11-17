<h1 align="center">⚡ AI Spam & Phishing Detector</h1>

<p align="center">
  <b>Email Spam Detection • URL Phishing Scanner • QR Text Scanner • Risk Dashboard</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Deployed-brightgreen?style=flat-square&logo=streamlit" />
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/ML-ScikitLearn-orange?style=flat-square&logo=scikitlearn" />
  <img src="https://img.shields.io/github/license/sajjala-siddardha/email-spam-detector?style=flat-square" />
  <img src="https://img.shields.io/github/stars/sajjala-siddardha/email-spam-detector?style=flat-square" />
</p>

---

## 🚀 Live App  
🔗 **https://email-spam-detector-score.streamlit.app**

---


---

## 🎯 Overview  
An AI-powered security tool that detects:

- **Spam Emails** using machine learning  
- **Phishing URLs** using advanced rule-based checks  
- **QR Code Text Analysis** *(image QR decoding not supported on Streamlit Cloud)*  
- **Risk Scoring (0–100)**  
- **Interactive Visualization Dashboard**

Fast • Lightweight • Cloud Deployable

---

## 📌 Features  

### 📩 Email Spam Detection  
- TF-IDF Vectorizer  
- Logistic Regression Classifier  
- **98–99% Accuracy**  
- Real-time predictions  

### 🔗 URL Phishing Analysis  
✔ Suspicious TLD check (`.xyz`, `.top`, `.icu`, `.zip`)  
✔ Shortened URL detection (`bit.ly`, `t.co`)  
✔ IP-based URL detection  
✔ Keyword detection (`login`, `reset`, `verify`, `bank`)  
✔ Per-URL risk scoring  

### 📱 QR Code Support (Text Only)
Streamlit Cloud **cannot install zbar**,  
so QR **images cannot be decoded**.

But **decoded text can be pasted and analyzed** ✔

### 📊 Dashboard Visualizations  
- Spam vs Not-Spam Bar Chart  
- Gauge Meter – Total Risk Score  
- URL Risk Donut Chart  
- Suspicious Keyword Frequency Chart  

---

## 🛠 Tech Stack  

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| ML Model | Scikit-learn |
| Charts | Plotly |
| Language | Python 3.10 |
| Deployment | Streamlit Cloud |

---

## 📂 Folder Structure  
*(Folder structure fixed — perfectly formatted)*
email-spam-detector/
│
├── app/
│   └── streamlit_app.py               # Main Streamlit UI
│
├── models/
│   ├── baseline_model.pkl             # TF-IDF logistic regression model
│   └── miniLM_onnx/                   # (Optional) ONNX model files
│
├── data/
│   ├── raw/
│   │   └── spam.csv                   # Original dataset
│   └── processed/
│       └── spam_clean.csv             # Cleaned dataset
│
├── src/
│   ├── __init__.py
│   ├── config.py                      # Configuration paths/settings
│   ├── data_prep.py                   # Data preprocessing
│   ├── evaluate.py                    # Model evaluation scripts
│   ├── explain.py                     # SHAP/explainability scripts
│   ├── export_onnx.py                 # ONNX export utility
│   ├── predict.py                     # Baseline prediction script
│   ├── predict_hybrid.py              # Hybrid model prediction
│   ├── train_baseline.py              # Train TF-IDF Logistic Regression
│   ├── train_hybrid.py                # Train CatBoost + MiniLM hybrid
│   └── train_transformer.py           # Train transformer embeddings
│
├── notebooks/
│   └── *.ipynb                        # Experiments & EDA
│
├── catboost_info/                    # CatBoost auto logs
│
├── setup_structure.py                 # Auto folder setup script
├── requirements.txt                   # Dependency list
├── README.md                          # Project documentation
└── LICENSE                            # MIT License
