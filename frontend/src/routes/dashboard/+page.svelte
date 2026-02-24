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
  color: #2563eb;
  margin-bottom: 18px;
  letter-spacing: 1px;
}
h2 {
  font-size: 1.3rem;
  color: #374151;
  margin-bottom: 32px;
}
a, .dashboard-btn {
  display: inline-block;
  background: #2563eb;
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
  background: #1d4ed8;
}
</style>

<div class="dashboard-landing-container">
  <h1>Tableau de bord</h1>
  <h2>Accédez à votre espace selon votre rôle</h2>
  <a href="/dashboard/admin" class="dashboard-btn">Espace Administrateur</a>
  <a href="/dashboard/coach" class="dashboard-btn">Espace Coach</a>
  <a href="/dashboard/user" class="dashboard-btn">Espace Utilisateur</a>
</div>