import requests
import json

class AIAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"

    def call_llm(self, prompt):
        try:
            response = requests.post(
                self.url,
                json={
                    "model": "phi3:mini",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=20

            )

            data = response.json()
            return data.get("response", "").strip()

        except Exception as e:
            print("❌ Ollama Error:", e)
            return None
     
    def safe_parse(self, text):
        try:
            if "{" not in text or "}" not in text:
                return None

            start = text.find("{")
            end = text.rfind("}") + 1

            json_str = text[start:end]

            data = json.loads(json_str)

            if "health" not in data or "recommendations" not in data:
                return None

            if not isinstance(data["recommendations"], list):
                return None

            if len(data["recommendations"]) != 3:
                return None

            return data

        except Exception as e:
            print("❌ Parse Error:", e)
            return None


    def validate_output(self, data):
        if len(data["health"].split()) > 12:
            return False

        for rec in data["recommendations"]:
            if len(rec.split()) > 5:
                return False

        return True   

    def generate_ai_response(self, data, risk):
        prompt = f"""
        You must return ONLY JSON.

        STRICT RULES:
        - No text before or after JSON
        - Recommendations must be SHORT (max 5 words)
        - Recommendations must match AQI level

        AQI behavior:
        - AQI <= 50 → encourage outdoor activity
        - AQI 51–100 → light caution
        - AQI 101–150 → reduce exposure
        - AQI > 150 → avoid outdoor activity

        Format:
        {{
        "health": "max 12 words",
        "recommendations": [
            "short action",
            "short action",
            "short action"
        ]
        }}

        Data:
        AQI: {data['aqi']}
        Risk: {risk['overallRisk']}
        Temperature: {data['temperature']}
        """

        for _ in range(3):  # retry loop
            result = self.call_llm(prompt)

            if not result:
                continue

            parsed = self.safe_parse(result)

            if parsed and self.validate_output(parsed):
                parsed["recommendations"] = self.refine_recommendations(
                    parsed["recommendations"],
                    data["aqi"],
                    data.get("dominantPollutant")
                )
                return parsed

        return self.fallback_combined(data, risk)
    
    def fallback_combined(self, data, risk):
        return {
            "health": f"AQI {data['aqi']} requires caution.",
            "recommendations": self.refine_recommendations([], data["aqi"])
        }

    def generate_insight(self, data, risk, trend, alert):
        prompt = f"""
        Return ONLY JSON.

        {{
        "summary": "combine AQI, trend, alert in 1 line",
        "cause": "city-aware explanation using pollutant + realistic urban causes",
        "riskOutlook": "future expectation",
        "confidence": "Low/Medium/High"
        }}

        Data:
        City: {data.get('city')}
        State: {data.get('state')}
        Country: {data.get('country')}

        AQI: {data['aqi']}
        Risk: {risk['overallRisk']}
        Trend: {trend}

        Dominant Pollutant (human readable): {data.get('dominantPollutant')}
        Pollution Source Hint: {data.get('pollutionSource')}

        Context Rules:
        - Use city context if relevant
        - Do NOT assume facts not supported by data
        - If unsure, say "likely due to common urban factors"

        Alert: {alert.get('type')}
        """

        result = self.call_llm(prompt)

        if not result:
            return self.fallback_insight(data, trend)

        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            parsed = json.loads(result[start:end])
            return parsed
        except:
            return self.fallback_insight(data, trend)
        
    def fallback_insight(self, data, trend):
        return {
            "summary": f"AQI {data['aqi']} with {trend.lower()}",
            "cause": f"Driven by {data.get('dominantPollutant')}",
            "riskOutlook": "Monitor closely",
            "confidence": "Low"
        }
    
    def answer_question(self, question, data, risk, trend, alert):
        prompt = f"""
        Answer the user question using the data.

        Keep answer:
        - Short
        - Clear
        - Helpful

        Question: {question}

        Context:
        AQI: {data['aqi']}
        Risk: {risk['overallRisk']}
        Trend: {trend}
        Alert: {alert.get('type')}
        Dominant Pollutant (human readable): {data.get('dominantPollutant')}
        Source: {data.get('pollutionSource')}

        Answer:
        """

        result = self.call_llm(prompt)

        if not result:
            return "Unable to answer right now"

        return result.strip()
    
    def refine_recommendations(self, recs, aqi, pollutant=None):
        base = []

        if aqi <= 50:
            base = [
                "Enjoy outdoor activities",
                "No mask needed",
                "Air quality is safe"
            ]
        elif aqi <= 100:
            base = [
                "Air is generally safe",
                "Sensitives limit exposure",
                "Stay hydrated"
            ]
        elif aqi <= 150:
            base = [
                "Limit outdoor activity",
                "Avoid heavy exercise",
                "Wear mask outdoors"
            ]
        else:
            base = [
                "Avoid outdoor activity",
                "Stay indoors mostly",
                "Use air purifier"
            ]

        # 🔥 pollutant awareness (small but powerful)
        if pollutant == "pm2_5":
            base[2] = "Use N95 mask"
        elif pollutant == "o3":
            base[1] = "Avoid midday exposure"

        return list(set(recs[:1] + base[:2]))
    