<script lang="ts">
  import { auth } from '$lib/stores/auth.store';
  import { goto } from '$app/navigation';

  let accessToken: string | null;
  auth.subscribe(value => accessToken = value.accessToken);

  function logout() {
    auth.logout();
    goto('/login');
  }
</script>

<header>
  <nav>
    <a href="/">Accueil</a>
    {#if accessToken}
      <a href="/dashboard">Tableau de bord</a>
    {:else}
      <a href="/login">Connexion</a>
    {/if}
  </nav>
</header>

<main>
  <slot />
</main>

<style>
  nav { display: flex; gap: 1rem; }
</style>
