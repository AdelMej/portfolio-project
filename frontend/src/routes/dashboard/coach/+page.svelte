<!-- COACH DASHBOARD: /frontend/src/routes/dashboard/coach/+page.svelte -->
<script lang="ts">
import { onMount } from 'svelte';
import { goto } from '$app/navigation';
import { fly, fade } from 'svelte/transition';
import { apiFetch } from '$lib/api/client';
import { auth } from '$lib/stores/auth.store';
import { listCoachSessions, type CompleteSession } from '$lib/api/sessions.api';
import SessionIcon from '$lib/components/SessionIcon.svelte';
import { Search } from 'lucide-svelte';

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

let sessions: CompleteSession[] = [];
let loading = true;
let error = '';
let ready = false;
let searchQuery = '';
let expandedSession: string | null = null;

function toggleParticipants(id: string) {
  expandedSession = expandedSession === id ? null : id;
}

// Calendar
let calendarDate = new Date();
$: calendarYear = calendarDate.getFullYear();
$: calendarMonth = calendarDate.getMonth();
$: calendarMonthName = calendarDate.toLocaleString('fr-FR', { month: 'long', year: 'numeric' });
$: calendarDays = buildCalendar(calendarYear, calendarMonth);
$: sessionDates = new Set(sessions.map(s => {
  const d = new Date(s.starts_at);
  return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
}));

function buildCalendar(year: number, month: number) {
  const first = new Date(year, month, 1);
  const last = new Date(year, month + 1, 0);
  const startDay = first.getDay();
  const days: (number | null)[] = [];
  for (let i = 0; i < startDay; i++) days.push(null);
  for (let d = 1; d <= last.getDate(); d++) days.push(d);
  return days;
}
function prevMonth() { calendarDate = new Date(calendarYear, calendarMonth - 1, 1); }
function nextMonth() { calendarDate = new Date(calendarYear, calendarMonth + 1, 1); }
function isToday(day: number | null) {
  if (!day) return false;
  const now = new Date();
  return day === now.getDate() && calendarMonth === now.getMonth() && calendarYear === now.getFullYear();
}
function hasSession(day: number | null) {
  if (!day) return false;
  return sessionDates.has(`${calendarYear}-${calendarMonth}-${day}`);
}

// Stats
$: activeSessions = sessions.filter(s => s.status !== 'cancelled');
$: cancelledSessions = sessions.filter(s => s.status === 'cancelled');
$: totalRevenue = sessions.reduce((sum, s) => sum + (s.price_cents ?? 0), 0);

// Filtered
$: filteredSessions = searchQuery
  ? sessions.filter(s => s.title.toLowerCase().includes(searchQuery.toLowerCase()))
  : sessions;

$: now = new Date();
$: activeFiltered = filteredSessions
  .filter(s => s.status !== 'cancelled' && new Date(s.ends_at) >= now)
  .sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());
$: finishedFiltered = filteredSessions
  .filter(s => s.status !== 'cancelled' && new Date(s.ends_at) < now)
  .sort((a, b) => new Date(b.starts_at).getTime() - new Date(a.starts_at).getTime());
$: cancelledFiltered = filteredSessions
  .filter(s => s.status === 'cancelled')
  .sort((a, b) => new Date(b.starts_at).getTime() - new Date(a.starts_at).getTime());

async function loadSessions() {
  loading = true;
  error = '';
  try {
    sessions = await listCoachSessions();
  } catch (e) {
    console.error(e);
    error = 'Impossible de charger les séances';
  } finally {
    loading = false;
  }
}

async function cancelSession(id: string) {
  if (!confirm('Voulez-vous vraiment annuler cette séance ?')) return;
  try {
    await apiFetch(`/sessions/${id}/cancel`, { method: 'PUT' });
    await loadSessions();
  } catch (e) {
    console.error(e);
    alert("Impossible d'annuler la séance");
  }
}

onMount(() => {
  ready = true;
  loadSessions();
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
.stat-icon.red { background: #fef2f2; color: #ef4444; }
.stat-num { font-size: 1.5rem; font-weight: 800; color: #111827; line-height: 1; letter-spacing: -0.02em; }
.stat-label { font-size: 0.72rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 500; }

.calendar-card {
  background: #fff;
  border-radius: 18px; padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.cal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.cal-header span { font-weight: 600; font-size: 0.9rem; color: #111827; text-transform: capitalize; }
.cal-btn {
  background: none; border: none; font-size: 1rem; cursor: pointer;
  color: #9ca3af; padding: 4px 8px; border-radius: 8px; transition: all 0.15s; box-shadow: none;
}
.cal-btn:hover { background: #f5f5f5; color: #374151; }
.cal-grid { display: grid; grid-template-columns: repeat(7,1fr); gap: 2px; text-align: center; font-size: 0.78rem; }
.cal-day-label { font-weight: 600; color: #9ca3af; padding: 4px 0; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.04em; }
.cal-day { padding: 5px 0; border-radius: 8px; color: #6b7280; font-size: 0.8rem; position: relative; }
.cal-day.today { background: #111827; color: white; font-weight: 600; }
.cal-day.has-session { background: #eff6ff; color: #3b82f6; font-weight: 600; }
.cal-day.has-session::after {
  content: ''; position: absolute; bottom: 2px; left: 50%; transform: translateX(-50%);
  width: 4px; height: 4px; background: #3b82f6; border-radius: 50%;
}

.sidebar-nav {
  background: #fff;
  border-radius: 18px; padding: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.sidebar-nav a {
  display: flex; align-items: center; gap: 10px;
  padding: 11px 14px; color: #6b7280; text-decoration: none;
  border-radius: 12px; font-size: 0.88rem; font-weight: 500;
  transition: background 0.15s, color 0.15s;
}
.sidebar-nav a:hover { background: #f9fafb; color: #111827; }
.sidebar-nav a.active { background: #111827; color: white; }

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

.sessions-panel {
  background: #fff;
  border-radius: 18px; padding: 28px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.section-title { font-size: 1.15rem; font-weight: 700; color: #111827; margin: 0 0 20px 0; letter-spacing: -0.01em; }

.session-card {
  display: flex; align-items: center; gap: 16px;
  padding: 18px 20px; border-radius: 14px;
  background: #fafafa; border: none;
  margin-bottom: 10px; transition: transform 0.15s, box-shadow 0.15s;
}
.session-card:last-child { margin-bottom: 0; }
.session-card:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(0,0,0,0.05); background: #f5f5f5; }

.session-card-wrapper { margin-bottom: 10px; }
.session-card-wrapper:last-child { margin-bottom: 0; }
.session-card-wrapper .session-card { margin-bottom: 0; }
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
@keyframes slideOpen { from { opacity: 0; max-height: 0; } to { opacity: 1; max-height: 300px; } }

.session-icon {
  width: 42px; height: 42px; border-radius: 12px;
  background: #374151;
  color: white; display: flex; align-items: center; justify-content: center;
  font-size: 0.85rem; font-weight: 800; flex-shrink: 0;
}
.session-info { flex: 1; min-width: 0; }
.session-title-text { font-weight: 600; font-size: 0.95rem; color: #111827; text-transform: capitalize; }
.session-date-text { font-size: 0.8rem; color: #9ca3af; margin-top: 3px; }
.session-price-text { font-size: 0.92rem; font-weight: 700; color: #111827; white-space: nowrap; }
.session-status {
  font-size: 0.7rem; font-weight: 600; padding: 4px 10px;
  border-radius: 20px; white-space: nowrap; letter-spacing: 0.01em;
}
.status-active { background: #f0fdf4; color: #16a34a; }
.status-cancelled { background: #fef2f2; color: #ef4444; }
.status-passed { background: #f3f4f6; color: #6b7280; }

.session-actions { display: flex; gap: 6px; flex-shrink: 0; flex-wrap: wrap; }
.btn-action {
  background: #f3f4f6; color: #374151; border: none;
  padding: 7px 14px; border-radius: 8px; font-size: 0.78rem;
  font-weight: 600; cursor: pointer; transition: all 0.15s; box-shadow: none;
  text-decoration: none; display: inline-block;
}
.btn-action:hover { background: #e5e7eb; color: #111827; }
.btn-action.green { background: #f0fdf4; color: #16a34a; }
.btn-action.green:hover { background: #dcfce7; color: #15803d; }
.btn-action.purple { background: #faf5ff; color: #a855f7; }
.btn-action.purple:hover { background: #f3e8ff; color: #7c3aed; }
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

.group-header {
  font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
  padding: 14px 0 8px; margin-top: 8px; border-bottom: 2px solid #f0f0f0;
}
.group-header:first-child { margin-top: 0; }
.active-header { color: #16a34a; border-bottom-color: #bbf7d0; }
.finished-header { color: #6b7280; border-bottom-color: #e5e7eb; }
.cancelled-header { color: #dc2626; border-bottom-color: #fecaca; }

@media (max-width: 768px) {
  .dashboard-layout { grid-template-columns: 1fr; }
  .sidebar { order: 2; }
  .main-content { order: 1; }
  .session-card { flex-wrap: wrap; gap: 10px; }
}
</style>

{#if ready}
<div class="dashboard-layout" in:fade={{ duration: 300 }}>
  <!-- SIDEBAR -->
  <aside class="sidebar" in:fly={{ x: -30, duration: 400 }}>
    <div class="profile-card">
      <div class="avatar">{firstName ? firstName[0] : '?'}{lastName ? lastName[0] : ''}</div>
      <div class="profile-name">{firstName} {lastName}</div>
      <div class="profile-role">Coach</div>
    </div>

    <div class="stats-card">
      <div class="stat-row">
        <div class="stat-icon blue">S</div>
        <div>
          <div class="stat-num">{activeSessions.length}</div>
          <div class="stat-label">séances actives</div>
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

    <div class="calendar-card">
      <div class="cal-header">
        <button class="cal-btn" on:click={prevMonth}>‹</button>
        <span>{calendarMonthName}</span>
        <button class="cal-btn" on:click={nextMonth}>›</button>
      </div>
      <div class="cal-grid">
        {#each ['D','L','M','M','J','V','S'] as label}
          <div class="cal-day-label">{label}</div>
        {/each}
        {#each calendarDays as day}
          <div class="cal-day" class:today={isToday(day)} class:has-session={hasSession(day)}>
            {day ?? ''}
          </div>
        {/each}
      </div>
    </div>

    <nav class="sidebar-nav">
      <a href="/">Accueil</a>
      <a href="/dashboard/coach" class="active">Mes séances</a>
      <a href="/sessions/create">Créer une séance</a>
    </nav>
  </aside>

  <!-- MAIN -->
  <div class="main-content">
    <div class="welcome-title" in:fly={{ y: -15, duration: 400 }}>
      Tableau de bord <span>Coach</span>
    </div>

    <div class="search-bar" in:fly={{ y: 10, duration: 350, delay: 100 }}>
      <input type="text" placeholder="Rechercher une séance..." bind:value={searchQuery} />
      <button class="search-btn"><Search size={18} /></button>
    </div>

    {#if loading}
      <div class="loading-center" in:fade>
        <div class="spinner"></div>
        <div style="color: #9ca3af; margin-top: 8px;">Chargement des séances…</div>
      </div>
    {:else if error}
      <div class="error-message" in:fade>{error}</div>
    {:else}
      <div class="sessions-panel" in:fly={{ y: 15, duration: 350, delay: 150 }}>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <h2 class="section-title" style="margin:0;">Mes séances ({filteredSessions.length})</h2>
          <a href="/sessions/create" class="btn-action">+ Créer une séance</a>
        </div>
        {#if filteredSessions.length === 0}
          <div class="empty-state">Aucune séance trouvée.</div>
        {:else}
          {#if activeFiltered.length > 0}
            <div class="group-header active-header">Actives ({activeFiltered.length})</div>
            {#each activeFiltered as s, i}
              <div class="session-card-wrapper" in:fly={{ x: -20, duration: 250, delay: 100 + i * 40 }}>
                <div class="session-card">
                  <div class="session-icon"><SessionIcon title={s.title} size={20} /></div>
                  <div class="session-info">
                    <div class="session-title-text">{s.title}</div>
                    <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                  </div>
                  <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
                  <span class="session-status status-active">Active</span>
                  <div class="session-actions">
                    <button class="btn-action green" on:click={() => toggleParticipants(s.id)}>Participants ({s.participants?.length ?? 0})</button>
                    <a href={`/sessions/${s.id}/attendance`} class="btn-action purple">Présence</a>
                    <button class="btn-cancel" on:click={() => cancelSession(s.id)}>Annuler</button>
                    <a href={`/dashboard/coach/sessions/${s.id}/edit`} class="btn-action">Modifier</a>
                  </div>
                </div>
                {#if expandedSession === s.id}
                  <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                    <div class="p-title">Participants inscrits ({s.participants?.length ?? 0})</div>
                    {#if !s.participants || s.participants.length === 0}
                      <div class="p-empty">Aucun participant inscrit.</div>
                    {:else}
                      <ul>
                        {#each s.participants as p}
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

          {#if finishedFiltered.length > 0}
            <div class="group-header finished-header">Terminées ({finishedFiltered.length})</div>
            {#each finishedFiltered as s, i}
              <div class="session-card-wrapper" in:fly={{ x: -20, duration: 250, delay: 100 + i * 40 }}>
                <div class="session-card">
                  <div class="session-icon"><SessionIcon title={s.title} size={20} /></div>
                  <div class="session-info">
                    <div class="session-title-text">{s.title}</div>
                    <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                  </div>
                  <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
                  <span class="session-status status-passed">Terminée</span>
                  <div class="session-actions">
                    <button class="btn-action green" on:click={() => toggleParticipants(s.id)}>Participants ({s.participants?.length ?? 0})</button>
                  </div>
                </div>
                {#if expandedSession === s.id}
                  <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                    <div class="p-title">Participants inscrits ({s.participants?.length ?? 0})</div>
                    {#if !s.participants || s.participants.length === 0}
                      <div class="p-empty">Aucun participant inscrit.</div>
                    {:else}
                      <ul>
                        {#each s.participants as p}
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

          {#if cancelledFiltered.length > 0}
            <div class="group-header cancelled-header">Annulées ({cancelledFiltered.length})</div>
            {#each cancelledFiltered as s, i}
              <div class="session-card-wrapper" in:fly={{ x: -20, duration: 250, delay: 100 + i * 40 }}>
                <div class="session-card">
                  <div class="session-icon"><SessionIcon title={s.title} size={20} /></div>
                  <div class="session-info">
                    <div class="session-title-text">{s.title}</div>
                    <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                  </div>
                  <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
                  <span class="session-status status-cancelled">Annulée</span>
                  <div class="session-actions">
                    <button class="btn-action green" on:click={() => toggleParticipants(s.id)}>Participants ({s.participants?.length ?? 0})</button>
                  </div>
                </div>
                {#if expandedSession === s.id}
                  <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                    <div class="p-title">Participants inscrits ({s.participants?.length ?? 0})</div>
                    {#if !s.participants || s.participants.length === 0}
                      <div class="p-empty">Aucun participant inscrit.</div>
                    {:else}
                      <ul>
                        {#each s.participants as p}
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
        {/if}
      </div>
    {/if}
  </div>
</div>
{/if}