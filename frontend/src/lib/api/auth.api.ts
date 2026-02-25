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
  return apiFetch<MeResponse>('/me/');
}

export function logout() {
  return apiFetch<void>('/auth/logout', { method: 'POST' });
}

// register function
export async function createUser(email: string, password: string): Promise<void> {
  return apiFetch<void>('/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}