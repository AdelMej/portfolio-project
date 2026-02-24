<script lang="ts">
  import { onMount } from 'svelte';
  import type { Session } from '$lib/api/sessions.api';
  import { listSessions } from '$lib/api/sessions.api';

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
.sessions-container {
  max-width: 800px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px #e5e7eb;
  padding: 36px 32px 32px 32px;
}
h1 {
  font-size: 2.2rem;
  margin-bottom: 24px;
  color: #2563eb;
  text-align: center;
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
.empty-message {
  color: #888;
  font-size: 18px;
  text-align: center;
  margin: 32px 0;
}
</style>

<div class="sessions-container">
  <h1>Gestion des séances</h1>

  {#if sessions.length === 0}
    <div class="empty-message">Aucune séance trouvée</div>
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
</div>