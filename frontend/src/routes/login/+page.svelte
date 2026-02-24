<script lang="ts">
import type { LoginResponse, MeResponse } from '$lib/api/auth.api';
import { login, getMe } from '$lib/api/auth.api';
import { auth } from '$lib/stores/auth.store';
import { goto } from '$app/navigation';
import { tick } from 'svelte';

let email = '';
let password = '';
let error = '';
let loading = false;

async function handleLogin() {
  loading = true;
  error = '';
  try {
    const tokenResponse: LoginResponse = await login(email, password);
    auth.login(tokenResponse.access_token);
    await tick();
    const me: MeResponse = await getMe();
    auth.login(tokenResponse.access_token, me.roles);

    if (me.roles.includes('admin')) goto('/dashboard/admin');
    else if (me.roles.includes('coach')) goto('/dashboard/coach');
    else goto('/dashboard/user');
  } catch (e: any) {
    if (e?.status === 401 || e?.message?.includes('Unauthorized')) {
      error = 'Email ou mot de passe incorrect';
    } else {
      console.warn('Warning fetching roles', e);
      error = 'Erreur de connexion';
    }
  } finally {
    loading = false;
  }
}
</script>

<style>
.login-container {
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
  margin-bottom: 28px;
  color: #2563eb;
  text-align: center;
  letter-spacing: 1px;
}
input {
  width: 100%;
  padding: 12px 10px;
  margin-bottom: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 1rem;
  background: #f9fafb;
  transition: border 0.2s;
}
input:focus {
  border: 1.5px solid #2563eb;
  outline: none;
}
button {
  width: 100%;
  background: #2563eb;
  color: white;
  border: none;
  padding: 12px 0;
  border-radius: 6px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 10px;
  transition: background 0.2s;
}
button:disabled {
  background: #a5b4fc;
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
</style>

<div class="login-container">
  <h1>Connexion à votre compte</h1>
  {#if error}
    <div class="error-message">{error}</div>
  {/if}
  <input
    type="email"
    placeholder="Adresse e-mail"
    bind:value={email}
    autocomplete="username"
    required
  />
  <input
    type="password"
    placeholder="Mot de passe"
    bind:value={password}
    autocomplete="current-password"
    required
  />
  <button on:click={handleLogin} disabled={loading}>
    {loading ? 'Connexion...' : 'Se connecter'}
  </button>
</div>