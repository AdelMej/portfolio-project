<script lang="ts">
  import { goto } from '$app/navigation';
  import { listSessions, type Session } from '$lib/api/sessions.api';
  import { onMount } from 'svelte';

  // keep it as an array
  let sessions: Session[] = [];

  onMount(async () => {
    // fetch and assign directly
    const res: any = await listSessions(); // keep 'any' to avoid type errors
    sessions = res.items || res; // if res has .items use it, else fallback
  });
</script>

<h1>Tableau de bord Coach</h1>

<button on:click={() => goto('/sessions/create')}>
  Créer une séance
</button>

<table>
  <thead>
    <tr>
      <th>Nom</th>
      <th>Date début</th>
      <th>Date fin</th>
      <th>Coach</th>
      <th>Nombre max participants</th>
      <th>Actions</th>
    </tr>
  </thead>

  <tbody>
    {#each sessions as session}
      <tr>
        <td>{session.title}</td>
        <td>{new Date(session.starts_at).toLocaleString('fr-FR')}</td>
        <td>{new Date(session.ends_at).toLocaleString('fr-FR')}</td>
        <td>{session.coach_name || session.coach_id}</td>
        <td>{session.max_participants || '-'}</td>
        <td>
          <button on:click={() => goto(`/sessions/${session.id}/participants`)}>
            Voir participants
          </button>
        </td>
      </tr>
    {/each}
  </tbody>
</table>
