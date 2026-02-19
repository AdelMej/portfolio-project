<script lang="ts">
  import { onMount } from 'svelte';
  import { apiFetch } from '$lib/api/client';

  type Session = {
    id: string;
    title: string;
    starts_at: string;
    ends_at: string;
    coach_name?: string;
    coach_id: string;
    max_participants?: number;
    participants_count?: number;
    status: 'scheduled' | 'cancelled';
  };

  let sessions: Session[] = [];
  let loading = true;
  let error = '';

  async function loadSessions() {
    loading = true;
    error = '';

    try {
      const data = await apiFetch('/sessions');
      sessions = data?.items ? data.items : [];
    } catch (e) {
      console.error(e);
      error = 'Impossible de charger les séances';
    } finally {
      loading = false;
    }
  }

  async function rejoindreSeance(id: string) {
    try {
      await apiFetch(`/sessions/${id}/join`, {
        method: 'POST'
      });

      await loadSessions(); // reload to update count
    } catch (e) {
      alert('Impossible de rejoindre cette séance');
    }
  }

  onMount(loadSessions);
</script>

<div class="container">
  <h1>Sessions disponibles</h1>

  {#if loading}
    <p>Chargement...</p>

  {:else if error}
    <p style="color:red">{error}</p>

  {:else if sessions.length === 0}
    <p>Aucune séance disponible.</p>

  {:else}
    <table>
      <thead>
        <tr>
          <th>Titre</th>
          <th>Début</th>
          <th>Fin</th>
          <th>Coach</th>
          <th>Places</th>
          <th></th>
        </tr>
      </thead>

      <tbody>
        {#each sessions as s}
          {#if s.status === 'scheduled'}
            <tr>
              <td>{s.title}</td>

              <td>
                {new Date(s.starts_at).toLocaleString('fr-FR')}
              </td>

              <td>
                {new Date(s.ends_at).toLocaleString('fr-FR')}
              </td>

              <td>
                {s.coach_name || s.coach_id}
              </td>

              <td>
                {s.participants_count ?? 0}
                /
                {s.max_participants ?? '-'}
              </td>

              <td>
                <button
                  disabled={s.participants_count === s.max_participants}
                  on:click={() => rejoindreSeance(s.id)}
                >
                  Rejoindre
                </button>
              </td>
            </tr>
          {/if}
        {/each}
      </tbody>
    </table>
  {/if}
</div>

<style>
  .container { padding: 40px; }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  th, td {
    padding: 10px;
    border: 1px solid #ddd;
  }

  th {
    background: #f3f4f6;
  }

  button {
    padding: 6px 12px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    background-color: #16a34a;
    color: white;
  }

  button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
  }
</style>
