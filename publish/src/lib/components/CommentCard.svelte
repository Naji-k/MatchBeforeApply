<script lang="ts">
  import type { ApplicationComment, CommentType } from '$lib/types.js';
  import { formatDate } from '$lib/utils/helpers.js';
  let { comment, ondelete }: { comment: ApplicationComment; ondelete: () => void } = $props();

  const TYPE_STYLE: Record<CommentType, string> = {
    general: 'color:#8892a4;border-color:#2e3250;background:transparent',
    company: 'color:#6c63ff;border-color:rgba(108,99,255,.4);background:rgba(108,99,255,.1)',
    interview: 'color:#4ade80;border-color:rgba(74,222,128,.4);background:rgba(74,222,128,.1)',
    qa: 'color:#f87171;border-color:rgba(248,113,113,.4);background:rgba(248,113,113,.1)'
  };
</script>

<div class="card comment-card" style="padding:1rem">
  <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.5rem">
    <span style="
      font-size:.75rem;font-weight:600;padding:.2rem .6rem;border-radius:999px;border:1px solid;
      text-transform:capitalize;{TYPE_STYLE[comment.type] || TYPE_STYLE.general}
    ">
      {comment.type}
    </span>
    <span style="font-size:.75rem;color:var(--color-text-muted);margin-left:auto">{formatDate(comment.created_at)}</span>
    <button
      class="delete-btn"
      onclick={ondelete}
      aria-label="Delete comment"
      title="Delete"
    >×</button>
  </div>

  {#if comment.question}
    <p style="font-size:.875rem;color:var(--color-text-muted);font-style:italic;margin-bottom:.35rem">
      Q: {comment.question}
    </p>
  {/if}
  <p style="font-size:.93rem;color:var(--color-text-primary);line-height:1.6">{comment.comment}</p>
</div>

<style>
  .delete-btn {
    background: none;
    border: none;
    color: var(--color-text-muted);
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0 .25rem;
    line-height: 1;
    opacity: 0;
    transition: color .2s, opacity .2s;
  }
  .comment-card:hover .delete-btn {
    opacity: 1;
  }
  .delete-btn:hover {
    color: var(--color-danger);
  }
</style>
