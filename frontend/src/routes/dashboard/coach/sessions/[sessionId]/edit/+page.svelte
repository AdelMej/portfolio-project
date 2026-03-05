<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { goto } from '$app/navigation';
	import { listCoachSessions, updateSession, type CompleteSession } from '$lib/api/sessions.api';

	let session: CompleteSession | null = null;
	let loading = true;
	let saving = false;
	let error = '';
	let success = '';

	let title = '';
	let date = '';
	let startTime = '';
	let endTime = '';
    let participants: any[] = [];

	onMount(async () => {
		loading = true;
		try {
			const sessionId = get(page).params.sessionId;
			const sessions = await listCoachSessions();
			session = sessions.find(s => s.id === sessionId) || null;
			if (session) {
				title = session.title;
				const startsAt = new Date(session.starts_at);
				const endsAt = new Date(session.ends_at);
				date = startsAt.toISOString().slice(0, 10);
				startTime = startsAt.toTimeString().slice(0, 5);
				endTime = endsAt.toTimeString().slice(0, 5);    
                participants = session.participants || [];
			} else {
				error = 'Seance non trouvee';
			}
		} catch (e) {
			error = 'Erreur lors du chargement de la seance';
		} finally {
			loading = false;
		}
	});

	async function handleSubmit() {
		if (!session) return;
		saving = true;
		error = '';
		success = '';
		try {
			const starts_at = new Date(date + "T" + startTime + ":00").toISOString();
			const ends_at = new Date(date + "T" + endTime + ":00").toISOString();
			await updateSession(session.id, { title, starts_at, ends_at });
			success = 'Seance mise a jour avec succes';
		} catch (e: any) {
			if (e?.code === 'session_overlapping') {
				error = 'Une autre séance existe déjà sur ce créneau horaire. Veuillez choisir un autre horaire.';
			} else {
				error = e?.detail ?? 'Erreur lors de la mise à jour';
			}
		} finally {
			saving = false;
		}
	}
</script>

<div class="edit-container">
	{#if loading}
		<div class="loading-center"><div class="spinner"></div></div>
		<div class="error-msg">{error}</div>
	{:else if session}
		<h1>Modifier la seance</h1>

		{#if success}
			<div class="success-msg">{success}</div>
		{/if}
		{#if error}
			<div class="error-msg">{error}</div>
		{/if}

		<form on:submit|preventDefault={handleSubmit}>
			<div class="form-group">
				<label for="title">Titre</label>
				<input id="title" type="text" bind:value={title} required minlength="3" />
			</div>

			<div class="form-group">
				<label for="date">Date</label>
				<input id="date" type="date" bind:value={date} required />
			</div>

			<div class="form-row">
				<div class="form-group">
					<label for="startTime">Heure de debut</label>
					<input id="startTime" type="time" bind:value={startTime} required />
				</div>
				<div class="form-group">
					<label for="endTime">Heure de fin</label>
					<input id="endTime" type="time" bind:value={endTime} required />
				</div>
			</div>

			<div class="form-group">
				<label for="status">Statut</label>
				<span id="status" class="badge {session.status === 'cancelled' ? 'badge-danger' : 'badge-success'}">
					{session.status === 'cancelled' ? 'Annulee' : 'Active'}
				</span>
			</div>

			<div class="actions">
				<button type="submit" class="btn-primary" disabled={saving}>
					{saving ? 'Enregistrement...' : 'Enregistrer'}
				</button>
				<button type="button" class="btn-secondary" on:click={() => goto('/dashboard/coach')}>
					&#8592; Retour
				</button>
			</div>
		</form>
	{:else}
		<div class="error-msg">Seance non trouvee</div>
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
.form-group {
  margin-bottom: 18px;
}
.form-group label {
  display: block;
  font-weight: 700;
  color: #374151;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}
.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.form-group input:focus {
  outline: none;
  border-color: #991b1b;
  box-shadow: 0 0 0 2px rgba(153,27,27,0.08);
}
.form-row {
  display: flex;
  gap: 16px;
}
.form-row .form-group {
  flex: 1;
}
.actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}
.btn-primary {
  flex: 1;
  padding: 12px 22px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  background: #991b1b;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  transition: background 0.2s, transform 0.15s;
}
.btn-primary:hover {
  background: #7f1d1d;
  transform: translateY(-1px);
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
.btn-secondary {
  padding: 12px 22px;
  border-radius: 8px;
  border: 1.5px solid #e5e7eb;
  cursor: pointer;
  background: white;
  color: #374151;
  font-weight: 700;
  font-size: 1rem;
  transition: background 0.2s;
}
.btn-secondary:hover {
  background: #f3f4f6;
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
