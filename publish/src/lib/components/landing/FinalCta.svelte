<script lang="ts">
  import { MessageCircle } from "@lucide/svelte";
  import { appConfigStore } from "$lib/stores.js";
  import { trackEvent } from "$lib/utils/analytics";
</script>

<section class="final-cta">
  <div class="inner">
    <h2 class="headline">Stop applying blind</h2>
    <p class="sub">
      Know your match. Track your applications. Stay in control.
    </p>
    <a
      href="/login"
      class="cta-btn"
      onclick={() => trackEvent("final_cta_click")}
    >
      Check my match — free
    </a>
    <p class="disclaimer">
      No credit card required &middot; 3 free analyses per day
    </p>

    {#if $appConfigStore.ENABLE_FAQ_CHAT}
      <p class="faq-nudge">
        <MessageCircle size={14} />
        Questions? Tap the chat bubble in the corner.
      </p>
    {/if}
  </div>
</section>

<style>
  .final-cta {
    padding: 5rem 1.5rem;
    background: linear-gradient(
      135deg,
      var(--color-accent) 0%,
      var(--color-accent-dark) 100%
    );
    text-align: center;
  }

  .inner {
    max-width: 600px;
    margin: 0 auto;
  }

  .headline {
    font-size: clamp(1.75rem, 4vw, 2.5rem);
    font-weight: 800;
    letter-spacing: -1px;
    color: #fff;
    margin: 0 0 1rem;
  }

  .sub {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.85);
    line-height: 1.7;
    margin: 0 0 2.5rem;
  }

  .cta-btn {
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

  .cta-btn:hover {
    opacity: 0.9;
  }

  .disclaimer {
    margin-top: 1.25rem;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.65);
  }

  .faq-nudge {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    margin-top: 0.75rem;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.75);
  }

  @media (max-width: 640px) {
    .final-cta {
      padding: 3.5rem 1.25rem;
    }
  }
</style>
