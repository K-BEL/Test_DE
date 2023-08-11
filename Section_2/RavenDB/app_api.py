from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyravendb.store import document_store
import json

app = FastAPI()

# Configure the RavenDB connection
document_store.configure(
    "YOUR_RAVENDB_URL",
    database="SITE1",
    cert_file=None,  # If using secure connection
    #api_key=("YOUR_API_KEY", "YOUR_API_SECRET")  # If using API key authentication
)

# Define a Pydantic model for the JSON data
class UserData(BaseModel):
    date: str
    time: str
    title1: str
    intro: str
    title2: str
    Taux: str
    Plafond: str
    Calcul_des_interets: str
    Interets_soumis_a_imposition: str
    Depot_initial: str
    Disponibilite: str
    Gestion_en_ligne: str
    Versement_en_ligne: str
    Conditions: str
    Mentions_legales: str

# Route to import JSON data into RavenDB
@app.post("/import_data")
def import_data():
    with open(r"C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site1.json", "r") as json_file:
        json_data = json.load(json_file)
        for item in json_data:
            user_data = UserData(**item)
            # Transform UserData into a dictionary to store in RavenDB
            raven_doc = user_data.dict()

            # Store the RavenDB document
            with document_store.open_session() as session:
                session.store(raven_doc)
                session.save_changes()

            return {"message": "Data imported successfully"}

# Route to retrieve JSON data from RavenDB
@app.get("/users/{user_id}", response_model=UserData)
def get_user(user_id: str):
    with document_store.open_session() as session:
        user_data = session.load(user_id)
        if user_data:
            return user_data
        else:
            raise HTTPException(status_code=404, detail="User not found")

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
