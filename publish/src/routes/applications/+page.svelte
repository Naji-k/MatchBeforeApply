<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import type { Application, ApplicationStatus } from '$lib/types.js';
  import { applicationsStore, showToast } from '$lib/stores.js';
  import { listApplications } from '$lib/api.js';
  import StatusBadge from '$lib/components/StatusBadge.svelte';
  import { formatDate, colorForScore } from '$lib/utils/helpers.js';

  let filter = $state<'all' | ApplicationStatus>('all');
  let sortBy = $state('newest');

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

  const STATUS_FILTERS: { value: 'all' | ApplicationStatus; label: string }[] = [
    { value: 'all', label: 'All' },
    { value: 'open', label: 'Open' },
    { value: 'in_progress', label: 'In Progress' },
    { value: 'accepted', label: 'Accepted' },
    { value: 'rejected', label: 'Rejected' }
  ];

  const SORT_OPTIONS = [
    { value: 'newest', label: 'Newest first' },
    { value: 'oldest', label: 'Oldest first' },
    { value: 'score_high', label: 'Score: high → low' },
    { value: 'score_low', label: 'Score: low → high' }
  ];

  const filtered = $derived.by(() => {
    let items = $applicationsStore.items;
    if (filter !== 'all') items = items.filter((a) => a.status === filter);
    switch (sortBy) {
      case 'oldest':
        return [...items].sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
      case 'score_high':
        return [...items].sort(
          (a, b) => (b.match_breakdown?.overall_score ?? 0) - (a.match_breakdown?.overall_score ?? 0)
        );
      case 'score_low':
        return [...items].sort(
          (a, b) => (a.match_breakdown?.overall_score ?? 0) - (b.match_breakdown?.overall_score ?? 0)
        );
      default:
        return [...items].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    }
  });

  function getTitle(app: Application): string { return app.jd_data?.job_title ?? '(No title)'; }
  function getCompany(app: Application): string { return app.jd_data?.company ?? '—'; }
</script>

<svelte:head><title>Applications — CV Matcher</title></svelte:head>

<div style="max-width:1000px;margin:0 auto;padding:2rem 1rem">
  <!-- Header -->
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem">
    <h1 style="font-size:1.6rem;font-weight:700">My Applications</h1>
    <a href="/applications/new" class="btn-primary" style="padding:.6rem 1.25rem;text-decoration:none;font-size:.95rem">
      + New Application
    </a>
  </div>

  <!-- Filters + Sort -->
  <div style="display:flex;flex-wrap:wrap;gap:.75rem;align-items:center;margin-bottom:1.5rem">
    <div style="display:flex;gap:.5rem;flex-wrap:wrap">
      {#each STATUS_FILTERS as f}
        <button
          style="
            padding:.35rem .9rem;border-radius:8px;font-size:.875rem;font-weight:500;
            border:1px solid;cursor:pointer;transition:all .2s;
            {filter === f.value
              ? 'background:var(--color-accent);border-color:var(--color-accent);color:#fff'
              : 'background:transparent;border-color:var(--color-border);color:var(--color-text-muted)'}
          "
          onclick={() => (filter = f.value)}
        >
          {f.label}
        </button>
      {/each}
    </div>
    <select
      class="input-field"
      style="width:auto;padding:.4rem .75rem;font-size:.875rem;cursor:pointer;margin-left:auto"
      bind:value={sortBy}
    >
      {#each SORT_OPTIONS as opt}
        <option value={opt.value}>{opt.label}</option>
      {/each}
    </select>
  </div>

  <!-- States -->
  {#if $applicationsStore.loading}
    <div style="text-align:center;padding:5rem 0;color:var(--color-text-muted)">Loading…</div>

  {:else if $applicationsStore.error}
    <div class="card" style="text-align:center;padding:3rem;color:var(--color-danger)">{$applicationsStore.error}</div>

  {:else if filtered.length === 0}
    <div class="card" style="text-align:center;padding:4rem 2rem">
      <p style="color:var(--color-text-muted);font-size:1.05rem;margin-bottom:1.5rem">
        {$applicationsStore.items.length === 0 ? 'No applications yet.' : 'No applications match this filter.'}
      </p>
      {#if $applicationsStore.items.length === 0}
        <a href="/applications/new" class="btn-primary" style="text-decoration:none;padding:.75rem 1.5rem">
          Analyse your first JD
        </a>
      {/if}
    </div>

  {:else}
    <div style="display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))">
      {#each filtered as app (app.id)}
        <button
          class="card app-card"
          style="text-align:left;cursor:pointer;width:100%;display:flex;flex-direction:column;gap:.75rem"
          onclick={() => goto(`/applications/${app.id}`)}
        >
          <div style="display:flex;align-items:flex-start;gap:.75rem">
            <div style="flex:1;min-width:0">
              <p style="font-weight:600;color:var(--color-text-primary);white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{getTitle(app)}</p>
              <p style="font-size:.875rem;color:var(--color-text-muted);margin-top:.2rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{getCompany(app)}</p>
            </div>
            {#if app.match_breakdown?.overall_score !== undefined}
              <span style="font-size:1.4rem;font-weight:800;flex-shrink:0;color:{colorForScore(app.match_breakdown.overall_score)}">
                {app.match_breakdown.overall_score}<small style="font-size:.7rem;font-weight:400;color:var(--color-text-muted)">/10</small>
              </span>
            {/if}
          </div>
          <div style="display:flex;align-items:center;justify-content:space-between">
            <StatusBadge status={app.status} />
            <span style="font-size:.75rem;color:var(--color-text-muted)">{formatDate(app.created_at)}</span>
          </div>
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .app-card { transition: border-color .2s; }
  .app-card:hover { border-color: rgba(108,99,255,.5); }
</style>
