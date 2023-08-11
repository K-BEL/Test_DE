#rom pyravendb.store import DocumentStore
#from pyravendb import DocumentStore
from ravendb import DocumentStore
import json

# Configure the RavenDB connection
document_store = DocumentStore(urls=["http://live-test.ravendb.net"], database="DSITE1")
document_store.initialize()

# Load the JSON data from the local file
with open(r"C:\Users\LENOVO\Desktop\Test_DE\Section_2\Saves\site1.json", "r") as json_file:
    json_data = json.load(json_file)

# Store the JSON data in RavenDB
with document_store.open_session() as session:
    for data in json_data:
        session.store(data)
    session.save_changes()

# Close the document store
document_store.close()
