from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import sensors, farms, recommendations, alerts

app = FastAPI(
    title="Tomchi Tech API",
    description="IoT suv tejash platformasi — backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensors.router,         prefix="/api/v1/sensors",         tags=["Sensors"])
app.include_router(farms.router,           prefix="/api/v1/farms",           tags=["Farms"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["AI"])
app.include_router(alerts.router,          prefix="/api/v1/alerts",          tags=["Alerts"])

@app.get("/")
def root():
    return {"status": "ok", "service": "Tomchi Tech API v0.1"}

@app.get("/health")
def health():
    return {"status": "healthy"}
