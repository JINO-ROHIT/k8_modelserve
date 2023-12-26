import requests
import  concurrent.futures

def send_request(concurrent_requests):
    url = "http://localhost:8000/predict"
    input_data = {
        "Age": 0,
        "Sex": 0,
        "ChestPainType": 0,
        "RestingBP": 0,
        "Cholesterol": 0,
        "FastingBS": 0,
        "RestingECG": 0,
        "MaxHR": 0,
        "ExerciseAngina": 0,
        "Oldpeak": 0,
        "ST_Slope": 0
    }

    response = requests.post(url, json=input_data)
    #print(response.json())
    return response.json(), response.elapsed.total_seconds()


concurrent_requests = 10
responses = []

with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
    for _, result in executor.map(send_request, range(concurrent_requests)):
        responses.append(result)

print(responses)