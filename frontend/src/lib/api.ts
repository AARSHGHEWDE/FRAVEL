import type { TripRequest, TripResponse } from "../types";

const BASE = "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || "Request failed");
  }
  return res.json();
}

export async function createTrip(trip: TripRequest): Promise<TripResponse> {
  return request<TripResponse>("/trips", { method: "POST", body: JSON.stringify(trip) });
}

export async function getTrip(tripId: string): Promise<TripResponse> {
  return request<TripResponse>(`/trips/${tripId}`);
}
