# 🌍 Climate Risk Intelligence Agent

A multi-agent AI system that analyzes environmental data and provides health insights, risk scoring, and recommendations.

## 🚀 Features

- 🌡️ Real-time weather data (temperature, humidity)
- 🌫️ AQI-based risk analysis
- 🧠 Multi-agent architecture:
  - Data Agent
  - Risk Agent
  - Memory Agent (trend detection)
  - AI Agent (LLM-powered insights)
- 🤖 Local LLM integration using Ollama (TinyLlama)
- 🔁 Fallback handling when LLM fails

## 🧠 Architecture

User → FastAPI → Agents:
- Data → Fetch data
- Risk → Compute risk
- Memory → Store history + trend
- AI → Generate insights

## ⚙️ Tech Stack

- Python + FastAPI
- Ollama (Local LLM)
- OpenWeather API
- Requests

## 🧪 Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload