import type { ApplicationStatus } from '../types.js';

export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function colorForScore(score: number): string {
  if (score >= 7) return '#4ade80';
  if (score >= 4) return '#facc15';
  return '#f87171';
}

export function statusLabel(status: ApplicationStatus): string {
  const labels: Record<ApplicationStatus, string> = {
    open: 'Open',
    in_progress: 'In Progress',
    accepted: 'Accepted',
    rejected: 'Rejected'
  };
  return labels[status] ?? status;
}

export function statusClasses(status: ApplicationStatus): string {
  const map: Record<ApplicationStatus, string> = {
    open: 'color: #8892a4; border-color: #2e3250;',
    in_progress: 'color: #6c63ff; border-color: rgba(108,99,255,.4); background: rgba(108,99,255,.1);',
    accepted: 'color: #4ade80; border-color: rgba(74,222,128,.4); background: rgba(74,222,128,.1);',
    rejected: 'color: #f87171; border-color: rgba(248,113,113,.4); background: rgba(248,113,113,.1);'
  };
  return map[status] ?? map.open;
}
