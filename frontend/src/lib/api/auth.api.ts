import { apiFetch } from './client';

export interface LoginResponse {
  access_token: string;
}

export interface MeResponse {
  email: string;
  roles: string[];
  id: string;
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

export interface MeProfileResponse {
  first_name: string;
  last_name: string;
}

export async function getMyProfile(): Promise<MeProfileResponse> {
  return apiFetch<MeProfileResponse>('/me/profile');
}

// Registration API call for new users
export async function createUser(email: string, password: string, first_name: string, last_name: string): Promise<void> {
  return apiFetch<void>('/auth/register', {
    method: 'PUT',
    body: JSON.stringify({ email, password, first_name, last_name }),
    headers: { 'Content-Type': 'application/json' }
  });
}