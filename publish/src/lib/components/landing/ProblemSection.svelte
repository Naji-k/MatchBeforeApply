<script lang="ts">
  import { ArrowRight, Ban, Compass } from "@lucide/svelte";
  import { reveal } from "$lib/utils/reveal.js";

  const loop = [
    { word: "Apply", note: "fire off another one" },
    { word: "Wait", note: "days of silence" },
    { word: "Forget", note: "where was that role?" },
    { word: "Repeat", note: "send it anyway" },
  ];
</script>

<section class="section">
  <div class="inner" use:reveal>
    <h2 class="title">The loop every job seeker knows</h2>
    <p class="subtitle">
      Applying is easy. Knowing whether you were ever a real candidate is not.
    </p>

    <div class="loop" role="list" aria-label="The application loop">
      {#each loop as step, i (step.word)}
        <div class="loop-item" role="listitem">
          <div class="loop-card">
            <span class="loop-icon"><Ban size={15} /></span>
            <span class="loop-word">{step.word}</span>
            <span class="loop-note">{step.note}</span>
          </div>
          {#if i < loop.length - 1}
            <span class="loop-arrow" aria-hidden="true">
              <ArrowRight size={16} strokeWidth={2.5} />
            </span>
          {/if}
        </div>
      {/each}
      <!-- arrow wrapping from last back to first -->
    </div>

    <div class="break-line">
      <span class="break-icon"><Compass size={18} /></span>
      <p>
        Match Before Apply breaks the loop: evaluate the fit
        <strong>before</strong> you apply — and track everything
        <strong>after</strong>.
      </p>
    </div>
  </div>
</section>

<style>
  .section {
    background: var(--color-bg);
    padding: 5rem 1.5rem;
    scroll-margin-top: 4rem;
  }

  .inner {
    max-width: 820px;
    margin: 0 auto;
    text-align: center;
  }

  .title {
    font-size: clamp(1.6rem, 3.4vw, 2.1rem);
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--color-text-primary);
    margin: 0 0 0.75rem;
  }

  .subtitle {
    font-size: 1.05rem;
    color: var(--color-text-muted);
    line-height: 1.7;
    margin: 0 0 3rem;
  }

  .loop {
    display: flex;
    align-items: stretch;
    justify-content: center;
    gap: 0.75rem;
    margin-bottom: 3rem;
  }

  .loop-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .loop-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.35rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    min-width: 7.5rem;
  }

  .loop-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: #fef2f2;
    color: var(--color-danger);
    opacity: 0.75;
  }

  .loop-word {
    font-size: 1rem;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .loop-note {
    font-size: 0.76rem;
    color: var(--color-text-muted);
  }

  .loop-arrow {
    display: flex;
    align-items: center;
    color: var(--color-border);
    flex-shrink: 0;
  }

  .break-line {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    max-width: 560px;
    margin: 0 auto;
    text-align: left;
    background: color-mix(
      in srgb,
      var(--color-accent) 5%,
      var(--color-surface)
    );
    border: 1px solid #bfdbfe;
    border-radius: 14px;
    padding: 1.15rem 1.35rem;
  }

  .break-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.25rem;
    height: 2.25rem;
    border-radius: 50%;
    background: #eff6ff;
    color: var(--color-accent);
    flex-shrink: 0;
  }

  .break-line p {
    font-size: 0.98rem;
    line-height: 1.65;
    color: var(--color-text-primary);
    margin: 0;
  }

  @media (max-width: 860px) {
    .loop {
      flex-direction: column;
      align-items: center;
      gap: 0.5rem;
    }

    .loop-item {
      flex-direction: column;
      gap: 0.5rem;
      width: 100%;
      max-width: 320px;
    }

    .loop-item .loop-arrow {
      transform: rotate(90deg);
    }
    .loop-card {
      flex-direction: row;
      width: 100%;
      justify-content: flex-start;
      padding: 0.85rem 1.1rem;
    }
  }
</style>
