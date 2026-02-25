<script lang="ts">
  import { createUser } from '$lib/api/auth.api';
  let email = '';
  let password = '';
  let error = '';
  let success = '';

  async function handleRegister() {
    error = '';
    success = '';
    try {
      await createUser(email, password);
      success = 'Inscription réussie !';
    } catch (e) {
      error = 'Erreur lors de l’inscription';
    }
  }
</script>

<h1>Inscription</h1>
{#if error}<div class="error-message">{error}</div>{/if}
{#if success}<div class="success-message">{success}</div>{/if}
<form on:submit|preventDefault={handleRegister}>
  <input type="email" bind:value={email} placeholder="Email" required />
  <input type="password" bind:value={password} placeholder="Mot de passe" required />
  <button type="submit">S’inscrire</button>
</form>