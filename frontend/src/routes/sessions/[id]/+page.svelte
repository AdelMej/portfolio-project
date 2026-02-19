<script lang="ts">
  import { onMount } from 'svelte';
  import { getSession } from '$lib/api/sessions.api';
  import { page } from '$app/stores';

  let session: any = null;

  onMount(async () => {
    const sessionId = $page.params.id;
    if (!sessionId) return;

    try {
      session = await getSession(sessionId);
    } catch (e) {
      console.error('Failed to load session', e);
    }
  });
</script>

{#if session}
  <h1>{session.title}</h1>
  <p>Date: {session.date}</p>
  <h3>Participants</h3>
  <ul>
    {#each session.participants as p}
      <li>{p.email}</li>
    {/each}
  </ul>
{:else}
  <p>Loading session...</p>
{/if}
