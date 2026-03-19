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
        if air_risk in ["High", "Unhealthy for Sensitive"]:
            overall = "High"
        elif heat_risk == "Moderate":
            overall = "Medium"
        else:
            overall = "Low"

        return {
            "airRisk": air_risk,
            "heatRisk": heat_risk,
            "overallRisk": overall
        }