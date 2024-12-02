from fastapi import FastAPI
import uvicorn
from lawbot import router as lawgpt_router
from predict_pipeline import router as bail_reckoner_router
from fir_pdf_gen import router as fir_router

app = FastAPI()

# Include routers with distinct prefixes
app.include_router(lawgpt_router, prefix="/lawgpt", tags=["LawGPT"])
app.include_router(bail_reckoner_router, prefix="/bail-reckoner", tags=["Bail Reckoner"])
app.include_router(fir_router, prefix="/generate-fir", tags=["Generate FIR"])

@app.get("/")
async def root():
    return {
        "message": "API Gateway is running",
        "routes": ["/lawgpt", "/bail-reckoner", "/generate-fir"]
    }
