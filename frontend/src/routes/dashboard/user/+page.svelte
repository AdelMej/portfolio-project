<script lang="ts">
import { onMount } from 'svelte';
import { fly, fade } from 'svelte/transition';
import { apiFetch } from '$lib/api/client';
import { goto } from '$app/navigation';
import { auth } from '$lib/stores/auth.store';
import { listSessions, type Session } from '$lib/api/sessions.api';
import SessionIcon from '$lib/components/SessionIcon.svelte';
import { Search, ChevronLeft, ChevronRight, X } from 'lucide-svelte';

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

// Participants state
let expandedSession: string | null = null;
let participantsCache: Record<string, {first_name: string; last_name: string}[]> = {};

function toggleParticipants(id: string) {
  if (expandedSession === id) { expandedSession = null; return; }
  expandedSession = id;
}

// Calendar state
let calendarDate = new Date();
let selectedDate: string | null = null;
$: calendarYear = calendarDate.getFullYear();
$: calendarMonth = calendarDate.getMonth();
$: calendarMonthName = calendarDate.toLocaleString('fr-FR', { month: 'long', year: 'numeric' });
$: calendarDays = buildCalendar(calendarYear, calendarMonth);

function toDateStr(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}
function todayStr(): string { return toDateStr(new Date()); }

$: mySessionDates = new Set(mySessions.map(s => toDateStr(new Date(s.starts_at))));
$: allSessionDates = new Set([...mySessions, ...availableSessions].map(s => toDateStr(new Date(s.starts_at))));

function buildCalendar(year: number, month: number): ({ day: number; dateStr: string } | null)[] {
  const first = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0).getDate();
  let startDow = first.getDay();
  startDow = startDow === 0 ? 6 : startDow - 1; // Mon=0
  const cells: ({ day: number; dateStr: string } | null)[] = [];
  for (let i = 0; i < startDow; i++) cells.push(null);
  for (let d = 1; d <= lastDay; d++) {
    const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    cells.push({ day: d, dateStr });
  }
  return cells;
}
function prevMonth() { calendarDate = new Date(calendarYear, calendarMonth - 1, 1); }
function nextMonth() { calendarDate = new Date(calendarYear, calendarMonth + 1, 1); }
function selectDay(dateStr: string) {
  selectedDate = selectedDate === dateStr ? null : dateStr;
}
function clearFilter() { selectedDate = null; }

// Stats
$: nextSession = mySessions
  .map(s => new Date(s.starts_at))
  .filter(d => d > new Date())
  .sort((a, b) => a.getTime() - b.getTime())[0] ?? null;
$: daysUntilNext = nextSession ? Math.ceil((nextSession.getTime() - Date.now()) / 86400000) : null;

// Helper: session status
function getStatus(s: Session): 'active' | 'finished' | 'cancelled' {
  if (s.status === 'cancelled') return 'cancelled';
  if (new Date(s.ends_at) < new Date()) return 'finished';
  return 'active';
}

// Apply search + date filter
function applyFilters(list: Session[], dateFilter: string | null, query: string): Session[] {
  let result = list;
  if (dateFilter) {
    result = result.filter(s => toDateStr(new Date(s.starts_at)) === dateFilter);
  }
  if (query) {
    const q = query.toLowerCase();
    result = result.filter(s => s.title.toLowerCase().includes(q) || s.coach_name.toLowerCase().includes(q));
  }
  return result;
}

// My sessions grouped by status
$: myFiltered = applyFilters(mySessions, selectedDate, searchQuery);
$: myActive = myFiltered.filter(s => getStatus(s) === 'active').sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());
$: myFinished = myFiltered.filter(s => getStatus(s) === 'finished').sort((a, b) => new Date(b.starts_at).getTime() - new Date(a.starts_at).getTime());
$: myCancelled = myFiltered.filter(s => getStatus(s) === 'cancelled').sort((a, b) => new Date(b.starts_at).getTime() - new Date(a.starts_at).getTime());

// Available sessions
$: joinableAvailable = availableSessions.filter(s => s.status !== 'cancelled' && new Date(s.ends_at) >= new Date());
$: filteredAvailable = applyFilters(joinableAvailable, selectedDate, searchQuery);

onMount(() => {
  ready = true;
  loadDashboard();
});

async function loadSessions(): Promise<Session[]> {
    const res = await apiFetch('/sessions');
    const items = Array.isArray(res.items) ? res.items : Array.isArray(res) ? res : [];
    // Cache participants from sessions response
    for (const s of items) {
      if (s.participants) {
        participantsCache[s.id] = s.participants;
      }
    }
    participantsCache = participantsCache;
    return items.map((raw: any) => ({
      id: raw.id,
      coach_id: raw.coach?.id ?? raw.coach_id ?? '',
      coach_name: raw.coach
        ? `${raw.coach.first_name} ${raw.coach.last_name}`
        : (raw.coach_name ?? 'Non défini'),
      title: raw.title,
      starts_at: raw.starts_at,
      ends_at: raw.ends_at,
      max_participants: raw.max_participants,
      price_cents: raw.price_cents,
      currency: raw.currency,
      status: raw.status,
    }));
}

async function loadMyRegistrations(): Promise<string[]> {
    try {
      const res = await apiFetch('/me/sessions/');
      const items = Array.isArray(res.items) ? res.items : Array.isArray(res) ? res : [];
      // Pre-populate participantsCache from /me/sessions/ data
      for (const s of items) {
        if (s.participants) {
          participantsCache[s.id] = s.participants;
        }
      }
      participantsCache = participantsCache;
      return items.map((s: any) => s.id);
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
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px;
  min-height: calc(100vh - 140px);
}

/* ===== SIDEBAR ===== */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.profile-card {
  background: #fff;
  border-radius: 18px;
  padding: 32px 20px 24px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.avatar {
  width: 76px;
  height: 76px;
  border-radius: 50%;
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white;
  font-size: 1.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  box-shadow: 0 4px 16px rgba(153, 27, 27, 0.18);
  text-transform: uppercase;
}
.profile-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 2px;
  letter-spacing: -0.01em;
}
.profile-role {
  color: #9ca3af;
  font-size: 0.8rem;
  font-style: italic;
  font-weight: 400;
}

.stats-card {
  background: #fff;
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.stat-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid #f5f5f5;
}
.stat-row:last-child { border-bottom: none; }
.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}
.stat-icon.blue { background: #eff6ff; color: #3b82f6; }
.stat-icon.orange { background: #fff7ed; color: #f97316; }
.stat-num {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111827;
  line-height: 1;
  letter-spacing: -0.02em;
}
.stat-label {
  font-size: 0.72rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-weight: 500;
}

/* Calendar */
.calendar-card {
  background: #fff;
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.cal-header span {
  font-weight: 600;
  font-size: 0.9rem;
  color: #111827;
  text-transform: capitalize;
}
.cal-btn {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: #9ca3af;
  padding: 4px 8px;
  border-radius: 8px;
  transition: all 0.15s;
  box-shadow: none;
}
.cal-btn:hover { background: #f5f5f5; color: #374151; }
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  text-align: center;
  font-size: 0.78rem;
}
.cal-day-label {
  font-weight: 600;
  color: #9ca3af;
  padding: 4px 0;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.cal-day {
  padding: 5px 0;
  border-radius: 8px;
  color: #6b7280;
  font-size: 0.8rem;
  position: relative;
  cursor: default;
  transition: background 0.12s, color 0.12s, transform 0.12s;
}
.cal-day.today {
  background: #f3f4f6;
  color: #374151;
  font-weight: 700;
}
.cal-day.has-session {
  background: #fef2f2;
  color: #991b1b;
  font-weight: 700;
  cursor: pointer;
  border: 1.5px solid #fecaca;
}
.cal-day.has-session:hover {
  background: #fecaca;
  color: #7f1d1d;
  transform: scale(1.06);
}
.cal-day.today.has-session {
  background: #fef2f2;
  color: #991b1b;
  border: 1.5px solid #991b1b;
}
.cal-day.selected {
  background: #991b1b !important;
  color: #fff !important;
  font-weight: 700;
  border-color: #991b1b !important;
  transform: scale(1.08);
  box-shadow: 0 2px 8px rgba(153,27,27,0.25);
}

/* Filter badge */
.filter-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 8px 16px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #991b1b;
}
.filter-clear {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px; height: 22px;
  border: none;
  background: #991b1b;
  color: #fff;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.15s;
}
.filter-clear:hover { background: #7f1d1d; }

/* Status group headers */
.status-group-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 10px;
  margin: 18px 0 10px;
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
.status-group-header:first-child { margin-top: 12px; }
.status-group-header.active { background: #f0fdf4; color: #16a34a; }
.status-group-header.finished { background: #f3f4f6; color: #6b7280; }
.status-group-header.cancelled { background: #fef2f2; color: #ef4444; }

/* Sidebar nav */
.sidebar-nav {
  background: #fff;
  border-radius: 18px;
  padding: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.sidebar-nav a {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 14px;
  color: #6b7280;
  text-decoration: none;
  border-radius: 12px;
  font-size: 0.88rem;
  font-weight: 500;
  transition: background 0.15s, color 0.15s;
}
.sidebar-nav a:hover { background: #f9fafb; color: #111827; }
.sidebar-nav a.active {
  background: #111827;
  color: white;
}

/* ===== MAIN CONTENT ===== */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.welcome-title {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  letter-spacing: -0.02em;
}
.welcome-title span { color: #991b1b; font-weight: 800; }

.search-bar {
  display: flex;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
  overflow: hidden;
}
.search-bar input {
  flex: 1;
  border: none;
  padding: 15px 20px;
  font-size: 0.92rem;
  outline: none;
  background: transparent;
  color: #374151;
}
.search-bar button {
  background: #1f2937;
  color: white;
  border: none;
  padding: 0 20px;
  cursor: pointer;
  font-size: 1rem;
  border-radius: 0;
  box-shadow: none;
  transition: background 0.15s;
}
.search-bar button:hover { background: #374151; }

/* Session cards */
.section-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  letter-spacing: -0.01em;
}
.sessions-panel {
  background: #fff;
  border-radius: 18px;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  border: none;
}
.session-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  border-radius: 14px;
  background: #fafafa;
  border: none;
  transition: transform 0.15s, box-shadow 0.15s;
}
.session-card-wrapper { margin-bottom: 10px; }
.session-card-wrapper:last-child { margin-bottom: 0; }
.session-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  background: #f5f5f5;
}
.session-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #374151;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.session-info { flex: 1; min-width: 0; }
.session-title-text {
  font-weight: 600;
  font-size: 0.95rem;
  color: #111827;
  text-transform: capitalize;
}
.session-date-text {
  font-size: 0.8rem;
  color: #9ca3af;
  margin-top: 3px;
}
.session-coach-text {
  font-size: 0.82rem;
  color: #6b7280;
  white-space: nowrap;
}
.session-price-text {
  font-size: 0.92rem;
  font-weight: 700;
  color: #111827;
  white-space: nowrap;
}
.session-status {
  font-size: 0.7rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  white-space: nowrap;
  letter-spacing: 0.01em;
}
.status-confirmed { background: #f0fdf4; color: #16a34a; }
.status-cancelled { background: #fef2f2; color: #ef4444; }
.status-passed { background: #f3f4f6; color: #6b7280; }
.session-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.btn-participants {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  box-shadow: none;
}
.btn-participants:hover { background: #e5e7eb; color: #111827; }

/* Participants dropdown */
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
.btn-join {
  background: #991b1b;
  color: white;
  border: none;
  padding: 7px 16px;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  box-shadow: none;
}
.btn-join:hover { background: #7f1d1d; }
.btn-join:disabled {
  background: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 40px 16px;
  color: #9ca3af;
}
.empty-state p {
  font-size: 1rem;
  font-style: italic;
  margin-bottom: 16px;
  color: #9ca3af;
}
.btn-discover {
  background: #1f2937;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 10px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-discover:hover {
  background: #374151;
}

.error-message {
  color: #991b1b;
  background: #fef2f2;
  padding: 12px 16px;
  border-radius: 12px;
  text-align: center;
  font-size: 0.88rem;
}

.spinner {
  display: inline-block;
  width: 32px;
  height: 32px;
  border: 2.5px solid #f0f0f0;
  border-top-color: #6b7280;
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
        <div class="stat-icon orange">P</div>
        <div>
          <div class="stat-num">{daysUntilNext !== null ? `${daysUntilNext}j` : '-'}</div>
          <div class="stat-label">{daysUntilNext !== null ? 'prochaine séance' : 'aucune à venir'}</div>
        </div>
      </div>
    </div>

    <div class="calendar-card">
      <div class="cal-header">
        <button class="cal-btn" on:click={prevMonth}><ChevronLeft size={14} /></button>
        <span>{calendarMonthName}</span>
        <button class="cal-btn" on:click={nextMonth}><ChevronRight size={14} /></button>
      </div>
      <div class="cal-grid">
        {#each ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'] as label}
          <div class="cal-day-label">{label}</div>
        {/each}
        {#each calendarDays as cell}
          {#if cell}
            <div
              class="cal-day"
              class:has-session={allSessionDates.has(cell.dateStr)}
              class:today={cell.dateStr === todayStr()}
              class:selected={cell.dateStr === selectedDate}
              on:click={() => allSessionDates.has(cell.dateStr) && selectDay(cell.dateStr)}
              on:keydown={(e) => e.key === 'Enter' && allSessionDates.has(cell.dateStr) && selectDay(cell.dateStr)}
              role="button"
              tabindex={allSessionDates.has(cell.dateStr) ? 0 : -1}
            >{cell.day}</div>
          {:else}
            <div class="cal-day"></div>
          {/if}
        {/each}
      </div>
    </div>

    <nav class="sidebar-nav">
      <a href="/">Accueil</a>
      <a href="/dashboard/user" class="active">Mes séances</a>
    </nav>
  </aside>

  <!-- MAIN -->
  <div class="main-content">
    <div class="welcome-title" in:fly={{ y: -15, duration: 400 }}>
      Bienvenue, <span>{firstName || 'utilisateur'}</span>
    </div>

    <div class="search-bar" in:fly={{ y: 10, duration: 350, delay: 100 }}>
      <input type="text" placeholder="Rechercher une séance..." bind:value={searchQuery} />
      <button><Search size={18} /></button>
    </div>

    {#if loading}
      <div class="loading-center" in:fade>
        <div class="spinner"></div>
        <div style="color: #9ca3af; margin-top: 8px;">Chargement des séances…</div>
      </div>
    {:else if error}
      <div class="error-message" in:fade>{error}</div>
    {:else}
      {#if selectedDate}
        <div class="filter-badge" in:fly={{ y: -6, duration: 180 }}>
          Séances du {new Date(selectedDate + 'T00:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}
          <button class="filter-clear" on:click={clearFilter}><X size={13} /></button>
        </div>
      {/if}

      <div class="sessions-panel" in:fly={{ y: 15, duration: 350, delay: 150 }}>
        <h2 class="section-title">Mes séances inscrites</h2>
        {#if myFiltered.length === 0}
          <div class="empty-state">
            <p>{selectedDate ? 'Aucune séance inscrite pour cette date.' : 'Aucune séance inscrite.'}</p>
          </div>
        {:else}
          <!-- Active -->
          {#if myActive.length > 0}
            <div class="status-group-header active">🟢 Active ({myActive.length})</div>
            {#each myActive as s, i}
              {@const idx = i}
              <div class="session-card-wrapper" in:fly={{ x: -20, duration: 250, delay: 200 + idx * 60 }}>
                <div class="session-card">
                  <div class="session-icon"><SessionIcon title={s.title} size={20} /></div>
                  <div class="session-info">
                    <div class="session-title-text">{s.title}</div>
                    <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                  </div>
                  <div class="session-coach-text">{s.coach_name}</div>
                  <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
                  <span class="session-status status-confirmed">Confirmé</span>
                  <div class="session-actions">
                    <button class="btn-participants" on:click={() => toggleParticipants(s.id)}>Participants</button>
                  </div>
                </div>
                {#if expandedSession === s.id}
                  <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                    <div class="p-title">Participants inscrits</div>
                    {#if !participantsCache[s.id] || participantsCache[s.id].length === 0}
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
          <!-- Terminée -->
          {#if myFinished.length > 0}
            <div class="status-group-header finished">⏹ Terminée ({myFinished.length})</div>
            {#each myFinished as s, i}
              <div class="session-card-wrapper" in:fly={{ x: -20, duration: 250, delay: 200 + i * 60 }}>
                <div class="session-card">
                  <div class="session-icon"><SessionIcon title={s.title} size={20} /></div>
                  <div class="session-info">
                    <div class="session-title-text">{s.title}</div>
                    <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                  </div>
                  <div class="session-coach-text">{s.coach_name}</div>
                  <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
                  <span class="session-status status-passed">Terminée</span>
                  <div class="session-actions">
                    <button class="btn-participants" on:click={() => toggleParticipants(s.id)}>Participants</button>
                  </div>
                </div>
                {#if expandedSession === s.id}
                  <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                    <div class="p-title">Participants inscrits</div>
                    {#if !participantsCache[s.id] || participantsCache[s.id].length === 0}
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
          <!-- Annulée -->
          {#if myCancelled.length > 0}
            <div class="status-group-header cancelled">✕ Annulée ({myCancelled.length})</div>
            {#each myCancelled as s, i}
              <div class="session-card-wrapper" in:fly={{ x: -20, duration: 250, delay: 200 + i * 60 }}>
                <div class="session-card">
                  <div class="session-icon"><SessionIcon title={s.title} size={20} /></div>
                  <div class="session-info">
                    <div class="session-title-text">{s.title}</div>
                    <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                  </div>
                  <div class="session-coach-text">{s.coach_name}</div>
                  <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>
                  <span class="session-status status-cancelled">Annulée</span>
                  <div class="session-actions">
                    <button class="btn-participants" on:click={() => toggleParticipants(s.id)}>Participants</button>
                  </div>
                </div>
                {#if expandedSession === s.id}
                  <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                    <div class="p-title">Participants inscrits</div>
                    {#if !participantsCache[s.id] || participantsCache[s.id].length === 0}
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
            <div class="session-card-wrapper" in:fly={{ x: -20, duration: 250, delay: 350 + i * 60 }}>
              <div class="session-card">
                <div class="session-icon"><SessionIcon title={s.title} size={20} /></div>
                <div class="session-info">
                  <div class="session-title-text">{s.title}</div>
                  <div class="session-date-text">{new Date(s.starts_at).toLocaleString('fr-FR')}</div>
                </div>
                <div class="session-coach-text">{s.coach_name}</div>
                <div class="session-price-text">{formatPrice(s.price_cents, s.currency)}</div>


                {#if s.status === 'cancelled'}
                  <span class="session-status status-cancelled">Annulée</span>
                {:else if new Date(s.ends_at) < new Date()}
                  <span class="session-status status-passed">Terminée</span>
                  <div class="session-actions">
                    <button class="btn-participants" on:click={() => toggleParticipants(s.id)}>Participants</button>
                  </div>
                {:else}
                  <div class="session-actions">
                    <button class="btn-participants" on:click={() => toggleParticipants(s.id)}>Participants</button>
                    <button class="btn-join" on:click={() => joinSession(s.id)} disabled={joiningId === s.id}>
                      {joiningId === s.id ? '...' : "S'inscrire"}
                    </button>
                  </div>
                {/if}
              </div>
              {#if expandedSession === s.id}
                <div class="participants-dropdown" in:fade={{ duration: 150 }}>
                  <div class="p-title">Participants inscrits</div>
                  {#if !participantsCache[s.id] || participantsCache[s.id].length === 0}
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
        </div>
      {/if}
    {/if}
  </div>
</div>
{/if}