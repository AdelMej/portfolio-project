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
      error = '';
    }
  } finally {
    loading = false;
  }
}
</script>

<h1>Connexion</h1>

<form on:submit|preventDefault={handleLogin}>
  <input type="email" placeholder="Email" bind:value={email} required />
  <input type="password" placeholder="Mot de passe" bind:value={password} required />
  <button type="submit" disabled={loading}>
    {loading ? 'Connexion...' : 'Se connecter'}
  </button>
</form>

{#if error}
  <p style="color:red">{error}</p>
{/if}
