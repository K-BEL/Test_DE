from fastapi import FastAPI, HTTPException
#rom pyravendb.store import DocumentStore
#from pyravendb import DocumentStore
from ravendb import DocumentStore

app = FastAPI()

# Configure the RavenDB connection
document_store = DocumentStore(urls=["http://live-test.ravendb.net"], database="DSITE1")
document_store.initialize()

class JsonData(dict):
    pass

@app.get("/json_data/{data_id}", response_model=JsonData)
def read_json_data(data_id: str):
    with document_store.open_session() as session:
        json_data = session.load(data_id)
        if not json_data:
            raise HTTPException(status_code=404, detail="JSON data not found")
        return json_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

