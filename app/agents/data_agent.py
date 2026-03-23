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

        if "list" not in data:
            raise Exception(f"AQI API failed: {data}")

        return data["list"][0]["main"]["aqi"]   
    
    def normalize_aqi(self, aqi):

        mapping = {
            1: random.randint(20, 50),
            2: random.randint(50, 100),
            3: random.randint(100, 150),
            4: random.randint(150, 200),
            5: random.randint(200, 300)
        }

        return mapping.get(aqi, 100)
    
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

        raw_aqi = self.get_aqi(weather["lat"], weather["lon"])
        aqi = self.normalize_aqi(raw_aqi)

        return {
            "city": city,
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "aqi": aqi
        }