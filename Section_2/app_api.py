import json
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

# Simulated API key for authentication
API_KEY = "PASS123"
api_key_header = APIKeyHeader(name="X-API-Key")

def authenticate(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Define your site paths
site_paths = [
    r'C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site1.json',
    r'C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site2.json',
    r'C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site3.json'
]

# Model to validate the request body
class RequestInfo(BaseModel):
    site_key: int  # Assuming site_key will be an index (1, 2, 3) to select the site
    data: dict  # You can adjust the data structure based on your needs

# POST endpoint to post JSON and select a site
@app.post("/postJSON")
async def post_json(info: RequestInfo, authorized: bool = Depends(authenticate)):
    selected_site_index = info.site_key - 1
    if 0 <= selected_site_index < len(site_paths):
        selected_site_path = site_paths[selected_site_index]
        # Write the posted JSON data to the selected site file
        with open(selected_site_path, 'w') as site_file:
            json.dump(info.data, site_file)
            return {
                "status": "SUCCESS",
                "message": f"JSON data posted to site {info.site_key}"
            }
    else:
        raise HTTPException(status_code=404, detail="Site not found")
    

# GET endpoint to visualize JSON data of a specific site
@app.get("/postJSON/visualize/{site_key}")
async def visualize_data(site_key: int, authorized: bool = Depends(authenticate)):
    selected_site_index = site_key - 1
    if 0 <= selected_site_index < len(site_paths):
        selected_site_path = site_paths[selected_site_index]
        try:
            with open(selected_site_path, 'r') as site_file:
                site_data = json.load(site_file)
                return JSONResponse(content=site_data, status_code=200)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
    else:
        raise HTTPException(status_code=404, detail="Site not found")
