from fastapi import FastAPI
from app.db.session import SessionLocal

app = FastAPI(title="Defect Tracker API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Defect Tracker API!"}

@app.get("/health")
def health_check():
    return {"status": "db ok"}