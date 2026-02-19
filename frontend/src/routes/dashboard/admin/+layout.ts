import { get } from 'svelte/store';
import { auth } from '$lib/stores/auth.store';
import { redirect } from '@sveltejs/kit';

export async function load() {
  const { accessToken } = get(auth);

  if (!accessToken) {
    throw redirect(302, '/login');
  }

  return {};
}