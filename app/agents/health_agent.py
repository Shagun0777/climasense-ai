class HealthAgent:
    def analyze(self, data, risk):
        aqi = data["aqi"]

        # 🔴 High Risk
        if aqi > 150:
            return {
                "riskLevel": "High",
                "affectedGroups": [
                    "Asthma patients",
                    "Heart patients",
                    "Children",
                    "Elderly"
                ],
                "explanation": f"AQI {aqi} is in unhealthy range"
            }

        # 🟠 Moderate Risk
        elif aqi > 100:
            return {
                "riskLevel": "Moderate",
                "affectedGroups": [
                    "Children",
                    "Elderly",
                    "People with respiratory issues"
                ]
            }

        # 🟢 Low Risk
        else:
            return {
                "riskLevel": "Low",
                "affectedGroups": ["General population"]
            }