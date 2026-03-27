import type { ApplicationStatus } from '../types.js';

export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function scorePercent(score: number): number {
  return Math.round(score * 10);
}

export function colorForScore(score: number): string {
  if (score >= 8) return '#16A34A';
  if (score >= 6) return '#F59E0B';
  return '#DC2626';
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
    open:        'color:#64748B;border-color:#CBD5E1;background:#F8FAFC',
    in_progress: 'color:#4F46E5;border-color:#C7D2FE;background:#EEF2FF',
    accepted:    'color:#16A34A;border-color:#BBF7D0;background:#F0FDF4',
    rejected:    'color:#DC2626;border-color:#FECACA;background:#FEF2F2'
  };
  return map[status] ?? map.open;
}
