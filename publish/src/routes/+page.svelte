<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import { get } from "svelte/store";
  import { authStore, setToken, setUser } from "$lib/stores.js";
  import * as api from "$lib/api.js";
  import ScoreIndicator from "$lib/components/ScoreIndicator.svelte";
  import SkillChips from "$lib/components/SkillChips.svelte";
  import {
    FileUp,
    ClipboardPaste,
    BadgePercent,
    Kanban,
    FileSearch,
    FileCheck,
    Globe,
  } from "@lucide/svelte";
  import { trackEvent } from "$lib/utils/analytics";
  import BrandTitle from "$lib/components/BrandTitle.svelte";

  let demoLoading = $state(false);
  let menuOpen = $state(false);
  let demoError = $state("");

  const previewScore = 7.8;
  const previewMatched = [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "REST APIs",
    "Git",
  ];
  const previewMissing = ["Docker", "Kubernetes"];

  onMount(() => {
    if (get(authStore).isAuthenticated) {
      goto("/applications");
    }
  });

  async function handleDemoLogin() {
    demoLoading = true;

    demoError = "";
    try {
      const data = await api.demoLogin();
      setToken(data.access_token);
      const user = await api.getMe();
      setUser(user);
      trackEvent("login_demo");
      goto("/applications");
    } catch (err) {
      demoError = (err as Error).message;
    } finally {
      demoLoading = false;
    }
  }
</script>

<svelte:head>
  <title>Match Before Apply — Know your match before you apply</title>
  <meta
    name="description"
    content="Upload your CV, paste a job description or job post URL, and get a clear match score, key gaps, and ATS insights — then track every application in one place."
  />
</svelte:head>

<!-- ── Landing Nav ── -->
<header class="landing-nav">
  <a href="/" class="brand-link">
    <BrandTitle />
  </a>

  <!-- Desktop links (hidden on mobile) -->
  <div class="landing-desktop-links">
    <a
      href="#how-it-works"
      class="nav-link"
      onclick={() => trackEvent("How_It_Works_Click")}
    >
      How it Works
    </a>
    <a
      href="#features"
      class="nav-link"
      onclick={() => trackEvent("features_click")}
    >
      Features
    </a>
    <a href="/login" class="btn-primary nav-cta">Get started</a>
  </div>

  <!-- Hamburger (mobile only) -->
  <button
    class="landing-hamburger"
    onclick={() => (menuOpen = !menuOpen)}
    aria-label="Toggle menu"
  >
    {menuOpen ? "✕" : "☰"}
  </button>
</header>

<!-- Mobile dropdown -->
{#if menuOpen}
  <nav class="landing-mobile-menu">
    <a
      href="#how-it-works"
      onclick={() => {
        menuOpen = false;
        trackEvent("How_It_Works_Click");
      }}
    >
      How it Works
    </a>
    <a
      href="#features"
      onclick={() => {
        menuOpen = false;
        trackEvent("features_click");
      }}
    >
      Features
    </a>
    <a href="/login" class="btn-primary" onclick={() => (menuOpen = false)}>
      Get started
    </a>
  </nav>
{/if}

<!-- ── Hero ── -->
<section class="hero-section">
  <div style="max-width:720px;margin:0 auto;text-align:center">
    <div class="eyebrow-pill">AI-powered job matching</div>

    <h1 class="hero-headline">
      Know your match<br />before you apply
    </h1>

    <p class="hero-sub">
      Upload your CV, paste a job description, and get a clear match score, key
      gaps, and ATS insights — then track every application in one place.
    </p>

    <div
      style="display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center;align-items:center"
    >
      <button
        class="btn-primary hero-cta"
        onclick={handleDemoLogin}
        disabled={demoLoading}
      >
        {demoLoading ? "Loading demo…" : "Try the demo"}
      </button>
      <a
        href="/login"
        class="btn-secondary hero-cta"
        style="text-decoration:none"
      >
        Get started for free
      </a>
    </div>

    {#if demoError}
      <p style="margin-top:1rem;color:var(--color-danger);font-size:.875rem">
        {demoError}
      </p>
    {/if}

    <p style="margin-top:1rem;font-size:.8rem;color:var(--color-text-muted)">
      No guessing. No blind applications.
    </p>
  </div>
</section>

<!-- ── How It Works ── -->
<section class="section section-surface" id="how-it-works">
  <div class="section-inner">
    <div class="section-header">
      <h2 class="section-title">A smarter way to apply</h2>
    </div>
    <div class="steps-grid">
      {#each [{ n: "01", title: "Upload your CV", desc: "Start with your experience and skills.", icon: FileUp }, { n: "02", title: "Paste the job description or URL", desc: "Compare your profile with the role — paste the job description or drop in a URL.", icon: ClipboardPaste }, { n: "03", title: "Get your match", desc: "See your match score and gaps instantly.", icon: BadgePercent }, { n: "04", title: "Track your application", desc: "Save it, add notes, and follow its status.", icon: Kanban }] as step (step.n)}
        <div
          class="card"
          style="display:flex;flex-direction:column;gap:.75rem;padding:1.5rem"
        >
          <span class="step-number">{step.n}</span>
          <h3
            style="font-size:1.1rem;font-weight:700;color:var(--color-text-primary);margin:0"
          >
            {step.title}
          </h3>
          <p
            style="font-size:.9rem;color:var(--color-text-muted);line-height:1.6;margin:0"
          >
            {step.desc}
          </p>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- ── Features ── -->
<section class="section section-bg" id="features">
  <div class="section-inner">
    <div class="section-header">
      <h2 class="section-title">
        Everything you need before and after applying
      </h2>
    </div>

    <div class="features-grid">
      {#each [{ icon: BadgePercent, title: "Match Score", desc: "See how well your CV aligns with a role before applying." }, { icon: FileSearch, title: "Gap Analysis", desc: "Understand what’s missing or unclear in your profile." }, { icon: FileCheck, title: "ATS Insights", desc: "Improve how your CV is interpreted by screening systems." }, { icon: Kanban, title: "Application Tracking", desc: "Keep all your applications in one place — with status, notes, and comments." }] as feature (feature.title)}
        <div
          class="card feature-card"
          style="padding:1.5rem;display:flex;flex-direction:column;gap:.75rem"
        >
          <div
            style="background:#eff6ff;padding:.5rem;border-radius:.5rem;width:fit-content"
          >
            <feature.icon size={18} color="var(--color-accent)" />
          </div>

          <h3
            style="font-size:1.1rem;font-weight:700;margin:0;color:var(--color-text-primary)"
          >
            {feature.title}
          </h3>

          <p
            style="font-size:.9rem;color:var(--color-text-muted);line-height:1.6;margin:0"
          >
            {feature.desc}
          </p>
        </div>
      {/each}
    </div>
  </div>
</section>

<!-- ── Story ── -->
<!-- <section class="section section-bg"> -->
<section class="section section-surface">
  <div
    class="section-inner"
    style="max-width:680px; background:var(--color-bg);border-radius:18px;padding:2.5rem"
  >
    <div class="section-header">
      <h2 class="section-title">Built because I needed it too</h2>
    </div>

    <blockquote class="story-quote">
      <p style="margin:0 0 1rem">
        This started during my own job search.<br /><br />
        Tracking applications was easy. <br />Knowing whether I was actually a
        good fit was not.
      </p>
      <p style="margin:0 0 1rem">
        Most candidates are guessing when they apply.<br />
        They don't know if they're a strong fit.<br /><br />
        And after applying, everything gets scattered — notes, statuses, follow-ups.
      </p>
      <p style="margin:0 0 1rem">
        So the process becomes:<br />
        apply &rarr; wait &rarr; forget &rarr; repeat.
      </p>
      <p style="margin:0">
        Instead of just organizing applications,<br />
        I built a tool to evaluate them first — and track them properly after.
      </p>
    </blockquote>

    <p class="story-attribution">— Naji,</p>
  </div>
</section>

<!-- ── Live Preview ── -->
<section class="section section-bg">
  <div class="section-inner" style="max-width:860px">
    <div class="section-header">
      <h2 class="section-title">Here’s what you’ll get</h2>
      <p class="section-sub">A sample result.</p>
    </div>

    <div class="card" style="padding:2rem">
      <div class="preview-header">
        <div>
          <h3
            style="font-size:1.1rem;font-weight:700;margin:0 0 .25rem;color:var(--color-text-primary)"
          >
            Senior Backend Engineer
          </h3>
          <p style="font-size:.9rem;color:var(--color-text-muted);margin:0">
            Acme Corp &middot; Remote
          </p>
        </div>
        <ScoreIndicator score={previewScore} size="lg" />
      </div>

      <SkillChips matched={previewMatched} missing={previewMissing} />

      <div
        style="margin-top:1.5rem;background:var(--color-surface-2);border-radius:12px;padding:1rem 1.25rem"
      >
        <p
          style="font-size:.8rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin:0 0 .5rem"
        >
          ATS Tip
        </p>
        <p
          style="font-size:.9rem;color:var(--color-text-primary);line-height:1.6;margin:0"
        >
          Add "containerization" or "Docker" explicitly in a Skills section —
          ATS scanners look for exact keyword matches before the resume reaches
          a recruiter.
        </p>
      </div>

      <p
        style="margin-top:1.25rem;font-size:.8rem;color:var(--color-text-muted);text-align:center;margin-bottom:0"
      >
        Demo mode uses simulated analysis results.
      </p>
    </div>
  </div>
</section>

<!-- ── Demo CTA ── -->
<!-- <section class="section section-surface">
  <div class="section-inner" style="max-width:600px;text-align:center">
    <h2 class="section-title">Try it with demo data</h2>
    <p
      style="color:var(--color-text-muted);font-size:1rem;margin:0 0 2rem;line-height:1.7"
    >
      Explore how match scoring and application tracking work together.
    </p>

    <button
      class="btn-primary"
      style="padding:.9rem 2rem;font-size:1rem;border-radius:12px"
      onclick={handleDemoLogin}
      disabled={demoLoading}
    >
      {demoLoading ? "Loading demo…" : "Try the demo"}
    </button>

    {#if demoError}
      <p style="margin-top:.75rem;color:var(--color-danger);font-size:.875rem">
        {demoError}
      </p>
    {/if}

    <p style="margin-top:1rem;font-size:.8rem;color:var(--color-text-muted)">
      Demo mode uses simulated analysis results.
    </p>
  </div>
</section> -->

<!-- ── Final CTA ── -->
<section class="final-cta-section">
  <div style="max-width:600px;margin:0 auto;text-align:center">
    <!-- <div -->
    <!-- class="card" -->
    <!-- style="display:flex;flex-direction:column;gap:.75rem;padding:1.5rem" -->
    <!-- > -->
    <h2 class="final-cta-headline">Stop applying blind</h2>
    <p class="final-cta-sub">
      Know your match. Track your applications. Stay in control.
    </p>
    <a href="/login" class="final-cta-btn">Get started for free</a>
    <p class="final-cta-disclaimer">
      No credit card required &middot; 3 free analyses per day
    </p>
  </div>
  <!-- </div> -->
</section>

<!-- ── Footer ── -->
<footer class="site-footer">
  <p style="margin:0 0 .35rem">
    <BrandTitle />
  </p>
  <div
    style="display:flex;align-items:center;justify-content:center;gap:.5rem;flex-wrap:wrap"
  >
    <p style="font-size:.8rem;color:var(--color-text-muted);margin:0">
      &copy; {new Date().getFullYear()} Built by
      <a
        href="https://linkedin.com/in/najikanounji"
        target="_blank"
        rel="noopener noreferrer"
        style="color: var(--color-accent); text-decoration: none;"
        >Naji Kanounji</a
      >
    </p>
    <a
      href="https://nkanounji.com"
      target="_blank"
      rel="noopener noreferrer"
      style="color: var(--color-accent); text-decoration: none;"
    >
      <Globe size={18} />
    </a>
  </div>
</footer>

<style>
  /* ── Nav ── */
  .landing-nav {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(248, 250, 252, 0.88);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--color-border);
    padding: 0 1.5rem;
    height: 3.75rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .brand-link {
    text-decoration: none;
  }

  .landing-desktop-links {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .nav-link {
    text-decoration: none;
    padding: 0.45rem 1rem;
    font-size: 0.875rem;
    color: var(--color-text-primary);
  }

  .nav-cta {
    text-decoration: none;
    padding: 0.45rem 1rem;
    font-size: 0.875rem;
  }

  .landing-hamburger {
    display: none;
    background: none;
    border: none;
    font-size: 1.25rem;
    cursor: pointer;
    color: var(--color-text-primary);
    padding: 0.25rem;
  }

  .landing-mobile-menu {
    position: sticky;
    top: 3.75rem;
    z-index: 40;
    background: rgba(248, 250, 252, 0.97);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    flex-direction: column;
    padding: 0.75rem 1.5rem 1rem;
    gap: 0.25rem;
  }

  .landing-mobile-menu a {
    text-decoration: none;
    padding: 0.6rem 0.5rem;
    font-size: 0.9rem;
    color: var(--color-text-primary);
  }

  @media (max-width: 640px) {
    .landing-desktop-links {
      display: none;
    }
    .landing-hamburger {
      display: block;
    }
  }

  /* ── Hero ── */
  .hero-section {
    background:
      radial-gradient(
        ellipse 80% 50% at 50% -10%,
        rgba(37, 99, 235, 0.12) 0%,
        transparent 60%
      ),
      var(--color-bg);
    padding: 5rem 1.5rem 4rem;
  }

  .eyebrow-pill {
    display: inline-flex;
    align-items: center;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--color-accent);
    margin-bottom: 1.5rem;
  }

  .hero-headline {
    font-size: clamp(2.25rem, 5vw, 3.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -1.5px;
    color: var(--color-text-primary);
    margin: 0 0 1.25rem;
  }

  .hero-sub {
    font-size: 1.125rem;
    color: var(--color-text-muted);
    line-height: 1.7;
    max-width: 580px;
    margin: 0 auto 2.5rem;
  }

  .hero-cta {
    padding: 0.8rem 1.75rem;
    font-size: 1rem;
    border-radius: 12px;
  }

  /* ── Sections ── */
  .section {
    padding: 5rem 1.5rem;
  }

  .section-bg {
    background: var(--color-bg);
  }

  .section-surface {
    background: var(--color-surface);
  }

  .section-inner {
    max-width: 900px;
    margin: 0 auto;
  }

  .section-header {
    text-align: center;
    margin-bottom: 3rem;
  }

  .section-title {
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--color-text-primary);
    margin: 0 0 0.75rem;
  }

  .section-sub {
    color: var(--color-text-muted);
    font-size: 1rem;
    margin: 0;
  }

  /* ── Steps grid ── */
  .steps-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2em;
  }

  .step-number {
    font-size: 2rem;
    font-weight: 800;
    color: var(--color-accent);
    opacity: 0.25;
    line-height: 1;
    display: block;
  }

  /* ── Features grid ── */
  .features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }

  .feature-card {
    display: flex;
    flex-direction: column;
  }

  /* .feature-icon {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
    display: block;
  } */

  /* ── Preview ── */
  .preview-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }

  /* ── Story ── */
  .story-quote {
    border-left: 3px solid var(--color-accent);
    padding-left: 1.5rem;
    margin: 0;
    font-size: 1.05rem;
    line-height: 1.8;
    color: var(--color-text-primary);
  }

  .story-attribution {
    margin-top: 1.5rem;
    font-size: 0.875rem;
    color: var(--color-text-muted);
    padding-left: 1.5rem;
  }

  /* ── Final CTA ── */
  .final-cta-section {
    padding: 5rem 1.5rem;
    background: linear-gradient(
      135deg,
      var(--color-accent) 0%,
      var(--color-accent-dark) 100%
    );
    text-align: center;
  }

  .final-cta-headline {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 800;
    letter-spacing: -1px;
    color: #fff;
    margin: 0 0 1rem;
  }

  .final-cta-sub {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.85);
    margin: 0 0 2.5rem;
    line-height: 1.7;
  }

  .final-cta-btn {
    display: inline-block;
    background: #fff;
    color: var(--color-accent);
    padding: 0.9rem 2.25rem;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 700;
    text-decoration: none;
    transition: opacity 0.2s;
  }

  .final-cta-btn:hover {
    opacity: 0.9;
  }

  .final-cta-disclaimer {
    margin-top: 1.25rem;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.65);
  }

  /* ── Footer ── */
  .site-footer {
    padding: 2rem 1.5rem;
    background: var(--color-surface);
    border-top: 1px solid var(--color-border);
    text-align: center;
  }

  /* ── Responsive ── */
  @media (max-width: 640px) {
    .steps-grid,
    .features-grid {
      grid-template-columns: 1fr;
    }

    .hero-section {
      padding: 3.5rem 1.25rem 3rem;
    }

    .section {
      padding: 3.5rem 1.25rem;
    }
  }
</style>
