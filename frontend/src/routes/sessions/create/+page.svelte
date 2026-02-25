<script lang="ts">
  import { goto } from '$app/navigation';
  import { listSessions, createSession } from '$lib/api/sessions.api';
  import { getStripeOnboardingLink } from '$lib/api/stripe.api';

  let name = '';
  let date = '';
  let coach = '';
  let maxParticipants = 0;

 async function submit() {
  const startsAt = new Date(date + "T10:00:00").toISOString();
  const endsAt = new Date(date + "T11:00:00").toISOString();

  try {
    await createSession({
      title: name,
      starts_at: startsAt,
      ends_at: endsAt,
      price_cents: 0,
      currency: "EUR"
    });
    goto('/dashboard/coach');
  } catch (e) {
    if (e && typeof e === 'object' && 'code' in e && e.code === 'invalid_stripe_account') {
      const { url } = await getStripeOnboardingLink();
      window.location.href = url;
    } else {
      // handle other errors (optional: show error message)
      alert('Erreur lors de la création de la session.');
    }
  }
}
</script>

<h1>Create Session</h1>

<input placeholder="Name" bind:value={name} />
<input type="date" bind:value={date} />
<input placeholder="Coach" bind:value={coach} />
<input type="number" bind:value={maxParticipants} />

<button on:click={submit}>Create</button>
<button on:click={() => goto('/dashboard/coach')}>Cancel</button>
