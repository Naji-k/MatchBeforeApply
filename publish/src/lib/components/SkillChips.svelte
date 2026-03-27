<script lang="ts">
  let { matched = [], missing = [] }: { matched?: string[]; missing?: string[] } = $props();
</script>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
  <div class="card">
    <h3 style="font-size:.95rem;font-weight:600;margin-bottom:.9rem">✅ Matched Skills</h3>
    <div style="display:flex;flex-wrap:wrap;gap:.45rem">
      {#if matched.length}
        {#each matched as skill}
          <span style="padding:.3rem .75rem;border-radius:999px;font-size:.8rem;font-weight:500;background:rgba(74,222,128,.12);color:#4ade80;border:1px solid rgba(74,222,128,.25)">
            {skill}
          </span>
        {/each}
      {:else}
        <span style="color:var(--color-text-muted);font-size:.85rem">None</span>
      {/if}
    </div>
  </div>

  <div class="card">
    <h3 style="font-size:.95rem;font-weight:600;margin-bottom:.9rem">❌ Missing Skills</h3>
    <div style="display:flex;flex-wrap:wrap;gap:.45rem">
      {#if missing.length}
        {#each missing as skill}
          <span style="padding:.3rem .75rem;border-radius:999px;font-size:.8rem;font-weight:500;background:rgba(248,113,113,.1);color:#f87171;border:1px solid rgba(248,113,113,.2)">
            {skill}
          </span>
        {/each}
      {:else}
        <span style="color:var(--color-text-muted);font-size:.85rem">None</span>
      {/if}
    </div>
  </div>
</div>

<style>
  @media (max-width: 560px) {
    div { grid-template-columns: 1fr !important; }
  }
</style>
