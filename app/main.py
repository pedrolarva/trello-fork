from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(title="Luizalabs Address Discovery API")

app.include_router(api_router, prefix="/addresses", tags=["addresses"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
