<!-- COACH DASHBOARD: /frontend/src/routes/dashboard/coach/+page.svelte -->
<script lang="ts">
import { onMount } from 'svelte';
import { goto } from '$app/navigation';
import { apiFetch } from '$lib/api/client';

type Session = {
  id: string;
  title: string;
  starts_at: string;
  ends_at: string;
  coach_name?: string;
  max_participants?: number;
};

let sessions: Session[] = [];
let loading = true;
let error = '';

async function loadSessions() {
  loading = true;
  error = '';

  try {
    const res = await apiFetch('/sessions');
    sessions = res.items ?? res ?? [];
  } catch (e) {
    console.error(e);
    error = 'Impossible de charger les séances';
  } finally {
    loading = false;
  }
}

async function cancelSession(id: string) {
  try {
    await apiFetch(`/sessions/${id}/cancel`, {
      method: 'PATCH'
    });

    await loadSessions();
  } catch (e) {
    console.error(e);
    alert("Impossible d'annuler la séance");
  }
}

onMount(loadSessions);
</script>

<style>
.gym-coach-container {
  max-width: 1000px;
  margin: 48px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #e5e7eb;
  padding: 48px 40px 40px 40px;
}
h1 {
  font-size: 2.4rem;
  margin-bottom: 32px;
  color: #2563eb;
  text-align: center;
  letter-spacing: 1px;
}
.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 32px;
}
.action-bar button {
  background: #2563eb;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
.action-bar button:hover {
  background: #1d4ed8;
}
table {
  width: 100%;
  border-collapse: collapse;
  background: #f9fafb;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 4px #f3f4f6;
}
th, td {
  padding: 16px 12px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}
th {
  background: #f3f4f6;
  color: #2563eb;
  font-weight: 700;
  font-size: 1.1rem;
}
tr:last-child td {
  border-bottom: none;
}
.coach-action-btn {
  background: #2563eb;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  margin-right: 8px;
  transition: background 0.2s;
}
.coach-action-btn.cancel {
  background: #fee2e2;
  color: #991b1b;
}
.coach-action-btn:last-child {
  margin-right: 0;
}
.error-message {
  color: #991b1b;
  background: #fee2e2;
  padding: 12px 18px;
  border-radius: 8px;
  margin-bottom: 24px;
  text-align: center;
}
.loading-message {
  color: #888;
  font-size: 20px;
  text-align: center;
  margin: 40px 0;
}
</style>

<div class="gym-coach-container">
  <h1>Tableau de bord Coach</h1>
  <div class="action-bar">
    <button on:click={() => goto('/sessions/create')}>Créer une séance</button>
  </div>

  {#if loading}
    <div class="loading-message">Chargement...</div>
  {:else if error}
    <div class="error-message">{error}</div>
  {:else}
    <table>
      <thead>
        <tr>
          <th>Titre</th>
          <th>Date début</th>
          <th>Date fin</th>
          <th>Coach</th>
          <th>Max</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {#each sessions as session}
          <tr>
            <td>{session.title}</td>
            <td>{new Date(session.starts_at).toLocaleString('fr-FR')}</td>
            <td>{new Date(session.ends_at).toLocaleString('fr-FR')}</td>
            <td>{session.coach_name ?? '-'}</td>
            <td>{session.max_participants ?? '-'}</td>
            <td>
              <button class="coach-action-btn" on:click={() => goto(`/sessions/${session.id}/participants`)}>
                Participants
              </button>
              <button class="coach-action-btn cancel" on:click={() => cancelSession(session.id)}>
                Annuler
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>