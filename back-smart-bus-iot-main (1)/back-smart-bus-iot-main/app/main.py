from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, sensor_routes
from app.core.database import init_db
#from app.utils.scheduler import start_scheduler
from app.core.config import settings
import uvicorn
import logging

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🚌 Smart Bus Stop API",
    description="API para monitoramento de temperatura, umidade e ônibus",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar DB
init_db()

# Rotas
app.include_router(auth_routes.router, prefix="/api")
app.include_router(sensor_routes.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Smart Bus Stop API 🚌"}

# @app.on_event("startup")
# async def startup_event():
#     start_scheduler()  # agora roda dentro do loop do FastAPI

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

