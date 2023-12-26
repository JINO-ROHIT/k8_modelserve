from fastapi import FastAPI, BackgroundTasks, HTTPException
import joblib
from fastapi.responses import JSONResponse
import uuid
import time 

import logging
logging.basicConfig(level=logging.INFO)

import os
import sys
models_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'model')
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(models_path)

from schemas import InputData

model = None

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global model
    model = joblib.load(f"{models_path}/ada_classifier.pkl")


def generate_job_id():
    return str(uuid.uuid4())

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    if job_id not in job_statuses:
        raise HTTPException(status_code=404, detail="Job not found")
    #logging.info(job_statuses[job_id])
    return job_statuses[job_id]


job_statuses = {}

def inference(job_id: str, input_data: InputData, start_time: time):
    try:
        prediction = model.predict([[input_data.Age, input_data.Sex, input_data.ChestPainType, input_data.RestingBP, input_data.Cholesterol, 
                                    input_data.FastingBS, input_data.RestingECG, input_data.MaxHR, input_data.ExerciseAngina, input_data.Oldpeak, input_data.ST_Slope]])
        
        elapsed_time = time.time() - start_time

        logging.info(f"The model prediction for job {job_id} is {prediction}. Time taken: {elapsed_time} seconds")
        job_statuses[job_id] = {"prediction": str(prediction[0]), "elapsed_time": str(elapsed_time)}
    except Exception as e:
        logging.error(f"Error in inference for job {job_id}: {e}")
        job_statuses[job_id] = {"error": str(e)}


@app.post("/predict")
async def predict(input_data: InputData, background_tasks: BackgroundTasks):
    job_id = generate_job_id()
    start_time = time.time()
    background_tasks.add_task(inference, job_id, input_data, start_time)
    return {"status": "pending", "job_id": job_id}
