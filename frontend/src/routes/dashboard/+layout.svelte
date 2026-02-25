<script lang="ts">
import { page } from '$app/stores';
import { auth } from '$lib/stores/auth.store';
import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import { get } from 'svelte/store';

function hasRole(role: string) {
  const roles = get(auth).roles;
  return Array.isArray(roles) && roles.includes(role);
}

let loggingOut = false;

async function logout() {
  loggingOut = true;
  await auth.logout();
  goto('/login');
  loggingOut = false;
}

onMount(() => {
  const { accessToken } = get(auth);
  if (!accessToken) {
    goto('/login');
  }
});
</script>

<header>
  <nav aria-label="Main navigation">
    <ul style="display: flex; gap: 1rem; list-style: none; padding: 0; margin: 0;">
      {#if hasRole('admin')}
        <li>
          <a href="/dashboard/admin" class:active={$page.url.pathname === '/dashboard/admin'}>Administration</a>
        </li>
      {/if}
      {#if hasRole('coach')}
        <li>
          <a href="/dashboard/coach" class:active={$page.url.pathname === '/dashboard/coach'}>Coach</a>
        </li>
      {/if}
      {#if hasRole('user')}
        <li>
          <a href="/dashboard/user" class:active={$page.url.pathname === '/dashboard/user'}>Mes séances</a>
        </li>
      {/if}
    </ul>
  </nav>
</header>

<main>
  <slot />
</main>

<style>
a.active {
  font-weight: bold;
  text-decoration: underline;
}
</style>