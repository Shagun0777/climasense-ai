import json
import time
from datetime import datetime
import os

class MemoryAgent:
    def __init__(self):
        self.file_path = "memory.json"

        # create file if not exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    def load_memory(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def save_memory(self, memory):
        with open(self.file_path, "w") as f:
            json.dump(memory, f, indent=2)

    def update(self, city, data):
        memory = self.load_memory()

        if city not in memory:
            memory[city] = []

        memory[city].append({
            "aqi": data["aqi"],
            "temperature": data["temperature"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # keep only last 5 records
        memory[city] = memory[city][-5:]

        self.save_memory(memory)

        return memory[city]

    def analyze_trend(self, city):
        memory = self.load_memory()

        if city not in memory or len(memory[city]) < 2:
            return "Not enough data for trend"

        last = memory[city][-1]
        prev = memory[city][-2]

        if last["aqi"] > prev["aqi"]:
            return "Air quality is worsening 📉"
        elif last["aqi"] < prev["aqi"]:
            return "Air quality is improving 📈"
        else:
            return "Air quality is stable"
        
    def get_average_aqi(self, city):
        memory = self.load_memory()

        if city not in memory or not memory[city]:
            return None

        values = [entry["aqi"] for entry in memory[city]]
        return sum(values) / len(values)


    def get_aqi_delta(self, city):
        memory = self.load_memory()

        if city not in memory or len(memory[city]) < 2:
            return None

        latest = memory[city][-1]["aqi"]
        prev = memory[city][-2]["aqi"]

        return latest - prev       