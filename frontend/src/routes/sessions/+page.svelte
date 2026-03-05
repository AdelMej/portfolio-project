<script lang="ts">
  import { onMount } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import { ChevronLeft, ChevronRight, X } from 'lucide-svelte';
  import type { Session } from '$lib/api/sessions.api';
  import { listSessions } from '$lib/api/sessions.api';
  import SessionIcon from '$lib/components/SessionIcon.svelte';

  let sessions: Session[] = [];
  let loading = true;
  let ready = false;

  // Calendar state
  let calendarDate = new Date(); // current month view
  let selectedDate: string | null = null; // 'YYYY-MM-DD' or null

  $: calendarYear = calendarDate.getFullYear();
  $: calendarMonth = calendarDate.getMonth();
  $: monthLabel = calendarDate.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' });

  // Set of dates (YYYY-MM-DD) that have sessions
  $: sessionDatesSet = new Set(sessions.map(s => {
    const d = new Date(s.starts_at);
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  }));

  // Build calendar grid
  $: calendarDays = buildCalendar(calendarYear, calendarMonth);

  function buildCalendar(year: number, month: number): ({ day: number; dateStr: string; inMonth: boolean } | null)[] {
    const first = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0).getDate();
    let startDow = first.getDay(); // 0=Sun
    startDow = startDow === 0 ? 6 : startDow - 1; // shift to Mon=0
    const cells: ({ day: number; dateStr: string; inMonth: boolean } | null)[] = [];
    // blanks before 1st
    for (let i = 0; i < startDow; i++) cells.push(null);
    for (let d = 1; d <= lastDay; d++) {
      const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      cells.push({ day: d, dateStr, inMonth: true });
    }
    return cells;
  }

  function prevMonth() { calendarDate = new Date(calendarYear, calendarMonth - 1, 1); }
  function nextMonth() { calendarDate = new Date(calendarYear, calendarMonth + 1, 1); }
  function selectDay(dateStr: string) {
    selectedDate = selectedDate === dateStr ? null : dateStr;
  }
  function clearFilter() { selectedDate = null; }

  // Filtered sessions
  $: filteredSessions = selectedDate
    ? sessions.filter(s => {
        const d = new Date(s.starts_at);
        const ds = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
        return ds === selectedDate;
      })
    : sessions;

  function formatPrice(cents?: number, currency?: string): string {
    if (cents == null) return '-';
    return (cents / 100).toFixed(2) + ' ' + (currency ?? 'EUR');
  }

  function todayStr(): string {
    const t = new Date();
    return `${t.getFullYear()}-${String(t.getMonth()+1).padStart(2,'0')}-${String(t.getDate()).padStart(2,'0')}`;
  }

  onMount(async () => {
    ready = true;
    try {
      const res: Session[] = await listSessions();
      const now = new Date();
      sessions = res
        .filter(s => s.status !== 'cancelled' && new Date(s.ends_at) >= now)
        .sort((a, b) => new Date(a.starts_at).getTime() - new Date(b.starts_at).getTime());
    } catch (err) {
      console.error('Failed to fetch sessions', err);
    } finally {
      loading = false;
    }
  });
</script>

<style>
.sessions-container {
  max-width: 860px;
  margin: 40px auto;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  padding: 40px 32px 32px 32px;
}
h1 {
  font-size: 2rem;
  margin-bottom: 28px;
  color: #111827;
  text-align: center;
  font-weight: 800;
  letter-spacing: -0.02em;
}
h1 span { color: #991b1b; }

/* ── Calendar ── */
.calendar-wrap {
  margin-bottom: 28px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  background: #fafafa;
}
.cal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f3f4f6;
  border-bottom: 1px solid #e5e7eb;
}
.cal-header span {
  font-weight: 700;
  font-size: 0.95rem;
  color: #111827;
  text-transform: capitalize;
}
.cal-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px; height: 30px;
  border: none;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
  color: #374151;
  transition: background 0.15s;
}
.cal-nav:hover { background: #e5e7eb; }
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  padding: 10px 10px 12px;
}
.cal-dow {
  font-size: 0.7rem;
  font-weight: 600;
  color: #9ca3af;
  text-align: center;
  padding: 4px 0;
  text-transform: uppercase;
}
.cal-cell {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.82rem;
  font-weight: 500;
  border-radius: 10px;
  cursor: default;
  color: #6b7280;
  transition: background 0.12s, color 0.12s, transform 0.12s;
  position: relative;
}
.cal-cell.has-session {
  background: #fef2f2;
  color: #991b1b;
  font-weight: 700;
  cursor: pointer;
  border: 1.5px solid #fecaca;
}
.cal-cell.has-session:hover {
  background: #fecaca;
  color: #7f1d1d;
  transform: scale(1.06);
}
.cal-cell.today {
  background: #f3f4f6;
  font-weight: 700;
  color: #374151;
  border: 1.5px solid #d1d5db;
}
.cal-cell.today.has-session {
  background: #fef2f2;
  color: #991b1b;
  border: 1.5px solid #991b1b;
}
.cal-cell.selected {
  background: #991b1b !important;
  color: #fff !important;
  font-weight: 700;
  border-color: #991b1b !important;
  transform: scale(1.08);
  box-shadow: 0 2px 8px rgba(153,27,27,0.25);
}

/* ── Active filter badge ── */
.filter-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 18px;
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

.session-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.session-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #fafafa;
  border-radius: 14px;
  margin-bottom: 10px;
  padding: 18px 20px;
  transition: transform 0.15s, box-shadow 0.15s;
}
.session-item:last-child { margin-bottom: 0; }
.session-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  background: #f5f5f5;
}
.s-icon {
  width: 42px; height: 42px; border-radius: 12px;
  background: #374151; color: white;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.s-info { flex: 1; min-width: 0; }
.s-title { font-weight: 600; font-size: 0.95rem; color: #111827; text-transform: capitalize; }
.s-sub { font-size: 0.8rem; color: #9ca3af; margin-top: 3px; }
.s-price { font-size: 0.92rem; font-weight: 700; color: #111827; white-space: nowrap; }
.s-badge {
  font-size: 0.7rem; font-weight: 600; padding: 4px 10px;
  border-radius: 20px; background: #f0fdf4; color: #16a34a;
  white-space: nowrap;
}
.empty-message {
  color: #9ca3af;
  font-size: 1rem;
  text-align: center;
  padding: 40px 16px;
  font-style: italic;
}
.spinner {
  display: inline-block; width: 32px; height: 32px;
  border: 2.5px solid #f0f0f0; border-top-color: #6b7280;
  border-radius: 50%; animation: spin 0.7s linear infinite; margin: 28px auto;
}
.loading-center { text-align: center; padding: 60px 0; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>

{#if ready}
<div class="sessions-container" in:fade={{ duration: 300 }}>
  <h1>Séances <span>disponibles</span></h1>

  {#if !loading}
    <!-- Calendar filter -->
    <div class="calendar-wrap" in:fly={{ y: -10, duration: 250 }}>
      <div class="cal-header">
        <button class="cal-nav" on:click={prevMonth}><ChevronLeft size={16} /></button>
        <span>{monthLabel}</span>
        <button class="cal-nav" on:click={nextMonth}><ChevronRight size={16} /></button>
      </div>
      <div class="cal-grid">
        {#each ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim'] as dow}
          <div class="cal-dow">{dow}</div>
        {/each}
        {#each calendarDays as cell}
          {#if cell}
            <div
              class="cal-cell"
              class:has-session={sessionDatesSet.has(cell.dateStr)}
              class:today={cell.dateStr === todayStr()}
              class:selected={cell.dateStr === selectedDate}
              on:click={() => sessionDatesSet.has(cell.dateStr) && selectDay(cell.dateStr)}
              on:keydown={(e) => e.key === 'Enter' && sessionDatesSet.has(cell.dateStr) && selectDay(cell.dateStr)}
              role="button"
              tabindex={sessionDatesSet.has(cell.dateStr) ? 0 : -1}
            >{cell.day}</div>
          {:else}
            <div class="cal-cell"></div>
          {/if}
        {/each}
      </div>
    </div>

    {#if selectedDate}
      <div class="filter-badge" in:fly={{ y: -6, duration: 180 }}>
        Séances du {new Date(selectedDate + 'T00:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}
        <button class="filter-clear" on:click={clearFilter}><X size={13} /></button>
      </div>
    {/if}
  {/if}

  {#if loading}
    <div class="loading-center"><div class="spinner"></div></div>
  {:else if filteredSessions.length === 0}
    <div class="empty-message">
      {#if selectedDate}
        Aucune séance disponible pour cette date.
      {:else}
        Aucune séance disponible pour le moment.
      {/if}
    </div>
  {:else}
    <ul class="session-list">
      {#each filteredSessions as s, i}
        <li class="session-item" in:fly={{ y: 15, duration: 250, delay: 80 + i * 50 }}>
          <div class="s-icon"><SessionIcon title={s.title} size={20} /></div>
          <div class="s-info">
            <div class="s-title">{s.title}</div>
            <div class="s-sub">{s.coach_name ?? ''} — {new Date(s.starts_at).toLocaleString('fr-FR')}</div>
          </div>
          <div class="s-price">{formatPrice(s.price_cents, s.currency)}</div>
          <span class="s-badge">Disponible</span>
        </li>
      {/each}
    </ul>
  {/if}
</div>
{/if}