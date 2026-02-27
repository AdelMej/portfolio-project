<script lang="ts">
  import { page } from '$app/stores';
  import { apiFetch } from '$lib/api/client';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';
  import { auth } from '$lib/stores/auth.store';

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

  function handleReturn() {
    const roles = get(auth).roles || [];
    if (roles.includes('admin')) {
      goto('/dashboard/admin');
    } else if (roles.includes('coach')) {
      goto('/dashboard/coach');
    } else {
      goto('/dashboard/user');
    }
  }

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

    <button on:click={handleReturn}>
      Retour
    </button>
  {/if}
</div>


<style>
  .container {
    max-width: 900px;
    margin: 40px auto;
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 16px #e5e7eb;
    padding: 36px 32px 32px 32px;
  }
  h1 {
    font-size: 2rem;
    color: #991b1b;
    margin-bottom: 18px;
  }
  h2 {
    font-size: 1.3rem;
    color: #374151;
    margin-top: 24px;
    margin-bottom: 12px;
  }
  p {
    margin: 8px 0;
    color: #374151;
    font-size: 1rem;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
    background: #f9fafb;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 4px #f3f4f6;
  }
  th, td {
    padding: 12px 10px;
    border-bottom: 1px solid #e5e7eb;
    text-align: left;
  }
  th {
    background: #f3f4f6;
    color: #991b1b;
    font-weight: 700;
  }
  tr:last-child td {
    border-bottom: none;
  }
  tr:hover td {
    background: #fef2f2;
  }
  .badge {
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
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
    margin-top: 24px;
    padding: 10px 22px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    background: #991b1b;
    color: white;
    font-weight: 700;
    font-size: 1rem;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(153,27,27,0.12);
  }
  button:hover {
    background: #7f1d1d;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(153,27,27,0.2);
  }
</style>
