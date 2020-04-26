import secrets
from hashlib import sha256

from fastapi import Cookie, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.secret_key = "ba217dd867bf9b31ca568c533cc0ecacb3c2d9e12d94cfca8731abc593eda237"
security = HTTPBasic()
app.sessions = {}


def get_token(user):
    return sha256(
        bytes(f"{user['username']}{user['password']}{app.secret_key}", encoding="utf8")
    ).hexdigest()


@app.get("/")
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


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


def check_token(
    token: str = Cookie(None), user: str = Depends(read_current_user),
):
    token = get_token(user)
    if token not in app.sessions:
        token = None
    return token


@app.get("/welcome")
def welcome(request: Request, token: str = Depends(check_token)):
    if token not in app.sessions:
        raise HTTPException(status_code=401, detail="Unauthorised")
    return templates.TemplateResponse(
        "greeting.html", {"request": request, "user": app.sessions[token]}
    )


@app.post("/login")
def login(response: Response, user: str = Depends(read_current_user)):
    session_token = get_token(user)
    app.sessions[session_token] = user["username"]
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"
    response.set_cookie(key="session_token", value=session_token)


@app.get("/logout")
def logout(
    req: Request, response: Response, token: str = Depends(check_token),
):
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/"
    app.sessions.pop(token)


@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}


class Patient(BaseModel):
    name: str
    surname: str


requests_count = 0
patients = {}


@app.api_route(path="/patient", methods=["GET", "POST"])
def patient(request: Request, patient: Patient = {}, token: str = Depends(check_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    if request.method == "POST":
        global requests_count
        requests_count += 1
        try:
            global patients
            patient = patients[requests_count]
        except KeyError:
            patients[requests_count] = patient
        return RedirectResponse(f"patient/{requests_count}")
    return patients


@app.api_route(path="/patient/{id}", methods=["GET", "DELETE"])
def patient_id(id, request: Request, token: str = Depends(check_token)):
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorised")
    try:
        global patients
        patient = patients[int(id)]
    except KeyError:
        raise HTTPException(status_code=204, detail="No content")
    if request.method == "GET":
        return patient
    del patients[int(id)]
    return Response(status_code=307)
