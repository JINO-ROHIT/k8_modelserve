import logging
import os
import sys
import time
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pymongo import MongoClient
import joblib

from schemas import InputData


load_dotenv()

logging.basicConfig(level=logging.INFO)

models_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'model')
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(models_path)

model = None
mongo_client = None
job_statuses_collection = None

app = FastAPI()

mongo_username = os.environ['MONGO_DB_USER']
mongo_password = os.environ['MONGO_DB_USER']

#print(mongo_username, mongo_password)

@app.on_event("startup")
async def startup_event():
    global model, mongo_client, job_statuses_collection
    model = joblib.load(f"{models_path}/ada_classifier.pkl")
    logging.info("The model has been initialized")

    mongo_client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@mymongo:27017")
    job_statuses_collection = mongo_client["predictions_db"]["job_statuses"]
    logging.info("The database connection is succesful")

def generate_job_id():
    return str(uuid.uuid4())

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    result = job_statuses_collection.find_one({"job_id": job_id}, {"_id": 0})
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return result

def inference(job_id: str, input_data: InputData, start_time: time):
    try:
        prediction = model.predict([[input_data.Age, input_data.Sex, input_data.ChestPainType, input_data.RestingBP, input_data.Cholesterol, 
                                    input_data.FastingBS, input_data.RestingECG, input_data.MaxHR, input_data.ExerciseAngina, input_data.Oldpeak, input_data.ST_Slope]])
        
        elapsed_time = time.time() - start_time

        logging.info(f"The model prediction for job {job_id} is {prediction}. Time taken: {elapsed_time} seconds")
        job_statuses_collection.insert_one({
            "job_id": job_id,
            "prediction": str(prediction[0]),
            "elapsed_time": str(elapsed_time)
        })
    except Exception as e:
        logging.error(f"Error in inference for job {job_id}: {e}")

@app.post("/predict")
async def predict(input_data: InputData, background_tasks: BackgroundTasks):
    job_id = generate_job_id()
    start_time = time.time()
    background_tasks.add_task(inference, job_id, input_data, start_time)
    return {"status": "pending", "job_id": job_id}
