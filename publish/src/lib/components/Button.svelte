<script lang="ts">
  import type { Snippet } from 'svelte';
  let { variant = 'primary', loading = false, disabled = false, type = 'button', onclick, children }: {
    variant?: 'primary' | 'secondary' | 'danger';
    loading?: boolean;
    disabled?: boolean;
    type?: 'button' | 'submit' | 'reset';
    onclick?: (e: MouseEvent) => void;
    children?: Snippet;
  } = $props();
  const cls: Record<string, string> = { primary: 'btn-primary', secondary: 'btn-secondary', danger: 'btn-danger' };
</script>

<button
  {type}
  class="{cls[variant] || cls.primary} inline-flex items-center justify-center gap-2"
  disabled={disabled || loading}
  {onclick}
>
  {#if loading}
    <svg
      style="width:1rem;height:1rem;animation:spin 1s linear infinite;flex-shrink:0"
      viewBox="0 0 24 24"
      fill="none"
    >
      <circle opacity="0.25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path opacity="0.75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
  {/if}
  {@render children?.()}
</button>

<style>
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
</style>
