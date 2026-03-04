<script lang="ts">
	import { auth } from '$lib/stores/auth.store';
	import { goto } from '$app/navigation';

	$: accessToken = $auth.accessToken;
	$: firstName = $auth.firstName;
	$: lastName = $auth.lastName;

  let menuOpen = false;

  function logout() {
    auth.logout();
    goto('/login');
  }

  function toggleMenu() {
    menuOpen = !menuOpen;
  }

  function closeMenu() {
    menuOpen = false;
  }
</script>

<svelte:head>
  <title>Actual Digital Gym</title>
</svelte:head>

<header class="main-header">
  <nav class="main-nav">
    <a href="/" class="nav-logo" on:click={closeMenu}><img src="/actual-logo.png" alt="actual" class="logo-img" /></a>
    <button class="hamburger" class:open={menuOpen} on:click={toggleMenu} aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <div class="nav-links" class:show={menuOpen}>
      <a href="/" on:click={closeMenu}>Accueil</a>
      {#if accessToken}
        <a href="/dashboard" on:click={closeMenu}>Tableau de bord</a>
        <button class="logout-btn" on:click={() => { logout(); closeMenu(); }}>Déconnexion</button>
      {:else}
        <a href="/login" on:click={closeMenu}>Connexion</a>
      {/if}
    </div>
  </nav>
</header>

{#if accessToken && firstName}
  <div class="welcome-banner">
    <span class="welcome-text">Bienvenue, <span class="welcome-name">{firstName}</span></span>
  </div>
{/if}

<main class="main-content">
	<slot />
</main>

<footer class="main-footer">
  <span>© {new Date().getFullYear()} actual — Tous droits réservés</span>
</footer>

<style>
.main-header {
  background: #fff;
  color: #1f2937;
  padding: 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.03);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(0,0,0,0.06);
}
.main-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  height: 64px;
}
.nav-logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1f2937;
  text-decoration: none;
  letter-spacing: 1px;
  transition: transform 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}
.nav-logo:hover {
  transform: scale(1.05);
}
.logo-img {
  height: 36px;
  width: auto;
  border-radius: 6px;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.welcome-banner {
  background: rgba(255,255,255,0.7);
  color: #1f2937;
  text-align: center;
  padding: 8px 16px;
  font-size: 0.95rem;
  letter-spacing: 0.2px;
  animation: slideDown 0.4s ease-out;
  border-bottom: 1px solid rgba(0,0,0,0.04);
  backdrop-filter: blur(8px);
}
.welcome-text {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  animation: fadeScale 0.6s ease-out 0.2s both;
}
.welcome-name {
  font-size: 1.05rem;
  font-weight: 700;
  text-transform: capitalize;
  color: #991b1b;
  letter-spacing: 0.3px;
}
@keyframes slideDown {
  from { transform: translateY(-100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
@keyframes fadeScale {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
.nav-links a {
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  position: relative;
  transition: color 0.2s;
  padding: 4px 0;
}
.nav-links a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 0;
  height: 2px;
  background: #991b1b;
  border-radius: 1px;
  transition: width 0.25s ease;
}
.nav-links a:hover::after {
  width: 100%;
}
.nav-links a:hover {
  color: #1f2937;
}
.logout-btn {
  background: #1f2937;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 7px 16px;
  font-weight: 600;
  font-size: 0.88rem;
  cursor: pointer;
  margin-left: 10px;
  transition: background 0.2s, transform 0.15s;
}
.logout-btn:hover {
  background: #374151;
  transform: translateY(-1px);
}
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px 64px 24px;
  min-height: calc(100vh - 64px - 56px);
}
.main-footer {
  background: rgba(255,255,255,0.6);
  text-align: center;
  padding: 16px 0;
  color: #9ca3af;
  font-size: 0.82rem;
  border-top: 1px solid rgba(0,0,0,0.04);
  backdrop-filter: blur(8px);
}

/* Hamburger menu for mobile */
.hamburger {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  flex-direction: column;
  gap: 5px;
}
.hamburger span {
  display: block;
  width: 26px;
  height: 3px;
  background: #374151;
  border-radius: 2px;
  transition: transform 0.25s, opacity 0.2s;
}
.hamburger.open span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}
.hamburger.open span:nth-child(2) {
  opacity: 0;
}
.hamburger.open span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

@media (max-width: 640px) {
  .hamburger {
    display: flex;
  }
  .nav-links {
    display: none;
    position: absolute;
    top: 64px;
    left: 0;
    right: 0;
    background: #fff;
    flex-direction: column;
    padding: 16px 32px;
    gap: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-bottom: 1px solid #e5e7eb;
  }
  .nav-links.show {
    display: flex;
  }
  .logout-btn {
    margin-left: 0;
    width: 100%;
    text-align: center;
  }
}
</style>
