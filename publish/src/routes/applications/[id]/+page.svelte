<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import { onMount } from "svelte";
  import type { ApplicationStatus, CommentType } from "$lib/types.js";
  import { currentAppStore, incrementUsage, showToast } from "$lib/stores.js";
  import * as api from "$lib/api.js";
  import ResultsCard from "$lib/components/ResultsCard.svelte";
  import SkillChips from "$lib/components/SkillChips.svelte";
  import CommentTimeline from "$lib/components/CommentTimeline.svelte";
  import LoadingSteps from "$lib/components/LoadingSteps.svelte";
  import Modal from "$lib/components/Modal.svelte";
  import ScoreIndicator from "$lib/components/ScoreIndicator.svelte";
  import { formatDate } from "$lib/utils/helpers.js";
  import { STATUS_OPTIONS } from "$lib/types.js";
  import { authStore } from "$lib/stores.js";

  const COMMENT_TYPES: CommentType[] = [
    "general",
    "company",
    "interview",
    "qa",
  ];

  let coverLetter = $state("");
  let status = $state<ApplicationStatus>("open");
  let savingCover = $state(false);
  let savingStatus = $state(false);
  let reanalyzing = $state(false);
  let showDeleteModal = $state(false);
  let commentFilter = $state<"all" | CommentType>("all");
  let newComment = $state<{
    type: CommentType;
    question: string;
    comment: string;
  }>({ type: "general", question: "", comment: "" });
  let submittingComment = $state(false);

  onMount(async () => {
    const id = page.params.id!;
    currentAppStore.update((s) => ({ ...s, loading: true, error: null }));
    try {
      const [app, comments] = await Promise.all([
        api.getApplication(id),
        api.getComments(id),
      ]);
      currentAppStore.set({ app, comments, loading: false, error: null });
      coverLetter = app.cover_letter ?? "";
      status = app.status ?? "open";
    } catch (err) {
      currentAppStore.update((s) => ({
        ...s,
        loading: false,
        error: (err as Error).message,
      }));
    }
  });

  async function saveCoverLetter(): Promise<void> {
    savingCover = true;
    try {
      await api.updateApplication(page.params.id!, {
        cover_letter: coverLetter,
      });
      showToast("Cover letter saved", "success");
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      savingCover = false;
    }
  }

  async function saveStatus(): Promise<void> {
    savingStatus = true;
    try {
      await api.updateApplication(page.params.id!, { status });
      currentAppStore.update((s) => ({
        ...s,
        app: s.app ? { ...s.app, status } : null,
      }));
      showToast("Status updated", "success");
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      savingStatus = false;
    }
  }

  async function reanalyze(): Promise<void> {
    if ($authStore.user?.id == import.meta.env.VITE_DEMO_USER) {
      showToast(
        "You're using the demo account 👀 Results are mock data — log in to see real analysis.",
        "info",
      );
    }
    reanalyzing = true;
    try {
      const updated = await api.analyzeApplication(page.params.id!);
      currentAppStore.update((s) => ({ ...s, app: updated }));
      showToast("Analysis complete!", "success");
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      reanalyzing = false;
      incrementUsage();
    }
  }

  async function deleteApp(): Promise<void> {
    try {
      await api.deleteApplication(page.params.id!);
      goto("/applications");
    } catch (err) {
      showToast((err as Error).message);
    }
  }

  async function addComment(): Promise<void> {
    if (!newComment.comment.trim()) return;
    submittingComment = true;
    try {
      const comment = await api.addComment(page.params.id!, {
        type: newComment.type,
        question: newComment.question || null,
        comment: newComment.comment,
      });
      currentAppStore.update((s) => ({
        ...s,
        comments: [...s.comments, comment],
      }));
      newComment = { type: "general", question: "", comment: "" };
    } catch (err) {
      showToast((err as Error).message);
    } finally {
      submittingComment = false;
    }
  }

  async function removeComment(commentId: number): Promise<void> {
    try {
      await api.deleteComment(page.params.id!, commentId);
      currentAppStore.update((s) => ({
        ...s,
        comments: s.comments.filter((c) => c.id !== commentId),
      }));
    } catch (err) {
      showToast((err as Error).message);
    }
  }

  const filteredComments = $derived(
    commentFilter === "all"
      ? $currentAppStore.comments
      : $currentAppStore.comments.filter((c) => c.type === commentFilter),
  );
</script>

<svelte:head>
  <title
    >{$currentAppStore.app?.jd_data?.job_title || "Application"} — AIJobBoard</title
  >
</svelte:head>

{#if $currentAppStore.loading}
  <div style="text-align:center;padding:5rem 0;color:var(--color-text-muted)">
    Loading…
  </div>
{:else if $currentAppStore.error}
  <div style="max-width:680px;margin:2rem auto;padding:0 1rem">
    <div
      class="card"
      style="text-align:center;color:var(--color-danger);padding:3rem"
    >
      {$currentAppStore.error}
    </div>
  </div>
{:else if $currentAppStore.app}
  {@const app = $currentAppStore.app}

  {#if reanalyzing}
    <LoadingSteps running={true} />
  {:else}
    <div
      style="max-width:900px;margin:0 auto;padding:2rem 1rem;display:flex;flex-direction:column;gap:1.5rem"
    >
      <!-- Header -->
      <div
        style="display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;flex-wrap:wrap"
      >
        <div>
          <a
            href="/applications"
            style="color:var(--color-text-muted);font-size:.875rem;text-decoration:none"
            >← Board</a
          >
          <h1 style="font-size:1.6rem;font-weight:700;margin-top:.25rem">
            {app.jd_data?.job_title || "Application"}
          </h1>
          <p style="color:var(--color-text-muted);font-size:.9rem">
            {app.jd_data?.company || "—"} · {formatDate(app.created_at)}
          </p>
        </div>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap">
          <button
            class="btn-secondary"
            style="font-size:.875rem;padding:.5rem 1rem"
            onclick={reanalyze}
          >
            Re-analyze
          </button>
          <button
            class="btn-danger"
            style="font-size:.875rem;padding:.5rem 1rem"
            onclick={() => (showDeleteModal = true)}
          >
            Delete
          </button>
        </div>
      </div>

      <!-- Status -->
      <div
        class="card"
        style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;padding:1rem 1.5rem"
      >
        <label
          for="status-select"
          style="font-size:.8rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em"
        >
          Status
        </label>
        <select
          id="status-select"
          class="input-field"
          style="width:auto;padding:.4rem .75rem;font-size:.875rem"
          bind:value={status}
        >
          {#each STATUS_OPTIONS as opt}
            <option value={opt.status}>{opt.label}</option>
          {/each}
        </select>
        <button
          class="btn-secondary"
          style="font-size:.875rem;padding:.4rem 1rem"
          onclick={saveStatus}
          disabled={savingStatus}
        >
          {savingStatus ? "Saving…" : "Save"}
        </button>
      </div>

      {#if app.match_breakdown}
        <div
          class="card"
          style="display:flex;align-items:center;justify-content:center;gap:2.5rem;flex-wrap:wrap;padding:1rem"
        >
          <ScoreIndicator score={app.match_breakdown.overall_score} size="lg" />
          <div>
            <p
              style="font-size:.8rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.4rem"
            >
              Overall Match
            </p>
            <p
              style="font-size:.95rem;color:var(--color-text-muted);line-height:1.8"
            >
              {app.match_breakdown.summary || "—"}
            </p>
          </div>
        </div>

        <!-- Breakdown bars + Skills -->
        <ResultsCard matchBreakdown={app.match_breakdown} />
        <SkillChips
          matched={app.match_breakdown.matched_skills || []}
          missing={app.match_breakdown.missing_skills || []}
        />
      {:else}
        <div class="card" style="text-align:center;padding:3rem">
          <p style="color:var(--color-text-muted);margin-bottom:1.25rem">
            No analysis yet.
          </p>
          <button
            class="btn-primary"
            style="padding:.75rem 1.5rem"
            onclick={reanalyze}>Run Analysis</button
          >
        </div>
      {/if}

      <!-- Cover Letter -->
      <div
        class="card"
        style="display:flex;flex-direction:column;gap:1rem;padding:1rem 1.5rem"
      >
        <h3 style="font-size:.95rem;font-weight:600;">Cover Letter</h3>
        <textarea
          class="input-field"
          rows="6"
          style="resize:vertical"
          placeholder="Write your cover letter here…"
          bind:value={coverLetter}
        ></textarea>
        <div style="display:flex;justify-content:flex-end">
          <button
            class="btn-secondary"
            style="font-size:.875rem;padding:.5rem 1.25rem"
            onclick={saveCoverLetter}
            disabled={savingCover}
          >
            {savingCover ? "Saving…" : "Save Cover Letter"}
          </button>
        </div>
      </div>

      <!-- Comments -->
      <div
        class="card"
        style="display:flex;flex-direction:column;gap:1.25rem;padding:1rem 1.5rem"
      >
        <div
          style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.75rem"
        >
          <h3 style="font-size:.95rem;font-weight:600;">
            Notes ({$currentAppStore.comments.length})
          </h3>
          <!-- Type filter pills -->
          <div style="display:flex;gap:.5rem;flex-wrap:wrap;">
            {#each ["all", ...COMMENT_TYPES] as type}
              <button
                style="
                  padding:.25rem .75rem;border-radius:999px;font-size:.75rem;font-weight:500;
                  border:1px solid;cursor:pointer;transition:all .2s;
                  {commentFilter === type
                  ? 'background:var(--color-accent);border-color:var(--color-accent);color:#fff'
                  : 'background:transparent;border-color:var(--color-border);color:var(--color-text-muted)'}
                "
                onclick={() => (commentFilter = type as "all" | CommentType)}
              >
                {type}
              </button>
            {/each}
          </div>
        </div>

        <CommentTimeline comments={filteredComments} ondelete={removeComment} />

        <!-- Add Comment -->
        <div
          style="border-top:1px solid var(--color-border);padding-top:1.25rem;display:flex;flex-direction:column;gap:1rem"
        >
          <p
            style="font-size:.8rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;"
          >
            Add Note
          </p>
          <div style="display:flex;gap:.5rem;flex-wrap:wrap;">
            {#each COMMENT_TYPES as type}
              <button
                type="button"
                style="
                  padding:.35rem .9rem;border-radius:8px;font-size:.8rem;font-weight:500;
                  border:1px solid;cursor:pointer;transition:all .2s;
                  {newComment.type === type
                  ? 'background:var(--color-accent);border-color:var(--color-accent);color:#fff'
                  : 'background:transparent;border-color:var(--color-border);color:var(--color-text-muted)'}
                "
                onclick={() => (newComment.type = type)}
              >
                {type}
              </button>
            {/each}
          </div>
          <input
            type="text"
            class="input-field"
            style="font-size:.9rem;"
            placeholder="Question (optional)"
            bind:value={newComment.question}
          />
          <textarea
            class="input-field"
            rows="3"
            style="resize:vertical;font-size:.9rem"
            placeholder="Your note…"
            bind:value={newComment.comment}
          ></textarea>
          <div style="display:flex;justify-content:flex-end">
            <button
              class="btn-primary"
              style="font-size:.875rem;padding:.5rem 1.25rem"
              onclick={addComment}
              disabled={submittingComment || !newComment.comment.trim()}
            >
              {submittingComment ? "Adding…" : "Add Note"}
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <Modal
    open={showDeleteModal}
    title="Delete Application"
    onclose={() => (showDeleteModal = false)}
    onconfirm={deleteApp}
  >
    Are you sure you want to delete this application? This action cannot be
    undone.
  </Modal>
{/if}
