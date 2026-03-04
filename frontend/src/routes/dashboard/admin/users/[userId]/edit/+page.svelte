<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import {
    getAdminUsers,
    grantRole,
    revokeRole,
    disableUser,
    reenableUser,
    type AdminUser
  } from '$lib/api/admin.api';
  import { get } from 'svelte/store';

  let user: AdminUser | null = null;
  let loading = true;
  let error = '';
  let success = '';
  let actionLoading = false;

  const ALL_ROLES = ['admin', 'coach', 'user'];

  onMount(async () => {
    loading = true;
    error = '';
    try {
      const userId = get(page).params.userId;
      const usersRes = await getAdminUsers(100, 0);
      user = usersRes.items.find((u: AdminUser) => u.id === userId) || null;
      if (!user) error = 'Utilisateur non trouvé';
    } catch (e) {
      error = "Erreur lors du chargement de l'utilisateur";
    } finally {
      loading = false;
    }
  });

  function hasRole(role: string): boolean {
    return user?.roles?.includes(role) ?? false;
  }

  async function toggleRole(role: string) {
    if (!user) return;
    actionLoading = true;
    error = '';
    success = '';
    try {
      if (hasRole(role)) {
        await revokeRole(user.id, role);
        user.roles = user.roles.filter(r => r !== role);
      } else {
        await grantRole(user.id, role);
        user.roles = [...user.roles, role];
      }
      user = user;
      success = 'Rôle mis à jour';
    } catch (e: any) {
      error = e?.detail ?? 'Erreur lors de la modification du rôle';
    } finally {
      actionLoading = false;
    }
  }

  async function toggleDisable() {
    if (!user) return;
    actionLoading = true;
    error = '';
    success = '';
    try {
      if (user.disabled_at) {
        await reenableUser(user.id);
        user.disabled_at = null;
        success = 'Utilisateur réactivé';
      } else {
        await disableUser(user.id, 'Désactivé par admin');
        user.disabled_at = new Date().toISOString();
        success = 'Utilisateur désactivé';
      }
      user = user;
    } catch (e: any) {
      error = e?.detail ?? "Erreur lors de la modification du statut";
    } finally {
      actionLoading = false;
    }
  }
</script>

<div class="edit-container">
  {#if loading}
    <div class="loading-center"><div class="spinner"></div></div>
  {:else if error && !user}
    <div class="error-msg">{error}</div>
  {:else if user}
    <h1>Modifier l'utilisateur</h1>

    {#if success}
      <div class="success-msg">{success}</div>
    {/if}
    {#if error}
      <div class="error-msg">{error}</div>
    {/if}

    <div class="field">
      <span class="field-label">Email</span>
      <div class="field-value">{user.email}</div>
    </div>

    <div class="field">
      <span class="field-label">Statut</span>
      <div class="field-value">
        {#if user.disabled_at}
          <span class="badge badge-danger">Désactivé</span>
        {:else}
          <span class="badge badge-success">Actif</span>
        {/if}
        <button
          class="btn-small {user.disabled_at ? 'btn-success' : 'btn-danger'}"
          on:click={toggleDisable}
          disabled={actionLoading}
        >
          {user.disabled_at ? 'Réactiver' : 'Désactiver'}
        </button>
      </div>
    </div>

    <div class="field">
      <span class="field-label">Rôles</span>
      <div class="roles-list">
        {#each ALL_ROLES as role}
          <label class="role-toggle">
            <input
              type="checkbox"
              checked={hasRole(role)}
              on:change={() => toggleRole(role)}
              disabled={actionLoading}
            />
            <span class="role-name">{role}</span>
          </label>
        {/each}
      </div>
    </div>

    <div class="field">
      <span class="field-label">Créé le</span>
      <div class="field-value">{new Date(user.created_at).toLocaleString('fr-FR')}</div>
    </div>

    <button class="btn-return" on:click={() => goto('/dashboard/admin')}>← Retour</button>
  {:else}
    <div class="error-msg">Utilisateur non trouvé</div>
  {/if}
</div>

<style>
.edit-container {
  max-width: 600px;
  margin: 60px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #e5e7eb;
  padding: 40px 32px;
}
h1 {
  font-size: 2rem;
  color: #1f2937;
  margin-bottom: 24px;
  text-align: center;
}
.field {
  padding: 16px 0;
  border-bottom: 1px solid #e5e7eb;
}
.field-label {
  display: block;
  font-weight: 700;
  color: #374151;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}
.field-value {
  color: #374151;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 12px;
}
.roles-list {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.role-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 6px 12px;
  background: #f9fafb;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: background 0.15s;
}
.role-toggle:hover {
  background: #f3f4f6;
}
.role-toggle input[type="checkbox"] {
  accent-color: #991b1b;
  width: 16px;
  height: 16px;
}
.role-name {
  font-weight: 600;
  color: #374151;
  text-transform: capitalize;
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
.btn-small {
  padding: 6px 14px;
  border-radius: 6px;
  border: none;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-success {
  background: #16a34a;
  color: white;
}
.btn-success:hover {
  background: #15803d;
}
.btn-danger {
  background: #dc2626;
  color: white;
}
.btn-danger:hover {
  background: #b91c1c;
}
.btn-small:disabled {
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
  transition: background 0.2s, transform 0.15s;
}
.btn-return:hover {
  background: #7f1d1d;
  transform: translateY(-1px);
}
.error-msg {
  color: #991b1b;
  background: #fee2e2;
  padding: 12px 16px;
  border-radius: 6px;
  text-align: center;
  margin-bottom: 16px;
}
.success-msg {
  color: #065f46;
  background: #d1fae5;
  padding: 12px 16px;
  border-radius: 6px;
  text-align: center;
  margin-bottom: 16px;
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
  border-top-color: #374151;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
