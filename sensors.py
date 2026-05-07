from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from app.services.simulator import (
    generate_all_readings, generate_reading,
    generate_history, SENSOR_CONFIGS, get_sensor_config,
)
from app.models.sensor import SensorReading, SensorConfig

router = APIRouter()


@router.get("/", response_model=List[SensorReading], summary="Barcha sensorlar hozirgi holati")
def list_all_sensors():
    return generate_all_readings()


@router.get("/configs", response_model=List[SensorConfig], summary="Sensor konfiguratsiyalari")
def list_configs():
    return SENSOR_CONFIGS


@router.get("/{sensor_id}", response_model=SensorReading, summary="Bitta sensor hozirgi o'qishi")
def get_sensor(sensor_id: str):
    cfg = get_sensor_config(sensor_id)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} topilmadi")
    return generate_reading(sensor_id)


@router.get("/{sensor_id}/history", response_model=List[SensorReading], summary="Sensor tarixi")
def get_sensor_history(
    sensor_id: str,
    hours: int = Query(default=24, ge=1, le=168, description="Necha soat tarixi"),
):
    cfg = get_sensor_config(sensor_id)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} topilmadi")
    return generate_history(sensor_id, hours=hours)


@router.get("/{sensor_id}/status", summary="Sensor holati xulosa")
def get_sensor_status(sensor_id: str):
    cfg = get_sensor_config(sensor_id)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Sensor {sensor_id} topilmadi")
    reading = generate_reading(sensor_id)
    needs_irrigation = reading.soil_moisture < cfg.irrigation_threshold
    return {
        "sensor_id": sensor_id,
        "farm_id": cfg.farm_id,
        "status": cfg.status,
        "soil_moisture": reading.soil_moisture,
        "threshold": cfg.irrigation_threshold,
        "needs_irrigation": needs_irrigation,
        "battery_level": reading.battery_level,
        "last_updated": reading.timestamp,
        "alert": "LOW_BATTERY" if reading.battery_level < 20 else None,
    }
