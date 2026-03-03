<script lang="ts">
	import { auth } from '$lib/stores/auth.store';
	import { goto } from '$app/navigation';

	let accessToken: string | null;
	auth.subscribe((value) => (accessToken = value.accessToken));

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

<main class="main-content">
	<slot />
</main>

<footer class="main-footer">
  <span>© {new Date().getFullYear()} actual — Tous droits réservés</span>
</footer>

<style>
.main-header {
  background: #991b1b;
  color: white;
  padding: 0;
  box-shadow: 0 2px 12px rgba(0,0,0,0.12);
  position: sticky;
  top: 0;
  z-index: 100;
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
  color: white;
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
.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.05rem;
  position: relative;
  transition: color 0.2s;
  padding-bottom: 2px;
}
.nav-links a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 0;
  height: 2px;
  background: #fca5a5;
  transition: width 0.25s ease;
}
.nav-links a:hover::after {
  width: 100%;
}
.nav-links a:hover {
  color: #fca5a5;
}
.logout-btn {
  background: #fff;
  color: #991b1b;
  border: none;
  border-radius: 6px;
  padding: 8px 18px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  margin-left: 10px;
  transition: background 0.2s, color 0.2s, transform 0.15s;
}
.logout-btn:hover {
  background: #fca5a5;
  color: #7f1d1d;
  transform: translateY(-1px);
}
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 16px 64px 16px;
  min-height: calc(100vh - 64px - 56px);
}
.main-footer {
  background: #f3f4f6;
  text-align: center;
  padding: 16px 0;
  color: #9ca3af;
  font-size: 0.85rem;
  border-top: 1px solid #e5e7eb;
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
  background: white;
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
    background: #991b1b;
    flex-direction: column;
    padding: 16px 32px;
    gap: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
