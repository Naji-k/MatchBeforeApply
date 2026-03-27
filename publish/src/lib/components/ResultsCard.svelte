<script lang="ts">
  import type { MatchBreakdown } from "$lib/types.js";

  let { matchBreakdown }: { matchBreakdown: MatchBreakdown } = $props();

  const skillsScore = $derived(matchBreakdown?.skills_score ?? 0);
  const expScore = $derived(matchBreakdown?.experience_score ?? 0);
</script>

<div
  class="card"
  style="display:flex;flex-direction:column;justify-content:center;gap:1.25rem;padding:.75rem"
>
  <div>
    <div
      style="display:flex;justify-content:space-between;margin:.4rem;font-size:.9rem"
    >
      <span style="color:var(--color-text-muted)">Skills</span>
      <strong>{skillsScore}/10</strong>
    </div>
    <div
      style="background:var(--color-surface-2);border-radius:999px;height:8px;overflow:hidden"
    >
      <div
        style="height:100%;border-radius:999px;background:var(--color-accent);width:{skillsScore *
          10}%;transition:width 1s ease"
      ></div>
    </div>
  </div>
  <div>
    <div
      style="display:flex;justify-content:space-between;margin:.4rem;font-size:.9rem"
    >
      <span style="color:var(--color-text-muted)">Experience</span>
      <strong>{expScore}/10</strong>
    </div>
    <div
      style="background:var(--color-surface-2);border-radius:999px;height:8px;overflow:hidden"
    >
      <div
        style="height:100%;border-radius:999px;background:var(--color-accent);width:{expScore *
          10}%;transition:width 1s ease"
      ></div>
    </div>
  </div>
</div>
