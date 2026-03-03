<script lang="ts">
import { onMount } from 'svelte';
import { fly, fade } from 'svelte/transition';
import { apiFetch } from '$lib/api/client';
import { goto } from '$app/navigation';
import { auth } from '$lib/stores/auth.store';
import { listSessions, type Session } from '$lib/api/sessions.api';

function formatPrice(cents?: number, currency?: string): string {
  if (cents == null) return '-';
  return (cents / 100).toFixed(2) + ' ' + (currency ?? 'EUR');
}

let firstName = '';
let lastName = '';
let email = '';
auth.subscribe((v) => {
  firstName = v.firstName ?? '';
  lastName = v.lastName ?? '';
  email = v.email ?? '';
});

let mySessions: Session[] = [];
let availableSessions: Session[] = [];

let loading = true;
let error = '';
let ready = false;
let joiningId = '';
let searchQuery = '';

// Calendar state
let calendarDate = new Date();
$: calendarYear = calendarDate.getFullYear();
$: calendarMonth = calendarDate.getMonth();
$: calendarMonthName = calendarDate.toLocaleString('fr-FR', { month: 'long', year: 'numeric' });
$: calendarDays = buildCalendar(calendarYear, calendarMonth);
$: sessionDates = new Set(mySessions.map(s => {
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
$: totalSpent = mySessions.reduce((sum, s) => sum + (s.price_cents ?? 0), 0);
$: nextSession = mySessions
  .map(s => new Date(s.starts_at))
  .filter(d => d > new Date())
  .sort((a, b) => a.getTime() - b.getTime())[0] ?? null;
$: daysUntilNext = nextSession ? Math.ceil((nextSession.getTime() - Date.now()) / 86400000) : null;

// Filtered sessions
$: filteredMySessions = searchQuery
  ? mySessions.filter(s => s.title.toLowerCase().includes(searchQuery.toLowerCase()) || s.coach_name.toLowerCase().includes(searchQuery.toLowerCase()))
  : mySessions;
$: filteredAvailable = searchQuery
  ? availableSessions.filter(s => s.title.toLowerCase().includes(searchQuery.toLowerCase()) || s.coach_name.toLowerCase().includes(searchQuery.toLowerCase()))
  : availableSessions;

onMount(() => {
  ready = true;
  loadDashboard();
});

async function loadSessions(): Promise<Session[]> {
    return listSessions();
}

async function loadMyRegistrations(): Promise<string[]> {
    try {
      const res = await apiFetch('/me/sessions/');
      const items = Array.isArray(res.items) ? res.items : Array.isArray(res) ? res : [];
      return items.map((s: Session) => s.id);
    } catch {
      return [];
    }
}

async function joinSession(sessionId: string) {
  joiningId = sessionId;
  try {

    const res =await apiFetch(`/sessions/${sessionId}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    console.log('Join session response:', res);
    if (res && res.require_payment) {
      if (res.payment_url) {
        window.location.href = res.payment_url;
      } else {
        alert('Le paiement est requis, mais aucun lien de paiement n\'a été fourni.');
      }
      return;
    }
    const session = availableSessions.find(s => s.id === sessionId);
    if (session) {
      mySessions = [...mySessions, session];
      availableSessions = availableSessions.filter(s => s.id !== sessionId);
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
    const [sessions, registeredIds] = await Promise.all([
      loadSessions(),
      loadMyRegistrations()
    ]);
    mySessions = sessions.filter(s => registeredIds.includes(s.id));
    availableSessions = sessions.filter(s => !registeredIds.includes(s.id));
  } catch (e) {
    console.error(e);
    error = 'Erreur lors du chargement';
  } finally {
    loading = false;
  }
}
</script>

<style>
/* ===== LAYOUT ===== */
.dashboard-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px;
  min-height: calc(100vh - 140px);
}

/* ===== SIDEBAR ===== */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.profile-card {
  background: rgba(255,255,255,0.95);
  border-radius: 16px;
  padding: 28px 20px 20px;
  text-align: center;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white;
  font-size: 2rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  box-shadow: 0 4px 12px rgba(153, 27, 27, 0.3);
  text-transform: uppercase;
}
.profile-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2px;
}
.profile-role {
  color: #991b1b;
  font-size: 0.85rem;
  font-style: italic;
}

.stats-card {
  background: rgba(255,255,255,0.95);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.stat-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f3f4f6;
}
.stat-row:last-child { border-bottom: none; }
.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}
.stat-icon.blue { background: #dbeafe; color: #2563eb; }
.stat-icon.green { background: #d1fae5; color: #059669; }
.stat-icon.orange { background: #ffedd5; color: #ea580c; }
.stat-num {
  font-size: 1.3rem;
  font-weight: 800;
  color: #1f2937;
  line-height: 1;
}
.stat-label {
  font-size: 0.78rem;
  color: #6b7280;
}

/* Calendar */
.calendar-card {
  background: rgba(255,255,255,0.95);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.cal-header span {
  font-weight: 700;
  font-size: 0.95rem;
  color: #1f2937;
  text-transform: capitalize;
}
.cal-btn {
  background: none;
  border: none;
  font-size: 1.1rem;
  cursor: pointer;
  color: #991b1b;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.15s;
  box-shadow: none;
}
.cal-btn:hover { background: #fef2f2; }
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  text-align: center;
  font-size: 0.8rem;
}
.cal-day-label {
  font-weight: 700;
  color: #6b7280;
  padding: 4px 0;
  font-size: 0.7rem;
}
.cal-day {
  padding: 5px 0;
  border-radius: 8px;
  color: #374151;
  font-size: 0.82rem;
  position: relative;
}
.cal-day.today {
  background: #991b1b;
  color: white;
  font-weight: 700;
}
.cal-day.has-session {
  background: #fef2f2;
  color: #991b1b;
  font-weight: 700;
}
.cal-day.has-session::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 5px;
  height: 5px;
  background: #dc2626;
  border-radius: 50%;
}

/* Sidebar nav */
.sidebar-nav {
  background: rgba(255,255,255,0.95);
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  color: #374151;
  text-decoration: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background 0.15s, color 0.15s;
}
.sidebar-nav a:hover { background: #fef2f2; color: #991b1b; }
.sidebar-nav a.active {
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white;
}

/* ===== MAIN CONTENT ===== */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.welcome-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1f2937;
}
.welcome-title span { color: #fff; background: #991b1b; padding: 2px 14px; border-radius: 20px; }

.search-bar {
  display: flex;
  background: rgba(255,255,255,0.95);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  overflow: hidden;
}
.search-bar input {
  flex: 1;
  border: none;
  padding: 14px 18px;
  font-size: 0.95rem;
  outline: none;
  background: transparent;
  color: #374151;
}
.search-bar button {
  background: #991b1b;
  color: white;
  border: none;
  padding: 0 18px;
  cursor: pointer;
  font-size: 1.1rem;
  border-radius: 0;
  box-shadow: none;
}

/* Session cards */
.section-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}
.sessions-panel {
  background: rgba(255,255,255,0.95);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
}
.session-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: #fef7f7;
  border: 1px solid #fecaca;
  margin-bottom: 12px;
  transition: transform 0.15s, box-shadow 0.15s;
}
.session-card:last-child { margin-bottom: 0; }
.session-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(153, 27, 27, 0.1);
}
.session-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.session-info { flex: 1; min-width: 0; }
.session-title-text {
  font-weight: 700;
  font-size: 1rem;
  color: #1f2937;
  text-transform: capitalize;
}
.session-date-text {
  font-size: 0.82rem;
  color: #6b7280;
  margin-top: 2px;
}
.session-coach-text {
  font-size: 0.85rem;
  color: #374151;
  white-space: nowrap;
}
.session-price-text {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1f2937;
  white-space: nowrap;
}
.session-status {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  white-space: nowrap;
}
.status-confirmed { background: #d1fae5; color: #065f46; }
.status-cancelled { background: #fee2e2; color: #991b1b; }
.session-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
.btn-cancel {
  background: #dc2626;
  color: white;
  border: none;
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: none;
}
.btn-cancel:hover { background: #b91c1c; }
.btn-join {
  background: #991b1b;
  color: white;
  border: none;
  padding: 7px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s;
  box-shadow: none;
}
.btn-join:hover { background: #7f1d1d; transform: translateY(-1px); }
.btn-join:disabled {
  background: #fca5a5;
  cursor: not-allowed;
  transform: none;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 32px 16px;
  color: #9ca3af;
}
.empty-state p {
  font-size: 1.1rem;
  font-style: italic;
  margin-bottom: 16px;
  color: #6b7280;
}
.btn-discover {
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 24px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(153, 27, 27, 0.2);
  transition: transform 0.15s, box-shadow 0.15s;
}
.btn-discover:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(153, 27, 27, 0.3);
}

.error-message {
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 16px;
  border-radius: 10px;
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
  padding: 60px 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 768px) {
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
  .sidebar { order: 2; }
  .main-content { order: 1; }
  .session-card {
    flex-wrap: wrap;
    gap: 10px;
  }
}
</style>

{#if ready}
<div class="dashboard-layout" in:fade={{ duration: 300 }}>
  <!-- SIDEBAR -->
  <aside class="sidebar" in:fly={{ x: -30, duration: 400 }}>
    <div class="profile-card">
      <div class="avatar">{firstName ? firstName[0] : '?'}{lastName ? lastName[0] : ''}</div>
      <div class="profile-name">{firstName} {lastName}</div>
      <div class="profile-role">Client Fidèle</div>
    </div>

    <div class="stats-card">
      <div class="stat-row">
        <div class="stat-icon blue">📅</div>
        <div>
          <div class="stat-num">{mySessions.length}</div>
          <div class="stat-label">séances inscrites</div>
        </div>
      </div>
      <div class="stat-row">
        <div class="stat-icon green">€</div>
        <div>
          <div class="stat-num">{(totalSpent / 100).toFixed(0)} €</div>
          <div class="stat-label">dépensées</div>
        </div>
      </div>
      <div class="stat-row">
        <div class="stat-icon orange">P</div>
        <div>
          <div class="stat-num">{daysUntilNext !== null ? `${daysUntilNext}j` : '-'}</div>
          <div class="stat-label">{daysUntilNext !== null ? 'prochaine séance' : 'aucune à venir'}</div>
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
      <a href="/dashboard/user" class="active">Mes séances</a>
      <a href="/sessions">Trouver une séance</a>
    </nav>
  </aside>

  <!-- MAIN -->
  <div class="main-content">
    <div class="welcome-title" in:fly={{ y: -15, duration: 400 }}>
      Bienvenue, <span>{firstName || 'utilisateur'}</span>
    </div>

    <div class="search-bar" in:fly={{ y: 10, duration: 350, delay: 100 }}>
      <input type="text" placeholder="Rechercher une séance..." bind:value={searchQuery} />
      <button>Q</button>
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
        <h2 class="section-title">Mes séances inscrites</h2>
        {#if filteredMySessions.length === 0}
          <div class="empty-state">
            <p>Aucune séance inscrite.</p>
          </div>
        {:else}
          {#each filteredMySessions as s, i}
            <div class="session-card" in:fly={{ x: -20, duration: 250, delay: 200 + i * 60 }}>
              <div class="session-icon">S</div>
              <div class="session-info">
                <div class="session-title-text">{s.title}</div>
                <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
              </div>
              <div class="session-coach-text">{s.coach_name}</div>
              <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
              {#if s.status === 'cancelled'}
                <span class="session-status status-cancelled">Annulée</span>
              {:else}
                <span class="session-status status-confirmed">Confirmé</span>
                <div class="session-actions">
                  <button class="btn-cancel">Annuler</button>
                </div>
              {/if}
            </div>
          {/each}
        {/if}
      </div>

      <h2 class="section-title" in:fly={{ y: 15, duration: 350, delay: 250 }}>Séances disponibles</h2>
      {#if filteredAvailable.length === 0}
        <div class="sessions-panel" in:fade={{ delay: 300 }}>
          <div class="empty-state">
            <p>Aucune séance disponible pour le moment.</p>
            <button class="btn-discover" on:click={() => goto('/sessions')}>Découvrir les séances disponibles</button>
          </div>
        </div>
      {:else}
        <div class="sessions-panel" in:fly={{ y: 15, duration: 350, delay: 300 }}>
          {#each filteredAvailable as s, i}
            <div class="session-card" in:fly={{ x: -20, duration: 250, delay: 350 + i * 60 }}>
              <div class="session-icon">S</div>
              <div class="session-info">
                <div class="session-title-text">{s.title}</div>
                <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
              </div>
              <div class="session-coach-text">{s.coach_name}</div>
              <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
              {#if s.status === 'cancelled'}
                <span class="session-status status-cancelled">Annulée</span>
              {:else}
                <div class="session-actions">
                  <button class="btn-join" on:click={() => joinSession(s.id)} disabled={joiningId === s.id}>
                    {joiningId === s.id ? '...' : "S'inscrire"}
                  </button>
                </div>
              {/if}
            </div>
          {/each}
        </div>
      {/if}
    {/if}
  </div>
</div>
{/if}