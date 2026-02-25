
<script lang="ts">
  import { onMount } from 'svelte';
  import type { Session } from '$lib/api/sessions.api';
  import { listSessions } from '$lib/api/sessions.api';
  import { auth } from '$lib/stores/auth.store';

  let sessions: Session[] = [];

  onMount(async () => {
    try {
      const res: Session[] = await listSessions();
      sessions = res;
    } catch (err) {
      console.error('Failed to fetch sessions', err);
    }
  });
</script>

<style>
.home-container {
  max-width: 900px;
  margin: 60px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #e5e7eb;
  padding: 48px 40px 40px 40px;
  text-align: center;
}
h1 {
  font-size: 2.6rem;
  color: #2563eb;
  margin-bottom: 18px;
  letter-spacing: 1px;
}
h2 {
  font-size: 1.5rem;
  color: #374151;
  margin-bottom: 32px;
}
a, .main-btn {
  display: inline-block;
  background: #2563eb;
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  margin: 18px 10px 0 10px;
  text-decoration: none;
  transition: background 0.2s;
}
a:hover, .main-btn:hover {
  background: #1d4ed8;
}
.home-links {
  margin-top: 32px;
}

.session-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 1px 4px #f3f4f6;
  margin-bottom: 16px;
  padding: 18px 22px;
  font-size: 1.1rem;
}
.session-title {
  font-weight: 600;
  color: #374151;
}
.session-date {
  color: #2563eb;
  font-size: 1rem;
  font-weight: 500;
}
</style>

<div class="home-container">
  <h1>Bienvenue à Actual Digital Gym</h1>
    <div class="home-links">
    {#if $auth.accessToken}
        <a href="/dashboard" class="main-btn">Tableau de bord</a>
    {:else}
        <a href="/login" class="main-btn">Connexion</a>
        <a href="/registration" class="main-btn">Inscription</a>
    {/if}
    </div>
</div>

<h2>Les séances disponibles</h2>
{#if sessions.length === 0}
  <div style="color: #888; margin-bottom: 18px;">Aucune séance disponible.</div>
{:else}
  <ul class="session-list">
    {#each sessions as s}
      <li class="session-item">
        <span class="session-title">{s.title}</span>
        <span class="session-date">{new Date(s.starts_at).toLocaleString('fr-FR')}</span>
      </li>
    {/each}
  </ul>
{/if}
