<script lang="ts">
  import { auth } from '$lib/stores/auth.store';
</script>

<h1>Bienvenue sur Actual Gym</h1>

{#if $auth.accessToken}
  <p>Vous êtes connecté. Accédez au <a href="/dashboard">tableau de bord</a>.</p>
{:else}
  <p>Veuillez vous <a href="/login">connecter</a> pour accéder aux séances.</p>
{/if}