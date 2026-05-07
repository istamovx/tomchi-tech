from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class SensorStatus(str, Enum):
    ONLINE  = "online"
    OFFLINE = "offline"
    WARNING = "warning"


class CropType(str, Enum):
    COTTON   = "paxta"
    WHEAT    = "bugdoy"
    TOMATO   = "pomidor"
    POTATO   = "kartoshka"
    CORN     = "makkajo'xori"
    GRAPE    = "uzum"
    ONION    = "piyoz"


class SensorReading(BaseModel):
    sensor_id:        str
    farm_id:          str
    timestamp:        datetime
    soil_moisture:    float = Field(..., ge=0,    le=100,  description="Tuproq namligi %")
    temperature:      float = Field(..., ge=-10,  le=60,   description="Harorat °C")
    humidity:         float = Field(..., ge=0,    le=100,  description="Havo namligi %")
    water_flow:       float = Field(..., ge=0,    le=1000, description="Suv oqimi L/soat")
    battery_level:    float = Field(..., ge=0,    le=100,  description="Batareya %")
    signal_strength:  int   = Field(..., ge=-120, le=0,    description="WiFi signal dBm")


class SensorConfig(BaseModel):
    sensor_id:              str
    farm_id:                str
    location_lat:           float
    location_lon:           float
    field_area_ha:          float  = Field(..., gt=0, description="Maydon (gektar)")
    crop_type:              CropType
    irrigation_threshold:   float  = Field(40.0, description="Sug'orish boshlash namligi %")
    status:                 SensorStatus = SensorStatus.ONLINE
    installed_at:           datetime


class Farm(BaseModel):
    farm_id:        str
    farmer_name:    str
    phone:          str
    region:         str
    district:       str
    total_area_ha:  float
    crop_type:      CropType
    sensor_count:   int = 0


class IrrigationEvent(BaseModel):
    farm_id:        str
    sensor_id:      str
    started_at:     datetime
    ended_at:       Optional[datetime] = None
    water_used_l:   Optional[float]    = None
    triggered_by:   str = "auto"      # "auto" | "manual"
