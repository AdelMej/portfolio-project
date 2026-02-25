<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { getAdminUsers, type AdminUser } from '$lib/api/admin.api';
  import { get } from 'svelte/store';
  
  let user: AdminUser | null = null;
  let loading = true;
  let error = '';

  onMount(async () => {
    loading = true;
    error = '';
    try {
      const userId = get(page).params.userId;
      const usersRes = await getAdminUsers();
      user = usersRes.items.find((u: AdminUser) => u.id === userId) || null;
      if (!user) error = 'Utilisateur non trouvé';
    } catch (e) {
      error = 'Erreur lors du chargement de l’utilisateur';
    } finally {
      loading = false;
    }
  });
</script>

{#if loading}
  <div>Chargement...</div>
{:else if error}
  <div style="color: red;">{error}</div>
{:else}
  <h1>Modifier l’utilisateur</h1>
  <div>Email: {user?.email}</div>
  <!-- Add your edit form here -->
{/if}