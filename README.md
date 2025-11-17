# ⚡ AI Spam & Phishing Detector  
### Email Spam Detection • URL Phishing Scan • QR Text Scanner • Risk Dashboard

## 🚀 Live App  
🔗 https://email-spam-detector-score.streamlit.app

---

## 🎯 Project Description  
This project is an AI-powered security tool that detects:

- Spam Emails using a Machine Learning model  
- Phishing URLs with rule-based analysis  
- QR Code Text (manual entry support)  
- Combined Risk Scoring (0–100)  
- Interactive Visualization Dashboard  

Fast, lightweight, deployable on Streamlit Cloud.

---

## 📌 Features

### 📩 Spam Email Detection  
- TF-IDF Vectorizer  
- Logistic Regression Model  
- 98–99% Accuracy  
- Real-time prediction  

### 🔗 URL Phishing Detection  
- Detects suspicious domain endings (.xyz, .top, .icu…)  
- Detects shortened URLs (bit.ly, t.co, tinyurl…)  
- Detects IP-based URLs  
- Detects phishing keywords (login, verify, bank, reset…)  
- Per-URL risk indicators  

### 📱 QR Code Support (Text Only)  
Streamlit Cloud does **NOT** support the `zbar` library.  
So QR images cannot be decoded, but **decoded QR text can be analyzed.**

### 📊 Visual Dashboard  
- Spam vs Not-Spam Bar Chart  
- Total Risk Score Gauge  
- URL Risk Donut Chart  
- Suspicious Keyword Frequency Chart  

---

## 🛠 Tech Stack  

| Component  | Technology |
|-----------|------------|
| Frontend  | Streamlit |
| ML Model  | Scikit-learn |
| Charts    | Plotly |
| Language  | Python 3.10 |
| Deployment| Streamlit Cloud |

---

## 📂 Folder Structure

email-spam-detector/
│
├── app/
│ └── streamlit_app.py
│
├── models/
│ └── baseline_model.pkl
│
├── requirements.txt
├── README.md
└── LICENSE

yaml
Copy code

---

## 🚀 Run Project Locally

```bash
git clone https://github.com/sajjala-siddardha/email-spam-detector.git
cd email-spam-detector
pip install -r requirements.txt
streamlit run app/streamlit_app.py
🍴 How to Fork This Repo
1. Click Fork (top-right of GitHub)
2. Clone your fork:
bash
Copy code
git clone https://github.com/YOUR-USERNAME/email-spam-detector.git
cd email-spam-detector
3. Make your changes
4. Commit & push
bash
Copy code
git add .
git commit -m "Updated features"
git push origin main
5. Deploy to Streamlit Cloud
Go to https://share.streamlit.io

Click New App

Select:

Repo: YOUR-USERNAME/email-spam-detector

Branch: main

File: app/streamlit_app.py

Click Deploy

Done! Your app is live.

📜 License
This project uses the MIT License.
You may use, modify, and distribute freely.

👨‍💻 Developer
Sajjala Siddardha
AIML @ SRKR Engineering College
📧 siddardhagaming@gmail.com
🌐 Portfolio: https://sajjala-portfolio.vercel.app
🐙 GitHub: https://github.com/sajjala-siddardha

⭐ Support
If you found this helpful, please ⭐ star the repository.
It motivates future improvements!

