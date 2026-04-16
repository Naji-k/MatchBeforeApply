<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import { authStore, logout, usageStore, isDemoUser } from "$lib/stores.js";
  import FeedbackModal from "$lib/components/FeedbackModal.svelte";

  let menuOpen = $state(false);
  let feedbackOpen = $state(false);

  function handleLogout() {
    logout();
    goto("/");
  }

  const links = [
    { href: "/applications", label: "Applications" },
    { href: "/profile", label: "Profile" },
  ];
</script>

<nav class="navbar">
  <a href="/applications" class="brand">
    Match Before
    <span style="color:var(--color-accent)">Apply</span>
  </a>

  <!-- Desktop links -->
  <div class="desktop-links">
    {#each links as link}
      <a
        href={link.href}
        class="nav-link"
        class:active={page.url.pathname.startsWith(link.href)}
      >
        {link.label}
      </a>
    {/each}
  </div>

  <!-- User info + logout (desktop) -->
  <div class="desktop-user">
    {#if $authStore.user}
      <span class="user-email"
        >{$authStore.user.full_name || $authStore.user.email}</span
      >
    {/if}
    {#if $usageStore !== null}
      {#if $isDemoUser}
        <span
          class="usage-pill"
          class:at-limit={$usageStore.used >= $usageStore.limit}
        >
          {$usageStore.used}/{$usageStore.limit} analyses
        </span>
      {/if}
    {/if}
    <button class="feedback-btn" onclick={() => (feedbackOpen = true)}
      >Feedback</button
    >
    <button onclick={handleLogout} class="logout-btn">Logout</button>
  </div>

  <!-- Hamburger (mobile) -->
  <button
    class="hamburger"
    onclick={() => (menuOpen = !menuOpen)}
    aria-label="Toggle menu"
  >
    {#if menuOpen}✕{:else}☰{/if}
  </button>
</nav>

<!-- Mobile menu -->
{#if menuOpen}
  <div class="mobile-menu">
    {#each links as link}
      <a
        href={link.href}
        class="mobile-link"
        onclick={() => (menuOpen = false)}
      >
        {link.label}
      </a>
    {/each}
    {#if $authStore.user}
      <span class="user-email" style="padding:.5rem 0"
        >{$authStore.user.email}</span
      >
    {/if}
    {#if $usageStore !== null && $isDemoUser === false}
      <span
        class="usage-pill"
        class:at-limit={$usageStore.used >= $usageStore.limit}
        style="padding:.25rem 0"
      >
        {$usageStore.used}/{$usageStore.limit} analyses today
      </span>
    {/if}
    <button
      class="feedback-btn"
      style="text-align:left;padding:.5rem 0"
      onclick={() => {
        menuOpen = false;
        feedbackOpen = true;
      }}>Feedback</button
    >
    <button
      onclick={handleLogout}
      class="logout-btn"
      style="text-align:left;padding:.5rem 0">Logout</button
    >
  </div>
{/if}

{#if feedbackOpen}
  <FeedbackModal onclose={() => (feedbackOpen = false)} />
{/if}

<style>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 40;
    height: 4rem;
    background: var(--color-surface);
    border-bottom: 1px solid var(--color-border);
    display: flex;
    align-items: center;
    padding: 0 1.5rem;
    gap: 2rem;
  }
  .brand {
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--color-text-primary);
    text-decoration: none;
    white-space: nowrap;
  }
  .desktop-links {
    display: flex;
    gap: 1.5rem;
    flex: 1;
  }
  .nav-link {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--color-text-muted);
    text-decoration: none;
    transition: color 0.2s;
  }
  .nav-link:hover,
  .nav-link.active {
    color: var(--color-text-primary);
  }
  .desktop-user {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-left: auto;
  }
  .user-email {
    font-size: 0.85rem;
    color: var(--color-text-muted);
  }
  .usage-pill {
    font-size: 0.78rem;
    color: var(--color-text-muted);
    background: var(--color-border);
    border-radius: 999px;
    padding: 0.15rem 0.6rem;
    white-space: nowrap;
  }
  .usage-pill.at-limit {
    color: var(--color-danger);
    background: color-mix(in srgb, var(--color-danger) 10%, transparent);
  }
  .logout-btn {
    background: none;
    border: none;
    font-size: 0.85rem;
    color: var(--color-text-muted);
    cursor: pointer;
    transition: color 0.2s;
  }
  .logout-btn:hover {
    color: var(--color-danger);
  }
  .feedback-btn {
    background: none;
    border: none;
    font-size: 0.85rem;
    color: var(--color-text-muted);
    cursor: pointer;
    transition: color 0.2s;
    padding: 0;
  }
  .feedback-btn:hover {
    color: var(--color-accent);
  }
  .hamburger {
    display: none;
    background: none;
    border: none;
    color: var(--color-text-muted);
    font-size: 1.3rem;
    cursor: pointer;
    margin-left: auto;
  }
  .mobile-menu {
    position: fixed;
    top: 4rem;
    left: 0;
    right: 0;
    z-index: 30;
    background: var(--color-surface);
    border-bottom: 1px solid var(--color-border);
    padding: 1rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  .mobile-link {
    color: var(--color-text-muted);
    text-decoration: none;
    padding: 0.5rem 0;
    transition: color 0.2s;
  }
  .mobile-link:hover {
    color: var(--color-text-primary);
  }

  @media (max-width: 640px) {
    .desktop-links,
    .desktop-user {
      display: none;
    }
    .hamburger {
      display: block;
    }
  }
</style>
