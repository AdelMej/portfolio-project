<!-- ATTENDANCE PAGE: /frontend/src/routes/sessions/[id]/attendance/+page.svelte -->
<script lang="ts">
import { onMount } from 'svelte';
import { page } from '$app/stores';
import { goto } from '$app/navigation';
import { fly, fade } from 'svelte/transition';
import { apiFetch } from '$lib/api/client';

interface SessionInfo {
  id: string;
  title: string;
  starts_at: string;
  ends_at: string;
  price_cents: number;
  currency: string;
  status: string;
  coach?: { first_name: string; last_name: string };
}

interface AttendanceParticipant {
  user_id: string;
  first_name: string;
  last_name: string;
}

let sessionId = '';
let session: SessionInfo | null = null;
let participants: AttendanceParticipant[] = [];
let attendanceMap: Record<string, boolean> = {};
let loading = true;
let submitting = false;
let error = '';
let success = '';
let attendanceClosed = false;
let alreadySubmitted = false;

$: sessionId = $page.params.id;

async function loadData() {
  loading = true;
  error = '';
  try {
    // Load session info via public endpoint
    const s = await apiFetch(`/sessions/${sessionId}`);
    session = s;

    // Load pre-attendance list
    try {
      const list: AttendanceParticipant[] = await apiFetch(`/sessions/${sessionId}/attendance`);
      if (list.length === 0) {
        // Attendance already submitted or no participants
        alreadySubmitted = true;
        participants = [];
      } else {
        participants = list;
        // Initialize all as absent
        attendanceMap = {};
        for (const p of list) {
          attendanceMap[p.user_id] = false;
        }
      }
    } catch (e: any) {
      if (e?.detail?.code === 'session_attendance_closed') {
        attendanceClosed = true;
      } else if (e?.detail?.code === 'session_attendance_already_done') {
        alreadySubmitted = true;
      } else {
        throw e;
      }
    }
  } catch (e: any) {
    console.error(e);
    error = e?.detail?.error ?? 'Impossible de charger les données de la séance.';
  } finally {
    loading = false;
  }
}

function toggleAttendance(userId: string) {
  attendanceMap[userId] = !attendanceMap[userId];
  attendanceMap = attendanceMap; // reactivity
}

function setAll(value: boolean) {
  for (const p of participants) {
    attendanceMap[p.user_id] = value;
  }
  attendanceMap = attendanceMap;
}

async function submitAttendance() {
  if (!confirm('Confirmer la liste de présence ? Cette action est définitive.')) return;
  submitting = true;
  error = '';
  success = '';
  try {
    const payload = {
      attendance: participants.map(p => ({
        user_id: p.user_id,
        attended: attendanceMap[p.user_id] ?? false
      }))
    };
    await apiFetch(`/sessions/${sessionId}/attendance`, {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
    success = 'Liste de présence enregistrée avec succès !';
    alreadySubmitted = true;
  } catch (e: any) {
    console.error(e);
    error = e?.detail?.error ?? "Erreur lors de l'enregistrement de la présence.";
  } finally {
    submitting = false;
  }
}

$: presentCount = Object.values(attendanceMap).filter(v => v).length;
$: absentCount = Object.values(attendanceMap).filter(v => !v).length;

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('fr-FR', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

function formatPrice(cents: number, currency: string) {
  return (cents / 100).toFixed(2) + ' ' + (currency ?? 'EUR');
}

onMount(() => { loadData(); });
</script>

<style>
.attendance-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 16px;
  min-height: calc(100vh - 140px);
}

.back-link {
  display: inline-flex; align-items: center; gap: 6px;
  color: #374151; text-decoration: none; font-weight: 600;
  font-size: 0.9rem; margin-bottom: 20px;
  transition: color 0.15s;
}
.back-link:hover { color: #1f2937; }

.page-title {
  font-size: 1.8rem; font-weight: 800; color: #1f2937;
  margin-bottom: 24px;
}
.page-title span {
  color: #991b1b; font-weight: 800;
}

/* SESSION INFO CARD */
.session-info-card {
  background: #fff;
  border-radius: 16px; padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}
.info-grid {
  display: grid; grid-template-columns: 160px 1fr;
  gap: 12px 16px; align-items: baseline;
}
.info-label {
  font-weight: 700; color: #374151; font-size: 0.92rem;
}
.info-value {
  color: #1f2937; font-size: 0.95rem;
}
.info-value.title-val {
  font-weight: 700; font-size: 1.1rem; text-transform: capitalize;
}
.participant-count-badge {
  display: inline-block; background: #991b1b; color: white;
  font-weight: 700; font-size: 0.85rem; padding: 3px 12px;
  border-radius: 20px;
}

/* ATTENDANCE TABLE */
.attendance-card {
  background: #fff;
  border-radius: 16px; padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}
.attendance-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px; flex-wrap: wrap; gap: 12px;
}
.attendance-title {
  font-size: 1.15rem; font-weight: 700; color: #1f2937; margin: 0;
}
.bulk-actions {
  display: flex; gap: 8px;
}
.bulk-btn {
  padding: 6px 14px; border-radius: 20px; font-size: 0.78rem;
  font-weight: 600; cursor: pointer; border: none;
  transition: background 0.2s; box-shadow: none;
}
.bulk-btn.all-present { background: #d1fae5; color: #065f46; }
.bulk-btn.all-present:hover { background: #a7f3d0; }
.bulk-btn.all-absent { background: #fee2e2; color: #991b1b; }
.bulk-btn.all-absent:hover { background: #fecaca; }

.attendance-table {
  width: 100%; border-collapse: separate; border-spacing: 0;
  border-radius: 12px; overflow: hidden;
  border: 1px solid #e5e7eb;
}
.attendance-table thead th {
  background: #374151; color: white;
  padding: 12px 16px; font-size: 0.85rem; font-weight: 700;
  text-align: left; white-space: nowrap;
}
.attendance-table tbody tr {
  transition: background 0.15s;
}
.attendance-table tbody tr:nth-child(even) { background: #f9fafb; }
.attendance-table tbody tr:hover { background: #f3f4f6; }
.attendance-table tbody td {
  padding: 14px 16px; font-size: 0.92rem; color: #374151;
  border-bottom: 1px solid #f3f4f6;
}
.attendance-table tbody tr:last-child td { border-bottom: none; }

.participant-cell {
  display: flex; align-items: center; gap: 10px;
}
.p-avatar {
  width: 34px; height: 34px; border-radius: 50%;
  background: #374151;
  color: white; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 0.7rem; flex-shrink: 0;
  text-transform: uppercase;
}
.p-name { font-weight: 600; }

/* PRESENCE TOGGLE */
.presence-toggle {
  display: flex; align-items: center; gap: 10px;
}
.toggle-switch {
  position: relative; width: 48px; height: 26px;
  background: #e5e7eb; border-radius: 13px;
  cursor: pointer; transition: background 0.2s;
  border: none; padding: 0; box-shadow: none;
}
.toggle-switch.active { background: #16a34a; }
.toggle-switch::after {
  content: ''; position: absolute;
  top: 3px; left: 3px;
  width: 20px; height: 20px;
  background: white; border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.toggle-switch.active::after { transform: translateX(22px); }
.toggle-label {
  font-size: 0.82rem; font-weight: 600;
  min-width: 55px;
}
.toggle-label.present { color: #16a34a; }
.toggle-label.absent { color: #dc2626; }

/* SUMMARY */
.summary-bar {
  display: flex; gap: 16px; align-items: center;
  padding: 16px 0; border-top: 1px solid #e5e7eb;
  margin-top: 16px; flex-wrap: wrap;
}
.summary-item {
  font-size: 0.88rem; font-weight: 600; display: flex; align-items: center; gap: 6px;
}
.summary-dot {
  width: 10px; height: 10px; border-radius: 50%;
}
.summary-dot.green { background: #16a34a; }
.summary-dot.red { background: #dc2626; }

/* SUBMIT */
.submit-section {
  text-align: right;
}
.btn-confirm {
  background: linear-gradient(135deg, #991b1b, #dc2626);
  color: white; border: none;
  padding: 14px 40px; border-radius: 12px;
  font-size: 1.05rem; font-weight: 700;
  cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 4px 12px rgba(153,27,27,0.3);
}
.btn-confirm:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(153,27,27,0.4); }
.btn-confirm:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

/* STATUS MESSAGES */
.msg-success {
  background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0;
  padding: 14px 20px; border-radius: 12px; text-align: center;
  font-weight: 600; font-size: 0.95rem; margin-bottom: 20px;
}
.msg-error {
  background: #fee2e2; color: #991b1b; border: 1px solid #fecaca;
  padding: 14px 20px; border-radius: 12px; text-align: center;
  font-weight: 600; font-size: 0.95rem; margin-bottom: 20px;
}
.msg-info {
  background: #f9fafb; color: #374151; border: 1px solid #e5e7eb;
  padding: 24px 20px; border-radius: 12px; text-align: center;
  font-size: 0.95rem;
}
.msg-info strong { color: #1f2937; }

.empty-state {
  text-align: center; padding: 40px 16px; color: #6b7280; font-style: italic;
}

.spinner {
  display: inline-block; width: 36px; height: 36px;
  border: 3px solid #e5e7eb; border-top-color: #374151;
  border-radius: 50%; animation: spin 0.7s linear infinite; margin: 28px auto;
}
.loading-center { text-align: center; padding: 80px 0; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 640px) {
  .info-grid { grid-template-columns: 1fr; gap: 4px 0; }
  .info-label { font-size: 0.82rem; }
  .attendance-table { font-size: 0.85rem; }
  .attendance-table thead th { padding: 10px 12px; }
  .attendance-table tbody td { padding: 10px 12px; }
  .btn-confirm { width: 100%; }
}
</style>

<div class="attendance-page">
  <a href="/dashboard/coach" class="back-link" in:fly={{ x: -10, duration: 200 }}>
    ← Retour au tableau de bord
  </a>

  <h1 class="page-title" in:fly={{ y: -15, duration: 400 }}>
    Liste de <span>présence</span>
  </h1>

  {#if loading}
    <div class="loading-center" in:fade>
      <div class="spinner"></div>
      <div style="color: #9ca3af; margin-top: 8px;">Chargement de la séance...</div>
    </div>
  {:else if error && !session}
    <div class="msg-error" in:fade>{error}</div>
  {:else if session}
    <!-- SESSION INFO -->
    <div class="session-info-card" in:fly={{ y: 15, duration: 350, delay: 100 }}>
      <div class="info-grid">
        <div class="info-label">Séance :</div>
        <div class="info-value title-val">{session.title}</div>

        <div class="info-label">Date :</div>
        <div class="info-value">{formatDate(session.starts_at)}</div>

        <div class="info-label">Fin :</div>
        <div class="info-value">{formatDate(session.ends_at)}</div>

        <div class="info-label">Prix :</div>
        <div class="info-value">{formatPrice(session.price_cents, session.currency)}</div>

        <div class="info-label">Participants :</div>
        <div class="info-value">
          <span class="participant-count-badge">{participants.length} inscrits</span>
        </div>
      </div>
    </div>

    {#if error}
      <div class="msg-error" in:fade>{error}</div>
    {/if}

    {#if success}
      <div class="msg-success" in:fade>{success}</div>
    {/if}

    {#if attendanceClosed}
      <div class="msg-info" in:fade>
        <strong>Présence non disponible.</strong><br>
        La fenêtre de prise de présence n'est pas encore ouverte pour cette séance.
      </div>
    {:else if alreadySubmitted}
      <div class="msg-info" in:fade>
        <strong>Présence déjà enregistrée.</strong><br>
        La liste de présence a déjà été soumise pour cette séance.
      </div>
    {:else if participants.length === 0}
      <div class="empty-state" in:fade>Aucun participant inscrit pour cette séance.</div>
    {:else}
      <!-- ATTENDANCE TABLE -->
      <div class="attendance-card" in:fly={{ y: 15, duration: 350, delay: 200 }}>
        <div class="attendance-header">
          <h2 class="attendance-title">Marquer la présence</h2>
          <div class="bulk-actions">
            <button class="bulk-btn all-present" on:click={() => setAll(true)}>Tous présents</button>
            <button class="bulk-btn all-absent" on:click={() => setAll(false)}>Tous absents</button>
          </div>
        </div>

        <table class="attendance-table">
          <thead>
            <tr>
              <th>Participant</th>
              <th>Présence</th>
            </tr>
          </thead>
          <tbody>
            {#each participants as p, i}
              <tr in:fly={{ x: -15, duration: 200, delay: 50 + i * 30 }}>
                <td>
                  <div class="participant-cell">
                    <span class="p-avatar">{(p.first_name?.[0] ?? '')}{(p.last_name?.[0] ?? '')}</span>
                    <span class="p-name">{p.first_name} {p.last_name}</span>
                  </div>
                </td>
                <td>
                  <div class="presence-toggle">
                    <button
                      class="toggle-switch"
                      class:active={attendanceMap[p.user_id]}
                      on:click={() => toggleAttendance(p.user_id)}
                      aria-label={attendanceMap[p.user_id] ? 'Marquer absent' : 'Marquer présent'}
                    ></button>
                    <span class="toggle-label" class:present={attendanceMap[p.user_id]} class:absent={!attendanceMap[p.user_id]}>
                      {attendanceMap[p.user_id] ? 'Présent' : 'Absent'}
                    </span>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>

        <div class="summary-bar">
          <div class="summary-item">
            <span class="summary-dot green"></span>
            Présents : {presentCount}
          </div>
          <div class="summary-item">
            <span class="summary-dot red"></span>
            Absents : {absentCount}
          </div>
          <div class="summary-item" style="margin-left: auto; color: #6b7280;">
            Total : {participants.length}
          </div>
        </div>
      </div>

      <!-- CONFIRM BUTTON -->
      <div class="submit-section" in:fly={{ y: 10, duration: 300, delay: 300 }}>
        <button
          class="btn-confirm"
          on:click={submitAttendance}
          disabled={submitting}
        >
          {submitting ? 'Enregistrement...' : 'Confirmer'}
        </button>
      </div>
    {/if}
  {/if}
</div>
