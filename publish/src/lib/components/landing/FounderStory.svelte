<script lang="ts">
  import { reveal } from "$lib/utils/reveal.js";
</script>

<section class="section">
  <div class="inner" use:reveal>
    <h2 class="title">Built because I needed it too</h2>

    <blockquote class="story-quote">
      <p>
        This started during my own job search. Tracking applications was easy —
        knowing whether I was actually a good fit was not. Most candidates apply
        blind, and afterwards everything scatters: notes, statuses, follow-ups.
        Apply, wait, forget, repeat.
      </p>
      <p>
        So instead of building another place to organize applications, I built
        one to evaluate them first — and track them properly after.
      </p>
    </blockquote>

    <p class="attribution">— Naji</p>
  </div>
</section>

<style>
  .section {
    background: var(--color-bg);
    padding: 5rem 1.5rem;
  }

  .inner {
    max-width: 640px;
    margin: 0 auto;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 18px;
    padding: 2.5rem;
  }

  .title {
    font-size: clamp(1.4rem, 3vw, 1.8rem);
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--color-text-primary);
    text-align: center;
    margin: 0 0 2rem;
  }

  .story-quote {
    border-left: 3px solid var(--color-accent);
    padding-left: 1.5rem;
    margin: 0;
  }

  .story-quote p {
    font-size: 1rem;
    line-height: 1.8;
    color: var(--color-text-primary);
    margin: 0 0 1.25rem;
  }

  .story-quote p:last-child {
    margin-bottom: 0;
  }

  .attribution {
    margin: 1.5rem 0 0;
    padding-left: 1.5rem;
    font-size: 0.875rem;
    color: var(--color-text-muted);
  }

  .attribution a {
    color: var(--color-accent);
    font-weight: 600;
    text-decoration: none;
  }

  .attribution a:hover {
    text-decoration: underline;
  }

  @media (max-width: 640px) {
    .section {
      padding: 3.5rem 1.25rem;
    }

    .inner {
      padding: 1.75rem 1.5rem;
    }
  }
</style>
