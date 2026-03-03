<script lang="ts">
  import { onMount } from 'svelte';
  import { fly, fade } from 'svelte/transition';
  import { createUser } from '$lib/api/auth.api';
  let email = '';
  let password = '';
  let error = '';
  let success = '';
  let loading = false;
  let ready = false;

  onMount(() => { ready = true; });

  async function handleRegister() {
    error = '';
    success = '';
    loading = true;
    try {
      await createUser(email, password);
      success = 'Inscription réussie ! Vous pouvez maintenant vous connecter.';
      email = '';
      password = '';
    } catch (e) {
      error = "Erreur lors de l'inscription";
    } finally {
      loading = false;
    }
  }
</script>

<style>
.register-container {
  max-width: 400px;
  margin: 80px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #e5e7eb;
  padding: 40px 32px 32px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
h1 {
  font-size: 2rem;
  margin-bottom: 8px;
  color: #991b1b;
  text-align: center;
  letter-spacing: 1px;
}
.reg-subtitle {
  color: #9ca3af;
  margin-bottom: 28px;
  font-size: 0.95rem;
}
form {
  width: 100%;
}
input {
  width: 100%;
  padding: 12px 14px;
  margin-bottom: 18px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  background: #f9fafb;
  transition: border 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}
input:focus {
  border: 1.5px solid #991b1b;
  outline: none;
  box-shadow: 0 0 0 3px rgba(153,27,27,0.1);
}
button[type="submit"] {
  width: 100%;
  background: #991b1b;
  color: white;
  border: none;
  padding: 13px 0;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 10px;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(153,27,27,0.12);
}
button[type="submit"]:hover:not(:disabled) {
  background: #7f1d1d;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(153,27,27,0.2);
}
button[type="submit"]:disabled {
  background: #fca5a5;
  cursor: not-allowed;
}
.error-message {
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 16px;
  border-radius: 6px;
  margin-bottom: 18px;
  text-align: center;
  width: 100%;
}
.success-message {
  color: #065f46;
  background: #d1fae5;
  padding: 10px 16px;
  border-radius: 6px;
  margin-bottom: 18px;
  text-align: center;
  width: 100%;
}
.login-link {
  margin-top: 14px;
  font-size: 0.9rem;
  color: #6b7280;
}
.login-link a {
  color: #991b1b;
  font-weight: 600;
  text-decoration: none;
}
.login-link a:hover {
  text-decoration: underline;
}
</style>

{#if ready}
<div class="register-container" in:fly={{ y: 30, duration: 400 }}>
  <h1>Inscription</h1>
  <p class="reg-subtitle">Créez votre compte</p>
  {#if error}<div class="error-message" in:fade={{ duration: 200 }}>{error}</div>{/if}
  {#if success}<div class="success-message" in:fade={{ duration: 200 }}>{success}</div>{/if}
  <form on:submit|preventDefault={handleRegister}>
    <input type="email" bind:value={email} placeholder="Adresse e-mail" required />
    <input type="password" bind:value={password} placeholder="Mot de passe" required />
    <button type="submit" disabled={loading}>{loading ? 'Inscription...' : "S'inscrire"}</button>
  </form>
  <div class="login-link">Déjà un compte ? <a href="/login">Se connecter</a></div>
</div>
{/if}
