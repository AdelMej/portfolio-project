<script lang="ts">
import { onMount } from 'svelte';
import { apiFetch } from '$lib/api/client';

type User = {
  id: string;
  email: string;
  roles?: string[];
};

let users: User[] = [];
let loading = true;
let error = '';

async function loadUsers() {
  loading = true;
  error = '';

  try {
    const data = await apiFetch('/users');
    users = data.items ?? data ?? [];
  } catch (e) {
    console.error(e);
    error = 'Erreur lors du chargement des utilisateurs';
  } finally {
    loading = false;
  }
}

onMount(loadUsers);
</script>

<div class="users-container">
  <h1>Gestion des utilisateurs</h1>

  {#if loading}
    <div class="loading-center"><div class="spinner"></div></div>
  {:else if error}
    <div class="error-msg">{error}</div>
  {:else}
    <table>
      <thead>
        <tr>
          <th>Email</th>
          <th>ID</th>
          <th>Rôles</th>
        </tr>
      </thead>
      <tbody>
        {#each users as user}
          <tr>
            <td>{user.email}</td>
            <td style="font-size:0.8rem;color:#9ca3af;">{user.id}</td>
            <td>{user.roles?.join(', ') ?? 'user'}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>

<style>
.users-container {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 16px #e5e7eb;
  padding: 36px 32px 32px 32px;
}
h1 {
  font-size: 2rem;
  color: #991b1b;
  text-align: center;
  margin-bottom: 24px;
}
table {
  width: 100%;
  border-collapse: collapse;
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
.error-msg {
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 16px;
  border-radius: 6px;
  text-align: center;
}
.loading-center {
  text-align: center;
  padding: 32px 0;
}
.spinner {
  display: inline-block;
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #991b1b;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>