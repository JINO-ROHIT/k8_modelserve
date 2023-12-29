# Model deployment using FASTAPI and local kubernetes

## Overview
This project demonstrates the deployment of a Scikit-learn model in Kubernetes using FastAPI as the backend. The API supports asynchronous processing, allowing concurrent users to effectively utilize its capabilities. The API behaves as a job queue, enabling efficient handling of multiple requests. After the job is done, results are written to a MongoDB database, and they can be retrieved later using the unique job ID.

## Getting Started

1. Start Minikube:

   ```bash
   minikube start --memory 4096
   ```
2. Deploy the fastapi application and mongodb database.

   ```bash
   kubectl apply -f fastapi_heart.yaml -f mongodb.yaml
   ```
4. Check the pods created.

   ```bash
   kubectl get pods
   ```
6. Check the service created.

   ```bash
   kubectl get svc
   ```
8. Access the FastAPI application.

   ```bash
   minikube service <service_name>
   ```

## Usage
1. You can use the FASTAPI Swagger to test the /predict and the /result endpoint.
2. Use curl to send a post request.
   - ```curl
     curl -X 'POST' \
     'http://127.0.0.1:63736/predict' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
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
     }```

  Server response will be something like this:
  ```json 
  {
  "status": "pending",
  "job_id": "<job_id>"
  }
  ```

  Now use the job id to the /result endpoint
  ```curl
   - curl -X 'GET' \
  'http://127.0.0.1:63736/result/7aec3773-4c22-4ac1-86ba-765af81f39f4' \
  -H 'accept: application/json'
  ```

  Sever response will be something like this:
  ```json
  {
  "job_id": "<job_id>",
  "prediction": "1",
  "elapsed_time": "0.059065818786621094"
 }
 ```
  
