<script lang="ts">
  import { goto } from '$app/navigation';
  import { createSession } from '$lib/api/sessions.api';

  let title = '';
  let date = '';
  let maxParticipants = 0;

  async function submit() {
    const startsAt = new Date(date).toISOString();
    const endsAt = new Date(new Date(date).getTime() + 60 * 60 * 1000).toISOString();

    await createSession({
      title,
      starts_at: startsAt,
      ends_at: endsAt,
      price_cents: 0,
      currency: "EUR"
    });

    goto('/dashboard/admin');
  }
</script>

<h1>Créer une séance</h1>

<input placeholder="Nom de la séance" bind:value={title} />
<input type="datetime-local" bind:value={date} />
<input type="number" bind:value={maxParticipants} />

<button on:click={submit}>Créer séance</button>
<button on:click={() => goto('/dashboard/admin')}>Cancel</button>
