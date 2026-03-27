<script lang="ts">
  import { goto } from '$app/navigation';
  import type { Application } from '$lib/types.js';
  import { formatDate } from '$lib/utils/helpers.js';
  import ScoreIndicator from './ScoreIndicator.svelte';
  import StatusBadge from './StatusBadge.svelte';

  let { app, draggable = false, ondragstart, showStatus = false }: {
    app: Application;
    draggable?: boolean;
    ondragstart?: (id: number) => void;
    showStatus?: boolean;
  } = $props();

  const title = $derived(app.jd_data?.job_title ?? '(No title)');
  const company = $derived(app.jd_data?.company ?? '—');
</script>

<button
  class="app-card card"
  style="text-align:left;cursor:pointer;width:100%;padding:1rem;display:flex;flex-direction:column;gap:.65rem"
  draggable={draggable}
  ondragstart={draggable && ondragstart ? (e) => { e.dataTransfer?.setData('text/plain', String(app.id)); ondragstart(app.id); } : undefined}
  onclick={() => goto(`/applications/${app.id}`)}
>
  <div style="display:flex;align-items:center;gap:.75rem">
    {#if app.match_breakdown?.overall_score !== undefined}
      <ScoreIndicator score={app.match_breakdown.overall_score} size="sm" />
    {:else}
      <div style="width:56px;height:56px;border-radius:50%;background:var(--color-surface-2);flex-shrink:0;display:flex;align-items:center;justify-content:center">
        <span style="font-size:.7rem;color:var(--color-text-muted)">—</span>
      </div>
    {/if}
    <div style="flex:1;min-width:0">
      <p style="font-weight:600;font-size:.9rem;color:var(--color-text-primary);overflow:hidden;text-overflow:ellipsis;">{title}</p>
      <p style="font-size:.8rem;color:var(--color-text-muted);margin-top:.15rem;overflow:hidden;text-overflow:ellipsis">{company}</p>
    </div>
  </div>
  <div style="display:flex;align-items:center;justify-content:space-between">
    {#if showStatus}
      <StatusBadge status={app.status} />
    {:else}
      <span></span>
    {/if}
    <span style="font-size:.72rem;color:var(--color-text-muted)">{formatDate(app.created_at)}</span>
  </div>
</button>

<style>
  .app-card {
    transition: box-shadow .2s, border-color .2s, transform .15s;
  }
  .app-card:hover {
    box-shadow: 0 4px 16px rgba(79, 70, 229, 0.1);
    border-color: rgba(79, 70, 229, 0.35);
    transform: translateY(-1px);
  }
</style>
