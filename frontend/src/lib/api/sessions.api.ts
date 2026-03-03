import { apiFetch } from '$lib/api/client';

export interface Session {
  id: string;
  coach_id: string;
  coach_name?: string;
  title: string;
  starts_at: string;
  ends_at: string;
  max_participants?: number;
  price_cents: number;
  currency: string;
  status: string;
}

export interface SessionsResponse {
  items: Session[];
  limit: number;
  offset: number;
  has_more: boolean;
}

export async function listSessions(): Promise<Session[]> {
  const res: SessionsResponse = await apiFetch('/sessions');
  return res.items;
}

export async function getSession(id: string): Promise<Session> {
  return apiFetch(`/sessions/${id}`);
}

export async function createSession(data: any) {
  return apiFetch('/sessions', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

export async function cancelSession(id: string) {
  return apiFetch(`/sessions/${id}/cancel`, {
    method: 'PUT'
  });
}