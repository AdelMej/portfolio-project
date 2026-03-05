<script lang="ts">
import { onMount } from 'svelte';
import { fly, fade } from 'svelte/transition';
import type { LoginResponse, MeResponse } from '$lib/api/auth.api';
import { login, getMe, getMyProfile } from '$lib/api/auth.api';
import { auth } from '$lib/stores/auth.store';
import { goto } from '$app/navigation';
import { tick } from 'svelte';

let email = '';
let password = '';
let error = '';
let loading = false;
let ready = false;

onMount(() => { ready = true; });

async function handleLogin() {
  loading = true;
  error = '';
  try {
    const tokenResponse: LoginResponse = await login(email, password);
    auth.login(tokenResponse.access_token);
    await tick();
    const me: MeResponse = await getMe();
    const profile = await getMyProfile();
    auth.login(tokenResponse.access_token, me.roles, me.id, me.email, profile.first_name, profile.last_name);

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

<svelte:head>
  <title>Connexion | Actual Digital Gym</title>
</svelte:head>

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
  margin-bottom: 8px;
  color: #1f2937;
  text-align: center;
  letter-spacing: 1px;
}
.login-subtitle {
  color: #9ca3af;
  margin-bottom: 28px;
  font-size: 0.95rem;
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
}
input:focus {
  border: 1.5px solid #991b1b;
  outline: none;
  box-shadow: 0 0 0 3px rgba(153,27,27,0.1);
}
button {
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
button:hover:not(:disabled) {
  background: #7f1d1d;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(153,27,27,0.2);
}
button:disabled {
  background: #d1d5db;
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
.register-link {
  margin-top: 14px;
  font-size: 0.9rem;
  color: #6b7280;
}
.register-link a {
  color: #991b1b;
  font-weight: 600;
  text-decoration: none;
}
.register-link a:hover {
  text-decoration: underline;
}
</style>

{#if ready}
<div class="login-container" in:fly={{ y: 30, duration: 400 }}>
  <h1>Connexion</h1>
  <p class="login-subtitle">Accédez à votre espace</p>
  {#if error}
    <div class="error-message" in:fade={{ duration: 200 }}>{error}</div>
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
    on:keydown={(e) => { if (e.key === 'Enter') handleLogin(); }}
  />
  <button on:click={handleLogin} disabled={loading}>
    {loading ? 'Connexion…' : 'Se connecter'}
  </button>
  <div class="register-link">Pas encore de compte ? <a href="/registration">S'inscrire</a></div>
</div>
{/if}