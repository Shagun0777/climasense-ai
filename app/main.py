from fastapi import FastAPI
from app.agents.data_agent import DataAgent
from app.agents.risk_agent import RiskAgent
from app.agents.ai_agent import AIAgent
from app.agents.memory_agent import MemoryAgent

ai_agent = AIAgent()

app = FastAPI()

data_agent = DataAgent()
risk_agent = RiskAgent()
memory_agent = MemoryAgent()

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

    health = ai_agent.generate_health_impact(data, risk)
    recommendations = ai_agent.generate_recommendations(data, risk)

    return {
        "data": data,
        "risk": risk,
        "trend": trend,          # 🔥 NEW
        "history": history,      # 🔥 NEW
        "healthImpact": health,
        "recommendations": recommendations
    }