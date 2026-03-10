import { apiFetch } from '$lib/api/client';

export interface SessionCoach {
  id: string;
  first_name: string;
  last_name: string;
}

export interface RawSession {
  id: string;
  coach?: SessionCoach;
  coach_id?: string;
  coach_name?: string;
  title: string;
  starts_at: string;
  ends_at: string;
  max_participants?: number;
  price_cents: number;
  currency: string;
  status: string;
}

export interface RawCompleteSession {
  id: string;
  coach?: SessionCoach;
  coach_id?: string;
  coach_name?: string;
  title: string;
  starts_at: string;
  ends_at: string;
  max_participants?: number;
  price_cents: number;
  currency: string;
  status: string;
  participants: { first_name: string; last_name: string}[];
}
export interface CompleteSession {
  id: string;
  coach_id: string;
  coach_name: string;
  title: string;
  starts_at: string;
  ends_at: string;
  max_participants?: number;
  price_cents: number;
  currency: string;
  status: string;
  participants: { first_name: string; last_name: string}[];
}

export interface Session {
  id: string;
  coach_id: string;
  coach_name: string;
  title: string;
  starts_at: string;
  ends_at: string;
  max_participants?: number;
  price_cents: number;
  currency: string;
  status: string;
}

export interface CompleteSessionsResponse {
  items: RawCompleteSession[];
  limit: number;
  offset: number;
  has_more: boolean;
}

export interface SessionsResponse {
  items: RawSession[];
  limit: number;
  offset: number;
  has_more: boolean;
}

function mapCompleteSession(raw: RawCompleteSession): CompleteSession {
     return {
    id: raw.id,
    coach_id: raw.coach?.id ?? raw.coach_id ?? '',
    coach_name: raw.coach
      ? `${raw.coach.first_name} ${raw.coach.last_name}`
      : (raw.coach_name ?? 'Non défini'),
    title: raw.title,
    starts_at: raw.starts_at,
    ends_at: raw.ends_at,
    max_participants: raw.max_participants,
    price_cents: raw.price_cents,
    currency: raw.currency,
    status: raw.status,
    participants: raw.participants || [],
  };
}

function mapSession(raw: RawSession): Session {
  return {
    id: raw.id,
    coach_id: raw.coach?.id ?? raw.coach_id ?? '',
    coach_name: raw.coach
      ? `${raw.coach.first_name} ${raw.coach.last_name}`
      : (raw.coach_name ?? 'Non défini'),
    title: raw.title,
    starts_at: raw.starts_at,
    ends_at: raw.ends_at,
    max_participants: raw.max_participants,
    price_cents: raw.price_cents,
    currency: raw.currency,
    status: raw.status,
  };
}

export async function listSessions(): Promise<Session[]> {
  const res: SessionsResponse = await apiFetch('/sessions');
  return res.items.map(mapSession);
}

export async function getSession(id: string): Promise<Session> {
  const raw: RawSession = await apiFetch(`/sessions/${id}`);
  return mapSession(raw);
}

export async function createSession(data: any) {
  return apiFetch('/sessions', {
    method: 'POST',
    body: JSON.stringify(data)
  });
}

export async function updateSession(id: string, data: { title: string; starts_at: string; ends_at: string }) {
  return apiFetch(`/sessions/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
}

export async function cancelSession(id: string) {
  return apiFetch(`/sessions/${id}/cancel`, {
    method: 'PUT'
  });
}

export async function cancelRegistration(sessionId: string): Promise<void> {
  return apiFetch<void>(`/sessions/${sessionId}/cancel-registration`, {
    method: 'POST'
  });
}

export async function listCoachSessions(): Promise<CompleteSession[]> {
  const res: CompleteSessionsResponse = await apiFetch('/coach/sessions');
  return res.items.map(mapCompleteSession);
}

