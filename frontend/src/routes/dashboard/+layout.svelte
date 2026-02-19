<script lang="ts">
  import { page } from '$app/stores';
  import { auth } from '$lib/stores/auth.store';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';

  function hasRole(required: string) {
    const roles = get(auth).roles || [];
    return roles.includes(required);
  }

  function logout() {
    auth.logout();
    goto('/login');
  }

  onMount(() => {
    const { accessToken, roles } = get(auth);
    const path = get(page).url.pathname;

    if (!accessToken) {
      goto('/login');
      return;
    }

    if (!roles || roles.length === 0) {
  // wait until roles are loaded, don't redirect yet
  return;
}

    if (path.startsWith('/dashboard/admin') && !hasRole('admin')) {
      goto('/dashboard');
      return;
    }

    if (path.startsWith('/dashboard/coach') && !hasRole('coach')) {
      goto('/dashboard');
      return;
    }

    if (path.startsWith('/dashboard/user') && !hasRole('user')) {
      goto('/dashboard');
      return;
    }
  });
</script>

<header>
  <nav>
    <a href="/dashboard">Tableau de bord</a>

    {#if hasRole('admin')}
      <a href="/dashboard/admin">Administration</a>
    {/if}

    {#if hasRole('coach')}
      <a href="/dashboard/coach">Coach</a>
    {/if}

   {#if hasRole('user')}
  <a href="/dashboard/user">Sessions disponibles</a>
  <a href="/dashboard/user/my-sessions">Mes séances</a>
   {/if}

    <button on:click={logout}>Se déconnecter</button>
  </nav>
</header>

<main>
  <slot />
</main>

<style>
  header { background: #f2f2f2; padding: 1rem; }
  nav { display: flex; gap: 1rem; align-items: center; }
  a { text-decoration: none; color: #333; }
  a:hover { text-decoration: underline; }
  button { margin-left: auto; cursor: pointer; }
  main { padding: 2rem; }
</style>
