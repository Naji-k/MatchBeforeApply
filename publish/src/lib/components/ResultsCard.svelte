<script lang="ts">
  import type { MatchBreakdown } from '$lib/types.js';
  import { colorForScore } from '$lib/utils/helpers.js';

  let { matchBreakdown }: { matchBreakdown: MatchBreakdown } = $props();

  const overall = $derived(matchBreakdown?.overall_score ?? 0);
  const skillsScore = $derived(matchBreakdown?.skills_score ?? 0);
  const expScore = $derived(matchBreakdown?.experience_score ?? 0);
  const summary = $derived(matchBreakdown?.summary || '—');
  const ringColor = $derived(colorForScore(overall));
  const circumference = 314;
  const offset = $derived(circumference - (overall / 10) * circumference);
</script>

<div class="scores-grid">
  <!-- Ring card -->
  <div class="card" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.75rem">
    <div class="score-ring">
      <svg viewBox="0 0 120 120" style="transform:rotate(-90deg);width:100%;height:100%">
        <circle class="ring-bg" cx="60" cy="60" r="50" />
        <circle
          class="ring-fill"
          cx="60"
          cy="60"
          r="50"
          style="stroke:{ringColor};stroke-dashoffset:{offset}"
        />
      </svg>
      <div class="ring-label">
        <span style="font-size:1.6rem;font-weight:800">{overall}</span>
        <small style="font-size:.75rem;color:var(--color-text-muted);font-weight:400;margin-top:-.2rem">/10</small>
      </div>
    </div>
    <p style="font-size:.85rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em">Overall Match</p>
  </div>

  <!-- Bars card -->
  <div class="card" style="display:flex;flex-direction:column;justify-content:center;gap:1.25rem">
    <div>
      <div style="display:flex;justify-content:space-between;margin-bottom:.4rem;font-size:.9rem">
        <span style="color:var(--color-text-muted)">Skills</span>
        <strong>{skillsScore}/10</strong>
      </div>
      <div style="background:var(--color-surface-2);border-radius:999px;height:8px;overflow:hidden">
        <div style="height:100%;border-radius:999px;background:var(--color-accent);width:{skillsScore * 10}%;transition:width 1s ease"></div>
      </div>
    </div>
    <div>
      <div style="display:flex;justify-content:space-between;margin-bottom:.4rem;font-size:.9rem">
        <span style="color:var(--color-text-muted)">Experience</span>
        <strong>{expScore}/10</strong>
      </div>
      <div style="background:var(--color-surface-2);border-radius:999px;height:8px;overflow:hidden">
        <div style="height:100%;border-radius:999px;background:var(--color-accent);width:{expScore * 10}%;transition:width 1s ease"></div>
      </div>
    </div>
  </div>

  <!-- Summary card -->
  <div class="card summary-card">
    <p style="font-size:.85rem;font-weight:600;color:var(--color-text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem">Summary</p>
    <p style="color:var(--color-text-muted);font-size:.95rem;line-height:1.6">{summary}</p>
  </div>
</div>

<style>
  .scores-grid {
    display: grid;
    grid-template-columns: auto 1fr 1fr;
    gap: 1rem;
  }
  @media (max-width: 620px) {
    .scores-grid { grid-template-columns: 1fr; }
  }
  .score-ring {
    position: relative;
    width: 120px;
    height: 120px;
  }
  .ring-bg {
    fill: none;
    stroke: var(--color-surface-2);
    stroke-width: 10;
  }
  .ring-fill {
    fill: none;
    stroke-width: 10;
    stroke-linecap: round;
    stroke-dasharray: 314;
    transition: stroke-dashoffset 1s ease;
  }
  .ring-label {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .summary-card {
    display: flex;
    flex-direction: column;
  }
</style>
