<script lang="ts">
  import { auth } from '$lib/stores/auth.store';
  import { get } from 'svelte/store';
  let email = '';
  let password = '';
  let error = '';
  let success = '';

  async function handleCreateUser() {
    error = '';
    success = '';
    try {
      const res = await fetch('/api/v1/users', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${get(auth).accessToken}`
        },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) {
        let data;
        try {
          data = await res.json();
        } catch {
          data = {};
        }
        throw new Error(data?.error || 'Erreur lors de la création');
      }
      success = 'Utilisateur créé avec succès !';
      email = '';
      password = '';
    } catch (e) {
        if (e instanceof Error) {
        error = e.message || 'Erreur lors de la création';
        } else {
        error = 'Erreur lors de la création';
        }
    }
}
</script>

<h1>Créer un nouvel utilisateur</h1>
{#if error}<div class="error-message">{error}</div>{/if}
{#if success}<div class="success-message">{success}</div>{/if}
<form on:submit|preventDefault={handleCreateUser}>
  <input type="email" bind:value={email} placeholder="Email" required />
  <input type="password" bind:value={password} placeholder="Mot de passe" required />
  <button type="submit">Créer</button>
</form>