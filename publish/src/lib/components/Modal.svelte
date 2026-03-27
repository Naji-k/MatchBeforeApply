<script lang="ts">
  import type { Snippet } from 'svelte';
  let { open = false, title = '', onclose, onconfirm, children }: {
    open?: boolean;
    title?: string;
    onclose?: () => void;
    onconfirm?: () => void;
    children?: Snippet;
  } = $props();
</script>

{#if open}
  <div
    style="position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.6)"
    onclick={onclose}
    role="dialog"
    aria-modal="true"
  >
    <div
      class="card"
      style="max-width:420px;width:100%;margin:0 1rem"
      onclick={(e) => e.stopPropagation()}
    >
      {#if title}
        <h2 style="font-size:1.1rem;font-weight:700;color:var(--color-text-primary);margin-bottom:1rem">{title}</h2>
      {/if}
      <div style="color:var(--color-text-muted);margin-bottom:1.5rem;font-size:.95rem;line-height:1.6">
        {@render children?.()}
      </div>
      <div style="display:flex;gap:.75rem;justify-content:flex-end">
        <button class="btn-secondary" onclick={onclose}>Cancel</button>
        <button class="btn-danger" style="padding:.5rem 1.25rem" onclick={onconfirm}>Delete</button>
      </div>
    </div>
  </div>
{/if}
