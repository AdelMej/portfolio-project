<script lang="ts">
  import { page } from '$app/stores';
  import { get } from 'svelte/store';
  import { onMount } from 'svelte';
  import { getSession, type Session } from '$lib/api/sessions.api';

  let session: Session | null = null;

  onMount(async () => {
    const id = get(page).params.id;

    if (!id) {
      console.error('No session id found in URL');
      return;
    }

    session = await getSession(id);
  });
</script>
