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

<div class="form-container">
  <h1>Créer une séance</h1>
  <div class="form-group">
    <input placeholder="Nom de la séance" bind:value={title} />
    <input type="datetime-local" bind:value={date} />
    <input type="number" bind:value={maxParticipants} placeholder="Max participants" />
  </div>
  <div class="form-actions">
    <button class="btn-primary" on:click={submit}>Créer séance</button>
    <button class="btn-secondary" on:click={() => goto('/dashboard/admin')}>Annuler</button>
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
  color: #991b1b;
  text-align: center;
  margin-bottom: 28px;
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
  transition: border 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}
input:focus {
  border-color: #991b1b;
  outline: none;
  box-shadow: 0 0 0 3px rgba(153,27,27,0.1);
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
  transition: background 0.2s, transform 0.15s;
}
.btn-primary:hover {
  background: #7f1d1d;
  transform: translateY(-1px);
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
