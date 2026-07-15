<script lang="ts">
  import { submitFeedback } from "$lib/api.js";

  let { onclose }: { onclose: () => void } = $props();

  let message = $state("");
  let status = $state<"idle" | "loading" | "success" | "error">("idle");
  let errorMsg = $state("");

  async function handleSend() {
    if (!message.trim()) return;
    status = "loading";
    try {
      await submitFeedback(message.trim());
      status = "success";
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : "Something went wrong.";
      status = "error";
    }
  }
</script>

<div class="backdrop" onclick={onclose} role="presentation"></div>

<div
  class="card dialog"
  role="dialog"
  aria-modal="true"
  aria-label="Send feedback"
>
  <h2
    style="font-size:1.1rem;font-weight:700;margin-bottom:.25rem; padding:1rem"
  >
    Send Feedback
  </h2>

  {#if status === "success"}
    <p
      style="color:var(--color-success);font-size:.95rem;margin:.5rem 0 1rem; padding:1rem"
    >
      Thanks! Your feedback has been sent.
    </p>
    <div style="display:flex;justify-content:flex-end">
      <button
        class="btn-primary"
        style="font-size:.875rem;padding:1rem"
        onclick={onclose}
      >
        Close
      </button>
    </div>
  {:else}
    <textarea
      class="input-field"
      rows="5"
      style="resize:vertical; padding:1rem"
      placeholder="What's on your mind?"
      bind:value={message}
      disabled={status === "loading"}></textarea>

    {#if status === "error"}
      <p style="color:var(--color-danger);font-size:.85rem;margin-bottom:.5rem">
        {errorMsg}
      </p>
    {/if}

    <div style="display:flex;justify-content:flex-end;gap:.75rem ;padding:1rem">
      <button
        class="btn-secondary"
        style="font-size:.875rem;padding:.5rem 1.25rem"
        onclick={onclose}
        disabled={status === "loading"}
      >
        Cancel
      </button>
      <button
        class="btn-primary"
        style="font-size:.875rem;padding:.5rem 1.25rem"
        onclick={handleSend}
        disabled={status === "loading" || !message.trim()}
      >
        {status === "loading" ? "Sending…" : "Send"}
      </button>
    </div>
  {/if}
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 50;
  }
  .dialog {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 51;
    width: min(92vw, 440px);
    display: flex;
    flex-direction: column;
  }
</style>
