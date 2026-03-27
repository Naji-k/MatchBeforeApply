<script lang="ts">
  import type { ApplicationComment } from '$lib/types.js';
  import CommentCard from './CommentCard.svelte';

  let { comments, ondelete }: {
    comments: ApplicationComment[];
    ondelete: (id: number) => void;
  } = $props();
</script>

{#if comments.length === 0}
  <p style="color:var(--color-text-muted);font-size:.9rem;padding:.5rem 0">No notes yet.</p>
{:else}
  <div class="timeline">
    {#each comments as comment (comment.id)}
      <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div style="flex:1;min-width:0">
          <CommentCard {comment} ondelete={() => ondelete(comment.id)} />
        </div>
      </div>
    {/each}
  </div>
{/if}

<style>
  .timeline {
    display: flex;
    flex-direction: column;
    gap: 0;
    position: relative;
  }
  .timeline::before {
    content: '';
    position: absolute;
    left: 7px;
    top: 12px;
    bottom: 12px;
    width: 2px;
    background: var(--color-border);
    border-radius: 2px;
  }
  .timeline-item {
    display: flex;
    align-items: flex-start;
    gap: .85rem;
    padding-bottom: .75rem;
    position: relative;
  }
  .timeline-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--color-surface);
    border: 2px solid var(--color-accent);
    flex-shrink: 0;
    margin-top: .85rem;
    position: relative;
    z-index: 1;
  }
</style>
