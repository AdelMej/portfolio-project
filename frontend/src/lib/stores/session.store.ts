import { writable } from 'svelte/store';
import type { Session } from '$lib/types/session';

export const mySessions = writable<Session[]>([]);
export const availableSessions = writable<Session[]>([]);