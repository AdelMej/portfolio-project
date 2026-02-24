
<script lang="ts">
  import { auth } from '$lib/stores/auth.store';
</script>

<style>
.home-container {
  max-width: 900px;
  margin: 60px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #e5e7eb;
  padding: 48px 40px 40px 40px;
  text-align: center;
}
h1 {
  font-size: 2.6rem;
  color: #2563eb;
  margin-bottom: 18px;
  letter-spacing: 1px;
}
h2 {
  font-size: 1.5rem;
  color: #374151;
  margin-bottom: 32px;
}
a, .main-btn {
  display: inline-block;
  background: #2563eb;
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  margin: 18px 10px 0 10px;
  text-decoration: none;
  transition: background 0.2s;
}
a:hover, .main-btn:hover {
  background: #1d4ed8;
}
.home-links {
  margin-top: 32px;
}
</style>

<div class="home-container">
  <h1>Bienvenue à Actual Digital Gym</h1>
  <h2>Votre espace pour gérer vos séances, coachs et participants</h2>
  <div class="home-links">
    {#if $auth.accessToken}
      <a href="/dashboard" class="main-btn">Tableau de bord</a>
    {:else}
      <a href="/login" class="main-btn">Connexion</a>
      <a href="/sessions" class="main-btn">Voir les séances</a>
    {/if}
  </div>
</div>