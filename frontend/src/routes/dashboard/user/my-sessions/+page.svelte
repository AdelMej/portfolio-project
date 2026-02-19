<script lang="ts">
  import { onMount } from 'svelte';
  import { apiFetch } from '$lib/api/client';

  type Session = {
    id: string;
    title: string;
    starts_at: string;
    ends_at: string;
    coach_name?: string;
  };

  let sessions: Session[] = [];
  let loading = true;
  let error = '';

  async function loadMySessions() {
    loading = true;
    error = '';

    try {
      const data = await apiFetch('/sessions/me');
      sessions = data?.items ? data.items : [];
    } catch (e) {
      error = 'Impossible de charger vos séances';
    } finally {
      loading = false;
    }
  }

  onMount(loadMySessions);
</script>

<h1>Mes séances</h1>

{#if loading}
  <p>Chargement...</p>

{:else if error}
  <p style="color:red">{error}</p>

{:else if sessions.length === 0}
  <p>Vous n’êtes inscrit à aucune séance.</p>

{:else}
  <ul>
    {#each sessions as s}
      <li>
        <strong>{s.title}</strong><br>
        {new Date(s.starts_at).toLocaleString('fr-FR')}<br>
        Coach: {s.coach_name ?? 'Inconnu'}
      </li>
    {/each}
  </ul>
{/if}
