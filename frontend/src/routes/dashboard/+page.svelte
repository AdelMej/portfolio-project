<script lang="ts">
  import { onMount } from 'svelte';
  import { listSessions } from '$lib/api/sessions.api';

  let sessions: any[] = [];
  let totalParticipants = 0;

  onMount(async () => {
  try {
    const fetchedSessions = await listSessions();
    sessions = Array.isArray(fetchedSessions) ? fetchedSessions : [];

    totalParticipants = sessions.reduce(
      (sum, s) => sum + (Array.isArray(s.participants) ? s.participants.length : 0),
      0
    );
  } catch (e) {
    console.error('Dashboard load error', e);
    sessions = [];
    totalParticipants = 0;
  }
});
</script>

<div class="layout">
  <!-- SIDEBAR -->
  <aside class="sidebar">
    <h2>Dashboard</h2>
    <a href="/dashboard">Overview</a>
    <a href="/sessions/create">Create Session</a>
  </aside>

  <!-- MAIN -->
  <section class="main">
    <header class="header">
      <h1>Admin Panel</h1>
    </header>

    <!-- STAT CARDS -->
    <div class="cards">
      <div class="card">
        <h3>Total Sessions</h3>
        <p>{sessions.length}</p>
      </div>

      <div class="card">
        <h3>Total Participants</h3>
        <p>{totalParticipants}</p>
      </div>

      <div class="card">
        <h3>Upcoming</h3>
        <p>{sessions.length}</p>
      </div>
    </div>

    <!-- SESSIONS TABLE -->
    <div class="window">
      <h2>Recent Sessions</h2>

      {#if sessions.length > 0}
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Date</th>
              <th>Participants</th>
            </tr>
          </thead>
          <tbody>
            {#each sessions as s}
              <tr>
                <td>
                  <a href={`/sessions/${s.id}`}>{s.title}</a>
                </td>
                <td>{s.date}</td>
                <td>{s.participants?.length || 0}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      {:else}
        <p>No sessions found.</p>
      {/if}
    </div>
  </section>
</div>

<style>
  .layout {
    display: flex;
    min-height: 100vh;
    font-family: sans-serif;
  }

  /* Sidebar */
  .sidebar {
    width: 220px;
    background: #1f2937;
    color: white;
    padding: 2rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .sidebar a {
    color: #d1d5db;
    text-decoration: none;
  }

  .sidebar a:hover {
    color: white;
  }

  /* Main */
  .main {
    flex: 1;
    padding: 2rem;
    background: #f3f4f6;
  }

  .header {
    margin-bottom: 2rem;
  }

  /* Cards */
  .cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }

  .card h3 {
    margin-bottom: 0.5rem;
  }

  .card p {
    font-size: 1.8rem;
    font-weight: bold;
  }

  /* Window */
  .window {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }

  th, td {
    padding: 0.8rem;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
  }

  tr:hover {
    background: #f9fafb;
  }
</style>