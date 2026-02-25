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

{#if loading}
	<div>Chargement...</div>
{:else if error}
	<div style="color: red;">{error}</div>
{:else if session}
	<h1>Modifier la séance</h1>
	<div>Titre: {session.title}</div>
	<!-- Add your edit form here -->
{/if}
