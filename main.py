from fastapi import FastAPI
import uvicorn
from app import router as lawgpt_router
from predict_pipeline import router as bail_reckoner_router

app = FastAPI()

# Include both routers with distinct prefixes
app.include_router(lawgpt_router, prefix="/lawgpt", tags=["LawGPT"])
app.include_router(bail_reckoner_router, prefix="/bail-reckoner", tags=["Bail Reckoner"])

@app.get("/")
async def root():
    return {
        "message": "API Gateway is running",
        "routes": ["/lawgpt", "/bail-reckoner"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
