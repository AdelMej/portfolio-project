<script lang="ts">
import { auth } from '$lib/stores/auth.store';
import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import { get } from 'svelte/store';

onMount(() => {
  const roles = get(auth).roles || [];
  if (roles.includes('admin')) goto('/dashboard/admin', { replaceState: true });
  else if (roles.includes('coach')) goto('/dashboard/coach', { replaceState: true });
  else goto('/dashboard/user', { replaceState: true });
});
</script>

<style>
.redirect-container {
  max-width: 400px;
  margin: 120px auto;
  text-align: center;
  color: #9ca3af;
  font-size: 0.95rem;
}
.spinner {
  display: inline-block;
  width: 28px; height: 28px;
  border: 3px solid #e5e7eb;
  border-top-color: #374151;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin-bottom: 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>

<div class="redirect-container">
  <div class="spinner"></div>
  <p>Redirection…</p>
</div>