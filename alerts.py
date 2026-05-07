from fastapi import APIRouter
from datetime import datetime
from app.services.simulator import SENSOR_CONFIGS, generate_reading

router = APIRouter()

@router.get("/", summary="Faol ogohlantirishlar")
def get_alerts():
    alerts = []
    for cfg in SENSOR_CONFIGS:
        reading = generate_reading(cfg.sensor_id)
        if reading.battery_level < 20:
            alerts.append({
                "type": "LOW_BATTERY", "severity": "warning",
                "sensor_id": cfg.sensor_id, "farm_id": cfg.farm_id,
                "message": f"Batareya past: {reading.battery_level:.0f}%",
                "value": reading.battery_level, "at": datetime.utcnow(),
            })
        if cfg.status.value == "offline":
            alerts.append({
                "type": "SENSOR_OFFLINE", "severity": "error",
                "sensor_id": cfg.sensor_id, "farm_id": cfg.farm_id,
                "message": "Sensor aloqasi uzilgan",
                "value": None, "at": datetime.utcnow(),
            })
        if reading.soil_moisture < cfg.irrigation_threshold - 15:
            alerts.append({
                "type": "CRITICAL_DRY", "severity": "critical",
                "sensor_id": cfg.sensor_id, "farm_id": cfg.farm_id,
                "message": f"Tuproq juda quruq: {reading.soil_moisture:.1f}%",
                "value": reading.soil_moisture, "at": datetime.utcnow(),
            })
    return {"count": len(alerts), "alerts": alerts}
