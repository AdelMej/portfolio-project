
<script lang="ts">
  import { onMount } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import type { Session } from '$lib/api/sessions.api';
  import { listSessions } from '$lib/api/sessions.api';
  import { auth } from '$lib/stores/auth.store';

  let sessions: Session[] = [];
  let loading = true;
  let ready = false;

  onMount(async () => {
    ready = true;
    try {
      const res: Session[] = await listSessions();
      sessions = res;
    } catch (err) {
      console.error('Failed to fetch sessions', err);
    } finally {
      loading = false;
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
  .hero {
    padding: 40px 0 20px 0;
  }
  h1 {
    font-size: 2.8rem;
    color: #1f2937;
    margin-bottom: 12px;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }
  .hero-logo {
    height: 48px;
    width: auto;
    border-radius: 8px;
  }
  .stats-bar {
    display: flex;
    justify-content: center;
    gap: 48px;
    margin: 28px 0 32px 0;
  }
  .stat {
    text-align: center;
  }
  .stat-number {
    font-size: 2rem;
    font-weight: 800;
    color: #1f2937;
  }
  .stat-label {
    font-size: 0.82rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 2px;
  }
  a, .main-btn {
    display: inline-block;
    background: #991b1b;
    color: white;
    border: none;
    padding: 14px 32px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 1.1rem;
    cursor: pointer;
    margin: 18px 10px 0 10px;
    text-decoration: none;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(153,27,27,0.13);
  }
  a:hover, .main-btn:hover {
    background: #7f1d1d;
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(153,27,27,0.22);
  }
  .home-links {
    margin-top: 32px;
  }

  h2 {
    font-size: 1.5rem;
    color: #374151;
    margin: 40px 0 20px 0;
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
    border-radius: 10px;
    box-shadow: 0 1px 4px #f3f4f6;
    margin-bottom: 12px;
    padding: 18px 22px;
    font-size: 1.1rem;
    transition: transform 0.18s, box-shadow 0.2s;
    cursor: default;
  }
  .session-item:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
  }
  .session-title {
    font-weight: 600;
    color: #374151;
  }
  .session-date {
    color: #374151;
    font-size: 1rem;
    font-weight: 500;
  }
  .session-price {
    color: #065f46;
    font-size: 1rem;
    font-weight: 600;
  }
  .session-coach {
    color: #6b7280;
    font-size: 0.9rem;
  }
  .spinner {
    display: inline-block;
    width: 36px;
    height: 36px;
    border: 3px solid #e5e7eb;
    border-top-color: #374151;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    margin: 28px auto;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  .empty-msg {
    color: #9ca3af;
    margin: 18px 0;
    font-size: 1rem;
  }
</style>

{#if ready}
<div class="home-container" in:fade={{ duration: 350 }}>
  <div class="hero" in:fly={{ y: -30, duration: 450 }}>
    <h1><img src="/actual-logo.png" alt="actual" class="hero-logo" /> Bienvenue chez actual</h1>
  </div>

  <div class="stats-bar" in:fly={{ y: 20, duration: 450, delay: 180 }}>
    <div class="stat">
      <div class="stat-number">{loading ? '…' : sessions.length}</div>
      <div class="stat-label">Séances</div>
    </div>
  </div>

  <div class="home-links" in:fly={{ y: 20, duration: 450, delay: 320 }}>
    {#if $auth.accessToken}
      <a href="/dashboard" class="main-btn">Tableau de bord</a>
    {:else}
      <a href="/login" class="main-btn">Connexion</a>
      <a href="/registration" class="main-btn">Inscription</a>
    {/if}
  </div>

  <h2 in:fly={{ y: 20, duration: 450, delay: 420 }}>Les séances disponibles</h2>

  {#if loading}
    <div class="spinner"></div>
  {:else if sessions.length === 0}
    <div class="empty-msg" in:fade>Aucune séance disponible.</div>
  {:else}
    <ul class="session-list">
      {#each sessions as s, i}
        <li class="session-item" in:fly={{ y: 20, duration: 280, delay: 480 + i * 70 }}>
          <span class="session-title">{s.title}</span>
          <span class="session-coach">{s.coach_name ?? ''}</span>
          <span class="session-date">{new Date(s.starts_at).toLocaleString('fr-FR')}</span>
          <span class="session-price">{s.price_cents != null ? (s.price_cents / 100).toFixed(2) + ' ' + (s.currency ?? 'EUR') : ''}</span>
        </li>
      {/each}
    </ul>
  {/if}
</div>
{/if}
