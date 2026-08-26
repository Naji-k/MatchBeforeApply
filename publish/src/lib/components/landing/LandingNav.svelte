<script lang="ts">
  import { Menu, X } from "@lucide/svelte";
  import { trackEvent } from "$lib/utils/analytics";
  import BrandTitle from "$lib/components/BrandTitle.svelte";

  let menuOpen = $state(false);

  const links = [
    {
      href: "#how-it-works",
      label: "How it works",
      event: "How_It_Works_Click",
    },
    { href: "#features", label: "Features", event: "features_click" },
    {
      href: "#sample-report",
      label: "Sample report",
      event: "sample_report_click",
    },
  ];
</script>

<header class="landing-nav">
  <a href="/" class="brand-link" aria-label="Match Before Apply — home">
    <BrandTitle />
  </a>

  <nav class="desktop-links" aria-label="Primary">
    {#each links as link (link.href)}
      <a
        href={link.href}
        class="nav-link"
        onclick={() => trackEvent(link.event)}
      >
        {link.label}
      </a>
    {/each}
    <a href="/login" class="nav-login">Log in</a>
    <a href="/login" class="btn-primary nav-cta">Get started</a>
  </nav>

  <button
    class="hamburger"
    onclick={() => (menuOpen = !menuOpen)}
    aria-label={menuOpen ? "Close menu" : "Open menu"}
    aria-expanded={menuOpen}
  >
    {#if menuOpen}
      <X size={22} />
    {:else}
      <Menu size={22} />
    {/if}
  </button>
</header>

{#if menuOpen}
  <nav class="mobile-menu" aria-label="Mobile">
    {#each links as link (link.href)}
      <a
        href={link.href}
        onclick={() => {
          menuOpen = false;
          trackEvent(link.event);
        }}
      >
        {link.label}
      </a>
    {/each}
    <div class="mobile-actions">
      <a href="/login" class="btn-secondary" onclick={() => (menuOpen = false)}>
        Log in
      </a>
      <a href="/login" class="btn-primary" onclick={() => (menuOpen = false)}>
        Get started
      </a>
    </div>
  </nav>
{/if}

<style>
  .landing-nav {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(248, 250, 252, 0.88);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
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

  .desktop-links {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .nav-link {
    text-decoration: none;
    padding: 0.45rem 0.9rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--color-text-muted);
    border-radius: 8px;
    transition:
      color 0.2s,
      background 0.2s;
    cursor: pointer;
  }

  .nav-link:hover {
    color: var(--color-text-primary);
    background: var(--color-surface-2);
  }

  .nav-login {
    text-decoration: none;
    padding: 0.45rem 0.9rem;
    margin-left: 0.75rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--color-text-primary);
    transition: color 0.2s;
    cursor: pointer;
  }

  .nav-login:hover {
    color: var(--color-accent);
  }

  .nav-cta {
    text-decoration: none;
    padding: 0.45rem 1rem;
    font-size: 0.875rem;
  }

  .hamburger {
    display: none;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    background: none;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    color: var(--color-text-primary);
    transition: background 0.2s;
  }

  .hamburger:hover {
    background: var(--color-surface-2);
  }

  .mobile-menu {
    position: sticky;
    top: 3.75rem;
    z-index: 40;
    background: rgba(248, 250, 252, 0.97);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    flex-direction: column;
    padding: 0.75rem 1.5rem 1.25rem;
    gap: 0.25rem;
  }

  .mobile-menu a:not(.btn-primary):not(.btn-secondary) {
    text-decoration: none;
    padding: 0.65rem 0.5rem;
    font-size: 0.95rem;
    color: var(--color-text-primary);
    border-radius: 8px;
  }

  .mobile-menu a:not(.btn-primary):not(.btn-secondary):hover {
    background: var(--color-surface-2);
  }

  .mobile-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 0.75rem;
  }

  .mobile-actions a {
    flex: 1;
    text-decoration: none;
  }

  @media (max-width: 768px) {
    .desktop-links {
      display: none;
    }
    .hamburger {
      display: flex;
    }
  }
</style>
