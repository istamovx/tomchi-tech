from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.simulator import generate_reading, get_sensor_config, CROP_PROFILES
from app.models.sensor import CropType

router = APIRouter()

# Ekin uchun optimal namlik diapazoni
OPTIMAL_MOISTURE: dict[CropType, tuple[float, float]] = {
    CropType.TOMATO:  (60, 80),
    CropType.POTATO:  (65, 80),
    CropType.COTTON:  (40, 60),
    CropType.GRAPE:   (45, 65),
    CropType.WHEAT:   (55, 75),
    CropType.CORN:    (50, 70),
    CropType.ONION:   (55, 70),
}


@router.get("/{sensor_id}", summary="Sensor uchun sug'orish tavsiyasi")
def get_recommendation(sensor_id: str):
    cfg = get_sensor_config(sensor_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Sensor topilmadi")

    reading = generate_reading(sensor_id)
    opt_min, opt_max = OPTIMAL_MOISTURE.get(cfg.crop_type, (45, 70))
    moisture = reading.soil_moisture
    profile = CROP_PROFILES.get(cfg.crop_type, {})

    # Tavsiya hisoblash
    if moisture < opt_min - 10:
        action = "IRRIGATE_NOW"
        urgency = "yuqori"
        water_needed_l = round((opt_min - moisture) / 100 * cfg.field_area_ha * 10_000 * 0.3, 0)
        message = f"Tuproq namligi juda past ({moisture}%). Darhol sug'orish zarur."
    elif moisture < opt_min:
        action = "IRRIGATE_SOON"
        urgency = "o'rta"
        water_needed_l = round((opt_min - moisture) / 100 * cfg.field_area_ha * 10_000 * 0.2, 0)
        message = f"Namlik pasaymoqda ({moisture}%). 4-6 soat ichida sug'orish tavsiya etiladi."
    elif moisture > opt_max:
        action = "STOP_IRRIGATION"
        urgency = "past"
        water_needed_l = 0
        message = f"Namlik yuqori ({moisture}%). Sug'orishni to'xtatish kerak."
    else:
        action = "NO_ACTION"
        urgency = "yo'q"
        water_needed_l = 0
        message = f"Namlik maqbul darajada ({moisture}%). Hech qanday harakat shart emas."

    # Suv tejash hisob (an'anaviy ariq vs bizning tizim)
    # An'anaviy usul har doim 6000 L/ha sarflaydi.
    # Bizning tizim 0 L sarflasa → 100% tejash, None emas.
    traditional_l = round(cfg.field_area_ha * 6_000, 0)
    our_l = water_needed_l
    if traditional_l > 0:
        saving_pct = round((1 - our_l / traditional_l) * 100, 1)
        # Agar our_l > traditional_l bo'lsa, tejash manfiy — cheklaymiz
        saving_pct = max(saving_pct, -999.0)
    else:
        saving_pct = 0.0

    return {
        "sensor_id": sensor_id,
        "farm_id": cfg.farm_id,
        "crop_type": cfg.crop_type,
        "generated_at": datetime.utcnow(),
        "current_moisture": moisture,
        "optimal_range": {"min": opt_min, "max": opt_max},
        "action": action,
        "urgency": urgency,
        "message": message,
        "water_needed_liters": water_needed_l,
        "traditional_method_liters": traditional_l,
        "water_saving_pct": saving_pct,
        "temperature_c": reading.temperature,
        "humidity_pct": reading.humidity,
    }


@router.get("/", summary="Barcha sensorlar uchun tavsiyalar")
def get_all_recommendations():
    from app.services.simulator import SENSOR_CONFIGS
    return [get_recommendation(cfg.sensor_id) for cfg in SENSOR_CONFIGS]
