<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { fade } from 'svelte/transition';

  let countdown = 5;

  onMount(() => {
    const interval = setInterval(() => {
      countdown--;
      if (countdown <= 0) {
        clearInterval(interval);
        goto('/dashboard');
      }
    }, 1000);
    return () => clearInterval(interval);
  });
</script>

<div class="return-container" in:fade={{ duration: 300 }}>
  <div class="return-card">
    <div class="icon">❌</div>
    <h1>Paiement annulé</h1>
    <p>Votre paiement a été annulé. Vous n'avez pas été débité.</p>
    <p class="redirect">Redirection vers le tableau de bord dans <strong>{countdown}s</strong></p>
    <a href="/dashboard" class="btn">Retour au tableau de bord</a>
  </div>
</div>

<style>
  .return-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 140px);
    padding: 24px;
  }
  .return-card {
    background: #fff;
    border-radius: 18px;
    padding: 48px 40px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
    max-width: 480px;
    width: 100%;
  }
  .icon { font-size: 3rem; margin-bottom: 16px; }
  h1 { font-size: 1.5rem; font-weight: 700; color: #111827; margin-bottom: 8px; }
  p { color: #6b7280; font-size: 0.95rem; margin-bottom: 8px; }
  .redirect { color: #9ca3af; font-size: 0.85rem; margin-top: 16px; }
  .btn {
    display: inline-block;
    background: #1f2937;
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.92rem;
    text-decoration: none;
    margin-top: 20px;
    transition: background 0.15s;
  }
  .btn:hover { background: #374151; }
</style>
