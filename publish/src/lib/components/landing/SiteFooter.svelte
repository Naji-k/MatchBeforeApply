<script lang="ts">
  import BrandTitle from "$lib/components/BrandTitle.svelte";

  const year = new Date().getFullYear();
</script>

<!-- Official LinkedIn mark (Simple Icons), brand icons are not shipped by lucide -->
<footer class="site-footer">
  <BrandTitle />
  <p class="tagline">Know your match before you apply.</p>

  <div class="links">
    <p class="copyright">
      &copy; {year}
      Naji Kanounji
    </p>
    <div class="socials">
      <a
        href="https://linkedin.com/in/najikanounji"
        target="_blank"
        rel="noopener noreferrer"
        aria-label="LinkedIn profile"
      >
        <svg
          viewBox="0 0 24 24"
          fill="currentColor"
          width="17"
          height="17"
          aria-hidden="true"
        >
          <path
            d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.225 0z"
          />
        </svg>
      </a>
    </div>
  </div>
</footer>

<style>
  .site-footer {
    padding: 2.5rem 1.5rem;
    background: var(--color-surface);
    border-top: 1px solid var(--color-border);
    text-align: center;
  }

  .tagline {
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin: 0.35rem 0 1.5rem;
  }

  .links {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.25rem;
    flex-wrap: wrap;
  }

  .copyright {
    font-size: 0.8rem;
    color: var(--color-text-muted);
    margin: 0;
  }

  .copyright a {
    color: var(--color-text-primary);
    font-weight: 500;
    text-decoration: none;
  }

  .copyright a:hover {
    color: var(--color-accent);
  }

  .socials {
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .socials a {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    border-radius: 8px;
    color: var(--color-text-muted);
    transition:
      color 0.2s,
      background 0.2s;
  }

  .socials a:hover {
    color: var(--color-accent);
    background: var(--color-surface-2);
  }
</style>
