// API client for the backend. Adds the X-API-Key header to every request.

import type { Call, Metrics } from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const API_KEY = import.meta.env.VITE_API_KEY || "dev_secret_change_me";

async function request<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "X-API-Key": API_KEY,
      "Content-Type": "application/json",
    },
  });
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  getMetrics: () => request<Metrics>("/metrics"),
  getCalls: (limit = 20) => request<Call[]>(`/calls?limit=${limit}`),
};
