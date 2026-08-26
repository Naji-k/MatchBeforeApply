<script lang="ts">
  import { BadgePercent, ClipboardPaste, FileUp, Kanban } from "@lucide/svelte";
  import { reveal } from "$lib/utils/reveal.js";

  const steps = [
    {
      n: "01",
      icon: FileUp,
      title: "Upload your CV once",
      desc: "Your resume becomes your profile. Update it anytime — every future analysis uses the latest version.",
    },
    {
      n: "02",
      icon: ClipboardPaste,
      title: "Drop in the job",
      desc: "Paste the description or just the posting URL — we read it either way.",
    },
    {
      n: "03",
      icon: BadgePercent,
      title: "Get your verdict",
      desc: "An overall match score, matched and missing skills, and what the ATS will think.",
    },
    {
      n: "04",
      icon: Kanban,
      title: "Track it like a pro",
      desc: "Save it to your board with status, notes, and comments — nothing slips through.",
    },
  ];
</script>

<section class="section" id="how-it-works">
  <div class="inner">
    <div class="header" use:reveal>
      <h2 class="title">From job post to tracked application</h2>
      <p class="subtitle">Four steps, a couple of minutes, zero guesswork.</p>
    </div>

    <ol class="timeline">
      {#each steps as step, i (step.n)}
        <li class="step" use:reveal={{ delay: i * 120 }}>
          <div class="node-col">
            <span class="node">{step.n}</span>
          </div>
          <div class="body">
            <h3 class="step-title">
              <step.icon size={17} color="var(--color-accent)" />
              {step.title}
            </h3>
            <p class="step-desc">{step.desc}</p>
          </div>
        </li>
      {/each}
    </ol>
  </div>
</section>

<style>
  .section {
    background: var(--color-surface);
    padding: 5rem 1.5rem;
    scroll-margin-top: 4rem;
  }

  .inner {
    max-width: 960px;
    margin: 0 auto;
  }

  .header {
    text-align: center;
    margin-bottom: 3.5rem;
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
    margin: 0;
  }

  .timeline {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
    margin: 0;
    padding: 0;
  }

  .step {
    text-align: center;
  }

  .node-col {
    position: relative;
    display: flex;
    justify-content: center;
    margin-bottom: 1.15rem;
  }

  .node {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.75rem;
    height: 2.75rem;
    border-radius: 50%;
    background: var(--color-accent);
    color: #fff;
    font-size: 0.95rem;
    font-weight: 800;
    box-shadow: 0 0 0 6px var(--color-surface);
    position: relative;
    z-index: 1;
  }

  /* Connector line between desktop nodes */
  .step:not(:last-child) .node-col::after {
    content: "";
    position: absolute;
    top: 1.375rem;
    left: calc(50% + 1.5rem);
    width: calc(100% + 2rem - 3rem);
    height: 2px;
    background: var(--color-border);
  }

  .step-title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--color-text-primary);
    margin: 0 0 0.5rem;
  }

  .step-desc {
    font-size: 0.88rem;
    line-height: 1.65;
    color: var(--color-text-muted);
    margin: 0;
    max-width: 220px;
    margin-inline: auto;
  }

  @media (max-width: 860px) {
    .timeline {
      grid-template-columns: 1fr;
      gap: 1.75rem;
      max-width: 420px;
      margin-inline: auto;
    }

    .step {
      display: grid;
      grid-template-columns: auto 1fr;
      column-gap: 1.25rem;
      text-align: left;
    }

    .node-col {
      justify-content: flex-start;
      margin-bottom: 0;
    }

    .node {
      width: 2.5rem;
      height: 2.5rem;
      font-size: 0.85rem;
      box-shadow: none;
    }

    .step:not(:last-child) .node-col::after {
      top: 2.75rem;
      left: 50%;
      transform: translateX(-50%);
      width: 2px;
      height: calc(100% - 2rem);
    }

    .step:last-child {
      min-height: 2.5rem;
    }

    .step-title {
      justify-content: flex-start;
      margin-top: 0.35rem;
    }

    .step-desc {
      max-width: none;
    }
  }

  @media (max-width: 640px) {
    .section {
      padding: 3.5rem 1.25rem;
    }
  }
</style>
