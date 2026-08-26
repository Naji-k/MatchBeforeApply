<script lang="ts">
  import { BadgePercent, FileCheck, FileSearch, Kanban } from "@lucide/svelte";
  import { reveal } from "$lib/utils/reveal.js";

  const features = [
    {
      icon: BadgePercent,
      title: "Match score",
      desc: "One honest number backed by a full breakdown — skills and experience — before you spend an hour tailoring an application.",
    },
    {
      icon: FileSearch,
      title: "Gap analysis",
      desc: "See exactly which required skills are missing or underplayed in your CV, so you know what to fix or address.",
    },
    {
      icon: FileCheck,
      title: "ATS insights",
      desc: "Actionable tips to make your CV readable to applicant tracking systems — keyword gaps included.",
    },
    {
      icon: Kanban,
      title: "Application tracking",
      desc: "A kanban board for every role you pursue: status, notes, interview prep Q&A — all attached to the match report.",
    },
  ];
</script>

<section class="section" id="features">
  <div class="inner">
    <div class="header" use:reveal>
      <h2 class="title">Everything you need, before and after applying</h2>
      <p class="subtitle">
        Not another place to dump applications — a tool that evaluates them
        first.
      </p>
    </div>

    <div class="grid">
      {#each features as feature, i (feature.title)}
        <div class="card feature" use:reveal={{ delay: i * 100 }}>
          <div class="icon-tile">
            <feature.icon size={20} />
          </div>
          <h3 class="feature-title">{feature.title}</h3>
          <p class="feature-desc">{feature.desc}</p>
        </div>
      {/each}
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
    max-width: 960px;
    margin: 0 auto;
  }

  .header {
    text-align: center;
    margin-bottom: 3rem;
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

  .grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }

  .feature {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1.75rem;
    transition:
      border-color 0.2s,
      box-shadow 0.2s;
  }

  .feature:hover {
    border-color: #bfdbfe;
    box-shadow:
      0 8px 24px rgba(15, 23, 42, 0.08),
      0 2px 8px rgba(15, 23, 42, 0.04);
  }

  .icon-tile {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.6rem;
    height: 2.6rem;
    border-radius: 10px;
    background: #eff6ff;
    color: var(--color-accent);
  }

  .feature-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--color-text-primary);
    margin: 0;
  }

  .feature-desc {
    font-size: 0.9rem;
    line-height: 1.65;
    color: var(--color-text-muted);
    margin: 0;
  }

  @media (max-width: 768px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 640px) {
    .section {
      padding: 3.5rem 1.25rem;
    }
  }
</style>
