// src/lib/api/client.ts
import { get } from 'svelte/store';
import { auth } from '$lib/stores/auth.store';
import { API_BASE_URL } from '$lib/config';

export async function apiFetch<T = any>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = get(auth).accessToken;

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: 'include'
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw errData;
  }

  return res.status === 204 ? (null as unknown as T) : (await res.json() as T);
}
