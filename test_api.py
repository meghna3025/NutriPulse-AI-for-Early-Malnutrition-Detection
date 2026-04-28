import requests
import json

url = "http://localhost:8000/analyze"
data = {
    "user_category": "Pregnant",
    "protein_intake_frequency": "Rarely",
    "daily_food_habits": "Low-calorie, skip breakfast",
    "symptoms": ["Fatigue", "Pale skin"],
    "meal_frequency": 2,
    "food_diversity_quality": "Low"
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
