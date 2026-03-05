<script lang="ts">
  import { onMount } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import type { Session } from '$lib/api/sessions.api';
  import { listSessions } from '$lib/api/sessions.api';
  import SessionIcon from '$lib/components/SessionIcon.svelte';

  let sessions: Session[] = [];
  let loading = true;
  let ready = false;

  function formatPrice(cents?: number, currency?: string): string {
    if (cents == null) return '-';
    return (cents / 100).toFixed(2) + ' ' + (currency ?? 'EUR');
  }

  onMount(async () => {
    ready = true;
    try {
      const res: Session[] = await listSessions();
      const now = new Date();
      sessions = res
        .filter(s => s.status !== 'cancelled' && new Date(s.ends_at) >= now)
        .sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());
    } catch (err) {
      console.error('Failed to fetch sessions', err);
    } finally {
      loading = false;
    }
  });
</script>

<style>
.sessions-container {
  max-width: 860px;
  margin: 40px auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  padding: 40px 32px 32px 32px;
}
h1 {
  font-size: 2rem;
  margin-bottom: 28px;
  color: #111827;
  text-align: center;
  font-weight: 800;
  letter-spacing: -0.02em;
}
h1 span { color: #991b1b; }
.session-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.session-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #fafafa;
  border-radius: 14px;
  margin-bottom: 10px;
  padding: 18px 20px;
  transition: transform 0.15s, box-shadow 0.15s;
}
.session-item:last-child { margin-bottom: 0; }
.session-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  background: #f5f5f5;
}
.s-icon {
  width: 42px; height: 42px; border-radius: 12px;
  background: #374151; color: white;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.s-info { flex: 1; min-width: 0; }
.s-title { font-weight: 600; font-size: 0.95rem; color: #111827; text-transform: capitalize; }
.s-sub { font-size: 0.8rem; color: #9ca3af; margin-top: 3px; }
.s-price { font-size: 0.92rem; font-weight: 700; color: #111827; white-space: nowrap; }
.s-badge {
  font-size: 0.7rem; font-weight: 600; padding: 4px 10px;
  border-radius: 20px; background: #f0fdf4; color: #16a34a;
  white-space: nowrap;
}
.empty-message {
  color: #9ca3af;
  font-size: 1rem;
  text-align: center;
  padding: 40px 16px;
  font-style: italic;
}
.spinner {
  display: inline-block; width: 32px; height: 32px;
  border: 2.5px solid #f0f0f0; border-top-color: #6b7280;
  border-radius: 50%; animation: spin 0.7s linear infinite; margin: 28px auto;
}
.loading-center { text-align: center; padding: 60px 0; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>

{#if ready}
<div class="sessions-container" in:fade={{ duration: 300 }}>
  <h1>Séances <span>disponibles</span></h1>

  {#if loading}
    <div class="loading-center"><div class="spinner"></div></div>
  {:else if sessions.length === 0}
    <div class="empty-message">Aucune séance disponible pour le moment.</div>
  {:else}
    <ul class="session-list">
      {#each sessions as s, i}
        <li class="session-item" in:fly={{ y: 15, duration: 250, delay: 80 + i * 50 }}>
          <div class="s-icon"><SessionIcon title={s.title} size={20} /></div>
          <div class="s-info">
            <div class="s-title">{s.title}</div>
            <div class="s-sub">{s.coach_name ?? ''} — {new Date(s.starts_at).toLocaleString('fr-FR')}</div>
          </div>
          <div class="s-price">{formatPrice(s.price_cents, s.currency)}</div>
          <span class="s-badge">Disponible</span>
        </li>
      {/each}
    </ul>
  {/if}
</div>
{/if}