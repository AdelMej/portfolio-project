import { apiFetch } from './client';

export interface AdminUser {
  id: string;
  email: string;
  roles: string[];
  disabled_at: string | null;
  disabled_reason: string | null;
  created_at: string;
}

export interface AdminUsersResponse {
  items: AdminUser[];
  limit: number;
  offset: number;
  has_more: boolean;
}

export async function getAdminUsers(limit = 20, offset = 0): Promise<AdminUsersResponse> {
  return apiFetch(`/admin/users/?limit=${limit}&offset=${offset}`);
}

export async function grantRole(userId: string, role: string) {
  return apiFetch(`/admin/users/${userId}/grant-role`, {
    method: 'POST',
    body: JSON.stringify({ role })
  });
}

export async function revokeRole(userId: string, role: string) {
  return apiFetch(`/admin/users/${userId}/revoke-role`, {
    method: 'POST',
    body: JSON.stringify({ role })
  });
}

export async function disableUser(userId: string, reason: string) {
  return apiFetch(`/admin/users/${userId}/disable`, {
    method: 'POST',
    body: JSON.stringify({ reason })
  });
}

export async function reenableUser(userId: string) {
  return apiFetch(`/admin/users/${userId}/reenable`, {
    method: 'POST'
  });
}
