<script lang="ts">
  import "../app.css";
  import type { Snippet } from "svelte";
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import {
    authStore,
    setToken,
    setUser,
    toastStore,
    setUsage,
    setIsDemoUser,
    appConfigStore,
  } from "$lib/stores.js";
  import * as api from "$lib/api.js";
  import { onMount } from "svelte";
  import Navbar from "$lib/components/Navbar.svelte";

  let { children }: { children: Snippet } = $props();
  let initialized = $state(false);

  const isPublicPage = $derived(
    page.url.pathname === "/login" || page.url.pathname === "/",
  );

  onMount(() => {
    let unsubscribe: (() => void) | undefined;

    (async () => {
      await api.loadConfig();

      const token = localStorage.getItem("token");
      if (token) {
        setToken(token);
        try {
          const user = await api.getMe();
          setUser(user);
          try {
            const profile = await api.getProfile();
            // use config instead of VITE_DEMO_USER
            if (profile.user_id === $appConfigStore.VITE_DEMO_USER) {
              console.log("Demo user detected, enabling demo mode");
              setIsDemoUser(true);
              setUsage(0);
            } else {
              setUsage(profile.daily_analyses_used);
            }
          } catch {
            // non-fatal
          }
        } catch {
          setToken(null);
        }
      }
      initialized = true;

      unsubscribe = authStore.subscribe((auth) => {
        if (!auth.isAuthenticated && !isPublicPage) {
          goto("/login");
        }
      });
    })();

    return () => unsubscribe?.();
  });
</script>

{#if !initialized && !isPublicPage}
  <div
    style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:var(--color-bg)"
  >
    <span style="color:var(--color-text-muted)">Loading…</span>
  </div>
{:else}
  {#if $authStore.isAuthenticated}
    <Navbar />
  {/if}

  <main
    style="min-height:100vh;padding-top:{$authStore.isAuthenticated
      ? '4rem'
      : '0'}"
  >
    {@render children()}
  </main>

  {#if $toastStore}
    <div
      style="
      position:fixed;bottom:1.5rem;right:1.5rem;z-index:60;
      padding:.75rem 1.25rem;border-radius:12px;font-size:.875rem;font-weight:500;
      box-shadow:0 4px 20px rgba(0,0,0,.12);
      {$toastStore.type === 'success'
        ? 'background:#F0FDF4;color:#16A34A;border:1px solid #BBF7D0'
        : $toastStore.type === 'info'
          ? 'background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE'
          : 'background:#FEF2F2;color:#DC2626;border:1px solid #FECACA'}
    "
    >
      {$toastStore.message}
    </div>
  {/if}
{/if}
