<script lang="ts">
  import { page } from '$app/stores';
  import { apiFetch } from '$lib/api/client';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';

  type Participant = {
    id: string;
    email: string;
    first_name?: string;
    last_name?: string;
  };

  type SessionDetail = {
    id: string;
    title: string;
    starts_at: string;
    ends_at: string;
    coach_id: string;
    coach_name?: string;
    max_participants?: number;
    participants?: Participant[];
    status: 'scheduled' | 'cancelled';
  };

  let session: SessionDetail | null = null;
  let loading = true;
  let error = '';

  async function loadSession() {
    loading = true;
    error = '';

    try {
      const sessionId = get(page).params.id;
      const data = await apiFetch(`/sessions/${sessionId}`);

      session = data?.items ? data.items[0] : data;

    } catch (e) {
      console.error('Erreur chargement session', e);
      error = 'Impossible de charger la séance';
      session = null;
    } finally {
      loading = false;
    }
  }

  onMount(loadSession);
</script>

<div class="container">
  {#if loading}
    <p>Chargement...</p>

  {:else if error}
    <p style="color:red">{error}</p>

  {:else if session}
    <h1>Participants – {session.title}</h1>

    <p>
      <strong>Coach :</strong>
      {session.coach_name || session.coach_id || 'Inconnu'}
    </p>

    <p>
      <strong>Début :</strong>
      {new Date(session.starts_at).toLocaleString('fr-FR')}
    </p>

    <p>
      <strong>Fin :</strong>
      {new Date(session.ends_at).toLocaleString('fr-FR')}
    </p>

    <p>
      <strong>Participants max :</strong>
      {session.max_participants ?? '-'}
    </p>

    <p>
      <strong>Statut :</strong>
      {#if session.status === 'cancelled'}
        <span class="badge badge-danger">Annulée</span>
      {:else}
        <span class="badge badge-success">Active</span>
      {/if}
    </p>

    <h2>
      Liste des participants ({session.participants?.length ?? 0})
    </h2>

    {#if !session.participants || session.participants.length === 0}
      <p>Aucun participant inscrit.</p>
    {:else}
      <table>
        <thead>
          <tr>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {#each session.participants as p}
            <tr>
              <td>{p.last_name || '-'}</td>
              <td>{p.first_name || '-'}</td>
              <td>{p.email}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}

    <button on:click={() => goto('/dashboard/admin')}>
      Retour
    </button>
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

  .badge {
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
  }

  .badge-success {
    background: #d1fae5;
    color: #065f46;
  }

  .badge-danger {
    background: #fee2e2;
    color: #991b1b;
  }

  button {
    margin-top: 20px;
    padding: 8px 14px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    background-color: #2563eb;
    color: white;
  }
</style>
