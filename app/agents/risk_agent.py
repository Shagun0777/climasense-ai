class RiskAgent:
    def analyze(self, data: dict):
        aqi = data["aqi"]
        temp = data["temperature"]

        # Air Quality Risk
        if aqi <= 50:
            air_risk = "Low"
        elif aqi <= 100:
            air_risk = "Moderate"
        elif aqi <= 150:
            air_risk = "Unhealthy for Sensitive Groups"
        else:
            air_risk = "High"

        # Heat Risk
        if temp < 25:
            heat_risk = "Low"
        elif temp < 35:
            heat_risk = "Moderate"
        else:
            heat_risk = "High"

        # Overall Risk (simple logic)
        if air_risk in ["High", "Unhealthy for Sensitive Groups"]:
            overall = "High"
        elif heat_risk == "Moderate":
            overall = "Medium"
        else:
            overall = "Low"

        # 🔥 scoring
        aqi_score = min(aqi / 3, 50)   # AQI weight
        temp_score = min(temp * 1.5, 50)

        risk_score = int(aqi_score + temp_score)

        return {
            "airRisk": air_risk,
            "heatRisk": heat_risk,
            "overallRisk": overall,
            "riskScore": risk_score,
            "reason": f"AQI contribution + temperature impact"
        }