<script lang="ts">
  import { CircleCheck, CircleX } from "@lucide/svelte";

  let {
    matched = [],
    missing = [],
  }: { matched?: string[]; missing?: string[] } = $props();
</script>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
  <div class="card">
    <h3 class="skill-head">
      <CircleCheck size={16} color="var(--color-success)" /> Matched Skills
    </h3>
    <div style="display:flex;flex-wrap:wrap;gap:.45rem;padding:.75rem">
      {#if matched.length}
        {#each matched as skill (skill)}
          <span
            style="padding:.3rem .75rem;border-radius:999px;font-size:.8rem;font-weight:500;background:#F0FDF4;color:#16A34A;border:1px solid #BBF7D0"
          >
            {skill}
          </span>
        {/each}
      {:else}
        <span style="color:var(--color-text-muted);font-size:.85rem">None</span>
      {/if}
    </div>
  </div>

  <div class="card">
    <h3 class="skill-head">
      <CircleX size={16} color="var(--color-danger)" /> Missing Skills
    </h3>
    <div style="display:flex;flex-wrap:wrap;gap:.45rem;padding:.75rem">
      {#if missing.length}
        {#each missing as skill (skill)}
          <span
            style="padding:.3rem .75rem;border-radius:999px;font-size:.8rem;font-weight:500;background:#FEF2F2;color:#DC2626;border:1px solid #FECACA"
          >
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
  .skill-head {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.95rem;
    font-weight: 600;
    padding: 0.75rem;
    margin: 0;
  }

  @media (max-width: 560px) {
    div {
      grid-template-columns: 1fr !important;
    }
  }
</style>
