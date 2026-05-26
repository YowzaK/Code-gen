from fastapi import FastAPI
from app.api.spec import router as spec_router
from app.api.pipeline import router as pipeline_router
from app.core.database import create_db_and_tables

app= FastAPI(
    title="Code-Gen AI native development Pipeline",
    version= "0.0.1"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(
    spec_router,
    prefix="/spec",
    tags=["Specification"],
)

app.include_router(
    pipeline_router,
    prefix="/pipeline",
    tags=["Pipeline"]
)

@app.get("/")
async def root():
    return{
        "Message" : "AI native development running"
    }