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
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
  min-height: calc(100vh - 140px);
}

/* SIDEBAR */
.sidebar { display: flex; flex-direction: column; gap: 16px; }
.profile-card {
  background: rgba(255,255,255,0.95);
  border-radius: 16px;
  padding: 28px 20px 20px;
  text-align: center;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.avatar {
  width: 80px; height: 80px; border-radius: 50%;
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white; font-size: 2rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 12px;
  box-shadow: 0 4px 12px rgba(153,27,27,0.3);
  text-transform: uppercase;
}
.profile-name { font-size: 1.2rem; font-weight: 700; color: #1f2937; margin-bottom: 2px; }
.profile-role { color: #991b1b; font-size: 0.85rem; font-style: italic; }

.stats-card {
  background: rgba(255,255,255,0.95);
  border-radius: 16px; padding: 16px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.stat-row {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid #f3f4f6;
}
.stat-row:last-child { border-bottom: none; }
.stat-icon {
  width: 36px; height: 36px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: 800; flex-shrink: 0;
}
.stat-icon.blue { background: #dbeafe; color: #2563eb; }
.stat-icon.green { background: #d1fae5; color: #059669; }
.stat-icon.red { background: #fee2e2; color: #dc2626; }
.stat-icon.purple { background: #ede9fe; color: #7c3aed; }
.stat-num { font-size: 1.3rem; font-weight: 800; color: #1f2937; line-height: 1; }
.stat-label { font-size: 0.78rem; color: #6b7280; }

.sidebar-nav {
  background: rgba(255,255,255,0.95);
  border-radius: 16px; padding: 8px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.sidebar-nav a, .sidebar-nav button.nav-btn {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; color: #374151; text-decoration: none;
  border-radius: 10px; font-size: 0.9rem; font-weight: 500;
  transition: background 0.15s, color 0.15s;
  width: 100%; background: none; border: none; cursor: pointer; box-shadow: none;
}
.sidebar-nav a:hover, .sidebar-nav button.nav-btn:hover { background: #fef2f2; color: #991b1b; }

/* MAIN */
.main-content { display: flex; flex-direction: column; gap: 20px; }
.welcome-title { font-size: 1.8rem; font-weight: 800; color: #1f2937; }
.welcome-title span { color: #fff; background: #991b1b; padding: 2px 14px; border-radius: 20px; }

.search-bar {
  display: flex; background: rgba(255,255,255,0.95);
  border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); overflow: hidden;
}
.search-bar input {
  flex: 1; border: none; padding: 14px 18px; font-size: 0.95rem;
  outline: none; background: transparent; color: #374151;
}
.search-bar .search-btn {
  background: #991b1b; color: white; border: none; padding: 0 18px;
  cursor: pointer; font-size: 0.9rem; font-weight: 700; border-radius: 0; box-shadow: none;
}

.tab-bar {
  display: flex; gap: 8px;
}
.tab-btn {
  padding: 10px 20px; border: none; border-radius: 10px 10px 0 0;
  font-weight: 700; font-size: 0.95rem; cursor: pointer;
  transition: background 0.2s, color 0.2s;
  box-shadow: none;
}
.tab-btn.active { background: rgba(255,255,255,0.95); color: #991b1b; }
.tab-btn:not(.active) { background: rgba(255,255,255,0.5); color: #6b7280; }
.tab-btn:not(.active):hover { background: rgba(255,255,255,0.75); }

.panel {
  background: rgba(255,255,255,0.95);
  border-radius: 0 16px 16px 16px;
  padding: 24px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.section-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;
}
.section-title { font-size: 1.2rem; font-weight: 700; color: #1f2937; margin: 0; }

/* CARDS */
.card-item {
  display: flex; align-items: center; gap: 16px;
  padding: 16px; border-radius: 12px;
  background: #fef7f7; border: 1px solid #fecaca;
  margin-bottom: 12px; transition: transform 0.15s, box-shadow 0.15s;
}
.card-item:last-child { margin-bottom: 0; }
.card-item:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(153,27,27,0.1); }

.card-item-wrapper { margin-bottom: 12px; }
.card-item-wrapper:last-child { margin-bottom: 0; }
.card-item-wrapper .card-item { margin-bottom: 0; }
.participants-dropdown {
  background: #fff; border: 1px solid #fecaca; border-top: none;
  border-radius: 0 0 12px 12px; padding: 12px 16px;
  animation: slideOpen 0.2s ease-out;
}
.participants-dropdown .p-title {
  font-weight: 700; font-size: 0.85rem; color: #991b1b; margin-bottom: 8px;
}
.participants-dropdown ul {
  list-style: none; margin: 0; padding: 0;
}
.participants-dropdown li {
  padding: 6px 12px; font-size: 0.88rem; color: #374151;
  border-bottom: 1px solid #f3f4f6; display: flex; align-items: center; gap: 8px;
}
.participants-dropdown li:last-child { border-bottom: none; }
.p-avatar {
  width: 28px; height: 28px; border-radius: 50%; font-size: 0.65rem;
  background: #991b1b; color: white; display: flex; align-items: center;
  justify-content: center; font-weight: 700; flex-shrink: 0; text-transform: uppercase;
}
.p-empty { color: #9ca3af; font-style: italic; font-size: 0.85rem; padding: 8px 0; }
.p-loading { text-align: center; padding: 12px 0; color: #9ca3af; font-size: 0.85rem; }
@keyframes slideOpen { from { opacity: 0; max-height: 0; } to { opacity: 1; max-height: 300px; } }

.card-icon {
  width: 44px; height: 44px; border-radius: 12px;
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white; display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem; font-weight: 800; flex-shrink: 0;
}
.card-icon.blue-icon { background: linear-gradient(135deg, #2563eb, #3b82f6); }
.card-info { flex: 1; min-width: 0; }
.card-title { font-weight: 700; font-size: 1rem; color: #1f2937; }
.card-sub { font-size: 0.82rem; color: #6b7280; margin-top: 2px; }
.card-badge {
  font-size: 0.75rem; font-weight: 600; padding: 4px 10px;
  border-radius: 20px; white-space: nowrap;
}
.badge-active { background: #d1fae5; color: #065f46; }
.badge-disabled { background: #fee2e2; color: #991b1b; }
.badge-cancelled { background: #fee2e2; color: #991b1b; }
.card-price { font-size: 0.95rem; font-weight: 700; color: #1f2937; white-space: nowrap; }

.card-actions { display: flex; gap: 8px; flex-shrink: 0; flex-wrap: wrap; }
.btn-action {
  background: #991b1b; color: white; border: none;
  padding: 7px 14px; border-radius: 20px; font-size: 0.8rem;
  font-weight: 600; cursor: pointer; transition: background 0.2s; box-shadow: none;
  text-decoration: none; display: inline-block;
}
.btn-action:hover { background: #7f1d1d; }
.btn-action.green { background: #16a34a; }
.btn-action.green:hover { background: #15803d; }
.btn-cancel {
  background: #dc2626; color: white; border: none;
  padding: 7px 14px; border-radius: 20px; font-size: 0.8rem;
  font-weight: 600; cursor: pointer; transition: background 0.2s; box-shadow: none;
}
.btn-cancel:hover { background: #b91c1c; }

.empty-state { text-align: center; padding: 32px 16px; color: #6b7280; font-style: italic; }

.error-message {
  color: #991b1b; background: #fee2e2;
  padding: 10px 16px; border-radius: 10px; text-align: center;
}
.spinner {
  display: inline-block; width: 36px; height: 36px;
  border: 3px solid #e5e7eb; border-top-color: #991b1b;
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