<script lang="ts">
  import { page } from '$app/stores';
  import { apiFetch } from '$lib/api/client';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';
  import { auth } from '$lib/stores/auth.store';
  import { fly, fade } from 'svelte/transition';

  type Participant = {
    id: string;
    email: string;
    first_name?: string;
    last_name?: string;
  };

  type SessionDetail = {
    id: string;
    title: string;
    starts_at: string;
    ends_at: string;
    coach_id: string;
    coach_name?: string;
    max_participants?: number;
    participants?: Participant[];
    status: 'scheduled' | 'cancelled';
  };

  /* ── Attendance types ── */
  type AttendanceLine = {
    user_id: string;
    first_name: string;
    last_name: string;
  };

  type AdminAttendanceLine = AttendanceLine & { attended: boolean };

  let session: SessionDetail | null = null;
  let loading = true;
  let error = '';

  /* ── Attendance state ── */
  let isCoach = false;
  let isAdmin = false;
  let attendanceList: AttendanceLine[] = [];
  let attendanceChecks: Record<string, boolean> = {};
  let attendanceOpen = false;
  let attendanceAlreadyDone = false;
  let attendanceLoading = false;
  let attendanceSubmitting = false;
  let attendanceSuccess = false;
  let attendanceError = '';

  /* Admin attendance results */
  let adminAttendance: AdminAttendanceLine[] = [];
  let adminAttendanceLoaded = false;
  let adminAttendanceError = '';

  async function loadSession() {
    loading = true;
    error = '';

    try {
      const sessionId = get(page).params.id;
      const data = await apiFetch(`/sessions/${sessionId}`);

      session = data?.items ? data.items[0] : data;
    } catch (e) {
      console.error('Erreur chargement session', e);
      error = 'Impossible de charger la séance';
      session = null;
    } finally {
      loading = false;
    }
  }

  async function loadAttendance() {
    const roles = get(auth).roles || [];
    isCoach = roles.includes('coach');
    isAdmin = roles.includes('admin');
    const sessionId = get(page).params.id;

    /* Coach: load pre-attendance list */
    if (isCoach) {
      attendanceLoading = true;
      try {
        const res = await apiFetch<AttendanceLine[]>(`/sessions/${sessionId}/attendance`);
        attendanceList = res ?? [];
        attendanceChecks = {};
        for (const a of attendanceList) {
          attendanceChecks[a.user_id] = false;
        }
        attendanceOpen = true;
      } catch (e: any) {
        const detail = e?.detail ?? '';
        if (typeof detail === 'string' && (detail.includes('not open') || detail.includes('not available'))) {
          attendanceOpen = false;
        } else if (typeof detail === 'string' && (detail.includes('already') || detail.includes('already done'))) {
          attendanceAlreadyDone = true;
          attendanceOpen = false;
        } else {
          attendanceOpen = false;
        }
      } finally {
        attendanceLoading = false;
      }
    }

    /* Admin: load attendance results */
    if (isAdmin) {
      try {
        const res = await apiFetch<AdminAttendanceLine[]>(`/admin/sessions/${sessionId}/attendance`);
        adminAttendance = res ?? [];
        adminAttendanceLoaded = true;
      } catch (e: any) {
        const detail = e?.detail ?? '';
        if (typeof detail === 'string' && detail.includes('not attended')) {
          adminAttendanceError = 'La présence n\'a pas encore été enregistrée pour cette séance.';
        } else {
          adminAttendanceError = '';
        }
        adminAttendanceLoaded = false;
      }
    }
  }

  async function submitAttendance() {
    attendanceSubmitting = true;
    attendanceError = '';
    attendanceSuccess = false;

    const sessionId = get(page).params.id;
    const payload = {
      attendance: attendanceList.map(a => ({
        user_id: a.user_id,
        attended: attendanceChecks[a.user_id] ?? false
      }))
    };

    try {
      await apiFetch(`/sessions/${sessionId}/attendance`, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      attendanceSuccess = true;
      attendanceOpen = false;
      attendanceAlreadyDone = true;
    } catch (e: any) {
      console.error('Erreur soumission présence', e);
      attendanceError = e?.detail ?? 'Impossible de soumettre la présence';
    } finally {
      attendanceSubmitting = false;
    }
  }

  function toggleAll(checked: boolean) {
    for (const a of attendanceList) {
      attendanceChecks[a.user_id] = checked;
    }
    attendanceChecks = { ...attendanceChecks };
  }

  onMount(async () => {
    await loadSession();
    await loadAttendance();
  });

  function handleReturn() {
    const roles = get(auth).roles || [];
    if (roles.includes('admin')) {
      goto('/dashboard/admin');
    } else if (roles.includes('coach')) {
      goto('/dashboard/coach');
    } else {
      goto('/dashboard/user');
    }
  }

  $: allChecked = attendanceList.length > 0 && attendanceList.every(a => attendanceChecks[a.user_id]);
  $: someChecked = attendanceList.some(a => attendanceChecks[a.user_id]);
</script>

<div class="container" in:fly={{ y: 30, duration: 400 }}>
  {#if loading}
    <div class="spinner-wrap" in:fade><div class="spinner"></div><p>Chargement...</p></div>

  {:else if error}
    <p class="error-msg">{error}</p>

  {:else if session}
    <h1 in:fly={{ y: -10, duration: 300 }}>Participants – {session.title}</h1>

    <div class="session-info" in:fade={{ delay: 100 }}>
      <p><strong>Coach :</strong> {session.coach_name || session.coach_id || 'Inconnu'}</p>
      <p><strong>Début :</strong> {new Date(session.starts_at).toLocaleString('fr-FR')}</p>
      <p><strong>Fin :</strong> {new Date(session.ends_at).toLocaleString('fr-FR')}</p>
      <p><strong>Participants max :</strong> {session.max_participants ?? '-'}</p>
      <p>
        <strong>Statut :</strong>
        {#if session.status === 'cancelled'}
          <span class="badge badge-danger">Annulée</span>
        {:else}
          <span class="badge badge-success">Active</span>
        {/if}
      </p>
    </div>

    <!-- ── Participant list ── -->
    <h2 in:fade={{ delay: 150 }}>
      Liste des participants ({session.participants?.length ?? 0})
    </h2>

    {#if !session.participants || session.participants.length === 0}
      <p>Aucun participant inscrit.</p>
    {:else}
      <table in:fly={{ y: 20, duration: 350, delay: 200 }}>
        <thead>
          <tr>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {#each session.participants as p, i}
            <tr in:fly={{ x: -15, duration: 250, delay: 250 + i * 40 }}>
              <td>{p.last_name || '-'}</td>
              <td>{p.first_name || '-'}</td>
              <td>{p.email}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}

    <!-- ══════════════════════════════════════════════════════
         COACH: Attendance checkboxes (Flow 3)
         ══════════════════════════════════════════════════════ -->
    {#if isCoach}
      <div class="attendance-section" in:fly={{ y: 20, duration: 350, delay: 300 }}>
        <h2>Présence</h2>

        {#if attendanceLoading}
          <div class="spinner-wrap"><div class="spinner"></div><p>Chargement présence...</p></div>

        {:else if attendanceSuccess}
          <div class="attendance-banner success" in:fade>
            Présence enregistrée avec succès !
          </div>

        {:else if attendanceAlreadyDone}
          <div class="attendance-banner info" in:fade>
            La présence a déjà été enregistrée pour cette séance.
          </div>

        {:else if attendanceOpen && attendanceList.length > 0}
          <p class="attendance-hint">Cochez les participants présents puis confirmez.</p>

          <table class="attendance-table">
            <thead>
              <tr>
                <th class="check-col">
                  <label class="check-label">
                    <input
                      type="checkbox"
                      checked={allChecked}
                      indeterminate={someChecked && !allChecked}
                      on:change={(e) => toggleAll(e.currentTarget.checked)}
                    />
                    Tous
                  </label>
                </th>
                <th>Nom</th>
                <th>Prénom</th>
              </tr>
            </thead>
            <tbody>
              {#each attendanceList as a, i}
                <tr
                  class:row-checked={attendanceChecks[a.user_id]}
                  in:fly={{ x: -15, duration: 250, delay: i * 40 }}
                >
                  <td class="check-col">
                    <input
                      type="checkbox"
                      bind:checked={attendanceChecks[a.user_id]}
                    />
                  </td>
                  <td>{a.last_name}</td>
                  <td>{a.first_name}</td>
                </tr>
              {/each}
            </tbody>
          </table>

          {#if attendanceError}
            <p class="error-msg" in:fade>{attendanceError}</p>
          {/if}

          <button
            class="btn-confirm"
            on:click={submitAttendance}
            disabled={attendanceSubmitting}
          >
            {#if attendanceSubmitting}
              <span class="btn-spinner"></span> Envoi...
            {:else}
              Confirmer la présence
            {/if}
          </button>

        {:else}
          <div class="attendance-banner info" in:fade>
            La prise de présence n'est pas encore disponible pour cette séance.
          </div>
        {/if}
      </div>
    {/if}

    <!-- ══════════════════════════════════════════════════════
         ADMIN: Attendance results
         ══════════════════════════════════════════════════════ -->
    {#if isAdmin}
      <div class="attendance-section" in:fly={{ y: 20, duration: 350, delay: 300 }}>
        <h2>Résultat de présence</h2>

        {#if adminAttendanceLoaded && adminAttendance.length > 0}
          <table class="attendance-table">
            <thead>
              <tr>
                <th>Nom</th>
                <th>Prénom</th>
                <th>Présence</th>
              </tr>
            </thead>
            <tbody>
              {#each adminAttendance as a, i}
                <tr
                  class:row-present={a.attended}
                  class:row-absent={!a.attended}
                  in:fly={{ x: -15, duration: 250, delay: i * 40 }}
                >
                  <td>{a.last_name}</td>
                  <td>{a.first_name}</td>
                  <td>
                    {#if a.attended}
                      <span class="badge badge-success">Présent</span>
                    {:else}
                      <span class="badge badge-danger">Absent</span>
                    {/if}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        {:else if adminAttendanceError}
          <div class="attendance-banner info" in:fade>{adminAttendanceError}</div>
        {:else}
          <div class="attendance-banner info" in:fade>Aucune donnée de présence disponible.</div>
        {/if}
      </div>
    {/if}

    <button class="btn-return" on:click={handleReturn}>
      Retour
    </button>
  {/if}
</div>


<style>
  .container {
    max-width: 960px;
    margin: 40px auto;
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 16px #e5e7eb;
    padding: 36px 32px 32px 32px;
  }
  h1 {
    font-size: 2rem;
    color: #991b1b;
    margin-bottom: 18px;
  }
  h2 {
    font-size: 1.3rem;
    color: #374151;
    margin-top: 24px;
    margin-bottom: 12px;
  }
  .session-info p {
    margin: 6px 0;
    color: #374151;
    font-size: 1rem;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
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
  tr:last-child td {
    border-bottom: none;
  }
  tr:hover td {
    background: #fef2f2;
  }
  .badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
  }
  .badge-success {
    background: #d1fae5;
    color: #065f46;
  }
  .badge-danger {
    background: #fee2e2;
    color: #991b1b;
  }

  /* ── Attendance section ── */
  .attendance-section {
    margin-top: 36px;
    padding-top: 28px;
    border-top: 2px solid #fecaca;
  }
  .attendance-section h2 {
    color: #991b1b;
    font-size: 1.4rem;
  }
  .attendance-hint {
    color: #6b7280;
    font-size: 0.95rem;
    margin-bottom: 8px;
  }
  .attendance-table .check-col {
    width: 80px;
    text-align: center;
  }
  .attendance-table input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: #991b1b;
    cursor: pointer;
  }
  .check-label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-weight: 600;
    font-size: 0.85rem;
    color: #374151;
    cursor: pointer;
    justify-content: center;
  }
  .row-checked td {
    background: #fef2f2 !important;
  }
  .row-present td {
    background: #f0fdf4 !important;
  }
  .row-absent td {
    background: #fff7ed !important;
  }
  .attendance-banner {
    padding: 14px 20px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    margin: 12px 0;
  }
  .attendance-banner.success {
    background: #d1fae5;
    color: #065f46;
    border: 1px solid #a7f3d0;
  }
  .attendance-banner.info {
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #fde68a;
  }
  .error-msg {
    color: #991b1b;
    background: #fee2e2;
    padding: 10px 16px;
    border-radius: 6px;
    margin: 10px 0;
    font-weight: 600;
  }

  /* ── Buttons ── */
  .btn-confirm {
    margin-top: 20px;
    padding: 12px 28px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    background: #16a34a;
    color: white;
    font-weight: 700;
    font-size: 1rem;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(22,163,74,0.15);
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .btn-confirm:hover:not(:disabled) {
    background: #15803d;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(22,163,74,0.25);
  }
  .btn-confirm:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  .btn-return {
    margin-top: 24px;
    padding: 10px 22px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    background: #991b1b;
    color: white;
    font-weight: 700;
    font-size: 1rem;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(153,27,27,0.12);
  }
  .btn-return:hover {
    background: #7f1d1d;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(153,27,27,0.2);
  }

  /* ── Spinners ── */
  .spinner-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 32px 0;
    color: #888;
  }
  .spinner {
    width: 36px;
    height: 36px;
    border: 4px solid #fecaca;
    border-top-color: #991b1b;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }
  .btn-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
