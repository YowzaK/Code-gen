from fastapi import FastAPI
from app.api.spec import router as spec_router

app= FastAPI(
    title="Code-Gen AI native development Pipeline",
    version= "0.0.1"
)

app.include_router(
    spec_router,
    prefix="/spec",
    tags=["Specification"],
)

@app.get("/")
async def root():
    return{
        "Message" : "AI native development running"
    }