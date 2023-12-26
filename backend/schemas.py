from pydantic import BaseModel

class InputData(BaseModel):
    Age: float
    Sex: float
    ChestPainType: float
    RestingBP: float
    Cholesterol: float
    FastingBS: float
    RestingECG: float
    MaxHR: float
    ExerciseAngina: float
    Oldpeak: float
    ST_Slope: float