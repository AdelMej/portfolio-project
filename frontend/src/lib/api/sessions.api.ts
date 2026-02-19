import { apiFetch } from './client';

export interface Session {
  id: string;
  coach_id: string;
  coach_name?: string;       // optional, populate from API or join
  title: string;
  starts_at: string;
  ends_at: string;
  max_participants?: number; // optional
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

// FIXED: Return full backend response type
export async function listSessions(): Promise<Session[]> {
  const res: SessionsResponse = await apiFetch('/sessions');
  return res.items; // <-- return only the items array
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
