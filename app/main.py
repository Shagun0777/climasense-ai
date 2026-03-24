from fastapi import FastAPI
from app.agents.data_agent import DataAgent
from app.agents.risk_agent import RiskAgent
from app.agents.ai_agent import AIAgent
from app.agents.memory_agent import MemoryAgent
from app.agents.alert_agent import AlertAgent
from app.agents.health_agent import HealthAgent
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body

ai_agent = AIAgent()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_agent = DataAgent()
risk_agent = RiskAgent()
memory_agent = MemoryAgent()
alert_agent = AlertAgent()
health_agent = HealthAgent()

@app.get("/")
def root():
    return {"message": "ClimaSense AI is running 🚀"}


@app.get("/climate/{city}")
def get_climate(city: str):
    data = data_agent.fetch(city)
    risk = risk_agent.analyze(data)

    # 🧠 memory update
    history = memory_agent.update(city, data)
    trend = memory_agent.analyze_trend(city)
    alert = alert_agent.analyze(city, data, history)
    health = health_agent.analyze(data, risk)

    ai_output = ai_agent.generate_ai_response(data, risk)
    ai_insight = ai_agent.generate_insight(data, risk, trend, alert)

    return {
        "data": data,
        "meta": {
            "source": data.get("dataSource"),
            "confidence": data.get("confidence")
        },
        "risk": risk,
        "trend": trend,
        "history": history,
        "alert": alert,
        "healthDetails": health,
        "healthImpact": ai_output.get("health", "No data"),
        "recommendations": ai_output.get("recommendations", []),
        "aiInsight": ai_insight
    }

@app.post("/ask")
def ask_ai(payload: dict = Body(...)):
    question = payload.get("question")
    city = payload.get("city")

    data = data_agent.fetch(city)
    risk = risk_agent.analyze(data)
    history = memory_agent.update(city, data)
    trend = memory_agent.analyze_trend(city)
    alert = alert_agent.analyze(city, data, history)

    answer = ai_agent.answer_question(question, data, risk, trend, alert)

    return {
        "question": question,
        "answer": answer
    }