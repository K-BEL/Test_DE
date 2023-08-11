import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

# Simulated API key for authentication
API_KEY = "PASS123"
api_key_header = APIKeyHeader(name="X-API-Key")

def authenticate(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

class DataResponse(BaseModel):
    data: dict

def load_json(json_path):
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
        return json_data

@app.get("/")
def read_root():
    return {"message": "Welcome to the JSON Data API!"}

@app.get("/data_sets", response_model=List[str])
def get_data_sets():
    return ["site1", "site2", "site3"]

@app.get("/data_sets/{data_set}", response_model=DataResponse)
def get_data(data_set: str, auth: None = Depends(authenticate)):
    if data_set == "site1":
        json_path = r"C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site1.json"
    elif data_set == "site2":
        json_path = r"C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site2.json"
    elif data_set == "site3":
        json_path = r"C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site3.json"
    else:
        raise HTTPException(status_code=404, detail="Data set not found")

    json_data = load_json(json_path)
    return DataResponse(data=json_data)

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
