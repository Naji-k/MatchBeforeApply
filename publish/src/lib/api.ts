import type {
  User,
  Application,
  ApplicationComment,
  Profile,
  CreateApplicationPayload,
  UpdateApplicationPayload,
  AddCommentPayload,
  ProfileUpdatePayload
} from './types.js';

const BASE = 'http://localhost:8000';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  json?: unknown;
  body?: BodyInit;
}

function getToken(): string | null {
  if (typeof localStorage === 'undefined') return null;
  return localStorage.getItem('token');
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = { ...options.headers };

  if (token) headers['Authorization'] = `Bearer ${token}`;

  let body: BodyInit | undefined = options.body;
  if (options.json !== undefined) {
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify(options.json);
  }

  const res = await fetch(`${BASE}${path}`, {
    method: options.method ?? 'GET',
    headers,
    body
  });

  if (!res.ok) {
    let message = `Error ${res.status}`;
    try {
      const err = (await res.json()) as { detail?: string };
      message = err.detail ?? message;
    } catch { /* ignore */ }
    throw new ApiError(message, res.status);
  }

  if (res.status === 204) return null as T;
  return res.json() as Promise<T>;
}

// ── Auth ──────────────────────────────────────────────
export async function login(email: string, password: string): Promise<{ access_token: string }> {
  const res = await fetch(`${BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password })
  });
  if (!res.ok) {
    const err = (await res.json().catch(() => ({}))) as { detail?: string };
    throw new ApiError(err.detail ?? 'Login failed', res.status);
  }
  return res.json() as Promise<{ access_token: string }>;
}

export function getMe(): Promise<User> {
  return request<User>('/api/auth/me');
}

// ── Profile ───────────────────────────────────────────
export function getProfile(): Promise<Profile> {
  return request<Profile>('/api/profile');
}

export function updateProfile(data: ProfileUpdatePayload): Promise<Profile> {
  return request<Profile>('/api/profile', { method: 'PUT', json: data });
}

export function uploadCV(file: File): Promise<Profile> {
  const form = new FormData();
  form.append('cv_file', file);
  return request<Profile>('/api/profile/upload-cv', { method: 'POST', body: form });
}

// ── Applications ──────────────────────────────────────
export function listApplications(): Promise<Application[]> {
  return request<Application[]>('/api/applications');
}

export function getApplication(id: number | string): Promise<Application> {
  return request<Application>(`/api/applications/${id}`);
}

export function createApplication(data: CreateApplicationPayload): Promise<Application> {
  return request<Application>('/api/applications', { method: 'POST', json: data });
}

export function updateApplication(id: number | string, data: UpdateApplicationPayload): Promise<Application> {
  return request<Application>(`/api/applications/${id}`, { method: 'PATCH', json: data });
}

export function deleteApplication(id: number | string): Promise<void> {
  return request<void>(`/api/applications/${id}`, { method: 'DELETE' });
}

export function analyzeApplication(id: number | string): Promise<Application> {
  return request<Application>(`/api/applications/${id}/analyze`, { method: 'POST' });
}

// ── Comments ──────────────────────────────────────────
export function getComments(appId: number | string): Promise<ApplicationComment[]> {
  return request<ApplicationComment[]>(`/api/applications/${appId}/comments`);
}

export function addComment(appId: number | string, data: AddCommentPayload): Promise<ApplicationComment> {
  return request<ApplicationComment>(`/api/applications/${appId}/comments`, { method: 'POST', json: data });
}

export function deleteComment(appId: number | string, commentId: number): Promise<void> {
  return request<void>(`/api/applications/${appId}/comments/${commentId}`, { method: 'DELETE' });
}
