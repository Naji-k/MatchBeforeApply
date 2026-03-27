<script lang="ts">
  import { onMount } from 'svelte';
  import { colorForScore, scorePercent } from '$lib/utils/helpers.js';

  let { score, size = 'sm' }: { score: number; size?: 'sm' | 'lg' } = $props();

  const dim = $derived(size === 'lg' ? 120 : 56);
  const radius = $derived(size === 'lg' ? 46 : 20);
  const strokeWidth = $derived(size === 'lg' ? 8 : 5);
  const circumference = $derived(2 * Math.PI * radius);
  const color = $derived(colorForScore(score));
  const pct = $derived(scorePercent(score));

  let offset = $state(0);

  onMount(() => {
    // Start at full offset (empty), animate to filled position
    offset = circumference - (score / 10) * circumference;
  });
</script>

<div
  style="
    position:relative;
    width:{dim}px;
    height:{dim}px;
    flex-shrink:0;
  "
>
  <svg
    viewBox="0 0 {dim} {dim}"
    style="transform:rotate(-90deg);width:100%;height:100%"
  >
    <circle
      cx="{dim / 2}"
      cy="{dim / 2}"
      r={radius}
      fill="none"
      stroke="var(--color-surface-2)"
      stroke-width={strokeWidth}
    />
    <circle
      cx="{dim / 2}"
      cy="{dim / 2}"
      r={radius}
      fill="none"
      stroke={color}
      stroke-width={strokeWidth}
      stroke-linecap="round"
      stroke-dasharray={circumference}
      stroke-dashoffset={offset}
      style="transition:stroke-dashoffset 1s ease"
    />
  </svg>
  <div
    style="
      position:absolute;
      inset:0;
      display:flex;
      flex-direction:column;
      align-items:center;
      justify-content:center;
      line-height:1;
    "
  >
    {#if size === 'lg'}
      <span style="font-size:2rem;font-weight:800;color:{color}">{pct}</span>
      <span style="font-size:.75rem;color:var(--color-text-muted);margin-top:.15rem">%</span>
    {:else}
      <span style="font-size:.9rem;font-weight:800;color:{color}">{pct}</span>
      <span style="font-size:.55rem;color:var(--color-text-muted)">%</span>
    {/if}
  </div>
</div>
