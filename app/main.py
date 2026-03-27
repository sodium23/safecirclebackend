from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "alive"}

@app.get("/health")
def health():
    return {"status": "ok"}
