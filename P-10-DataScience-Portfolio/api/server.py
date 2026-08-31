from fastapi import FastAPI
from pydantic import BaseModel
import joblib, pandas as pd

app = FastAPI(title='Housing API')

class Req(BaseModel):
    rooms: int
    area: float
    location: str

loc_map = {'Rural':0,'Suburban':1,'Urban':2}

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/predict')
def predict(r: Req):
    model = joblib.load('model/trained_model.pkl')
    loc = loc_map.get(r.location,0)
    X = pd.DataFrame([[r.rooms, r.area, loc]], columns=['Rooms','Area','Location_code'])
    pred = model.predict(X)[0]
    return {'predicted_price': float(pred)}
