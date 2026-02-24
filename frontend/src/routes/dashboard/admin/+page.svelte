<!-- SESSIONS LIST: /frontend/src/routes/sessions/+page.svelte -->
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

let mySessions: Session[] = [];
let availableSessions: Session[] = [];

let loading = true;
let error = '';

const LOCAL_KEY = 'user_sessions';

function getLocalSessions(): string[] {
  try {
    return JSON.parse(localStorage.getItem(LOCAL_KEY) || '[]');
  } catch {
    return [];
  }
}

function setLocalSessions(ids: string[]) {
  localStorage.setItem(LOCAL_KEY, JSON.stringify(ids));
}

async function loadSessions(): Promise<Session[]> {
  const res = await apiFetch('/sessions');
  return res.items ?? res ?? [];
}

async function joinSession(sessionId: string) {
  try {
    await apiFetch(`/sessions/${sessionId}/attendance`, {
      method: 'POST'
    });
    const session = availableSessions.find(s => s.id === sessionId);
    if (session) {
      mySessions = [...mySessions, session];
      availableSessions = availableSessions.filter(s => s.id !== sessionId);
      const ids = getLocalSessions();
      setLocalSessions([...ids, sessionId]);
    }
  } catch (e) {
    console.error(e);
    alert("Impossible de s'inscrire");
  }
}

async function loadDashboard() {
  loading = true;
  error = '';
  try {
    const sessions = await loadSessions();
    const localIds = getLocalSessions();
    mySessions = sessions.filter(s => localIds.includes(s.id));
    availableSessions = sessions.filter(s => !localIds.includes(s.id));
  } catch (e) {
    console.error(e);
    error = 'Erreur lors du chargement';
  } finally {
    loading = false;
  }
}

onMount(loadDashboard);
</script>

<style>
.gym-user-container {
  max-width: 900px;
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
h2 {
  font-size: 1.3rem;
  margin-top: 32px;
  margin-bottom: 12px;
  color: #374151;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 24px;
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
  color: #2563eb;
  font-weight: 700;
}
tr:last-child td {
  border-bottom: none;
}
button {
  background: #2563eb;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover {
  background: #1d4ed8;
}
.error-message {
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 16px;
  border-radius: 6px;
  margin-bottom: 18px;
  text-align: center;
}
.loading-message {
  color: #888;
  font-size: 18px;
  text-align: center;
  margin: 32px 0;
}
</style>

<div class="gym-user-container">
  <h1>Tableau de bord utilisateur</h1>

  {#if loading}
    <div class="loading-message">Chargement...</div>
  {:else if error}
    <div class="error-message">{error}</div>
  {:else}
    <h2>Mes séances inscrites</h2>
    {#if mySessions.length === 0}
      <div style="color: #888; margin-bottom: 18px;">Aucune séance inscrite.</div>
    {:else}
      <table>
        <thead>
          <tr>
            <th>Titre</th>
            <th>Date</th>
            <th>Coach</th>
          </tr>
        </thead>
        <tbody>
          {#each mySessions as s}
            <tr>
              <td>{s.title}</td>
              <td>{new Date(s.starts_at).toLocaleString('fr-FR')}</td>
              <td>{s.coach_name ?? 'Non défini'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}

    <h2>Mes séances disponibles</h2>
    {#if availableSessions.length === 0}
      <div style="color: #888; margin-bottom: 18px;">Aucune séance disponible.</div>
    {:else}
      <table>
        <thead>
          <tr>
            <th>Titre</th>
            <th>Date</th>
            <th>Coach</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {#each availableSessions as s}
            <tr>
              <td>{s.title}</td>
              <td>{new Date(s.starts_at).toLocaleString('fr-FR')}</td>
              <td>{s.coach_name ?? 'Non défini'}</td>
              <td>
                <button on:click={() => joinSession(s.id)}>
                  S'inscrire
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  {/if}
</div>