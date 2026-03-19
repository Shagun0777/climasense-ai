import requests

class AIAgent:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"

    def call_llm(self, prompt):
        try:
            response = requests.post(
                self.url,
                json={
                    "model": "tinyllama",
                    "prompt": prompt,
                    "stream": False
                }
            )

            data = response.json()
            return data.get("response", "").strip()

        except Exception as e:
            print("❌ Ollama Error:", e)
            return None

    # 🔥 HEALTH IMPACT
    def generate_health_impact(self, data, risk):
        prompt = f"""
        You must follow instructions strictly.

        AQI: {data['aqi']}
        Risk: {risk['airRisk']}

        Rules:
        - Output ONLY 1 short sentence
        - Max 15 words
        - No introduction
        - No explanation
        - No extra text
        - No formatting

        Example:
        AQI 150 can cause breathing issues.

        Now generate output:
        """

        result = self.call_llm(prompt)

        if result:
            cleaned = result.split("\n")[0][:120]  # 🔥 hard limit
            print("✅ LLM HEALTH:", cleaned)
            return cleaned

        return self.fallback_health(data, risk)

    # 🔥 RECOMMENDATIONS
    def generate_recommendations(self, data, risk):
        prompt = f"""
        Follow instructions STRICTLY.

        AQI: {data['aqi']}
        Temp: {data['temperature']}
        Risk: {risk['overallRisk']}

        Rules:
        - EXACTLY 3 bullet points
        - Each under 6 words
        - No explanation
        - No extra text

        Format:
        1. Wear mask
        2. Avoid outdoor activity
        3. Stay hydrated

        Now generate:
        """

        result = self.call_llm(prompt)

        if result:
            lines = result.split("\n")

            # 🔥 strict filtering
            valid = []
            for line in lines:
                if line.strip().startswith(("1.", "2.", "3.")):
                    valid.append(line.strip())

            if len(valid) >= 3:
                cleaned = "\n".join(valid[:3])
                print("✅ LLM RECOMMEND:", cleaned)
                return cleaned

        return self.fallback_recommendations(data, risk)

    # 🔥 FALLBACKS
    def fallback_health(self, data, risk):
        return f"AQI {data['aqi']} may impact respiratory health."

    def fallback_recommendations(self, data, risk):
        return "1. Avoid outdoor exposure\n2. Wear mask\n3. Stay hydrated"