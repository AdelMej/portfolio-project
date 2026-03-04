<script lang="ts">
  import {
    Dumbbell, Trophy, HeartPulse, Activity,
    Flame, Footprints,
    Users,
    Timer
  } from 'lucide-svelte';

  export let title: string = '';
  export let size: number = 20;

  const SPORT_ICONS = [
    Dumbbell, Trophy, HeartPulse, Activity,
    Flame, Footprints,
    Users,
    Timer
  ];

  function hashTitle(t: string): number {
    let h = 0;
    for (let i = 0; i < t.length; i++) {
      h = ((h << 5) - h + t.charCodeAt(i)) | 0;
    }
    return Math.abs(h);
  }

  $: iconComponent = SPORT_ICONS[hashTitle(title) % SPORT_ICONS.length];
</script>

<svelte:component this={iconComponent} {size} />
