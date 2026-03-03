<!-- frontend/src/routes/dashboard/admin/+page.svelte -->
<script lang="ts">

  import { onMount } from 'svelte';
  import { getAdminUsers, type AdminUser } from '$lib/api/admin.api';
  import { listSessions, cancelSession, type Session } from '$lib/api/sessions.api';
  import { goto } from '$app/navigation';
  import { afterNavigate } from '$app/navigation';
  import { apiFetch } from '$lib/api/client';

  let users: AdminUser[] = [];
  let sessions: Session[] = [];
  let loading = true;
  let error = '';
  let cancellingId = '';

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
      const sessionRes = await listSessions();
      sessions = sessionRes ?? [];
    } catch (e) {
      error = "Erreur lors du chargement des données.";
    } finally {
      loading = false;
    }
  }

  onMount(loadDashboardData);

  afterNavigate(() => {
    loadDashboardData();
  });
</script>

<style>
.admin-dashboard-container {
  max-width: 1100px;
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
tr:last-child td {
  border-bottom: none;
}
tr:hover td {
  background: #fef2f2;
}
.dashboard-btn {
  display: inline-block;
  background: #991b1b;
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(153,27,27,0.12);
}
.dashboard-btn:hover {
  background: #7f1d1d;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(153,27,27,0.2);
}
button {
  background: #991b1b;
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(153,27,27,0.12);
}
button:hover {
  background: #7f1d1d;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(153,27,27,0.2);
}
.spinner {
  display: inline-block;
  width: 32px;
  height: 32px;
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
.error-msg {
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 16px;
  border-radius: 6px;
  text-align: center;
  margin-bottom: 18px;
}
</style>

<div class="admin-dashboard-container">
  <h1>Tableau de bord Admin</h1>
  {#if loading}
    <div class="loading-center"><div class="spinner"></div></div>
  {:else if error}
    <div class="error-msg">{error}</div>
  {:else}
    <h2>Gestion des utilisateurs</h2>
      <a href="/dashboard/admin/users/registration" class="dashboard-btn" style="margin-bottom: 18px; display: inline-block;">Créer un nouvel utilisateur</a>
    <table>
      <thead>
        <tr>
          <th>Email</th>
          <th>Rôles</th>
          <th>Statut</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {#each users as user}
          <tr>
            <td>{user.email}</td>
            <td>{user.roles ? user.roles.join(', ') : ''}</td>
            <td>{user.disabled_at ? 'Désactivé' : 'Actif'}</td>
            <td><a href={`/dashboard/admin/users/${user.id}/edit`} class="dashboard-btn">Modifier</a></td>
          </tr>
        {/each}
      </tbody>
    </table>

    <h2>Gestion des séances</h2>
    <table>
      <thead>
        <tr>
          <th>Titre</th>
          <th>Date</th>
          <th>Coach</th>
          <th>Prix</th>
          <th>Statut</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        {#each sessions as s}
            <tr>
            <td>{s.title}</td>
            <td>{new Date(s.starts_at).toLocaleString('fr-FR')}</td>
            <td>{s.coach_name}</td>
            <td>{s.price_cents != null ? (s.price_cents / 100).toFixed(2) + ' ' + (s.currency ?? 'EUR') : '-'}</td>
            <td>{s.status === 'cancelled' ? 'Annulée' : 'Active'}</td>
            <td>
                {#if s.status !== 'cancelled'}
                  <button on:click={() => adminCancelSession(s.id)} disabled={cancellingId === s.id}>
                    {cancellingId === s.id ? '...' : 'Annuler'}
                  </button>
                {/if}
                <button on:click={() => goto(`/sessions/${s.id}/participants`)} style="margin-left: 8px;">Voir participants</button>
            </td>
            </tr>
        {/each}
        </tbody>
    </table>
  {/if}
</div>