<script lang="ts">
  import { onMount } from "svelte";

  let {
    running = true,
    activeStep = -1,
    doneSteps = new Set<number>(),
    controlled = false,
  }: {
    running?: boolean;
    activeStep?: number;
    doneSteps?: Set<number>;
    controlled?: boolean;
  } = $props();

  const STEPS: { label: string; ms: number }[] = [
    { label: "📋 Reading job description", ms: 800 },
    { label: "📄 Parsing your CV", ms: 1600 },
    { label: "🎯 Scoring the match", ms: 2400 },
    { label: "💡 Generating match insights", ms: 3200 },
  ];

  let internalActive = $state(-1);
  let internalDone = $state(new Set<number>());
  let timers: ReturnType<typeof setTimeout>[] = [];

  let displayActive = $derived(activeStep >= 0 ? activeStep : internalActive);
  let displayDone = $derived(doneSteps.size > 0 ? doneSteps : internalDone);

  onMount(() => {
    if (running && !controlled) startSteps();
    return () => timers.forEach(clearTimeout);
  });

  function startSteps() {
    STEPS.forEach((s, i) => {
      const nextMs = STEPS[i + 1]?.ms ?? s.ms + 800;

      timers.push(
        setTimeout(() => {
          internalActive = i;
        }, s.ms),
        setTimeout(() => {
          internalDone = new Set([...internalDone, i]);
          if (internalActive === i) internalActive = -1;
        }, nextMs - 100),
      );
    });
  }
</script>

<div
  style="display:flex;align-items:center;justify-content:center;min-height:60vh;padding:2rem"
>
  <div
    class="card"
    style="text-align:center;padding:3rem 2rem;max-width:400px;width:100%"
  >
    <h2 style="font-size:1.4rem;font-weight:700;margin-bottom:2rem">
      Analyzing your CV…
    </h2>
    <ul
      style="list-style:none;display:flex;flex-direction:column;gap:.85rem;text-align:left;max-width:300px;margin:0 auto"
    >
      {#each STEPS as step, i}
        <li
          style="
          padding:.7rem 1rem;
          border-radius:8px;
          border:1px solid;
          font-size:.95rem;
          transition:all .4s;
          {displayDone.has(i)
            ? 'border-color:#BBF7D0;color:#16A34A;background:#F0FDF4;'
            : displayActive === i
              ? 'border-color:#C7D2FE;color:#4F46E5;background:#EEF2FF;'
              : 'border-color:var(--color-border);color:var(--color-text-muted);'}
        "
        >
          {step.label}
          {#if displayDone.has(i)}<span style="margin-left:.5rem">✓</span>{/if}
        </li>
      {/each}
    </ul>
  </div>
</div>
