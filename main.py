from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/method")
def method():
    return {"method": "GET"}


@app.post("/method")
def method():
    return {"method": "POST"}


@app.put("/method")
def method():
    return {"method": "PUT"}


@app.delete("/method")
def method():
    return {"method": "DELETE"}


class Patient(BaseModel):
    name: str
    surename: str


requests_count = 0
patients = {}


@app.post("/patient")
def patient(patient: Patient):
    global requests_count
    requests_count += 1
    try:
        global patients
        patient = patients[requests_count]
    except KeyError:
        patients[requests_count] = patient
    return {"id": requests_count, "patient": patient}


@app.get("/patient/{pk}")
def patient(pk):
    try:
        global patients
        patient = patients[int(pk)]
    except KeyError:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
