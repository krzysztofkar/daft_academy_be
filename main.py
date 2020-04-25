import secrets
from hashlib import sha256

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()
app.secret_key = "ba217dd867bf9b31ca568c533cc0ecacb3c2d9e12d94cfca8731abc593eda237"

security = HTTPBasic()


@app.get("/")
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome():
    return {"message": "Hello"}


def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": credentials.username, "password": credentials.password}


@app.post("/login")
def login(response: Response, user: str = Depends(read_current_user)):
    session_token = sha256(
        bytes(f"{user['username']}{user['password']}{app.secret_key}", encoding="utf8")
    ).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
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
def patient(patient: Patient, user: str = Depends(read_current_user)):
    global requests_count
    requests_count += 1
    try:
        global patients
        patient = patients[requests_count]
    except KeyError:
        patients[requests_count] = patient
    return {"id": requests_count, "patient": patient}


@app.get("/patient/{pk}")
def patient(pk, user: str = Depends(read_current_user)):
    try:
        global patients
        patient = patients[int(pk)]
    except KeyError:
        raise HTTPException(status_code=204, detail="No content")
    return patient
