import axios from 'axios';

const BASE_URL = 'https://tomchi-tech-api.onrender.com/api/v1';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// ── Types ─────────────────────────────────────────────────────
export type SensorStatus = 'online' | 'offline' | 'warning';
export type CropType = 'pomidor' | 'kartoshka' | 'paxta' | 'uzum' | 'bugdoy' | "makkajo'xori" | 'piyoz';

export interface SensorReading {
  sensor_id: string;
  farm_id: string;
  timestamp: string;
  soil_moisture: number;
  temperature: number;
  humidity: number;
  water_flow: number;
  battery_level: number;
  signal_strength: number;
}

export interface SensorConfig {
  sensor_id: string;
  farm_id: string;
  location_lat: number;
  location_lon: number;
  field_area_ha: number;
  crop_type: CropType;
  irrigation_threshold: number;
  status: SensorStatus;
  installed_at: string;
}

export interface Farm {
  farm_id: string;
  farmer_name: string;
  phone: string;
  region: string;
  district: string;
  total_area_ha: number;
  crop_type: CropType;
  sensor_count: number;
}

export interface Recommendation {
  sensor_id: string;
  farm_id: string;
  crop_type: CropType;
  generated_at: string;
  current_moisture: number;
  optimal_range: { min: number; max: number };
  action: 'IRRIGATE_NOW' | 'IRRIGATE_SOON' | 'STOP_IRRIGATION' | 'NO_ACTION';
  urgency: string;
  message: string;
  water_needed_liters: number;
  traditional_method_liters: number;
  water_saving_pct: number;
  temperature_c: number;
  humidity_pct: number;
}

export interface Alert {
  type: string;
  severity: 'warning' | 'error' | 'critical';
  sensor_id: string;
  farm_id: string;
  message: string;
  value: number | null;
  at: string;
}

// ── API calls ─────────────────────────────────────────────────
export const sensorsApi = {
  getAll: () => api.get<SensorReading[]>('/sensors/').then(r => r.data),
  getOne: (id: string) => api.get<SensorReading>(`/sensors/${id}`).then(r => r.data),
  getConfigs: () => api.get<SensorConfig[]>('/sensors/configs').then(r => r.data),
  getHistory: (id: string, hours = 24) =>
    api.get<SensorReading[]>(`/sensors/${id}/history?hours=${hours}`).then(r => r.data),
  getStatus: (id: string) => api.get(`/sensors/${id}/status`).then(r => r.data),
};

export const farmsApi = {
  getAll: () => api.get<Farm[]>('/farms/').then(r => r.data),
  getOne: (id: string) => api.get<Farm>(`/farms/${id}`).then(r => r.data),
  getSummary: (id: string) => api.get(`/farms/${id}/summary`).then(r => r.data),
};

export const recommendationsApi = {
  getAll: () => api.get<Recommendation[]>('/recommendations/').then(r => r.data),
  getOne: (id: string) => api.get<Recommendation>(`/recommendations/${id}`).then(r => r.data),
};

export const alertsApi = {
  getAll: () => api.get<{ count: number; alerts: Alert[] }>('/alerts/').then(r => r.data),
};

export default api;
