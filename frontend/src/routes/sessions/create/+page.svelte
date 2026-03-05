<script lang="ts">
	import { goto } from '$app/navigation';
	import { listSessions, createSession } from '$lib/api/sessions.api';
	import { getStripeOnboardingLink } from '$lib/api/stripe.api';
	import { AlertTriangle } from 'lucide-svelte';

	let name = '';
	let date = '';
	let startTime = '';
	let endTime = '';
	let price = '';
	let errorMsg = '';
	let stripeError = false;
	let stripeOnboardingUrl = '';
	let submitting = false;

	async function redirectToStripe() {
		try {
			const { url } = await getStripeOnboardingLink();
			window.location.href = url;
		} catch {
			errorMsg = 'Impossible de récupérer le lien Stripe. Réessayez plus tard.';
		}
	}

	async function submit() {
		errorMsg = '';
		stripeError = false;

		if (!date || !startTime || !endTime) {
			errorMsg = "Veuillez remplir la date, l'heure de début et l'heure de fin.";
			return;
		}
		if (!name.trim()) {
			errorMsg = 'Veuillez entrer un nom de séance.';
			return;
		}

		const priceNum = parseFloat(price) || 0;
		if (priceNum < 0) {
			errorMsg = 'Le prix ne peut pas être négatif.';
			return;
		}

		const startsAt = new Date(date + 'T' + startTime + ':00').toISOString();
		const endsAt = new Date(date + 'T' + endTime + ':00').toISOString();

  submitting = true;
  try {
    await createSession({
      title: name.trim(),
      starts_at: startsAt,
      ends_at: endsAt,
      price_cents: Math.round(priceNum * 100),
      currency: 'EUR'
    });
    goto('/dashboard/coach');
  } catch (e) {
    if (e && typeof e === 'object' && 'code' in e && e.code === 'invalid_stripe_account') {
      stripeError = true;
      errorMsg = 'Votre compte Stripe n\'est pas encore configuré. Veuillez compléter votre inscription Stripe avant de créer une séance.';
    } else if (e && typeof e === 'object' && 'code' in e && e.code === 'session_overlapping') {
      errorMsg = 'Une autre séance existe déjà sur ce créneau horaire. Veuillez choisir un autre horaire.';
    } else {
      errorMsg = 'Erreur lors de la création de la séance.';
    }
  } finally {
    submitting = false;
  }
}
</script>

<div class="form-container">
	<h1>Créer une séance</h1>

	{#if errorMsg}
		<div class="error-banner" class:stripe-error={stripeError}>
			<AlertTriangle size={20} />
			<div class="error-content">
				<p>{errorMsg}</p>
				{#if stripeError}
					<button class="btn-stripe" on:click={redirectToStripe}>
						Configurer mon compte Stripe →
					</button>
				{/if}
			</div>
		</div>
	{/if}

	<div class="form-group">
		<input placeholder="Nom de la séance" bind:value={name} />
		<input type="date" bind:value={date} />
		<div class="form-row">
			<div class="form-field">
				<label class="form-label" for="start-time">Heure de début</label>
				<input id="start-time" type="time" bind:value={startTime} />
			</div>
			<div class="form-field">
				<label class="form-label" for="end-time">Heure de fin</label>
				<input id="end-time" type="time" bind:value={endTime} />
			</div>
		</div>
		<label class="form-label" for="price">Prix (EUR)</label>
		<input
			id="price"
			type="text"
			inputmode="decimal"
			bind:value={price}
			min="0"
			placeholder="Ex: 20.00"
		/>
	</div>
	<div class="form-actions">
		<button class="btn-primary" on:click={submit} disabled={submitting}>
			{submitting ? 'Création...' : 'Créer'}
		</button>
		<button class="btn-secondary" on:click={() => goto('/dashboard/coach')}>Annuler</button>
	</div>
</div>

<style>
	.form-container {
		max-width: 500px;
		margin: 60px auto;
		background: #fff;
		border-radius: 16px;
		box-shadow: 0 4px 24px #e5e7eb;
		padding: 40px 32px 32px 32px;
	}
	h1 {
		font-size: 2rem;
		color: #1f2937;
		text-align: center;
		margin-bottom: 28px;
	}
	.error-banner {
		display: flex;
		gap: 12px;
		align-items: flex-start;
		padding: 14px 16px;
		border-radius: 10px;
		background: #fef2f2;
		border: 1px solid #fecaca;
		color: #991b1b;
		margin-bottom: 20px;
		font-size: 0.93rem;
		line-height: 1.5;
	}
	.error-banner.stripe-error {
		background: #fffbeb;
		border-color: #fde68a;
		color: #92400e;
	}
	.error-content {
		flex: 1;
	}
	.error-content p {
		margin: 0 0 10px 0;
	}
	.error-content p:last-child {
		margin-bottom: 0;
	}
	.btn-stripe {
		display: inline-block;
		background: #7c3aed;
		color: white;
		border: none;
		padding: 8px 18px;
		border-radius: 6px;
		font-weight: 600;
		font-size: 0.9rem;
		cursor: pointer;
		transition:
			background 0.2s,
			transform 0.15s;
	}
	.btn-stripe:hover {
		background: #6d28d9;
		transform: translateY(-1px);
	}
	.form-group {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}
	input {
		width: 100%;
		padding: 12px 14px;
		border: 1.5px solid #e5e7eb;
		border-radius: 8px;
		font-size: 1rem;
		background: #f9fafb;
		transition:
			border 0.2s,
			box-shadow 0.2s;
		box-sizing: border-box;
	}
	input:focus {
		border-color: #991b1b;
		outline: none;
		box-shadow: 0 0 0 3px rgba(153, 27, 27, 0.1);
	}
	.form-label {
		font-weight: 600;
		color: #374151;
		font-size: 0.95rem;
		margin-bottom: -8px;
	}
	.form-row {
		display: flex;
		gap: 12px;
	}
	.form-field {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.form-actions {
		display: flex;
		gap: 12px;
		margin-top: 24px;
	}
	.btn-primary {
		flex: 1;
		background: #991b1b;
		color: white;
		border: none;
		padding: 12px 0;
		border-radius: 8px;
		font-weight: 700;
		font-size: 1rem;
		cursor: pointer;
		transition:
			background 0.2s,
			transform 0.15s;
	}
	.btn-primary:hover:not(:disabled) {
		background: #7f1d1d;
		transform: translateY(-1px);
	}
	.btn-primary:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
	.btn-secondary {
		flex: 1;
		background: #f3f4f6;
		color: #374151;
		border: 1px solid #e5e7eb;
		padding: 12px 0;
		border-radius: 8px;
		font-weight: 600;
		font-size: 1rem;
		cursor: pointer;
		transition: background 0.2s;
	}
	.btn-secondary:hover {
		background: #e5e7eb;
	}
</style>
