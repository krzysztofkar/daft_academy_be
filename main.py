from fastapi import FastAPI

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
