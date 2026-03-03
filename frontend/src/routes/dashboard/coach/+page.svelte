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
  participants_count?: number;
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
  color: #991b1b;
  text-align: center;
  letter-spacing: 1px;
}
.action-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 32px;
}
.action-bar button {
  background: #991b1b;
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
  background: #7f1d1d;
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
  color: #991b1b;
  font-weight: 700;
  font-size: 1.1rem;
}
tr:last-child td {
  border-bottom: none;
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

.participants-btn {
  background: #991b1b !important;
  color: white !important;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.participants-btn:hover {
  background: #7f1d1d !important;
}
.attendance-btn {
  background: #16a34a !important;
  color: white !important;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.attendance-btn:hover {
  background: #15803d !important;
}
</style>

<div class="gym-coach-container">
  <h1>Tableau de bord Coach</h1>
  <div class="action-bar">
    <button class="dashboard-btn participants-btn" on:click={() => goto('/sessions/create')}>Créer une séance</button>
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
        <th>Date</th>
        <th>Coach</th>
        <th>Participants</th>
        <th>Action</th>
        </tr>
    </thead>
    <tbody>
        {#each sessions as s}
        <tr>
            <td>{s.title}</td>
            <td>{new Date(s.starts_at).toLocaleString('fr-FR')}</td>
            <td>{s.coach_name ?? 'Non défini'}</td>
            <td>{s.participants_count ?? 0}{s.max_participants ? ` / ${s.max_participants}` : ''}</td>
            <td>
            <a href={`/dashboard/coach/sessions/${s.id}/edit`} class="dashboard-btn participants-btn">Modifier</a>
                <button class="dashboard-btn participants-btn" on:click={() => goto(`/sessions/${s.id}/participants`)} style="margin-left: 8px;">
                  Participants
                </button>
                <button class="dashboard-btn attendance-btn" on:click={() => goto(`/sessions/${s.id}/participants`)} style="margin-left: 8px;">
                  Présence
                </button>
            </td>
        </tr>
        {/each}
 
    
    </tbody>
    </table>
  {/if}
</div>