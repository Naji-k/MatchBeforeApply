<script lang="ts">
  import { appConfigStore } from "$lib/stores.js";
  import * as api from "$lib/api.js";
  import FeedbackModal from "$lib/components/FeedbackModal.svelte";
  import type { FaqMessage } from "$lib/types.js";

  const MAX_QUESTION_LENGTH = 500;

  let open = $state(false);
  let question = $state("");
  let pending = $state(false);
  let messages = $state<FaqMessage[]>([]);
  let logEl = $state<HTMLDivElement | null>(null);
  let feedbackOpen = $state(false);

  const canSend = $derived(question.trim().length > 0 && !pending);

  function scrollToBottom() {
    requestAnimationFrame(() => {
      if (logEl) logEl.scrollTop = logEl.scrollHeight;
    });
  }

  async function send() {
    if (!canSend) return;

    const asked = question.trim();
    question = "";
    messages = [...messages, { role: "user", content: asked }];
    pending = true;
    scrollToBottom();

    try {
      const result = await api.askFaq(asked);
      messages = [
        ...messages,
        {
          role: "assistant",
          content: result.answer,
          grounded: result.grounded,
        },
      ];
    } catch (error) {
      const content =
        error instanceof api.ApiError && error.status === 429
          ? "That's a lot of questions — give it a minute and try again."
          : "Something went wrong reaching the assistant. Please try again.";
      messages = [...messages, { role: "assistant", content, failed: true }];
    } finally {
      pending = false;
      scrollToBottom();
    }
  }

  function onKeydown(event: KeyboardEvent) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      send();
    }
  }
</script>

{#if $appConfigStore.ENABLE_FAQ_CHAT}
  {#if open}
    <div class="faq-panel">
      <div class="faq-header">
        <span>Ask about this app (BETA)</span>
        <button
          class="faq-close"
          onclick={() => (open = false)}
          aria-label="Close chat">×</button
        >
      </div>

      <div class="faq-log" bind:this={logEl}>
        {#if messages.length === 0}
          <p class="faq-hint">
            Hello! I'm a virtual assistant. Ask me questions about this app, and
            I'll do my best to answer them.
          </p>
        {/if}

        <!-- Keyed by index: the log is append-only, so entries never reorder. -->
        {#each messages as message, i (i)}
          <div
            class="faq-msg {message.role === 'user'
              ? 'faq-msg-user'
              : ''} {message.failed ? 'faq-msg-failed' : ''}"
          >
            {message.content}
          </div>
          {#if message.grounded === false}
            <button
              class="btn-primary"
              style="align-self:flex-start;font-size:.8125rem;padding:.35rem .75rem"
              onclick={() => (feedbackOpen = true)}
            >
              Feedback
            </button>
          {/if}
        {/each}

        {#if pending}
          <div class="faq-typing" aria-label="Thinking">
            <span></span><span></span><span></span>
          </div>
        {/if}
      </div>

      <div class="faq-composer">
        <input
          class="faq-input"
          bind:value={question}
          onkeydown={onKeydown}
          maxlength={MAX_QUESTION_LENGTH}
          placeholder="Ask a question…"
          aria-label="Your question"
        />
        <button
          class="faq-send"
          onclick={send}
          disabled={!canSend}
          aria-label="Send question">↑</button
        >
      </div>
    </div>
  {/if}

  <button
    class="faq-bubble"
    onclick={() => (open = !open)}
    aria-label={open ? "Close FAQ chat" : "Open FAQ chat"}
  >
    {open ? "×" : "?"}
  </button>

  {#if feedbackOpen}
    <FeedbackModal onclose={() => (feedbackOpen = false)} />
  {/if}
{/if}
