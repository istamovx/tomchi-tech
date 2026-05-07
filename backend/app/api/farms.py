from fastapi import APIRouter, HTTPException
from typing import List
from app.services.simulator import FARMS, get_farm, SENSOR_CONFIGS
from app.models.sensor import Farm

router = APIRouter()


@router.get("/", response_model=List[Farm], summary="Barcha fermalar ro'yxati")
def list_farms():
    return FARMS


@router.get("/{farm_id}", response_model=Farm, summary="Bitta ferma ma'lumoti")
def get_farm_by_id(farm_id: str):
    farm = get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Ferma {farm_id} topilmadi")
    return farm


@router.get("/{farm_id}/sensors", summary="Ferma sensorlari")
def get_farm_sensors(farm_id: str):
    farm = get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Ferma {farm_id} topilmadi")
    sensors = [cfg for cfg in SENSOR_CONFIGS if cfg.farm_id == farm_id]
    return {
        "farm_id": farm_id,
        "farmer_name": farm.farmer_name,
        "sensor_count": len(sensors),
        "sensors": sensors,
    }


@router.get("/{farm_id}/summary", summary="Ferma umumiy holati")
def get_farm_summary(farm_id: str):
    from app.services.simulator import generate_reading
    farm = get_farm(farm_id)
    if not farm:
        raise HTTPException(status_code=404, detail=f"Ferma {farm_id} topilmadi")
    sensors = [cfg for cfg in SENSOR_CONFIGS if cfg.farm_id == farm_id]
    readings = [generate_reading(cfg.sensor_id) for cfg in sensors]
    avg_moisture = round(sum(r.soil_moisture for r in readings) / len(readings), 1) if readings else 0
    return {
        "farm_id": farm_id,
        "farmer_name": farm.farmer_name,
        "region": farm.region,
        "district": farm.district,
        "total_area_ha": farm.total_area_ha,
        "crop_type": farm.crop_type,
        "sensor_count": len(sensors),
        "avg_soil_moisture": avg_moisture,
        "needs_irrigation": any(
            r.soil_moisture < cfg.irrigation_threshold
            for r, cfg in zip(readings, sensors)
        ),
    }
