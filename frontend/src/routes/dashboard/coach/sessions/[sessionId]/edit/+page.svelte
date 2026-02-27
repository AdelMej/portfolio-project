<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { listSessions, type Session } from '$lib/api/sessions.api';

	let session: Session | null = null;
	let loading = true;
	let error = '';

	onMount(async () => {
		loading = true;
		try {
			const sessionId = get(page).params.sessionId;
			const sessions = await listSessions();
			session = sessions.find(s => s.id === sessionId) || null;
			if (!session) error = 'Séance non trouvée';
		} catch (e) {
			error = 'Erreur lors du chargement de la séance';
		} finally {
			loading = false;
		}
	});
</script>

<div class="edit-container">
{#if loading}
	<div class="loading-center"><div class="spinner"></div></div>
{:else if error}
	<div class="error-msg">{error}</div>
{:else if session}
	<h1>Modifier la séance</h1>
	<div class="field"><strong>Titre :</strong> {session.title}</div>
	<!-- Add your edit form here -->
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
  color: #991b1b;
  margin-bottom: 24px;
  text-align: center;
}
.field {
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
  color: #374151;
  font-size: 1rem;
}
.error-msg {
  color: #991b1b;
  background: #fee2e2;
  padding: 12px 16px;
  border-radius: 6px;
  text-align: center;
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
  border-top-color: #991b1b;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
