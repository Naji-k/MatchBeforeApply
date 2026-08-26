<script lang="ts">
  import { ArrowRight, Lightbulb } from "@lucide/svelte";
  import ScoreIndicator from "$lib/components/ScoreIndicator.svelte";
  import SkillChips from "$lib/components/SkillChips.svelte";
  import { reveal } from "$lib/utils/reveal.js";
  import { trackEvent } from "$lib/utils/analytics";

  const previewScore = 8;
  const previewMatched = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "Docker",
    "REST APIs",
    "CI/CD",
    "AWS",
    "Microservices",
  ];
  const previewMissing = ["Kafka", "RabbitMQ", "Terraform"];
</script>

<section class="section" id="sample-report">
  <div class="inner" use:reveal>
    <div class="header">
      <h2 class="title">Here's what you'll get</h2>
      <p class="subtitle">A real sample report — score, gaps, and ATS tips.</p>
    </div>

    <div class="browser-frame">
      <div class="browser-bar">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="url">matchbeforeapply.com/applications/42</span>
      </div>

      <div class="report-body">
        <div class="report-head">
          <div>
            <h3 class="job-title">Senior Backend Engineer</h3>
            <p class="job-meta">
              TechCorp &middot; Remote &middot; Analyzed in 40s
            </p>
          </div>
          <ScoreIndicator score={previewScore} size="lg" />
        </div>

        <SkillChips matched={previewMatched} missing={previewMissing} />

        <div class="ats-box">
          <p class="ats-label"><Lightbulb size={15} /> ATS tip</p>
          <p class="ats-text">
            Include Terraform or other IaC tools if you have used them in past
            projects, and mention open-source contributions on GitHub — both are
            explicit keywords this posting screens for.
          </p>
        </div>

        <a
          href="/login"
          class="report-cta"
          onclick={() => trackEvent("sample_report_cta_click")}
        >
          Create a free account to see your report
          <ArrowRight size={15} />
        </a>
      </div>
    </div>
  </div>
</section>

<style>
  .section {
    background: var(--color-surface);
    padding: 5rem 1.5rem;
    scroll-margin-top: 4rem;
  }

  .inner {
    max-width: 780px;
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

  .browser-frame {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 16px;
    box-shadow:
      0 20px 50px rgba(15, 23, 42, 0.1),
      0 4px 14px rgba(15, 23, 42, 0.05);
    overflow: hidden;
  }

  .browser-bar {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.75rem 1.1rem;
    background: var(--color-surface-2);
    border-bottom: 1px solid var(--color-border);
  }

  .dot {
    width: 0.6rem;
    height: 0.6rem;
    border-radius: 50%;
    background: var(--color-border);
  }

  .url {
    margin-left: 0.6rem;
    flex: 1;
    min-width: 0;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 999px;
    padding: 0.25rem 0.85rem;
    font-size: 0.72rem;
    color: var(--color-text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .report-body {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .report-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1.25rem;
  }

  .job-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--color-text-primary);
    margin: 0 0 0.3rem;
  }

  .job-meta {
    font-size: 0.88rem;
    color: var(--color-text-muted);
    margin: 0;
  }

  .ats-box {
    background: color-mix(
      in srgb,
      var(--color-accent) 5%,
      var(--color-surface)
    );
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    padding: 1rem 1.25rem;
  }

  .ats-label {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-accent);
    margin: 0 0 0.45rem;
  }

  .ats-text {
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--color-text-primary);
    margin: 0;
  }

  .report-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--color-accent);
    text-decoration: none;
    transition: gap 0.2s;
    cursor: pointer;
  }

  .report-cta:hover {
    gap: 0.65rem;
  }

  @media (max-width: 640px) {
    .section {
      padding: 3.5rem 1.25rem;
    }

    .report-body {
      padding: 1.35rem;
    }
  }
</style>
