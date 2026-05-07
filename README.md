# Tomchi Tech 🌱💧

**O'zbekiston uchun aqlli suv tejash platformasi**

IoT sensorlar + AI tavsiyalar + Fermer ilovasi

---

## Loyiha tuzilmasi

```
tomchi-tech/
├── backend/          # FastAPI REST API
│   ├── app/
│   │   ├── main.py
│   │   ├── api/          # Endpoints: sensors, farms, recommendations, alerts
│   │   ├── models/       # Pydantic modellari
│   │   └── services/     # simulator.py — soxta sensor ma'lumotlari
│   └── requirements.txt
├── hardware/         # ESP32 firmware (keyinroq)
├── mobile/           # React Native ilovasi (keyinroq)
├── ai/               # ML modellar (keyinroq)
└── infra/            # Docker, CI/CD
```

## Tezkor ishga tushirish

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## MVP holati

- [x] 6 soxta sensor simulyatori
- [x] REST API (sensors, farms, recommendations, alerts)
- [ ] Real ESP32 firmware
- [ ] Mobile app
- [ ] MQTT broker
- [ ] TimescaleDB

## Sensorlar

| ID   | Fermer            | Ekin       | Hudud      | Holati  |
|------|-------------------|------------|------------|---------|
| S001 | Akbar Toshmatov   | Pomidor    | Qibray     | Online  |
| S002 | Muhabbat Yusupova | Kartoshka  | Bo'stonliq | Online  |
| S003 | Sherzod Raximov   | Paxta      | Guliston   | Warning |
| S004 | Nodira Xasanova   | Uzum       | Marg'ilon  | Online  |
| S005 | Behruz Mirzayev   | Bug'doy    | Urgut      | Online  |
| S006 | Zulfiya Qodirov   | Makkajo'xori| Chortoq  | Offline |
