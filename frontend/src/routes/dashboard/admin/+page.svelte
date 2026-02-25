<!-- frontend/src/routes/dashboard/admin/+page.svelte -->
<script lang="ts">
  import { onMount } from 'svelte';
  import { getAdminUsers, type AdminUser } from '$lib/api/admin.api';
  import { listSessions, type Session } from '$lib/api/sessions.api';

  let users: AdminUser[] = [];
  let sessions: Session[] = [];
  let loading = true;
  let error = '';

  onMount(async () => {
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
  });
</script>

<style>
.admin-dashboard-container {
  max-width: 1100px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 16px #e5e7eb;
  padding: 36px 32px 32px 32px;
}
h1 {
  font-size: 2.2rem;
  margin-bottom: 24px;
  color: #2563eb;
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
  color: #2563eb;
  font-weight: 700;
}
tr:last-child td {
  border-bottom: none;
}
</style>

<div class="admin-dashboard-container">
  <h1>Admin Dashboard</h1>
  {#if loading}
    <div>Chargement...</div>
  {:else if error}
    <div style="color: red;">{error}</div>
  {:else}
    <h2>Gestion des utilisateurs</h2>
    <table>
      <thead>
        <tr>
          <th>Email</th>
          <th>Rôles</th>
          <th>Statut</th>
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

    <a href="/dashboard/admin/new-session" class="dashboard-btn">Ajouter une séance</a>

    <h2>Gestion des séances</h2>
    <table>
      <thead>
        <tr>
          <th>Titre</th>
          <th>Date</th>
          <th>Coach</th>
        </tr>
      </thead>
      <tbody>
        {#each sessions as s}
          <tr>
            <td>{s.title}</td>
            <td>{new Date(s.starts_at).toLocaleString('fr-FR')}</td>
            <td>{s.coach_name ?? 'Non défini'}</td>
            <td><a href={`/dashboard/admin/sessions/${s.id}/edit`} class="dashboard-btn">Modifier</a></td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>