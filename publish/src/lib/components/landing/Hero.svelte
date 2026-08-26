<script lang="ts">
  import {
    ArrowRight,
    BadgePercent,
    Kanban,
    Lightbulb,
    Lock,
    Sparkles,
  } from "@lucide/svelte";
  import ScoreIndicator from "$lib/components/ScoreIndicator.svelte";
  import { trackEvent } from "$lib/utils/analytics";

  const previewScore = 8;
  const matched = ["Python", "FastAPI", "PostgreSQL", "REST APIs", "AWS"];
  const missing = ["Kafka", "Terraform"];
</script>

<section class="hero">
  <div class="hero-inner">
    <div class="hero-copy">
      <div class="eyebrow-pill anim rise">
        <Sparkles size={14} />
        AI-powered job matching
      </div>

      <h1 class="headline anim rise" style="animation-delay:80ms">
        Know your match<br />before you apply
      </h1>

      <p class="sub anim rise" style="animation-delay:160ms">
        Upload your CV once. Paste any job description or URL. Get an honest
        match score, the skill gaps that matter, and ATS tips — before you hit
        send.
      </p>

      <div class="cta-row anim rise" style="animation-delay:240ms">
        <a
          href="/login"
          class="btn-primary cta-primary"
          onclick={() => trackEvent("hero_cta_click")}
        >
          Check my match — free
        </a>
        <a href="#sample-report" class="cta-secondary">
          See a sample report
          <ArrowRight size={16} />
        </a>
      </div>

      <p class="microcopy anim rise" style="animation-delay:320ms">
        <Lock size={13} />
        Free to start &middot; No credit card &middot; Your CV stays private
      </p>
    </div>

    <!-- Product mockup -->
    <div class="mockup-wrap anim rise" style="animation-delay:200ms">
      <div class="floating-badge badge-board">
        <span class="badge-icon"><Kanban size={15} /></span>
        Saved to your board
      </div>

      <div class="browser-card">
        <div class="browser-bar">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="url">matchbeforeapply.com/applications/42</span>
        </div>

        <div class="report">
          <div class="report-head">
            <div>
              <p class="job-title">Senior Backend Engineer</p>
              <p class="job-meta">TechCorp &middot; Remote</p>
            </div>
            <ScoreIndicator score={previewScore} size="lg" />
          </div>

          <div class="skills-row">
            <div class="skill-group">
              <p class="skill-label matched-label">
                <BadgePercent size={13} /> Matched skills
              </p>
              <div class="chips">
                {#each matched as skill, i (skill)}
                  <span
                    class="chip chip-match anim pop"
                    style="animation-delay:{500 + i * 70}ms">{skill}</span
                  >
                {/each}
              </div>
            </div>
            <div class="skill-group">
              <p class="skill-label missing-label">Gaps</p>
              <div class="chips">
                {#each missing as skill, i (skill)}
                  <span
                    class="chip chip-missing anim pop"
                    style="animation-delay:{850 + i * 70}ms">{skill}</span
                  >
                {/each}
              </div>
            </div>
          </div>

          <div class="ats-box">
            <p class="ats-label"><Lightbulb size={14} /> ATS tip</p>
            <p class="ats-text">
              Add "infrastructure as code" explicitly in a Skills section — ATS
              scanners look for exact keyword matches before a recruiter ever
              sees your CV.
            </p>
          </div>
        </div>
      </div>

      <div class="floating-badge badge-score">
        <span class="badge-icon accent"><BadgePercent size={15} /></span>
        12 ATS keywords found
      </div>
    </div>
  </div>
</section>

<style>
  .hero {
    background:
      radial-gradient(
        ellipse 70% 55% at 75% -10%,
        rgba(37, 99, 235, 0.12) 0%,
        transparent 60%
      ),
      radial-gradient(
        ellipse 50% 40% at 15% 10%,
        rgba(37, 99, 235, 0.06) 0%,
        transparent 55%
      ),
      var(--color-bg);
    padding: 4.5rem 1.5rem 5rem;
    overflow: hidden;
  }

  .hero-inner {
    max-width: 1080px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 4rem;
    align-items: center;
  }

  /* ── Copy column ── */
  .eyebrow-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 999px;
    padding: 0.35rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--color-accent);
    margin-bottom: 1.5rem;
  }

  .headline {
    font-size: clamp(2.25rem, 5vw, 3.4rem);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -1.5px;
    color: var(--color-text-primary);
    margin: 0 0 1.25rem;
  }

  .sub {
    font-size: 1.125rem;
    color: var(--color-text-muted);
    line-height: 1.7;
    max-width: 480px;
    margin: 0 0 2rem;
  }

  .cta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.85rem;
    align-items: center;
  }

  .cta-primary {
    padding: 0.85rem 1.6rem;
    font-size: 1rem;
    border-radius: 12px;
    text-decoration: none;
  }

  .cta-secondary {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.85rem 1.25rem;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--color-accent);
    text-decoration: none;
    border-radius: 12px;
    transition:
      background 0.2s,
      gap 0.2s;
    cursor: pointer;
  }

  .cta-secondary:hover {
    background: #eff6ff;
    gap: 0.65rem;
  }

  .microcopy {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    margin-top: 1.25rem;
    font-size: 0.8rem;
    color: var(--color-text-muted);
  }

  /* ── Mockup column ── */
  .mockup-wrap {
    position: relative;
  }

  .browser-card {
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 16px;
    box-shadow:
      0 24px 60px rgba(15, 23, 42, 0.12),
      0 4px 16px rgba(15, 23, 42, 0.06);
    overflow: hidden;
  }

  .browser-bar {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.7rem 1rem;
    background: var(--color-surface-2);
    border-bottom: 1px solid var(--color-border);
  }

  .dot {
    width: 0.55rem;
    height: 0.55rem;
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
    padding: 0.2rem 0.75rem;
    font-size: 0.68rem;
    color: var(--color-text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .report {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.1rem;
  }

  .report-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
  }

  .job-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--color-text-primary);
    margin: 0 0 0.2rem;
  }

  .job-meta {
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin: 0;
  }

  .skills-row {
    display: grid;
    grid-template-columns: 1.3fr 0.7fr;
    gap: 1rem;
  }

  .skill-group {
    background: var(--color-bg);
    border: 1px solid var(--color-border);
    border-radius: 12px;
    padding: 0.85rem;
  }

  .skill-label {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.55rem;
  }

  .matched-label {
    color: var(--color-success);
  }

  .missing-label {
    color: var(--color-danger);
  }

  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }

  .chip {
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 500;
    white-space: nowrap;
  }

  .chip-match {
    background: #f0fdf4;
    color: #16a34a;
    border: 1px solid #bbf7d0;
  }

  .chip-missing {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
  }

  .ats-box {
    background: color-mix(
      in srgb,
      var(--color-accent) 5%,
      var(--color-surface)
    );
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    padding: 0.9rem 1rem;
  }

  .ats-label {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-accent);
    margin: 0 0 0.4rem;
  }

  .ats-text {
    font-size: 0.84rem;
    line-height: 1.55;
    color: var(--color-text-primary);
    margin: 0;
  }

  /* ── Floating badges ── */
  .floating-badge {
    position: absolute;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 0.45rem;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 999px;
    padding: 0.5rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--color-text-primary);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.1);
  }

  .badge-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
    background: var(--color-surface-2);
    color: var(--color-text-muted);
  }

  .badge-icon.accent {
    background: #eff6ff;
    color: var(--color-accent);
  }

  .badge-board {
    top: -1rem;
    right: -0.75rem;
    animation: rise 0.5s ease-out 900ms both;
  }

  .badge-score {
    bottom: -1rem;
    left: -0.75rem;
    animation: rise 0.5s ease-out 1050ms both;
  }

  /* ── Entrance animations ── */
  .anim.rise {
    animation: rise 0.5s ease-out both;
  }

  .anim.pop {
    animation: pop 0.35s ease-out both;
  }

  @keyframes rise {
    from {
      opacity: 0;
      transform: translateY(18px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes pop {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .anim.rise,
    .anim.pop,
    .badge-board,
    .badge-score {
      animation: none !important;
      opacity: 1 !important;
      transform: none !important;
    }
  }

  /* ── Responsive ── */
  @media (max-width: 1024px) {
    .hero-inner {
      grid-template-columns: 1fr;
      gap: 3.5rem;
    }

    .sub {
      max-width: 560px;
    }

    .mockup-wrap {
      max-width: 520px;
      margin: 0 auto;
      width: 100%;
    }
  }

  @media (max-width: 640px) {
    .hero {
      padding: 3.5rem 1.25rem 4rem;
    }

    .report {
      padding: 1.1rem;
    }

    .skills-row {
      grid-template-columns: 1fr;
    }

    .floating-badge {
      display: none;
    }
  }
</style>
