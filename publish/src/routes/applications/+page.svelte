<script lang="ts">
  import { onMount } from "svelte";
  import {
    STATUS_OPTIONS,
    type Application,
    type ApplicationStatus,
  } from "$lib/types.js";
  import { applicationsStore, showToast } from "$lib/stores.js";
  import { listApplications, updateApplication } from "$lib/api.js";
  import KanbanColumn from "$lib/components/KanbanColumn.svelte";
  import ApplicationCard from "$lib/components/ApplicationCard.svelte";

  let search = $state("");
  let draggedId = $state<number | null>(null);
  let dragOverStatus = $state<ApplicationStatus | null>(null);

  const COLUMNS = STATUS_OPTIONS;

  onMount(async () => {
    applicationsStore.update((s) => ({ ...s, loading: true, error: null }));
    try {
      const items = await listApplications();
      applicationsStore.update((s) => ({ ...s, items, loading: false }));
    } catch (err) {
      const msg = (err as Error).message;
      applicationsStore.update((s) => ({ ...s, loading: false, error: msg }));
      showToast(msg);
    }
  });

  const searchLower = $derived(search.toLowerCase());

  const filteredItems = $derived(
    searchLower
      ? $applicationsStore.items.filter((a) => {
          const title = (a.jd_data?.job_title ?? "").toLowerCase();
          const company = (a.jd_data?.company ?? "").toLowerCase();
          return title.includes(searchLower) || company.includes(searchLower);
        })
      : $applicationsStore.items,
  );

  function colItems(status: ApplicationStatus): Application[] {
    return filteredItems.filter((a) => a.status === status);
  }

  // Stats
  const totalCount = $derived($applicationsStore.items.length);
  const activeCount = $derived(
    $applicationsStore.items.filter(
      (a) => a.status === "in_progress" || a.status === "accepted",
    ).length,
  );
  // const avgScore = $derived.by(() => {
  //   const scored = $applicationsStore.items.filter(
  //     (a) => a.match_breakdown?.overall_score !== undefined,
  //   );
  //   if (!scored.length) return null;
  //   const sum = scored.reduce(
  //     (acc, a) => acc + a.match_breakdown!.overall_score * 10,
  //     0,
  //   );
  //   return Math.round(sum / scored.length);
  // });

  // Drag & Drop
  function onDragStart(id: number) {
    draggedId = id;
  }

  function onDragOver(e: DragEvent, status: ApplicationStatus) {
    e.preventDefault();
    dragOverStatus = status;
  }

  function onDragLeave() {
    dragOverStatus = null;
  }

  async function onDrop(newStatus: ApplicationStatus) {
    if (!draggedId) return;
    const id = draggedId;
    draggedId = null;
    dragOverStatus = null;

    const prev = $applicationsStore.items.find((a) => a.id === id)?.status;
    if (prev === newStatus) return;

    // Optimistic update
    applicationsStore.update((s) => ({
      ...s,
      items: s.items.map((a) =>
        a.id === id ? { ...a, status: newStatus } : a,
      ),
    }));

    try {
      await updateApplication(String(id), { status: newStatus });
      showToast("Status updated", "success");
    } catch (err) {
      showToast((err as Error).message);
      // Roll back
      applicationsStore.update((s) => ({
        ...s,
        items: s.items.map((a) => (a.id === id ? { ...a, status: prev! } : a)),
      }));
    }
  }
</script>

<svelte:head><title>Applications — MatchBeforeApply</title></svelte:head>

<div style="max-width:1200px;margin:0 auto;padding:1.5rem 1rem">
  <!-- Header -->
  <div
    style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem"
  >
    <h1 style="font-size:1.6rem;font-weight:700">Applications</h1>
    <a
      href="/applications/new"
      class="btn-primary"
      style="padding:.6rem 1.25rem;text-decoration:none;font-size:.9rem"
    >
      + New Application
    </a>
  </div>

  <!-- Stats bar -->
  <div style="display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap">
    <div class="card" style="flex:1;min-width:130px;padding:1rem 1.25rem">
      <p
        style="font-size:.75rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.35rem"
      >
        Total
      </p>
      <p
        style="font-size:1.6rem;font-weight:800;color:var(--color-text-primary)"
      >
        {totalCount}
      </p>
    </div>
    <!-- <div class="card" style="flex:1;min-width:130px;padding:1rem 1.25rem">
      <p
        style="font-size:.75rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.35rem"
      >
        Avg Score
      </p>
      <p
        style="font-size:1.6rem;font-weight:800;color:var(--color-text-primary)"
      >
        {avgScore !== null ? avgScore + "%" : "—"}
      </p>
    </div> -->
    <div class="card" style="flex:1;min-width:130px;padding:1rem 1.25rem">
      <p
        style="font-size:.75rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.35rem"
      >
        Active
      </p>
      <p style="font-size:1.6rem;font-weight:800;color:var(--color-accent)">
        {activeCount}
      </p>
    </div>
  </div>

  <!-- Search -->
  <div style="margin-bottom:1.25rem">
    <input
      type="search"
      class="input-field"
      style="max-width:320px;font-size:.9rem"
      placeholder="Search by title or company…"
      bind:value={search}
    />
  </div>

  {#if $applicationsStore.loading}
    <div style="text-align:center;padding:5rem 0;color:var(--color-text-muted)">
      Loading…
    </div>
  {:else if $applicationsStore.error}
    <div
      class="card"
      style="text-align:center;padding:3rem;color:var(--color-danger)"
    >
      {$applicationsStore.error}
    </div>
  {:else if $applicationsStore.items.length === 0}
    <div class="card" style="text-align:center;padding:4rem 2rem">
      <p
        style="color:var(--color-text-muted);font-size:1.05rem;margin-bottom:1.5rem"
      >
        No applications yet.
      </p>
      <a
        href="/applications/new"
        class="btn-primary"
        style="text-decoration:none;padding:.75rem 1.5rem"
      >
        Analyze your first JD
      </a>
    </div>
  {:else}
    <!-- Kanban board (desktop) -->
    <div class="kanban-board">
      {#each COLUMNS as col (col.status)}
        <KanbanColumn
          status={col.status}
          label={col.label}
          applications={colItems(col.status)}
          isDragOver={dragOverStatus === col.status}
          ondragover={(e) => onDragOver(e, col.status)}
          ondragleave={onDragLeave}
          ondrop={() => onDrop(col.status)}
          ondragstart={onDragStart}
        />
      {/each}
    </div>

    <!-- Mobile list -->
    <div class="mobile-list">
      {#each COLUMNS as col (col.status)}
        {@const items = colItems(col.status)}
        {#if items.length > 0}
          <div>
            <h2
              style="font-size:.85rem;font-weight:700;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.65rem"
            >
              {col.label} ({items.length})
            </h2>
            <div style="display:flex;flex-direction:column;gap:.6rem">
              {#each items as app (app.id)}
                <ApplicationCard {app} showStatus={false} />
              {/each}
            </div>
          </div>
        {/if}
      {/each}
    </div>
  {/if}
</div>

<style>
  .kanban-board {
    display: flex;
    gap: 1.25rem;
    overflow-x: auto;
    align-items: flex-start;
    padding-bottom: 1rem;
  }
  .mobile-list {
    display: none;
    flex-direction: column;
    gap: 2rem;
  }
  @media (max-width: 768px) {
    .kanban-board {
      display: none;
    }
    .mobile-list {
      display: flex;
    }
  }
</style>
