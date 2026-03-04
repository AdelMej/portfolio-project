<script lang="ts">
import { auth } from '$lib/stores/auth.store';
import { get } from 'svelte/store';

const roles = get(auth).roles || [];
</script>

<style>
.dashboard-landing-container {
  max-width: 700px;
  margin: 60px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #e5e7eb;
  padding: 48px 40px 40px 40px;
  text-align: center;
}
h1 {
  font-size: 2.2rem;
  color: #1f2937;
  margin-bottom: 18px;
  letter-spacing: 1px;
}
a, .dashboard-btn {
  display: inline-block;
  background: #991b1b;
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  margin: 18px 10px 0 10px;
  text-decoration: none;
  transition: background 0.2s;
}
a:hover, .dashboard-btn:hover {
  background: #7f1d1d;
}
</style>

<div class="dashboard-landing-container">
  <h1>Tableau de bord</h1>
  {#if roles.includes('admin')}
    <a href="/dashboard/admin" class="dashboard-btn">Espace Administrateur</a>
    <!-- Add more admin-only buttons here -->
  {:else if roles.includes('coach')}
    <a href="/dashboard/coach" class="dashboard-btn">Espace Coach</a>
    <!-- Add more coach-only buttons here -->
  {:else}
    <a href="/dashboard/user" class="dashboard-btn">Espace Utilisateur</a>
    <!-- Add more user-only buttons here -->
  {/if}
</div>