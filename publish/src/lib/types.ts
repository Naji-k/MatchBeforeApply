export type ApplicationStatus =
  | "open"
  | "in_progress"
  | "accepted"
  | "rejected";
export type CommentType = "general" | "company" | "interview" | "qa";

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_email_verified: boolean;
}

export interface Profile {
  id: number;
  user_id: number;
  cv_text?: string;
  updated_at: string;
  daily_analyses_used: number;
}

export interface MatchBreakdown {
  overall_score: number;
  skills_score: number;
  experience_score?: number;
  matched_skills: string[];
  missing_skills: string[];
  summary: string;
}

export interface AtsTips {
  tips: string[];
}

export interface JdData {
  job_title?: string;
  company?: string;
  required_skills?: string[];
  [key: string]: unknown;
}

export interface Application {
  id: number;
  user_id: number;
  jd_source: string;
  jd_type: "text" | "url";
  jd_text?: string;
  jd_url?: string;
  match_score?: number;
  match_breakdown?: MatchBreakdown;
  ats_tips?: AtsTips;
  jd_data?: JdData;
  cover_letter?: string;
  status: ApplicationStatus;
  created_at: string;
  updated_at: string;
}

export interface ApplicationComment {
  id: number;
  application_id: number;
  user_id: number;
  type: CommentType;
  question?: string;
  comment: string;
  created_at: string;
}

// Store state shapes
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export interface ApplicationsState {
  items: Application[];
  loading: boolean;
  error: string | null;
}

export interface CurrentAppState {
  app: Application | null;
  comments: ApplicationComment[];
  loading: boolean;
  error: string | null;
}

export interface Toast {
  message: string;
  type: "success" | "error" | "info";
}

// API request payloads
export interface CreateApplicationPayload {
  jd_source: string;
  jd_type: "text" | "url";
  jd_url?: string;
  run_analysis: boolean;
}

export interface UpdateApplicationPayload {
  status?: ApplicationStatus;
  cover_letter?: string;
  jd_url?: string;
}

export interface AddCommentPayload {
  type: CommentType;
  question: string | null;
  comment: string;
}

export interface ProfileUpdatePayload {
  cv_text?: string;
}

export const STATUS_OPTIONS: { status: ApplicationStatus; label: string }[] = [
  { status: "open", label: "Open/Prepare to Apply" },
  { status: "in_progress", label: "Applied" },
  { status: "accepted", label: "In Progress" },
  { status: "rejected", label: "Rejected/Closed" },
];
