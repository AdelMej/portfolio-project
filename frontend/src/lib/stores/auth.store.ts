import { writable } from 'svelte/store';

interface AuthState {
  accessToken: string | null;
  roles?: string[];
}

function createAuth() {
  const { subscribe, set, update } = writable<AuthState>({ accessToken: null });

  return {
    subscribe,
    login: (token: string, roles: string[] = []) => set({ accessToken: token, roles }),
    logout: () => set({ accessToken: null, roles: [] }),
  };
}

export const auth = createAuth();