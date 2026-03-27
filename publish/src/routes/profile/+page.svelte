<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";
  import type { Profile } from "$lib/types.js";
  import { authStore, logout, showToast } from "$lib/stores.js";
  import { getProfile, uploadCV } from "$lib/api.js";
  import { formatDate } from "$lib/utils/helpers.js";

  let profile = $state<Profile | null>(null);
  let loading = $state(true);
  let uploading = $state(false);
  let uploadSuccess = $state("");
  let dragOver = $state(false);
  let fileInput: HTMLInputElement;

  onMount(async () => {
    try {
      profile = await getProfile();
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      loading = false;
    }
  });

  async function handleUpload(file: File): Promise<void> {
    if (file.type !== "application/pdf") {
      showToast("Please upload a PDF file.");
      return;
    }
    uploading = true;
    uploadSuccess = "";
    try {
      await uploadCV(file);
      profile = await getProfile();
      uploadSuccess = `✓ CV uploaded: ${file.name}`;
      showToast("CV uploaded successfully!", "success");
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      uploading = false;
    }
  }

  function onFileChange(e: Event): void {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (file) handleUpload(file);
    (e.target as HTMLInputElement).value = "";
  }

  function onDrop(e: DragEvent): void {
    e.preventDefault();
    dragOver = false;
    const file = e.dataTransfer?.files?.[0];
    if (file) handleUpload(file);
  }

  function handleLogout(): void {
    logout();
    goto("/login");
  }
</script>

<svelte:head><title>Profile — AIJobBoard</title></svelte:head>

<div
  style="max-width:600px;margin:0 auto;padding:2rem 1rem;display:flex;flex-direction:column;gap:1.5rem"
>
  <h1 style="font-size:1.6rem;font-weight:700">Profile</h1>

  <!-- Account info -->
  {#if $authStore.user}
    <div class="card" style="padding:.75rem">
      <p
        style="font-size:.8rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.75rem"
      >
        Account
      </p>
      {#if $authStore.user.full_name}
        <p style="font-weight:600;font-size:1.05rem;margin-bottom:.25rem">
          {$authStore.user.full_name}
        </p>
      {/if}
      <p style="color:var(--color-text-muted);font-size:.9rem">
        {$authStore.user.email}
      </p>
    </div>
  {/if}

  <!-- CV upload -->
  <div
    class="card"
    style="display:flex;flex-direction:column;gap:1rem;padding:.75rem"
  >
    <p
      style="font-size:.8rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em"
    >
      Your CV
    </p>

    {#if loading}
      <p style="color:var(--color-text-muted);font-size:.9rem;margin:.75rem">
        Loading…
      </p>
    {:else if profile?.cv_text}
      <div style="display:flex;align-items:center;gap:.5rem;font-size:.9rem">
        <span style="color:var(--color-success)">✓</span>
        <span>CV uploaded</span>
        {#if profile.updated_at}
          <span
            style="font-size:.8rem;color:var(--color-text-muted);margin-left:.25rem;"
            >· Updated {formatDate(profile.updated_at)}</span
          >
        {/if}
      </div>
    {:else}
      <p style="color:var(--color-text-muted);font-size:.9rem">
        No CV uploaded yet.
      </p>
    {/if}

    {#if uploadSuccess}
      <p style="color:var(--color-success);font-size:.875rem">
        {uploadSuccess}
      </p>
    {/if}

    <!-- Drop zone -->
    <div
      style="
        border:2px dashed;border-radius:14px;padding:2.5rem 1rem;text-align:center;
        cursor:pointer;transition:all .2s;
        {dragOver
        ? 'border-color:var(--color-accent);background:rgba(108,99,255,.06)'
        : 'border-color:var(--color-border)'}
      "
      ondragover={(e) => {
        e.preventDefault();
        dragOver = true;
      }}
      ondragleave={() => (dragOver = false)}
      ondrop={onDrop}
      onclick={() => fileInput.click()}
      role="button"
      tabindex="0"
      onkeydown={(e) => e.key === "Enter" && fileInput.click()}
      aria-label="Upload CV PDF"
    >
      {#if uploading}
        <p style="color:var(--color-text-muted)">Uploading…</p>
      {:else}
        <p style="color:var(--color-text-muted);margin-bottom:.4rem">
          Drag & drop your PDF here
        </p>
        <p style="font-size:.875rem;color:var(--color-text-muted)">
          or click to browse
        </p>
      {/if}
    </div>

    <input
      type="file"
      accept=".pdf"
      style="display:none"
      bind:this={fileInput}
      onchange={onFileChange}
    />

    <button
      class="btn-secondary"
      style="width:100%;padding:.75rem"
      onclick={() => fileInput.click()}
      disabled={uploading}
    >
      {profile?.cv_text ? "Replace CV" : "Upload CV"}
    </button>
  </div>

  <!-- Logout -->
  <div class="card">
    <button
      class="btn-danger"
      style="width:100%;padding:.85rem"
      onclick={handleLogout}
    >
      Logout
    </button>
  </div>
</div>
