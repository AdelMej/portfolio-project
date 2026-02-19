import { apiFetch } from './client';

export interface LoginResponse {
  access_token: string;
}

export interface MeResponse {
  email: string;
  roles: string[];
}

// login function
export async function login(email: string, password: string): Promise<LoginResponse> {
  return apiFetch<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

// getMe function
export async function getMe(): Promise<MeResponse> {
  return apiFetch<MeResponse>('/auth/me');
}

export function logout() {
  return apiFetch<void>('/auth/logout', { method: 'POST' });
}