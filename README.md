# 🌍 Climate Intelligence (ClimaSense AI)

> Turning real-time environmental data into **actionable intelligence using AI agents**

---

## 🚀 Demo Highlights

- 🔴 High AQI → Alerts + strict recommendations  
- 🟡 Moderate AQI → Balanced guidance  
- 🟢 Low AQI → Safe activity suggestions  

👉 Not just a dashboard — a **decision-making assistant**

---

## 🧠 What is this?

Climate Intelligence is an **AI-powered system** that:

- Fetches real-time AQI data
- Understands environmental risk
- Explains *why* pollution is happening
- Predicts future risk trends
- Answers natural language queries

---

## ✨ Key Features

### 🌫️ Real-Time AQI Monitoring
- Live AQI per city
- Risk classification (Low → Severe)
- City + State awareness
- Health-aware dominant pollutant detection

---

### 🧠 AI Insight Engine
- Summary of air conditions  
- Root cause analysis (city-aware)  
- Future risk outlook  
- **Confidence scoring (data reliability)**  

---

### ⚠️ Smart Alert System
- Detects sudden AQI spikes  
- Highlights critical conditions  
- Triggers warning UI  

---

### 📋 Agentic Recommendations
- Dynamic (not rule-based)  
- Based on AQI + pollutant  
- Real-world actionable guidance  

---

### 💬 Conversational AI Assistant
Ask questions like:
- “Can I go outside today?”
- “Is it safe for kids?”
- “Why is pollution high?”

👉 Answers are grounded in **real-time data**

---

### 📊 Pollution Intelligence
- Visual breakdown of pollutants  
- Severity-based color indicators  
- Dominant pollutant based on **health impact (not raw value)**  

---

## 📊 Confidence Score (Transparency Feature)

The system assigns confidence levels based on:

- Data source reliability (IQAir vs fallback)
- Historical trend availability
- AI output validity

| Confidence | Meaning |
|----------|--------|
| High | Reliable real-time + stable AI output |
| Medium | Partial data / moderate certainty |
| Low | Limited data or fallback used |

---

## 🖼️ Screenshots

### 🔹 1. Smart AQI Dashboard (City-Aware Insights)
![Dashboard Kanpur](./screenshots/Dashboard%20Kanpur.jpeg)

👉 Shows:
- City + State detection
- AQI with risk classification
- Dominant pollutant (user-friendly)
- AI-generated insight

---

### 🔹 2. High Pollution Scenario with Alerts
![High AQI Alert](./screenshots/High%20AQI%20Alert.jpeg)

👉 Shows:
- Severe AQI (Delhi)
- Alert detection system
- High-risk recommendations
- Context-aware AI reasoning

---

### 🔹 3. Low Pollution Scenario (Safe Conditions)
![Good AQI](./screenshots/good-aqi.jpeg)

👉 Shows:
- Safe AQI levels
- Positive recommendations
- System adaptability across environments

---

### 🔹 4. AI Insight Engine (Deep Reasoning)
![AI Insight](./screenshots/AI%20Insight.jpeg)

👉 Shows:
- Summary, Cause, Outlook
- City-aware reasoning
- Confidence scoring

---

### 🔹 5. Pollution Breakdown Visualization
![Pollution Breakdown](./screenshots/Pollution%20Breakdown.jpeg)

👉 Shows:
- Component-level pollution
- Severity-based coloring
- Interactive tooltip insights

---

### 🔹 6. Conversational AI Assistant
![AI Chat](./screenshots/AI%20Chat.jpeg)

👉 Shows:
- Natural language queries
- Context-aware answers based on AQI

---

### 🔹 7. Context-Aware Q&A (Health Guidance)
![AI Health Query](./screenshots/AI%20Health%20Query.jpeg)

👉 Shows:
- Personalized safety advice
- Health-focused recommendations

---

### 🔹 9. Alert Component (Focused View)
![Alert Component](./screenshots/Alert%20Panel.jpeg)

👉 Shows:
- Real-time anomaly detection
- Visual alert system

---

## 🏗️ Architecture

- Designed with modular agent architecture for scalability

```

Frontend (React + Vite)  
↓  
Backend (FastAPI APIs)  
↓  
Multi-Agent Intelligence Layer  
↓  
LLM (Ollama - Local)

```


---

## 🤖 AI Agent System

This project follows a **modular multi-agent design**:

| Agent | Responsibility |
|------|--------------|
| Data Agent | Fetches AQI data |
| Risk Agent | Computes environmental risk |
| Memory Agent | Tracks historical trends |
| Alert Agent | Detects anomalies |
| Health Agent | Maps AQI → health impact |
| AI Agent | Generates insights, recommendations, answers |

---

## 🧪 Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- Recharts

### Backend
- FastAPI
- Python

### AI Layer
- Ollama (phi3 / local LLM)
- Prompt-engineered reasoning

---

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/Shagun0777/climasense-ai
cd climasense-ai
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## ⚠️ Note on AI Model

This project uses Ollama (local LLM).

- Requires local setup
- Not deployed in cloud version
- Can be replaced with OpenAI / Groq APIs

## 🚀 Future Improvements

- Hosted LLM integration (Groq / OpenAI)
- Personalized health recommendations
- Weather + pollution correlation
- Mobile optimization
- Real-time alerts

## 🎯 Why This Project Matters

This project demonstrates:

- ✅ Building real-world AI systems (not just models)  
- ✅ Designing modular multi-agent architectures  
- ✅ Integrating LLMs with structured outputs  
- ✅ Translating raw data into actionable decisions  
- ✅ Full-stack product thinking with clean UI/UX  

## 👨‍💻 Author

Shagun Tripathi

## 📌 Repository

👉 https://github.com/Shagun0777/climasense-ai

> This project focuses on making AI useful, not just impressive.




