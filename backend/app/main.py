from fastapi import FastAPI

app= FastAPI(
    title="Code-Gen AI native development Pipeline",
    version= "0.0.1"
)

@app.get("/")
async def root():
    return{
        "Message" : "AI native development running"
    }