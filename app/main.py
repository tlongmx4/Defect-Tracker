from fastapi import FastAPI
from app.api.routes.defects import router as defects
from app.db.session import engine
from app.db.base import Base
from app.db import models

app = FastAPI(title="Defect Tracker API")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Defect Tracker API!"}

@app.get("/health")
def health_check():
    return {"status": "db ok"}

app.include_router(defects, prefix="/api")

