<script lang="ts">
import { onMount } from 'svelte';
import { fly, fade } from 'svelte/transition';
import { apiFetch } from '$lib/api/client';
import { goto } from '$app/navigation';
import { auth } from '$lib/stores/auth.store';

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
let ready = false;
let joiningId = '';

import { get } from 'svelte/store';
let LOCAL_KEY = '';

function updateLocalKey() {
  const state = get(auth);
  LOCAL_KEY = `user_sessions_${state.userId ?? 'unknown'}`;
}

onMount(() => {
  ready = true;
  updateLocalKey();
  loadDashboard();
});

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
    if (Array.isArray(res.items)) return res.items;
    if (Array.isArray(res)) return res;
return [];
}

async function joinSession(sessionId: string) {
  joiningId = sessionId;
  try {
    await apiFetch(`/sessions/${sessionId}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const session = availableSessions.find(s => s.id === sessionId);
    if (session) {
      mySessions = [...mySessions, session];
      availableSessions = availableSessions.filter(s => s.id !== sessionId);
      const ids = getLocalSessions();
      setLocalSessions([...ids, sessionId]);
    }
  } catch (e) {
    error = "Impossible de s'inscrire";
    console.error(e);
  } finally {
    joiningId = '';
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
</script>

<style>
.gym-user-container {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 16px #e5e7eb;
  padding: 36px 32px 32px 32px;
}
h1 {
  font-size: 2.2rem;
  margin-bottom: 24px;
  color: #991b1b;
  text-align: center;
}
h2 {
  font-size: 1.3rem;
  margin-top: 32px;
  margin-bottom: 12px;
  color: #374151;
  display: flex;
  align-items: center;
  gap: 8px;
}
h2 .badge {
  background: #991b1b;
  color: white;
  font-size: 0.8rem;
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 700;
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
  color: #991b1b;
  font-weight: 700;
}
tr {
  transition: background 0.15s;
}
tr:hover td {
  background: #fef2f2;
}
tr:last-child td {
  border-bottom: none;
}
button {
  background: #991b1b;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 1px 4px rgba(153,27,27,0.12);
}
button:hover {
  background: #7f1d1d;
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(153,27,27,0.18);
}
button:disabled {
  background: #fca5a5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
.error-message {
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 16px;
  border-radius: 6px;
  margin-bottom: 18px;
  text-align: center;
}
.spinner {
  display: inline-block;
  width: 36px;
  height: 36px;
  border: 3px solid #e5e7eb;
  border-top-color: #991b1b;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin: 28px auto;
}
.loading-center {
  text-align: center;
  padding: 32px 0;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
.empty-msg {
  color: #9ca3af;
  margin: 14px 0 18px 0;
  font-style: italic;
}
</style>

{#if ready}
<div class="gym-user-container" in:fade={{ duration: 300 }}>
  <h1 in:fly={{ y: -20, duration: 400 }}>Tableau de bord utilisateur</h1>

  {#if loading}
    <div class="loading-center" in:fade>
      <div class="spinner"></div>
      <div style="color: #9ca3af; margin-top: 8px;">Chargement des séances…</div>
    </div>
  {:else if error}
    <div class="error-message" in:fade>{error}</div>
  {:else}
    <h2 in:fly={{ y: 15, duration: 350, delay: 100 }}>
      Mes séances inscrites <span class="badge">{mySessions.length}</span>
    </h2>
    {#if mySessions.length === 0}
      <div class="empty-msg" in:fade={{ delay: 150 }}>Aucune séance inscrite.</div>
    {:else}
      <div in:fly={{ y: 15, duration: 350, delay: 150 }}>
      <table>
        <thead>
          <tr>
            <th>Titre</th>
            <th>Date</th>
            <th>Coach</th>
          </tr>
        </thead>
        <tbody>
          {#each mySessions as s, i}
            <tr in:fly={{ x: -20, duration: 250, delay: 200 + i * 60 }}>
              <td>{s.title}</td>
              <td>{new Date(s.starts_at).toLocaleString('fr-FR')}</td>
              <td>{s.coach_name ?? 'Non défini'}</td>
            </tr>
          {/each}
        </tbody>
      </table>
      </div>
    {/if}

    {#if error}
      <div class="error-message" in:fade>{error}</div>
    {/if}

    <h2 in:fly={{ y: 15, duration: 350, delay: 250 }}>
      Séances disponibles <span class="badge">{availableSessions.length}</span>
    </h2>
    {#if availableSessions.length === 0}
      <div class="empty-msg" in:fade={{ delay: 300 }}>Aucune séance disponible.</div>
    {:else}
      <div in:fly={{ y: 15, duration: 350, delay: 300 }}>
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
          {#each availableSessions as s, i}
            <tr in:fly={{ x: -20, duration: 250, delay: 350 + i * 60 }}>
              <td>{s.title}</td>
              <td>{new Date(s.starts_at).toLocaleString('fr-FR')}</td>
              <td>{s.coach_name ?? 'Non défini'}</td>
              <td>
                <button on:click={() => joinSession(s.id)} disabled={joiningId === s.id}>
                  {joiningId === s.id ? '...' : "S'inscrire"}
                </button>
                <button on:click={() => goto(`/sessions/${s.id}/participants`)} style="margin-left: 8px;">
                  Voir participants
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
      </div>
    {/if}
  {/if}
</div>
{/if}