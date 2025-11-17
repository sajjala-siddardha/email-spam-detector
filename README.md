# ⚡ AI Spam & Phishing Detector
### **Email Spam Detection • URL Phishing Scan • QR Text Scanner • Risk Dashboard**

[![Streamlit App](https://img.shields.io/badge/Live_App-Streamlit-brightgreen?logo=streamlit)](https://email-spam-detector-score.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)]()
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)
![Stars](https://img.shields.io/github/stars/sajjala-siddardha/email-spam-detector?style=social)

---

## 🚀 **Live App**
👉 **https://email-spam-detector-score.streamlit.app**

---

## 🎯 **Project Summary**

This project is an **AI-powered security tool** that identifies:

🔹 **Spam Emails** using a machine learning classifier  
🔹 **Phishing URLs** with rule-based analysis  
🔹 **QR Code Text Scanning (manual text input)**  
🔹 **Combined Risk Score (0–100)**  
🔹 **Interactive Visual Dashboard** for insights  

Fast, lightweight, and fully deployable using **Streamlit Cloud**.

---

## ✨ **Key Features**

### 📩 **1. Spam Email Detection**
- TF-IDF Vectorizer  
- Logistic Regression Model  
- ~98–99% accuracy  
- Real-time predictions  
- Lightweight & CPU-optimized  

---

### 🔗 **2. URL Phishing Detector**
Detects:

✔ Suspicious domain endings (.xyz, .top, .icu, .loan…)  
✔ URL shorteners (bit.ly, t.co, tinyurl…)  
✔ IP-based URLs  
✔ Malicious keywords (login, verify, bank, reset…)  
✔ Risk score per URL  

---

### 📱 **3. QR Code Support (Text Only)**
⚠ **Streamlit Cloud does NOT support zbar**, so QR images cannot be decoded.  
However, decoded **QR text can be pasted** and analyzed safely.

---

### 📊 **4. Visual Dashboard**
Includes:

📌 Spam vs Not-Spam Bar Chart  
📌 Overall Risk Score Gauge  
📌 URL Risk Donut Chart  
📌 Suspicious Keyword Frequency Graph  

---

## 🛠 **Tech Stack**

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| ML Model | Scikit-learn (TF-IDF + Logistic Regression) |
| Charts | Plotly |
| Language | Python 3.10 |
| Deployment | Streamlit Cloud |

---

# 📂 **Project Folder Structure**

```text
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
│   ├── data_prep.py                   # Data preprocessing steps
│   ├── evaluate.py                    # Model evaluation functions
│   ├── explain.py                     # Explainability scripts (SHAP)
│   ├── export_onnx.py                 # ONNX export utility
│   ├── predict.py                     # Baseline TF-IDF predictions
│   ├── predict_hybrid.py              # (Optional) Hybrid model prediction
│   ├── train_baseline.py              # Train logistic regression baseline
│   ├── train_hybrid.py                # Train CatBoost + Transformer model
│   └── train_transformer.py           # Train MiniLM embeddings
│
├── notebooks/
│   └── *.ipynb                        # EDA & experimentation notebooks
│
├── catboost_info/                     # CatBoost training logs
│
├── requirements.txt                   # Python dependencies
├── README.md                          # Documentation
└── LICENSE                            # MIT License

Run This Project Locally
git clone https://github.com/sajjala-siddardha/email-spam-detector.git
cd email-spam-detector
pip install -r requirements.txt
streamlit run app/streamlit_app.py

🌐 Deploy to Streamlit Cloud
Go to: https://share.streamlit.io
Click New App
Select your forked repository
App settings:
Field	Value
Repo	YOUR-USERNAME/email-spam-detector
Branch	main
File	app/streamlit_app.py
Click Deploy
Done! 🎉 Your app is now live.

📜 License
This project is licensed under the MIT License.
You are free to use, modify, and distribute it.

👨‍💻 Developer
Sajjala Siddardha
AIML @ SRKR Engineering College
📧 Email: siddardhagaming@gmail.com
🌐 Portfolio: https://sajjala-portfolio.vercel.app
🐙 GitHub: https://github.com/sajjala-siddardha

⭐ Support This Project
If this project helped you, please ⭐ star the repo — it motivates future updates!
