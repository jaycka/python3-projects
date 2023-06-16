import os
import requests
from datetime import datetime

nutrition_api_id = os.environ.get('nutrition_api_id')
nutrition_api_key = os.environ.get('nutrition_api_key')
nutrition_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
sheety_endpoint = 'https://api.sheety.co/b3393adeed7a4f8ca1a28f884370e59e/workoutTracking/workouts'
# today = datetime.today().strftime('%Y-%m-%d')
# now = datetime.now().strftime('%H:%M:%S')

exercise_text = input("Tell me which exercises you did: ")
nutrition_params = {
    'query': exercise_text,
    'gender': 'male',
    'weight_kg': 90,
    'height_cm': 185,
    'age': 33
}
nutrition_headers = {
    'x-app-id': nutrition_api_id,
    'x-app-key': nutrition_api_key
}

response = requests.post(url=nutrition_endpoint, json=nutrition_params, headers=nutrition_headers)
response.raise_for_status()

sheety_headers = {
    'Authorization': "Bearer " + os.environ.get('sheety_token')
}
for i in response.json()['exercises']:
    sheety_params = {
        'workout': {
            'date': datetime.today().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%X'),
            'exercise': i['name'].title(),
            'duration': i['duration_min'],
            'calories': i['nf_calories']
        }
    }
    sheety_response = requests.post(url=sheety_endpoint, json=sheety_params, headers=sheety_headers)
    sheety_response.raise_for_status()
