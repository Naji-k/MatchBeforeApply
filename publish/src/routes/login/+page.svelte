<script lang="ts" module>
  declare const google: {
    accounts: {
      id: {
        initialize: (config: object) => void;
        renderButton: (el: HTMLElement | null, options: object) => void;
      };
    };
  };
</script>

<script lang="ts">
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";
  import { authStore, setToken, setUser, showToast } from "$lib/stores.js";
  import { login, register, googleAuth, getMe } from "$lib/api.js";
  import { validateEmail } from "$lib/utils/validation.js";
  import { onMount } from "svelte";

  let mode = $state<"login" | "signup">("login");
  let email = $state("");
  let password = $state("");
  let fullName = $state("");
  let loading = $state(false);
  let error = $state("");

  onMount(() => {
    if (get(authStore).isAuthenticated) {
      goto("/applications");
      return;
    }

    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    if (clientId && typeof google !== "undefined") {
      google.accounts.id.initialize({
        client_id: clientId,
        callback: handleGoogleResponse,
      });
      google.accounts.id.renderButton(document.getElementById("google-btn"), {
        theme: "outline",
        size: "large",
        shape: "rectangular",
        width: 340,
        text: "continue_with",
      });
    }
  });

  async function handleGoogleResponse(response: { credential: string }) {
    loading = true;
    error = "";
    try {
      const data = await googleAuth(response.credential);
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

  function switchMode(next: "login" | "signup") {
    mode = next;
    error = "";
  }

  async function handleSubmit(e: SubmitEvent): Promise<void> {
    e.preventDefault();
    error = "";

    if (mode === "signup" && !fullName.trim()) {
      error = "Please enter your full name.";
      return;
    }
    if (!validateEmail(email)) {
      error = "Please enter a valid email.";
      return;
    }
    if (!password || password.length < 6) {
      error = "Password must be at least 6 characters.";
      return;
    }

    loading = true;
    try {
      if (mode === "signup") {
        await register(email, password, fullName.trim());
      }
      const data = await login(email, password);
      const token = data.access_token;
      setToken(token);
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

<svelte:head
  ><title>{mode === "signup" ? "Sign Up" : "Login"} — MatchBeforeApply</title
  ></svelte:head
>

<div
  style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:1rem;background:var(--color-bg)"
>
  <div style="width:100%;max-width:420px">
    <!-- Hero -->
    <div style="text-align:center;margin-bottom:2rem">
      <h1 style="font-size:2rem;font-weight:800;letter-spacing:-1px">
        Match Before
        <span style="color:var(--color-accent)">Apply</span>
      </h1>
      <p style="color:var(--color-text-muted);margin-top:.5rem">
        {mode === "signup" ? "Create your account" : "Welcome back"}
      </p>
    </div>

    <form
      class="card"
      style="display:flex;flex-direction:column;gap:0.7rem"
      onsubmit={handleSubmit}
    >
      {#if error}
        <div
          style="background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);color:#f87171;font-size:.875rem;padding:.75rem 1rem;border-radius:10px"
        >
          {error}
        </div>
      {/if}

      {#if mode === "signup"}
        <div style="display:flex;flex-direction:column;gap:.5rem;margin:.75rem">
          <label
            for="fullName"
            style="font-size:.85rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;"
            >Full Name</label
          >
          <input
            id="fullName"
            type="text"
            class="input-field"
            bind:value={fullName}
            placeholder="Jane Smith"
            required
          />
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
        style="width:80%;padding:.75rem;font-size:1rem;margin:auto;"
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
            {mode === "signup" ? "Creating account…" : "Signing in…"}
          </span>
        {:else}
          {mode === "signup" ? "Create account" : "Log in"}
        {/if}
      </button>

      <!-- Divider -->
      <div
        style="display:flex;align-items:center;gap:.75rem;margin:.25rem .75rem 0"
      >
        <div style="flex:1;height:1px;background:var(--color-border)"></div>
        <span style="font-size:.8rem;color:var(--color-text-muted)">or</span>
        <div style="flex:1;height:1px;background:var(--color-border)"></div>
      </div>

      <!-- Google Sign-In button -->
      <div
        style="display:flex;justify-content:center;margin:.25rem .75rem .5rem"
      >
        <div id="google-btn"></div>
      </div>
      <!-- {#if import.meta.env.VITE_ENABLE_SIGNUP === "true"} -->
      <p
        style="text-align:center;font-size:.875rem;color:var(--color-text-muted);margin-bottom:.75rem"
      >
        {#if mode === "login"}
          Don't have an account?
          <button
            type="button"
            style="background:none;border:none;color:var(--color-accent);cursor:pointer;font-size:.875rem;font-weight:600;padding:0"
            onclick={() => switchMode("signup")}>Sign up</button
          >
        {:else}
          Already have an account?
          <button
            type="button"
            style="background:none;border:none;color:var(--color-accent);cursor:pointer;font-size:.875rem;font-weight:600;padding:0"
            onclick={() => switchMode("login")}>Log in</button
          >
        {/if}
      </p>
      <!-- {:else} -->
      <button
        type="button"
        style="width:100%;padding:.75rem;font-size:.875rem;font-weight:600;background:rgba(0,0,0,.05);border:1px solid var(--color-border);border-radius:8px;color:var(--color-text);cursor:pointer;margin-top:.75rem;transition:background 200ms"
        onclick={async () => {
          loading = true;
          error = "";
          try {
            const data = await login("user@user.com", "string");
            setToken(data.access_token);
            const user = await getMe();
            setUser(user);
            showToast(
              "You're in demo mode 👀 You can explore with mock data, but analyzing resumes and saving applications are disabled. Log in to try it for real.",
              "info",
            );
            goto("/applications");
          } catch (err) {
            error = (err as Error).message;
          } finally {
            loading = false;
          }
        }}
        disabled={loading}
      >
        {loading ? "Logging in…" : "Try Demo Account"}
      </button>
      <!-- {/if} -->
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
