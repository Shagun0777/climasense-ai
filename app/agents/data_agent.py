import requests
import random
import os
from dotenv import load_dotenv


load_dotenv()

class DataAgent:
    def __init__(self):
        self.weather_api_key = os.getenv("WEATHER_API_KEY")

    def get_weather(self, city: str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if "main" not in data:
            raise Exception(f"Weather API failed: {data}")

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "lat": data["coord"]["lat"],    
            "lon": data["coord"]["lon"]     
        }

    def get_mock_aqi(self, city: str):
        return random.randint(80, 200)

    def get_aqi(self, lat, lon):
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.weather_api_key}"
        response = requests.get(url)
        data = response.json()
        print("AQI RAW RESPONSE:", data)

        if "list" not in data:
            raise Exception(f"AQI API failed: {data}")

        components = data["list"][0]["components"]
        return components   

    def convert_pm25_to_aqi(self, pm25):
        if pm25 <= 12:
            return int((pm25 / 12) * 50)
        elif pm25 <= 35.4:
            return int(((pm25 - 12) / (35.4 - 12)) * 50 + 50)
        elif pm25 <= 55.4:
            return int(((pm25 - 35.4) / (55.4 - 35.4)) * 50 + 100)
        elif pm25 <= 150.4:
            return int(((pm25 - 55.4) / (150.4 - 55.4)) * 100 + 150)
        else:
            return int(min(300, pm25 * 2))
        
    def get_dominant_pollutant(self, components):
        filtered = {
            "pm2_5": components["pm2_5"],
            "pm10": components["pm10"],
            "no2": components["no2"],
            "o3": components["o3"]
        }

        return max(filtered, key=filtered.get)
       
    def estimate_source(self, components):
        if components["no2"] > 20:
            return "Traffic pollution"

        if components["so2"] > 10:
            return "Industrial pollution"

        if components["pm2_5"] > 50:
            return "Dust / Construction"

        return "Mixed sources"

    def classify_pollutant_level(self, name, value):
        if name == "pm2_5":
            if value <= 12: return "Good"
            elif value <= 35: return "Moderate"
            elif value <= 55: return "Unhealthy"
            else: return "Severe"

        if name == "pm10":
            if value <= 50: return "Good"
            elif value <= 100: return "Moderate"
            else: return "Unhealthy"

        if name == "no2":
            if value <= 40: return "Good"
            elif value <= 80: return "Moderate"
            else: return "Unhealthy"

        if name == "o3":
            if value <= 50: return "Good"
            elif value <= 100: return "Moderate"
            else: return "Unhealthy"

        if name == "co":
            return "Moderate"

        if name == "so2":
            return "Good"

        if name == "nh3":
            return "Moderate"

        return "Unknown"

    def fetch(self, city: str):

        # # 🔥 HANDLE TEST CITIES FIRST (NO API CALL)
        # if city == "test":
        #     # simulate changing AQI each call
        #     import random
        #     return {
        #         "city": city,
        #         "temperature": random.choice([25, 30, 35]),
        #         "humidity": 40,
        #         "aqi": random.choice([100, 140, 170])
        #     }

        # ✅ NORMAL FLOW
        weather = self.get_weather(city)

        components = self.get_aqi(weather["lat"], weather["lon"])

        levels = {}

        for key, value in components.items():
            levels[key] = self.classify_pollutant_level(key, value)

        pm25 = components["pm2_5"]
        aqi = self.convert_pm25_to_aqi(pm25)

        dominant = self.get_dominant_pollutant(components)
        source = self.estimate_source(components)

        return {
            "city": city,
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "aqi": aqi,
            "components": components,
            "levels": levels,
            "dominantPollutant": dominant,
            "pollutionSource": source
        }