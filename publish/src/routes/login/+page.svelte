<script lang="ts">
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";
  import { authStore, setToken, setUser } from "$lib/stores.js";
  import { login, getMe } from "$lib/api.js";
  import { validateEmail } from "$lib/utils/validation.js";
  import { onMount } from "svelte";

  let email = $state("");
  let password = $state("");
  let loading = $state(false);
  let error = $state("");

  onMount(() => {
    if (get(authStore).isAuthenticated) goto("/applications");
  });

  async function handleSubmit(e: SubmitEvent): Promise<void> {
    e.preventDefault();
    error = "";

    if (!validateEmail(email)) {
      error = "Please enter a valid email.";
      return;
    }
    if (!password) {
      error = "Please enter your password.";
      return;
    }

    loading = true;
    try {
      const data = await login(email, password);
      setToken(data.access_token);
      const user = await getMe();
      setUser(user);
      goto("/applications");
    } catch (err) {
      error = (err as Error).message;
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head><title>Login — AIJobBoard</title></svelte:head>

<div
  style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:1rem;background:var(--color-bg)"
>
  <div style="width:100%;max-width:420px">
    <!-- Hero -->
    <div style="text-align:center;margin-bottom:2rem">
      <h1 style="font-size:2rem;font-weight:800;letter-spacing:-1px">
        <span style="color:var(--color-accent)">AI</span>JobBoard
      </h1>
      <p style="color:var(--color-text-muted);margin-top:.5rem">
        Sign in to your account
      </p>
    </div>

    <form
      class="card"
      style="display:flex;flex-direction:column;gap:1.4rem"
      onsubmit={handleSubmit}
    >
      {#if error}
        <div
          style="background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);color:#f87171;font-size:.875rem;padding:.75rem 1rem;border-radius:10px"
        >
          {error}
        </div>
      {/if}

      <div style="display:flex;flex-direction:column;gap:.5rem;margin:.75rem">
        <label
          for="email"
          style="font-size:.85rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;"
          >Email</label
        >
        <input
          id="email"
          type="email"
          class="input-field"
          bind:value={email}
          placeholder="you@example.com"
          required
        />
      </div>

      <div style="display:flex;flex-direction:column;gap:.5rem;margin:.75rem">
        <label
          for="password"
          style="font-size:.85rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em"
          >Password</label
        >
        <input
          id="password"
          type="password"
          class="input-field"
          bind:value={password}
          placeholder="••••••••"
          required
        />
      </div>

      <button
        type="submit"
        class="btn-primary"
        style="width:80%;padding:.75rem;font-size:1rem;margin:auto; margin-bottom: .75rem;"
        disabled={loading}
      >
        {#if loading}
          <span
            style="display:inline-flex;align-items:center;gap:.5rem;justify-content:center"
          >
            <svg
              style="width:1rem;height:1rem;animation:spin 1s linear infinite"
              viewBox="0 0 24 24"
              fill="none"
            >
              <circle
                opacity=".25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              />
              <path
                opacity=".75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            Signing in…
          </span>
        {:else}
          Login
        {/if}
      </button>
    </form>
  </div>
</div>

<style>
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
