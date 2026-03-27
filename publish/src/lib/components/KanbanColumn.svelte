<script lang="ts">
  import type { Application, ApplicationStatus } from "$lib/types.js";
  import ApplicationCard from "./ApplicationCard.svelte";

  let {
    status,
    label,
    applications,
    isDragOver,
    ondragover,
    ondragleave,
    ondrop,
    ondragstart,
  }: {
    status: ApplicationStatus;
    label: string;
    applications: Application[];
    isDragOver: boolean;
    ondragover: (e: DragEvent) => void;
    ondragleave: () => void;
    ondrop: () => void;
    ondragstart: (id: number) => void;
  } = $props();

  const STATUS_ACCENT: Record<ApplicationStatus, string> = {
    open: "#64748B",
    in_progress: "#4F46E5",
    accepted: "#16A34A",
    rejected: "#DC2626",
  };
  const accent = $derived(STATUS_ACCENT[status]);
</script>

<div
  class="column"
  style="border-top:3px solid {accent};{isDragOver
    ? 'background:rgba(79,70,229,.04);border-color:rgba(79,70,229,.5)'
    : ''}"
  {ondragover}
  {ondragleave}
  {ondrop}
  role="region"
  aria-label="{label} column"
>
  <!-- Column header -->
  <div
    style="display:flex;align-items:center;gap:.5rem;padding:.75rem 1rem;border-bottom:1px solid var(--color-border)"
  >
    <span
      style="font-size:.85rem;font-weight:700;color:var(--color-text-primary)"
      >{label}</span
    >
    <span
      style="
        font-size:.7rem;font-weight:700;
        padding:.1rem .45rem;border-radius:999px;
        background:{accent}1a;color:{accent};
        line-height:1.4;
      "
    >
      {applications.length}
    </span>
  </div>

  <!-- Cards -->
  <div class="card-list">
    {#each applications as app (app.id)}
      <ApplicationCard {app} draggable={true} {ondragstart} />
    {/each}

    {#if isDragOver}
      <div
        style="
        border:2px dashed rgba(79,70,229,.4);
        border-radius:12px;
        padding:1.5rem;
        text-align:center;
        font-size:.8rem;
        color:rgba(79,70,229,.7);
        background:rgba(79,70,229,.03);
      "
      >
        Drop here
      </div>
    {:else if applications.length === 0}
      <div
        style="
        padding:2rem 1rem;
        text-align:center;
        font-size:.8rem;
        color:var(--color-text-muted);
        border:2px dashed var(--color-border);
        border-radius:12px;
      "
      >
        No applications
      </div>
    {/if}
  </div>
</div>

<style>
  .column {
    background: var(--color-surface-2);
    border-radius: 14px;
    border: 1px solid var(--color-border);
    display: flex;
    flex-direction: column;
    min-width: 240px;
    flex: 1;
    transition:
      background 0.2s,
      border-color 0.2s;
  }
  .card-list {
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
    padding: 0.75rem;
    overflow-y: auto;
    max-height: calc(100vh - 280px);
    min-height: 120px;
  }
</style>
