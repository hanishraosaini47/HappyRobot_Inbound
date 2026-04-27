// API client for the backend. Adds the X-API-Key header to every request.

import type { Call, Metrics } from "./types";

// Production values — backend deployed on Fly.io
const BASE_URL = "https://happyrobot-inbound-carrier1.fly.dev";
const API_KEY = "49747487c922046a150c8c03d945167f3dcd8c3eb4cf4a36129966cce7990973";

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