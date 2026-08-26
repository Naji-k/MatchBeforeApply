<script lang="ts">
  import { Bot, Gift, ShieldCheck, Sparkles } from "@lucide/svelte";

  const signals = [
    { icon: Bot, label: "4-agent AI pipeline" },
    { icon: Sparkles, label: "Powered by Google Gemini" },
    { icon: ShieldCheck, label: "Your CV stays private" },
    { icon: Gift, label: "3 free analyses every day" },
  ];
</script>

<div class="trust-strip">
  <div class="inner">
    {#each signals as signal (signal.label)}
      <span class="signal">
        <signal.icon size={15} />
        {signal.label}
      </span>
    {/each}
  </div>
</div>

<style>
  .trust-strip {
    background: var(--color-surface);
    border-top: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    padding: 1rem 1.5rem;
  }

  .inner {
    max-width: 1080px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem 2.5rem;
  }

  .signal {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--color-text-muted);
  }

  .signal :global(svg) {
    color: var(--color-accent);
    flex-shrink: 0;
  }

  @media (max-width: 640px) {
    .inner {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem 1rem;
      justify-items: start;
    }
  }
</style>
