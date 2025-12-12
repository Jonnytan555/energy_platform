import axios from "axios";
import { jwtDecode } from "jwt-decode";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
  timeout: 30000,
});

// Attach Bearer token automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto logout on 401
api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err?.response?.status === 401) {
      localStorage.removeItem("access_token");
    }
    return Promise.reject(err);
  }
);

export interface TokenPayload {
  sub: string; // email
  id?: number;
  role?: string;
  exp?: number;
  iat?: number;
  [key: string]: any;
}

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
}

export function getToken(): string | null {
  return localStorage.getItem("access_token");
}

export function setToken(token: string) {
  localStorage.setItem("access_token", token);
}

export function logout() {
  localStorage.removeItem("access_token");
}

export function getCurrentUser(): TokenPayload | null {
  const token = getToken();
  if (!token) return null;

  try {
    const payload = jwtDecode<TokenPayload>(token);

    // expiry check
    if (payload.exp && payload.exp * 1000 < Date.now()) {
      logout();
      return null;
    }

    return payload;
  } catch {
    return null;
  }
}

// ---------- Auth ----------
export async function login(email: string, password: string): Promise<void> {
  const res = await api.post<TokenResponse>("/auth/login", { email, password });
  setToken(res.data.access_token);
}

export async function register(email: string, password: string): Promise<{ id: number; email: string }> {
  const res = await api.post("/auth/register", { email, password });
  return res.data;
}

export async function refreshToken(): Promise<void> {
  const res = await api.post<TokenResponse>("/auth/refresh");
  setToken(res.data.access_token);
}

export async function me(): Promise<{ id: number; email: string }> {
  const res = await api.get("/auth/me");
  return res.data;
}

// ---------- AGSI ----------
export type AgsiRow = {
  date: string;
  full_pct?: number;
  gas_in_storage_gwh?: number;
  injection?: number;
  withdrawal?: number;
  working_gas_gwh?: number;
  trend?: string | number | null;
  [key: string]: any;
};

export async function fetchAgsiData(zone: string, pages?: number): Promise<AgsiRow[]> {
  const params: Record<string, any> = {};
  if (pages && pages > 0) params.pages = pages;
  const res = await api.get(`/storage/agsi/${zone}/data`, { params });
  return res.data;
}

export async function scrapeAgsiSync(zone: string, pages?: number): Promise<AgsiRow[]> {
  const params: Record<string, any> = {};
  if (pages && pages > 0) params.pages = pages;
  const res = await api.post(`/storage/agsi/${zone}/scrape`, null, { params });
  return res.data;
}

// ---------- ALSI ----------
export type AlsiRow = {
  date: string;

  // your response handler might use either of these:
  inventory_gwh?: number;
  lng_storage_gwh?: number;

  sendOut?: number;
  dtmi_gwh?: number;
  dtrs?: number;

  contractedCapacity?: number;
  availableCapacity?: number;

  [key: string]: any;
};

export async function fetchAlsiData(country: string = "EU"): Promise<AlsiRow[]> {
  const res = await api.get(`/storage/alsi`, { params: { country } });
  return res.data;
}

export async function scrapeAlsi(country: string = "EU"): Promise<{ rows_persisted: number; data: AlsiRow[] }> {
  const res = await api.post(`/storage/alsi/scrape`, null, { params: { country } });
  return res.data;
}

export type AgsiLatestRow = AgsiRow & {
  version?: number;
  is_latest?: boolean;
  created_date?: string | null;
};

export async function fetchAgsiLatest(limit: number = 365): Promise<AgsiLatestRow[]> {
  const res = await api.get(`/storage/agsi/eu/latest`, { params: { limit } });
  return res.data;
}

export type AlsiLatestRow = AlsiRow & {
  version?: number;
  is_latest?: boolean;
  created_date?: string | null;
};

export async function fetchAlsiLatest(limit: number = 365): Promise<AlsiLatestRow[]> {
  const res = await api.get(`/storage/alsi/latest`, { params: { limit } });
  return res.data;
}


export default api;
