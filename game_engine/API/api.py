from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/matador/start")
def read_item():
    return {"text": "Matador started!"}