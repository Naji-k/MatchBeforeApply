<script lang="ts">
  import '../app.css';
  import type { Snippet } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/state';
  import { authStore, setToken, setUser, toastStore } from '$lib/stores.js';
  import * as api from '$lib/api.js';
  import { onMount } from 'svelte';
  import Navbar from '$lib/components/Navbar.svelte';

  let { children }: { children: Snippet } = $props();
  let initialized = $state(false);

  const isLoginPage = $derived(page.url.pathname === '/login');

  onMount(async () => {
    const token = localStorage.getItem('token');
    if (token) {
      setToken(token);
      try {
        const user = await api.getMe();
        setUser(user);
      } catch {
        setToken(null);
      }
    }
    initialized = true;

    const unsubscribe = authStore.subscribe((auth) => {
      if (!auth.isAuthenticated && !page.url.pathname.includes('/login')) {
        goto('/login');
      }
    });
    return unsubscribe;
  });
</script>

{#if !initialized && !isLoginPage}
  <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;background:#0f1117">
    <span style="color:#8892a4">Loading…</span>
  </div>
{:else}
  {#if $authStore.isAuthenticated}
    <Navbar />
  {/if}

  <main style="min-height:100vh;padding-top:{$authStore.isAuthenticated ? '4rem' : '0'}">
    {@render children()}
  </main>

  {#if $toastStore}
    <div
      style="
        position:fixed;bottom:1.5rem;right:1.5rem;z-index:60;
        padding:.75rem 1.25rem;border-radius:12px;font-size:.875rem;font-weight:500;
        box-shadow:0 4px 20px rgba(0,0,0,.4);
        {$toastStore.type === 'success'
          ? 'background:rgba(74,222,128,.15);color:#4ade80;border:1px solid rgba(74,222,128,.3)'
          : 'background:rgba(248,113,113,.15);color:#f87171;border:1px solid rgba(248,113,113,.3)'}
      "
    >
      {$toastStore.message}
    </div>
  {/if}
{/if}
