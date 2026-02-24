<script lang="ts">
import { page } from '$app/stores';
import { auth } from '$lib/stores/auth.store';
import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import { get } from 'svelte/store';

function hasRole(role: string) {
  return get(auth).roles?.includes(role);
}

function logout() {
  auth.logout();
  goto('/login');
}

onMount(() => {
  const { accessToken } = get(auth);

  if (!accessToken) {
    goto('/login');
  }
});
</script>

<header>
<nav>

{#if hasRole('admin')}
<a href="/dashboard/admin">Administration</a>
{/if}

{#if hasRole('coach')}
<a href="/dashboard/coach">Coach</a>
{/if}

{#if hasRole('user')}
<a href="/dashboard/user">Mes séances</a>
{/if}

<button on:click={logout}>
Se déconnecter
</button>

</nav>
</header>

<main>
<slot />
</main>