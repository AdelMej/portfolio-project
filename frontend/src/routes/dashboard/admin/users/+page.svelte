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

<h1>Gestion des utilisateurs</h1>

{#if loading}
<p>Chargement...</p>

{:else if error}
<p style="color:red">{error}</p>

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
<td>{user.id}</td>
<td>{user.roles?.join(', ') ?? 'user'}</td>
</tr>
{/each}
</tbody>
</table>

{/if}