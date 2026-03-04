<script lang="ts">
import { page } from '$app/stores';
import { auth } from '$lib/stores/auth.store';
import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import { get } from 'svelte/store';
import { browser } from '$app/environment';

let authenticated = false;

$: roles = $auth.roles ?? [];
$: tabCount = (['admin', 'coach', 'user'].filter(r => roles.includes(r))).length;

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
    return;
  }
  authenticated = true;
});

// Reactive guard: if token is cleared while on dashboard, redirect
$: if (browser && !$auth.accessToken && authenticated) {
  goto('/login');
}
</script>

<svelte:head>
  <title>Tableau de bord | Actual Digital Gym</title>
</svelte:head>

{#if authenticated}
<div class="dash-layout">
  {#if tabCount > 1}
  <nav class="dash-nav" aria-label="Main navigation">
    <ul>
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
  {/if}

  <main>
    <slot />
  </main>
</div>
{/if}

<style>
.dash-layout {
  max-width: 1200px;
  margin: 0 auto;
}
.dash-nav {
  background: #fff;
  border-radius: 10px;
  margin-bottom: 24px;
  padding: 0 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  border: 1px solid #e5e7eb;
}
.dash-nav ul {
  display: flex;
  gap: 0;
  list-style: none;
  padding: 0;
  margin: 0;
}
.dash-nav li {
  flex: 1;
}
.dash-nav a {
  display: block;
  text-align: center;
  padding: 12px 18px;
  color: #374151;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  border-bottom: 3px solid transparent;
  transition: color 0.2s, border-color 0.2s, background 0.15s;
  border-radius: 8px 8px 0 0;
}
.dash-nav a:hover {
  color: #1f2937;
  background: #f3f4f6;
}
.dash-nav a.active {
  color: #991b1b;
  border-bottom-color: #991b1b;
  background: #fff;
  font-weight: 700;
}
</style>