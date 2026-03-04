// src/lib/api/client.ts
import { get } from 'svelte/store';
import { auth } from '$lib/stores/auth.store';
import { API_BASE_URL } from '$lib/config';

let isRefreshing = false;
let refreshPromise: Promise<string | null> | null = null;

async function tryRefreshToken(): Promise<string | null> {
  if (isRefreshing && refreshPromise) return refreshPromise;
  isRefreshing = true;
  refreshPromise = (async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!res.ok) return null;
      const data = await res.json();
      const newToken = data.access_token;
      if (newToken) {
        const current = get(auth);
        auth.login(newToken, current.roles ?? [], current.userId, current.email, current.firstName, current.lastName);
        return newToken;
      }
      return null;
    } catch {
      return null;
    } finally {
      isRefreshing = false;
      refreshPromise = null;
    }
  })();
  return refreshPromise;
}

export async function apiFetch<T = any>(endpoint: string, options: RequestInit = {}, _retried = false): Promise<T> {
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

  if (res.status === 401 && !_retried && !endpoint.includes('/auth/')) {
    const newToken = await tryRefreshToken();
    if (newToken) {
      return apiFetch<T>(endpoint, options, true);
    }
    auth.logout();
    if (typeof window !== 'undefined') window.location.href = '/login';
    throw { status: 401, message: 'Session expired' };
  }

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw errData;
  }

  return res.status === 204 ? (null as unknown as T) : (await res.json() as T);
}
