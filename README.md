# Tomchi Tech 🌱💧

**O'zbekiston uchun aqlli suv tejash platformasi**

IoT sensorlar + AI tavsiyalar + Fermer ilovasi

---

## Loyiha tuzilmasi

```
tomchi-tech/
├── backend/                   # FastAPI REST API
│   ├── app/
│   │   ├── main.py            # FastAPI app, router ulanishlari
│   │   ├── api/               # Endpointlar
│   │   │   ├── sensors.py     # GET /api/v1/sensors/
│   │   │   ├── farms.py       # GET /api/v1/farms/
│   │   │   ├── recommendations.py  # GET /api/v1/recommendations/
│   │   │   └── alerts.py      # GET /api/v1/alerts/
│   │   ├── models/
│   │   │   └── sensor.py      # Pydantic modellari (SensorReading, Farm, ...)
│   │   └── services/
│   │       └── simulator.py   # 6 soxta sensor simulyatori
│   ├── requirements.txt
│   └── .env.example
├── hardware/                  # ESP32 firmware (keyinroq)
├── mobile/                    # React Native ilovasi (keyinroq)
└── infra/                     # Docker, CI/CD (keyinroq)
```

---

## Tezkor ishga tushirish

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

---

## API Endpointlar

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/v1/sensors/` | Barcha sensorlar holati |
| GET | `/api/v1/sensors/{id}` | Bitta sensor o'qishi |
| GET | `/api/v1/sensors/{id}/history?hours=24` | Sensor tarixi |
| GET | `/api/v1/sensors/{id}/status` | Sensor holati xulosa |
| GET | `/api/v1/farms/` | Barcha fermalar |
| GET | `/api/v1/farms/{id}/summary` | Ferma umumiy holati |
| GET | `/api/v1/recommendations/` | Barcha sensorlar tavsiyasi |
| GET | `/api/v1/recommendations/{id}` | Bitta sensor tavsiyasi |
| GET | `/api/v1/alerts/` | Faol ogohlantirishlar |

---

## MVP holati

- [x] 6 soxta sensor simulyatori
- [x] REST API — sensors, farms, recommendations, alerts
- [x] `water_saving_pct` hisoblash (100% tejash NO_ACTION holatida)
- [x] `farms.py` API — ro'yxat, summary, sensor bog'liqligi
- [ ] Real ESP32 firmware
- [ ] Mobile app (React Native)
- [ ] MQTT broker
- [ ] TimescaleDB
- [ ] Docker Compose

---

## Sensorlar

| ID   | Fermer            | Ekin            | Hudud      | Holati  |
|------|-------------------|-----------------|------------|---------|
| S001 | Akbar Toshmatov   | Pomidor         | Qibray     | Online  |
| S002 | Muhabbat Yusupova | Kartoshka       | Bo'stonliq | Online  |
| S003 | Sherzod Raximov   | Paxta           | Guliston   | Warning |
| S004 | Nodira Xasanova   | Uzum            | Marg'ilon  | Online  |
| S005 | Behruz Mirzayev   | Bug'doy         | Urgut      | Online  |
| S006 | Zulfiya Qodirov   | Makkajo'xori    | Chortoq    | Offline |

---

## Texnologiyalar

- **Backend:** Python 3.11+, FastAPI, Pydantic v2, Uvicorn
- **Hardware (rejalashtirilgan):** ESP32, soil moisture sensor, DHT22
- **Mobile (rejalashtirilgan):** React Native
- **DB (rejalashtirilgan):** TimescaleDB (IoT time-series)
