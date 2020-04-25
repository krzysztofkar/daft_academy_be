from hashlib import sha256

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI()
app.secret_key = "ba217dd867bf9b31ca568c533cc0ecacb3c2d9e12d94cfca8731abc593eda237"


@app.get("/")
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome():
    return {"message": "Hello"}


@app.post("/login")
def login(login: str, password: str, response: Response):
    cred = sha256(bytes(f"trudnYPaC13Nt{app.secret_key}", encoding="utf8")).hexdigest()
    session_token = sha256(
        bytes(f"{login}{password}{app.secret_key}", encoding="UTF-8")
    ).hexdigest()

    response.set_cookie(key="session_token", value=session_token)
    if session_token != cred:
        raise HTTPException(status_code=401, detail="Unauthorised")
    return RedirectResponse("/welcome")


@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}


class Patient(BaseModel):
    name: str
    surename: str


requests_count = -1
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
        raise HTTPException(status_code=204, detail="No content")
    return patient
