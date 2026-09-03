# 🛡️ TrustLens

### AI-Powered Digital Safety Guardian

**TrustLens** is an AI-powered digital safety tool designed to help users identify potentially harmful or suspicious digital content and understand **what makes it risky and what they should do next**.

Instead of simply detecting scams, TrustLens focuses on **explaining the risk and guiding users toward safer actions**.

🚀 **Live Demo:** https://trust-lens-lake.vercel.app/

---

## ✨ Features

* 🔍 **Suspicious Text Analysis**
  Analyze messages, emails, or other text for potential scam indicators.

* 🔗 **URL Analysis**
  Check suspicious or unfamiliar links for potential security risks.

* 🖼️ **Image/Screenshot Analysis**
  Upload screenshots of suspicious messages, websites, or conversations for analysis.

* 🎙️ **Voice Analysis**
  Analyze voice input for potentially suspicious content.

* ⚠️ **Risk Detection**
  Identifies suspicious patterns and provides a risk assessment.

* 💡 **Explainable Results**
  Explains *why* something may be dangerous instead of only displaying a result.

* 🛡️ **Safety Recommendations**
  Provides practical next steps to help users respond safely.

* 📝 **User Feedback**
  Users can submit feedback about their experience with TrustLens.

---

## 🎯 Problem Statement

Online scams and digital fraud are becoming increasingly sophisticated.

Users often receive:

* Phishing messages
* Fake offers
* Suspicious links
* Fraudulent payment requests
* Impersonation messages
* Malicious screenshots
* Social engineering attempts

The problem isn't only **"Is this a scam?"**

The more important question is:

> **"Is this safe, and what should I do next?"**

TrustLens was created to answer exactly that.

---

## 💡 Our Solution

TrustLens acts as a **digital safety assistant**.

The user can provide suspicious content through text, URL, image, or voice.

TrustLens then:

```text
User Input
    ↓
Content Analysis
    ↓
Risk Detection
    ↓
Risk Explanation
    ↓
Recommended Safe Action
```

This makes cybersecurity information easier to understand, especially for users who may not have technical security knowledge.

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │       User          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   TrustLens UI      │
                 │  Next.js + Tailwind │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    FastAPI Backend  │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          Text Analysis  URL Analysis  Image Analysis
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                 ┌─────────────────────┐
                 │   Risk Assessment   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Explanation +       │
                 │ Safety Recommendation│
                 └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

* **Next.js**
* **React**
* **JavaScript**
* **Tailwind CSS**

### Backend

* **Python**
* **FastAPI**
* REST APIs

### Analysis

* Text-based scam/risk detection
* URL analysis
* Image analysis
* Voice analysis

### Data & Services

* Google Sheets for feedback storage
* Vercel for frontend deployment
* Render for backend deployment

---

## 📂 Project Structure

```text
TrustLens/
│
├── frontend/
│   ├── app/
│   │   ├── page.js
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── ...
│
├── README.md
└── ...
```

> The exact structure may vary depending on the current project branch.

---

## 🔌 API Endpoints

The backend provides endpoints for different types of analysis:

| Method | Endpoint         | Purpose                          |
| ------ | ---------------- | -------------------------------- |
| `GET`  | `/`              | Check whether the API is running |
| `POST` | `/analyze/text`  | Analyze suspicious text          |
| `POST` | `/analyze/url`   | Analyze a URL                    |
| `POST` | `/analyze/image` | Analyze an uploaded image        |
| `POST` | `/analyze/voice` | Analyze voice input              |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Sanskrutipanchal/TrustLens.git
cd TrustLens
```

### 2. Backend Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The backend will run locally at:

```text
http://127.0.0.1:8000
```

---

### 3. Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open the application in your browser:

```text
http://localhost:3000
```

---

## 🔐 Environment Variables

Create a `.env` file for required configuration.

Example:

```env
# Backend
API_URL=your_backend_url

# Add other required API keys/configuration here
```

⚠️ **Never commit API keys, passwords, or other secrets to GitHub.**

---

## 📊 Feedback System

TrustLens includes a feedback mechanism that allows users to share their experience after using the application.

Feedback is stored in **Google Sheets**, allowing the team to review user responses and improve the application.

---

## 🌐 Deployment

TrustLens uses:

* **Vercel** → Frontend deployment
* **Render** → Backend deployment

### Live Application

🚀 https://trust-lens-lake.vercel.app/

---

## 🔒 Safety Disclaimer

TrustLens is an assistance tool and should not be considered a complete cybersecurity solution.

A low-risk result does **not guarantee that content is safe**.

Users should avoid sharing passwords, OTPs, banking credentials, private keys, or other sensitive information with suspicious sources.

When in doubt, verify information through an official source before taking action.

---

## 🎯 Future Improvements

Some potential improvements include:

* 🤖 More advanced AI-based threat detection
* 🌐 Real-time URL reputation checking
* 📱 Mobile application
* 📧 Browser/email integration
* 🧠 Improved phishing and social-engineering detection
* 🌍 Multi-language support
* 📈 User analytics dashboard
* 🔔 Real-time scam alerts
* 🔍 Integration with threat-intelligence databases

---

## 👩‍💻 Team

Built with ❤️ as a **hackathon project** focused on making digital safety easier and more accessible.

---

## ⭐ Support

If you find TrustLens useful, consider giving the repository a ⭐ on GitHub and sharing your feedback.

**Stay Alert. Stay Safe. Trust, but Verify. 🛡️**
