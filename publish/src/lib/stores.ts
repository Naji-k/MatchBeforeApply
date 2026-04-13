import { writable } from "svelte/store";
import type {
  AuthState,
  ApplicationsState,
  CurrentAppState,
  Toast,
  User,
} from "./types.js";

export const authStore = writable<AuthState>({
  user: null,
  token: null,
  isAuthenticated: false,
  loading: false,
  error: null,
});

export function setToken(token: string | null): void {
  authStore.update((s) => ({ ...s, token, isAuthenticated: !!token }));
  if (typeof localStorage !== "undefined") {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }
}

export function setUser(user: User): void {
  authStore.update((s) => ({ ...s, user }));
}

export function logout(): void {
  setToken(null);
  authStore.update((s) => ({ ...s, user: null, isAuthenticated: false }));
}

export const applicationsStore = writable<ApplicationsState>({
  items: [],
  loading: false,
  error: null,
});

export const currentAppStore = writable<CurrentAppState>({
  app: null,
  comments: [],
  loading: false,
  error: null,
});

export const toastStore = writable<Toast | null>(null);

const DAILY_LIMIT = 3;

export const usageStore = writable<{ used: number; limit: number } | null>(
  null,
);

export function setUsage(used: number): void {
  usageStore.set({ used, limit: DAILY_LIMIT });
}

export function incrementUsage(): void {
  usageStore.update((s) =>
    s ? { ...s, used: Math.min(s.used + 1, DAILY_LIMIT) } : s,
  );
}

export function showToast(
  message: string,
  type: "success" | "info" | "error" = "error",
): void {
  toastStore.set({ message, type });
  if (type === "info") {
    setTimeout(() => toastStore.set(null), 6000);
  } else {
    setTimeout(() => toastStore.set(null), 4000);
  }
}
