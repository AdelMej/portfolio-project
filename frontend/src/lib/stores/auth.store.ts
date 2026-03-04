import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface AuthState {
  accessToken: string | null;
  roles?: string[];
  userId?: string;
  email?: string;
  firstName?: string;
  lastName?: string;
}

const STORAGE_KEY = 'auth_state';

function loadFromStorage(): AuthState {
  if (!browser) return { accessToken: null };
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch { /* ignore */ }
  return { accessToken: null };
}

function saveToStorage(state: AuthState) {
  if (!browser) return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch { /* ignore */ }
}

function clearStorage() {
  if (!browser) return;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch { /* ignore */ }
}

function createAuth() {
  const initial = loadFromStorage();
  const { subscribe, set } = writable<AuthState>(initial);

  return {
    subscribe,
    login: (token: string, roles: string[] = [], userId?: string, email?: string, firstName?: string, lastName?: string) => {
      const state: AuthState = { accessToken: token, roles, userId, email, firstName, lastName };
      saveToStorage(state);
      set(state);
    },
    logout: () => {
      clearStorage();
      set({ accessToken: null, roles: [] });
    },
  };
}

export const auth = createAuth();