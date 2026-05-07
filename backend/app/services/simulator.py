"""
Soxta sensor simulyatori — 6 ta sensor, O'zbekiston sharoiti
Haqiqiy sensorlar o'rnatilguncha shu modul ishlatiladi.
"""

import random
import math
from datetime import datetime, timedelta
from typing import List, Dict
from app.models.sensor import SensorReading, SensorConfig, Farm, CropType, SensorStatus


# ─── 6 ta ferma ta'rifi ───────────────────────────────────────────────────────
FARMS: List[Farm] = [
    Farm(farm_id="F001", farmer_name="Akbar Toshmatov", phone="+998901234567",
         region="Toshkent", district="Qibray", total_area_ha=3.5, crop_type=CropType.TOMATO, sensor_count=1),
    Farm(farm_id="F002", farmer_name="Muhabbat Yusupova", phone="+998901234568",
         region="Toshkent", district="Bo'stonliq", total_area_ha=2.0, crop_type=CropType.POTATO, sensor_count=1),
    Farm(farm_id="F003", farmer_name="Sherzod Raximov", phone="+998901234569",
         region="Sirdaryo", district="Guliston", total_area_ha=8.0, crop_type=CropType.COTTON, sensor_count=1),
    Farm(farm_id="F004", farmer_name="Nodira Xasanova", phone="+998901234570",
         region="Farg'ona", district="Marg'ilon", total_area_ha=1.5, crop_type=CropType.GRAPE, sensor_count=1),
    Farm(farm_id="F005", farmer_name="Behruz Mirzayev", phone="+998901234571",
         region="Samarqand", district="Urgut", total_area_ha=5.0, crop_type=CropType.WHEAT, sensor_count=1),
    Farm(farm_id="F006", farmer_name="Zulfiya Qodirov", phone="+998901234572",
         region="Namangan", district="Chortoq", total_area_ha=4.0, crop_type=CropType.CORN, sensor_count=1),
]

# ─── Sensor konfiguratsiyalari ────────────────────────────────────────────────
SENSOR_CONFIGS: List[SensorConfig] = [
    SensorConfig(sensor_id="S001", farm_id="F001", location_lat=41.2995, location_lon=69.6200,
                 field_area_ha=3.5, crop_type=CropType.TOMATO, irrigation_threshold=45.0,
                 status=SensorStatus.ONLINE, installed_at=datetime(2025, 3, 1)),
    SensorConfig(sensor_id="S002", farm_id="F002", location_lat=41.5320, location_lon=69.6720,
                 field_area_ha=2.0, crop_type=CropType.POTATO, irrigation_threshold=50.0,
                 status=SensorStatus.ONLINE, installed_at=datetime(2025, 3, 5)),
    SensorConfig(sensor_id="S003", farm_id="F003", location_lat=40.4886, location_lon=68.7738,
                 field_area_ha=8.0, crop_type=CropType.COTTON, irrigation_threshold=35.0,
                 status=SensorStatus.WARNING, installed_at=datetime(2025, 3, 10)),
    SensorConfig(sensor_id="S004", farm_id="F004", location_lat=40.4621, location_lon=71.7243,
                 field_area_ha=1.5, crop_type=CropType.GRAPE, irrigation_threshold=40.0,
                 status=SensorStatus.ONLINE, installed_at=datetime(2025, 3, 15)),
    SensorConfig(sensor_id="S005", farm_id="F005", location_lat=39.6270, location_lon=66.9749,
                 field_area_ha=5.0, crop_type=CropType.WHEAT, irrigation_threshold=55.0,
                 status=SensorStatus.ONLINE, installed_at=datetime(2025, 3, 20)),
    SensorConfig(sensor_id="S006", farm_id="F006", location_lat=41.0994, location_lon=71.0932,
                 field_area_ha=4.0, crop_type=CropType.CORN, irrigation_threshold=42.0,
                 status=SensorStatus.OFFLINE, installed_at=datetime(2025, 4, 1)),
]

# ─── Ekin bazaviy parametrlari ────────────────────────────────────────────────
CROP_PROFILES: Dict[CropType, Dict] = {
    CropType.TOMATO:   {"base_moisture": 65, "temp_preference": 25, "water_sensitivity": 1.2},
    CropType.POTATO:   {"base_moisture": 70, "temp_preference": 18, "water_sensitivity": 1.0},
    CropType.COTTON:   {"base_moisture": 45, "temp_preference": 30, "water_sensitivity": 0.7},
    CropType.GRAPE:    {"base_moisture": 50, "temp_preference": 22, "water_sensitivity": 0.8},
    CropType.WHEAT:    {"base_moisture": 60, "temp_preference": 20, "water_sensitivity": 0.9},
    CropType.CORN:     {"base_moisture": 55, "temp_preference": 27, "water_sensitivity": 1.1},
    CropType.ONION:    {"base_moisture": 60, "temp_preference": 20, "water_sensitivity": 1.0},
}


def _diurnal(hour: int, amplitude: float, peak_hour: int = 14) -> float:
    """Kunlik sinusoidal o'zgarish (harorat va namlik uchun)."""
    return amplitude * math.sin(math.pi * (hour - 6) / 12) if 6 <= hour <= 18 else -amplitude * 0.3


def generate_reading(sensor_id: str, at: datetime | None = None) -> SensorReading:
    """Bir sensor uchun bir ta realistik o'qish hosil qiladi."""
    cfg = next(c for c in SENSOR_CONFIGS if c.sensor_id == sensor_id)
    farm = next(f for f in FARMS if f.farm_id == cfg.farm_id)
    profile = CROP_PROFILES[cfg.crop_type]
    now = at or datetime.utcnow()
    hour = now.hour

    # Offline sensor — minimal ma'lumot
    if cfg.status == SensorStatus.OFFLINE:
        return SensorReading(
            sensor_id=sensor_id, farm_id=cfg.farm_id, timestamp=now,
            soil_moisture=0, temperature=0, humidity=0,
            water_flow=0, battery_level=0, signal_strength=-120,
        )

    # Harorat: bazaviy + kunlik + tasodif
    base_temp = profile["temp_preference"]
    temperature = round(base_temp + _diurnal(hour, 8) + random.gauss(0, 1.5), 1)

    # Namlik: harorat ortsa kamayadi
    base_moist = profile["base_moisture"]
    soil_moisture = round(
        base_moist - (temperature - base_temp) * 0.4 + random.gauss(0, 3), 1
    )
    soil_moisture = max(10, min(95, soil_moisture))

    # Havo namligi: teskari harorat bilan
    humidity = round(75 - _diurnal(hour, 15) + random.gauss(0, 5), 1)
    humidity = max(20, min(98, humidity))

    # Suv oqimi: sug'orish bo'lsa katta, yo'qsa nol
    irrigating = soil_moisture < cfg.irrigation_threshold and cfg.status == SensorStatus.ONLINE
    if irrigating:
        water_flow = round(cfg.field_area_ha * random.uniform(18, 28), 1)
    else:
        water_flow = round(random.uniform(0, 0.5), 2)

    # WARNING sensori uchun past batareya
    battery = round(random.uniform(12, 22) if cfg.status == SensorStatus.WARNING
                    else random.uniform(68, 99), 1)

    signal = random.randint(-75, -35) if cfg.status != SensorStatus.OFFLINE else -120

    return SensorReading(
        sensor_id=sensor_id,
        farm_id=cfg.farm_id,
        timestamp=now,
        soil_moisture=soil_moisture,
        temperature=temperature,
        humidity=humidity,
        water_flow=water_flow,
        battery_level=battery,
        signal_strength=signal,
    )


def generate_all_readings(at: datetime | None = None) -> List[SensorReading]:
    """Barcha 6 sensor uchun hozirgi o'qishlarni qaytaradi."""
    return [generate_reading(cfg.sensor_id, at) for cfg in SENSOR_CONFIGS]


def generate_history(sensor_id: str, hours: int = 24) -> List[SensorReading]:
    """Oxirgi N soat uchun tarixiy ma'lumot (har 15 daqiqada)."""
    readings = []
    now = datetime.utcnow()
    for minutes_ago in range(hours * 60, 0, -15):
        t = now - timedelta(minutes=minutes_ago)
        readings.append(generate_reading(sensor_id, at=t))
    return readings


def get_farm(farm_id: str) -> Farm | None:
    return next((f for f in FARMS if f.farm_id == farm_id), None)


def get_sensor_config(sensor_id: str) -> SensorConfig | None:
    return next((c for c in SENSOR_CONFIGS if c.sensor_id == sensor_id), None)
