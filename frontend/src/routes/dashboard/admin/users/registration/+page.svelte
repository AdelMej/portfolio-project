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

<div class="form-container">
  <h1>Créer un nouvel utilisateur</h1>
  {#if error}<div class="error-message">{error}</div>{/if}
  {#if success}<div class="success-message">{success}</div>{/if}
  <form on:submit|preventDefault={handleCreateUser}>
    <input type="email" bind:value={email} placeholder="Adresse e-mail" required />
    <input type="password" bind:value={password} placeholder="Mot de passe" required />
    <button type="submit">Créer l'utilisateur</button>
  </form>
</div>

<style>
.form-container {
  max-width: 450px;
  margin: 60px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #e5e7eb;
  padding: 40px 32px 32px 32px;
  text-align: center;
}
h1 {
  font-size: 1.8rem;
  color: #991b1b;
  margin-bottom: 24px;
}
input {
  width: 100%;
  padding: 12px 14px;
  margin-bottom: 16px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  background: #f9fafb;
  transition: border 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}
input:focus {
  border-color: #991b1b;
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
  transition: background 0.2s, transform 0.15s;
  box-shadow: 0 2px 8px rgba(153,27,27,0.12);
}
button[type="submit"]:hover {
  background: #7f1d1d;
  transform: translateY(-1px);
}
.error-message {
  color: #991b1b;
  background: #fee2e2;
  padding: 10px 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}
.success-message {
  color: #065f46;
  background: #d1fae5;
  padding: 10px 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}
</style>