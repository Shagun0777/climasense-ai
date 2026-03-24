class AlertAgent:
    def analyze(self, city, data, history):
        if len(history) < 2:
            return {"alert": False, "type": None, "message": None}

        latest = history[-1]
        prev = history[-2]

        # 🔥 HIGH PRIORITY → always check first
        if latest["aqi"] > 150:
            return {
                "alert": True,
                "type": "HIGH_RISK",
                "message": "Air quality is unhealthy",
                "reason": f"AQI reached {latest['aqi']}"
            }

        # 🔥 AQI SPIKE
        if latest["aqi"] - prev["aqi"] > 30:
            return {
                "alert": True,
                "type": "AQI_SPIKE",
                "message": "Sudden air quality worsening detected",
                "reason": f"Jumped from {prev['aqi']} → {latest['aqi']}"
            }

        # 🔥 TEMP SPIKE
        if latest["temperature"] - prev["temperature"] > 5:
            return {
                "alert": True,
                "type": "TEMP_SPIKE",
                "message": "Temperature increased sharply",
                "reason": f"Temperature rose from {prev['temperature']} → {latest['temperature']}"
            }

        return {
            "alert": False,
            "type": None,
            "message": None
        }