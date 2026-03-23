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
                timeout=10

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

        If you fail, return EMPTY {{}}.

        STRICT RULES:
        - No text before JSON
        - No text after JSON
        - No explanation

        Format:
        {{
        "health": "max 12 words",
        "recommendations": [
            "max 5 words",
            "max 5 words",
            "max 5 words"
        ]
        }}

        Data:
        AQI: {data['aqi']}
        Temp: {data['temperature']}
        Risk: {risk['overallRisk']}
        """

        for _ in range(3):  # retry loop
            result = self.call_llm(prompt)

            if not result:
                continue

            parsed = self.safe_parse(result)

            if parsed and self.validate_output(parsed):
                print("✅ LLM FINAL:", parsed)
                return parsed

        return self.fallback_combined(data, risk)
    
    def fallback_combined(self, data, risk):
        return {
            "health": f"AQI {data['aqi']} may affect breathing.",
            "recommendations": [
                "Avoid outdoor exposure",
                "Wear mask",
                "Stay hydrated"
            ]
        }