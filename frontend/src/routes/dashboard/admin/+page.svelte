<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { apiFetch } from '$lib/api/client';

  // Match backend fields
  type Session = {
    id: string;
    title: string;
    starts_at: string;
    ends_at: string;
    coach_id: string;
    coach_name?: string; // optional if backend sends it
    max_participants?: number;
    participants_count?: number;
    status: 'scheduled' | 'cancelled';
  };

  let seances: Session[] = [];
  let chargement = true;
  let error = '';

  async function chargerSeances() {
    chargement = true;
    error = '';
    try {
      const data = await apiFetch('/sessions');
      // Use items array if exists
      seances = Array.isArray(data.items) ? data.items : [];
    } catch (e: any) {
      console.error('Erreur lors du chargement des séances', e);
      error = 'Impossible de charger les séances';
      seances = [];
    } finally {
      chargement = false;
    }
  }

  async function annulerSeance(id: string) {
    try {
      await apiFetch(`/sessions/${id}/cancel`, { method: 'PUT' });
      await chargerSeances(); // reload after cancellation
    } catch (e: any) {
      console.error('Erreur lors de l\'annulation', e);
      alert('Impossible d\'annuler cette séance');
    }
  }

  onMount(chargerSeances);
</script>

<div class="container">
  <div class="header">
    <h1>Gestion des séances</h1>
    <button class="btn-primary" on:click={() => goto('/dashboard/admin/new-session')}>
      + Créer une séance
    </button>
  </div>

  {#if chargement}
    <p>Chargement...</p>
  {:else if error}
    <p style="color:red">{error}</p>
  {:else if seances.length === 0}
    <p>Aucune séance trouvée.</p>
  {:else}
    <table>
      <thead>
        <tr>
          <th>Titre</th>
          <th>Début</th>
          <th>Fin</th>
          <th>Coach</th>
          <th>Participants max</th>
          <th>Actuels</th>
          <th>Statut</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {#each seances as seance}
          <tr>
            <td>{seance.title}</td>
            <td>{new Date(seance.starts_at).toLocaleString('fr-FR')}</td>
            <td>{new Date(seance.ends_at).toLocaleString('fr-FR')}</td>
            <td>{seance.coach_name || seance.coach_id}</td>
            <td>{seance.max_participants ?? '-'}</td>
            <td>{seance.participants_count ?? 0}</td>
            <td>
              {#if seance.status === 'cancelled'}
                <span class="badge badge-danger">Annulée</span>
              {:else}
                <span class="badge badge-success">Active</span>
              {/if}
            </td>
            <td class="actions">
              <button on:click={() => goto(`/sessions/${seance.id}/participants`)}>
                Voir participants
              </button>
              <button on:click={() => goto(`/sessions/${seance.id}`)}>
                Modifier
              </button>
              {#if seance.status !== 'cancelled'}
                <button class="btn-danger" on:click={() => annulerSeance(seance.id)}>
                  Annuler
                </button>
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>
