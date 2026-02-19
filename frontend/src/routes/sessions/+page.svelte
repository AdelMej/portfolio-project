<script lang="ts">
  import { onMount } from 'svelte';
  import type { Session, SessionsResponse } from '$lib/api/sessions.api';
  import { listSessions } from '$lib/api/sessions.api';

  let sessions: Session[] = [];

  onMount(async () => {
  try {
  const res: SessionsResponse = await listSessions();
  sessions = res.items;
} catch (err) {
  console.error('Failed to fetch sessions', err);
}
  });
</script>

<h1>Gestion des séances</h1>

{#if sessions.length === 0}
  <p>Aucune séance trouvée</p>
{:else}
  <ul>
    {#each sessions as s}
      <li>{s.title} - {new Date(s.starts_at).toLocaleString()}</li>
    {/each}
  </ul>
{/if}
