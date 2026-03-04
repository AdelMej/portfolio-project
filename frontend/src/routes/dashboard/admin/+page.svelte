<!-- ADMIN DASHBOARD: /frontend/src/routes/dashboard/admin/+page.svelte -->
<script lang="ts">
import { onMount } from 'svelte';
import { afterNavigate } from '$app/navigation';
import { fly, fade } from 'svelte/transition';
import { apiFetch } from '$lib/api/client';
import { auth } from '$lib/stores/auth.store';
import { getAdminUsers, type AdminUser } from '$lib/api/admin.api';
import { listSessions, cancelSession, type Session } from '$lib/api/sessions.api';

function formatPrice(cents?: number, currency?: string): string {
  if (cents == null) return '-';
  return (cents / 100).toFixed(2) + ' ' + (currency ?? 'EUR');
}

let firstName = '';
let lastName = '';
auth.subscribe((v) => {
  firstName = v.firstName ?? '';
  lastName = v.lastName ?? '';
});

let users: AdminUser[] = [];
let sessions: Session[] = [];
let loading = true;
let error = '';
let cancellingId = '';
let ready = false;
let activeTab: 'users' | 'sessions' = 'users';
let searchQuery = '';
let expandedSession: string | null = null;
let participantsCache: Record<string, {first_name: string; last_name: string}[]> = {};
let loadingParticipants: string | null = null;

async function toggleParticipants(id: string) {
  if (expandedSession === id) { expandedSession = null; return; }
  expandedSession = id;
  if (participantsCache[id]) return;
  loadingParticipants = id;
  try {
    const data = await apiFetch(`/admin/sessions/${id}/participants`);
    participantsCache[id] = data;
    participantsCache = participantsCache; // trigger reactivity
  } catch {
    participantsCache[id] = [];
  } finally {
    loadingParticipants = null;
  }
}

$: activeUsers = users.filter(u => !u.disabled_at);
$: disabledUsers = users.filter(u => u.disabled_at);
$: activeSessions = sessions.filter(s => s.status !== 'cancelled');
$: cancelledSessions = sessions.filter(s => s.status === 'cancelled');

$: filteredUsers = searchQuery
  ? users.filter(u => u.email.toLowerCase().includes(searchQuery.toLowerCase()))
  : users;

$: filteredSessions = searchQuery
  ? sessions.filter(s =>
      s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (s.coach_name ?? '').toLowerCase().includes(searchQuery.toLowerCase())
    )
  : sessions;

async function adminCancelSession(sessionId: string) {
  if (!confirm('Voulez-vous vraiment annuler cette séance ?')) return;
  cancellingId = sessionId;
  try {
    await apiFetch(`/admin/sessions/${sessionId}/cancel`, { method: 'PUT' });
    await loadDashboardData();
  } catch (e) {
    error = "Erreur lors de l'annulation de la séance.";
  } finally {
    cancellingId = '';
  }
}

async function loadDashboardData() {
  loading = true;
  try {
    const usersRes = await getAdminUsers();
    users = usersRes?.items ?? [];
    const adminSessionsRes = await apiFetch('/admin/sessions/?limit=100&offset=0');
    const items = adminSessionsRes?.items ?? [];
    sessions = items.map((s: any) => ({
      ...s,
      coach_name: s.coach_name ?? null
    }));
  } catch (e) {
    error = "Erreur lors du chargement des données.";
  } finally {
    loading = false;
  }
}

onMount(() => {
  ready = true;
  loadDashboardData();
});

afterNavigate(() => {
  loadDashboardData();
});
</script>

<style>
.dashboard-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
  min-height: calc(100vh - 140px);
}

/* SIDEBAR */
.sidebar { display: flex; flex-direction: column; gap: 20px; }
.profile-card {
  background: #fff;
  border-radius: 18px;
  padding: 32px 20px 24px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.avatar {
  width: 76px; height: 76px; border-radius: 50%;
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white; font-size: 1.8rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 14px;
  box-shadow: 0 4px 16px rgba(153,27,27,0.18);
  text-transform: uppercase;
}
.profile-name { font-size: 1.1rem; font-weight: 700; color: #111827; margin-bottom: 2px; letter-spacing: -0.01em; }
.profile-role { color: #9ca3af; font-size: 0.8rem; font-style: italic; font-weight: 400; }

.stats-card {
  background: #fff;
  border-radius: 18px; padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.stat-row {
  display: flex; align-items: center; gap: 14px;
  padding: 14px 0; border-bottom: 1px solid #f5f5f5;
}
.stat-row:last-child { border-bottom: none; }
.stat-icon {
  width: 40px; height: 40px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: 800; flex-shrink: 0;
}
.stat-icon.blue { background: #eff6ff; color: #3b82f6; }
.stat-icon.green { background: #f0fdf4; color: #22c55e; }
.stat-icon.red { background: #fef2f2; color: #ef4444; }
.stat-icon.purple { background: #faf5ff; color: #a855f7; }
.stat-num { font-size: 1.5rem; font-weight: 800; color: #111827; line-height: 1; letter-spacing: -0.02em; }
.stat-label { font-size: 0.72rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 500; }

.sidebar-nav {
  background: #fff;
  border-radius: 18px; padding: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.sidebar-nav a, .sidebar-nav button.nav-btn {
  display: flex; align-items: center; gap: 10px;
  padding: 11px 14px; color: #6b7280; text-decoration: none;
  border-radius: 12px; font-size: 0.88rem; font-weight: 500;
  transition: background 0.15s, color 0.15s;
  width: 100%; background: none; border: none; cursor: pointer; box-shadow: none;
}
.sidebar-nav a:hover, .sidebar-nav button.nav-btn:hover { background: #f9fafb; color: #111827; }

/* MAIN */
.main-content { display: flex; flex-direction: column; gap: 24px; }
.welcome-title { font-size: 2rem; font-weight: 800; color: #111827; letter-spacing: -0.02em; }
.welcome-title span { color: #991b1b; font-weight: 800; }

.search-bar {
  display: flex; background: #fff;
  border-radius: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none; overflow: hidden;
}
.search-bar input {
  flex: 1; border: none; padding: 15px 20px; font-size: 0.92rem;
  outline: none; background: transparent; color: #374151;
}
.search-bar .search-btn {
  background: #1f2937; color: white; border: none; padding: 0 20px;
  cursor: pointer; font-size: 0.88rem; font-weight: 600; border-radius: 0; box-shadow: none;
  transition: background 0.15s;
}
.search-bar .search-btn:hover { background: #374151; }

.tab-bar {
  display: flex; gap: 4px;
}
.tab-btn {
  padding: 10px 22px; border: none; border-radius: 10px;
  font-weight: 600; font-size: 0.88rem; cursor: pointer;
  transition: all 0.2s; box-shadow: none;
}
.tab-btn.active { background: #fff; color: #111827; box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04); }
.tab-btn:not(.active) { background: transparent; color: #9ca3af; border: none; }
.tab-btn:not(.active):hover { color: #6b7280; background: rgba(255,255,255,0.5); }

.panel {
  background: #fff;
  border-radius: 18px;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.section-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
}
.section-title { font-size: 1.15rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.01em; }

/* CARDS */
.card-item {
  display: flex; align-items: center; gap: 16px;
  padding: 18px 20px; border-radius: 14px;
  background: #fafafa; border: none;
  margin-bottom: 10px; transition: transform 0.15s, box-shadow 0.15s;
}
.card-item:last-child { margin-bottom: 0; }
.card-item:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(0,0,0,0.05); background: #f5f5f5; }

.card-item-wrapper { margin-bottom: 10px; }
.card-item-wrapper:last-child { margin-bottom: 0; }
.card-item-wrapper .card-item { margin-bottom: 0; }
.participants-dropdown {
  background: #fafafa; border: none; border-top: 1px solid #f0f0f0;
  border-radius: 0 0 14px 14px; padding: 14px 20px;
  animation: slideOpen 0.2s ease-out;
}
.participants-dropdown .p-title {
  font-weight: 600; font-size: 0.8rem; color: #6b7280; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.04em;
}
.participants-dropdown ul {
  list-style: none; margin: 0; padding: 0;
}
.participants-dropdown li {
  padding: 8px 12px; font-size: 0.86rem; color: #374151;
  border-bottom: 1px solid #f5f5f5; display: flex; align-items: center; gap: 10px;
}
.participants-dropdown li:last-child { border-bottom: none; }
.p-avatar {
  width: 30px; height: 30px; border-radius: 50%; font-size: 0.62rem;
  background: #374151; color: white; display: flex; align-items: center;
  justify-content: center; font-weight: 700; flex-shrink: 0; text-transform: uppercase;
}
.p-empty { color: #9ca3af; font-style: italic; font-size: 0.82rem; padding: 8px 0; }
.p-loading { text-align: center; padding: 12px 0; color: #9ca3af; font-size: 0.82rem; }
@keyframes slideOpen { from { opacity: 0; max-height: 0; } to { opacity: 1; max-height: 300px; } }

.card-icon {
  width: 42px; height: 42px; border-radius: 12px;
  background: #374151;
  color: white; display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: 800; flex-shrink: 0;
}
.card-icon.blue-icon { background: #3b82f6; }
.card-info { flex: 1; min-width: 0; }
.card-title { font-weight: 600; font-size: 0.95rem; color: #111827; }
.card-sub { font-size: 0.8rem; color: #9ca3af; margin-top: 3px; }
.card-badge {
  font-size: 0.7rem; font-weight: 600; padding: 4px 10px;
  border-radius: 20px; white-space: nowrap; letter-spacing: 0.01em;
}
.badge-active { background: #f0fdf4; color: #16a34a; }
.badge-disabled { background: #fef2f2; color: #ef4444; }
.badge-cancelled { background: #fef2f2; color: #ef4444; }
.card-price { font-size: 0.92rem; font-weight: 700; color: #111827; white-space: nowrap; }

.card-actions { display: flex; gap: 6px; flex-shrink: 0; flex-wrap: wrap; }
.btn-action {
  background: #f3f4f6; color: #374151; border: none;
  padding: 7px 14px; border-radius: 8px; font-size: 0.78rem;
  font-weight: 600; cursor: pointer; transition: all 0.15s; box-shadow: none;
  text-decoration: none; display: inline-block;
}
.btn-action:hover { background: #e5e7eb; color: #111827; }
.btn-action.green { background: #f0fdf4; color: #16a34a; }
.btn-action.green:hover { background: #dcfce7; color: #15803d; }
.btn-cancel {
  background: #fef2f2; color: #dc2626; border: none;
  padding: 7px 14px; border-radius: 8px; font-size: 0.78rem;
  font-weight: 600; cursor: pointer; transition: all 0.15s; box-shadow: none;
}
.btn-cancel:hover { background: #fee2e2; color: #b91c1c; }

.empty-state { text-align: center; padding: 40px 16px; color: #9ca3af; font-style: italic; }

.error-message {
  color: #991b1b; background: #fef2f2;
  padding: 12px 16px; border-radius: 12px; text-align: center; font-size: 0.88rem;
}
.spinner {
  display: inline-block; width: 32px; height: 32px;
  border: 2.5px solid #f0f0f0; border-top-color: #6b7280;
  border-radius: 50%; animation: spin 0.7s linear infinite; margin: 28px auto;
}
.loading-center { text-align: center; padding: 60px 0; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .dashboard-layout { grid-template-columns: 1fr; }
  .sidebar { order: 2; }
  .main-content { order: 1; }
  .card-item { flex-wrap: wrap; gap: 10px; }
}
</style>

{#if ready}
<div class="dashboard-layout" in:fade={{ duration: 300 }}>
  <!-- SIDEBAR -->
  <aside class="sidebar" in:fly={{ x: -30, duration: 400 }}>
    <div class="profile-card">
      <div class="avatar">{firstName ? firstName[0] : '?'}{lastName ? lastName[0] : ''}</div>
      <div class="profile-name">{firstName} {lastName}</div>
      <div class="profile-role">Administrateur</div>
    </div>

    <div class="stats-card">
      <div class="stat-row">
        <div class="stat-icon blue">U</div>
        <div>
          <div class="stat-num">{users.length}</div>
          <div class="stat-label">utilisateurs</div>
        </div>
      </div>
      <div class="stat-row">
        <div class="stat-icon green">A</div>
        <div>
          <div class="stat-num">{activeUsers.length}</div>
          <div class="stat-label">utilisateurs actifs</div>
        </div>
      </div>
      <div class="stat-row">
        <div class="stat-icon purple">S</div>
        <div>
          <div class="stat-num">{sessions.length}</div>
          <div class="stat-label">séances total</div>
        </div>
      </div>
      <div class="stat-row">
        <div class="stat-icon red">X</div>
        <div>
          <div class="stat-num">{cancelledSessions.length}</div>
          <div class="stat-label">séances annulées</div>
        </div>
      </div>
    </div>

    <nav class="sidebar-nav">
      <a href="/">Accueil</a>
      <button class="nav-btn" class:active={activeTab === 'users'} on:click={() => activeTab = 'users'}>Utilisateurs</button>
      <button class="nav-btn" class:active={activeTab === 'sessions'} on:click={() => activeTab = 'sessions'}>Séances</button>
    </nav>
  </aside>

  <!-- MAIN -->
  <div class="main-content">
    <div class="welcome-title" in:fly={{ y: -15, duration: 400 }}>
      Tableau de bord <span>Admin</span>
    </div>

    <div class="search-bar" in:fly={{ y: 10, duration: 350, delay: 100 }}>
      <input type="text" placeholder={activeTab === 'users' ? 'Rechercher un utilisateur...' : 'Rechercher une séance...'} bind:value={searchQuery} />
      <button class="search-btn">Q</button>
    </div>

    {#if loading}
      <div class="loading-center" in:fade>
        <div class="spinner"></div>
        <div style="color: #9ca3af; margin-top: 8px;">Chargement des données…</div>
      </div>
    {:else if error}
      <div class="error-message" in:fade>{error}</div>
    {:else}
      <div class="tab-bar" in:fly={{ y: 10, duration: 300, delay: 120 }}>
        <button class="tab-btn" class:active={activeTab === 'users'} on:click={() => activeTab = 'users'}>Utilisateurs ({users.length})</button>
        <button class="tab-btn" class:active={activeTab === 'sessions'} on:click={() => activeTab = 'sessions'}>Séances ({sessions.length})</button>
      </div>

      {#if activeTab === 'users'}
        <div class="panel" in:fly={{ y: 15, duration: 350, delay: 150 }}>
          <div class="section-header">
            <h2 class="section-title">Gestion des utilisateurs</h2>
            <a href="/dashboard/admin/users/registration" class="btn-action">+ Créer un utilisateur</a>
          </div>
          {#if filteredUsers.length === 0}
            <div class="empty-state">Aucun utilisateur trouvé.</div>
          {:else}
            {#each filteredUsers as user, i}
              <div class="card-item" in:fly={{ x: -20, duration: 250, delay: 200 + i * 50 }}>
                <div class="card-icon blue-icon">U</div>
                <div class="card-info">
                  <div class="card-title">{user.email}</div>
                  <div class="card-sub">{user.roles ? user.roles.join(', ') : 'Aucun rôle'}</div>
                </div>
                <span class="card-badge" class:badge-active={!user.disabled_at} class:badge-disabled={user.disabled_at}>
                  {user.disabled_at ? 'Désactivé' : 'Actif'}
                </span>
                <div class="card-actions">
                  <a href={`/dashboard/admin/users/${user.id}/edit`} class="btn-action">Modifier</a>
                </div>
              </div>
            {/each}
          {/if}
        </div>
      {:else}
        <div class="panel" in:fly={{ y: 15, duration: 350, delay: 150 }}>
          <div class="section-header">
            <h2 class="section-title">Gestion des séances</h2>
          </div>
          {#if filteredSessions.length === 0}
            <div class="empty-state">Aucune séance trouvée.</div>
          {:else}
            {#each filteredSessions as s, i}
              <div class="card-item-wrapper" in:fly={{ x: -20, duration: 250, delay: 200 + i * 50 }}>
                <div class="card-item">
                  <div class="card-icon">S</div>
                  <div class="card-info">
                    <div class="card-title">{s.title}</div>
                    <div class="card-sub">Coach : {s.coach_name ?? '-'} — {new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                  </div>
                  <div class="card-price">{formatPrice(s.price_cents, s.currency)}</div>
                  <span class="card-badge" class:badge-active={s.status !== 'cancelled'} class:badge-cancelled={s.status === 'cancelled'}>
                    {s.status === 'cancelled' ? 'Annulée' : 'Active'}
                  </span>
                  <div class="card-actions">
                    <button class="btn-action green" on:click={() => toggleParticipants(s.id)}>Participants</button>
                    {#if s.status !== 'cancelled'}
                      <a href={`/dashboard/coach/sessions/${s.id}/edit`} class="btn-action">Modifier</a>
                      <button class="btn-cancel" on:click={() => adminCancelSession(s.id)} disabled={cancellingId === s.id}>
                        {cancellingId === s.id ? '...' : 'Annuler'}
                      </button>
                    {/if}
                  </div>
                </div>
                {#if expandedSession === s.id}
                  <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                    <div class="p-title">Participants inscrits</div>
                    {#if loadingParticipants === s.id}
                      <div class="p-loading">Chargement...</div>
                    {:else if !participantsCache[s.id] || participantsCache[s.id].length === 0}
                      <div class="p-empty">Aucun participant inscrit.</div>
                    {:else}
                      <ul>
                        {#each participantsCache[s.id] as p}
                          <li>
                            <span class="p-avatar">{(p.first_name?.[0] ?? '')}{(p.last_name?.[0] ?? '')}</span>
                            {p.first_name} {p.last_name}
                          </li>
                        {/each}
                      </ul>
                    {/if}
                  </div>
                {/if}
              </div>
            {/each}
          {/if}
        </div>
      {/if}
    {/if}
  </div>
</div>
{/if}