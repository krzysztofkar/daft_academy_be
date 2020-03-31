from fastapi import FastAPI, Cookie
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
    surname: str


requests_count = 0


@app.post("/patient")
def patient(patient: Patient):
    global requests_count
    requests_count += 1
    return {"id": requests_count, "patient": patient}
