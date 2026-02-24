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

<header class="main-header">
  <nav class="main-nav">
    <a href="/" class="nav-logo">Actual Digital Gym</a>
    <div class="nav-links">
      <a href="/">Accueil</a>
      {#if accessToken}
        <a href="/dashboard">Tableau de bord</a>
        <button class="logout-btn" on:click={logout}>Déconnexion</button>
      {:else}
        <a href="/login">Connexion</a>
      {/if}
    </div>
  </nav>
</header>

<main class="main-content">
  <slot />
</main>

<style>
.main-header {
  background: #2563eb;
  color: white;
  padding: 0;
  box-shadow: 0 2px 8px #e5e7eb;
}
.main-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  height: 64px;
}
.nav-logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  text-decoration: none;
  letter-spacing: 1px;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.05rem;
  transition: color 0.2s;
}
.nav-links a:hover {
  color: #a5b4fc;
}
.logout-btn {
  background: #fff;
  color: #2563eb;
  border: none;
  border-radius: 6px;
  padding: 8px 18px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-left: 10px;
  transition: background 0.2s, color 0.2s;
}
.logout-btn:hover {
  background: #a5b4fc;
  color: #1d4ed8;
}
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px 64px 16px;
}
</style>