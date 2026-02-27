import { writable } from 'svelte/store';

interface AuthState {
  accessToken: string | null;
  roles?: string[];
  userId?: string;
  email?: string;
}

function createAuth() {
  const { subscribe, set, update } = writable<AuthState>({ accessToken: null });

  return {
    subscribe,
    login: (token: string, roles: string[] = [], userId?: string, email?: string) =>
    set({ accessToken: token, roles, userId, email }),
    logout: () => set({ accessToken: null, roles: [] }),
  };
}

export const auth = createAuth();