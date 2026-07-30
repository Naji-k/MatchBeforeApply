# MatchBeforeApply 🎯

**An AI-powered job application assistant** — upload your CV once, paste any job description, and get an instant match score with actionable ATS tips. Every analysis is automatically saved as an application card so you can track your job hunt from first look to final offer.

Built as a full-stack showcase of **multi-agent AI orchestration** (Google ADK + Gemini), an async **FastAPI** backend, and a modern **SvelteKit (Svelte 5)** frontend.

---

## ✨ Features

- **📄 One-time CV upload** — upload your CV as a PDF; the text is extracted (`pdfplumber`) and stored in your profile for reuse across all analyses.
- **🔗 Analyze any job description** — paste a JD as raw text *or* just a URL; the app scrapes and parses the posting automatically.
- **🤖 AI match scoring** — a pipeline of four specialized AI agents compares your CV against the JD and produces an overall match score, a skills breakdown, matched/missing skills, and a summary.
- **✅ ATS optimization tips** — concrete, JD-specific suggestions to get your CV past Applicant Tracking Systems.
- **🗂️ Application tracking board** — every analysis becomes an application card on a Kanban board with statuses (`open`, `in progress`, `accepted`, `rejected`), filtering, and sorting.
- **💬 Comments & interview notes** — attach typed notes (general, company research, interview, Q&A) to each application.
- **🔐 Secure by default** — JWT authentication (argon2 password hashing) on all protected endpoints; per-user data isolation.

---

## 🧠 How the AI Agents Work

The core of the app is a **multi-agent pipeline** built with the [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) running on **Gemini 2.5 Flash**. Instead of one giant prompt, the work is split across four specialized agents orchestrated by a `SequentialAgent`. Each agent reads from and writes to a shared session **state**, so every step builds on the previous one:

```
SequentialAgent (root_agent — "cv_job_matcher")
  │
  ├── [1] JD Agent     — scrapes the job posting (scrape_url tool) or  parses pasted
  │                      text into structured data (title, company, required skills…)
  │                      → writes state["jd_data"]
  │
  ├── [2] CV Agent     — parses the user's stored CV text into structured data
  │                      (skills, experience, education…)
  │                      → reads state["cv_text"], writes state["cv_data"]
  │
  ├── [3] Match Agent  — compares CV vs. JD and scores the fit
  │                      (overall score, skills score, matched/missing skills, summary)
  │                      → reads cv_data + jd_data, writes state["match_result"]
  │
  └── [4] ATS Agent    — generates tailored ATS optimization tips for this exact JD
                         → reads cv_data + jd_data, writes state["ats_tips"]
```

**Why this design?**

- **Separation of concerns** — each agent has one narrow, well-defined job with its own focused prompt.
- **Tool use** — the JD Agent calls a custom `scrape_url` tool.
- **Shared state pipeline** — agents communicate through ADK session state (`jd_data`, `cv_data`, `match_result`, `ats_tips`), making data flow explicit and each stage independently testable.
- **Dev-friendly** — when `ENV=development`, `run_analysis()` returns a realistic mock payload instead of calling the live pipeline, so the full app can be developed with zero API cost.

---

## 🏗️ Architecture

| Layer | Tech |
|---|---|
| AI / Agents | Google ADK (`SequentialAgent`), Gemini 2.5 Flash, custom scraping tool |
| Backend | FastAPI, async SQLAlchemy + asyncpg, Alembic migrations, Pydantic v2 |
| Auth | JWT (`python-jose`) + argon2 (`passlib`) |
| Frontend | SvelteKit 2 (Svelte 5 runes), TypeScript, Tailwind CSS v4, Vite 8 |
| Database | PostgreSQL (users, profiles, applications, comments) |
| Tooling | Ruff, ESLint 9, Prettier, svelte-check, pre-commit hooks |
| Deployment | Multi-stage Dockerfile (Node build → Python runtime) fronted by Caddy |
| Reverse Proxy | Caddy (static frontend + reverse proxy to FastAPI, scanner blocking, security headers) |

---

## 🚀 Getting Started (Self-Hosted, Dockerized)

The whole stack — PostgreSQL, FastAPI backend, SvelteKit frontend, and Caddy — is containerized and runs with a single command. No local Python/Node setup required to run the app.

### Prerequisites

- Docker + Docker Compose
- A Google AI (Gemini) API key — only needed to run the live agent pipeline (`ENV=production`); without it the app runs fine using mocked analysis results

### 1. Configure environment

```bash
cp backend/.env.example backend/.env
```

Fill in `backend/.env` (`GOOGLE_API_KEY`, `SECRET_KEY`, etc.) — see [Environment](#-environment) below for details.

### 2. Build & start

```bash
./install.sh up
```

This builds the app image from the `Dockerfile` (multi-stage: SvelteKit build → Python runtime + Caddy) and starts it alongside PostgreSQL via `docker-compose.yml`. On boot, `entrypoint.sh` runs Alembic migrations, starts FastAPI, waits for it to be healthy, then starts Caddy — serving everything on one port:

```
http://localhost:8080
```

### Managing the stack

`install.sh` wraps Docker Compose for day-to-day self-hosting:

```bash
./install.sh help       # show the command menu
```

---

## 🔧 Environment

All configuration lives in `backend/.env` (see `backend/.env.example`):
you can fill only required variables (`GOOGLE_API_KEY`, `MODEL`, `DATABASE_URL`, `SECRET_KEY`) and leave optional ones blank. The frontend receives its config via the `/config` endpoint.

---

## 📡 API Overview

```
POST /api/auth/register                  Create account
POST /api/auth/login                     Get JWT token
GET  /api/auth/me                        Current user

GET  /api/profile                        Get/create profile (cv_text)
PUT  /api/profile                        Update CV text
POST /api/profile/upload-cv              Upload PDF → extract & store text

GET    /api/applications                 List my applications
POST   /api/applications                 Create (+ optional instant analysis)
GET    /api/applications/{id}            Get one
PATCH  /api/applications/{id}            Update status / cover letter
DELETE /api/applications/{id}            Delete (cascades comments)
POST   /api/applications/{id}/analyze    (Re-)run AI analysis
GET    /api/applications/{id}/comments   List comments
POST   /api/applications/{id}/comments   Add comment
DELETE /api/applications/{id}/comments/{cid}  Delete comment
```

All `/api/profile` and `/api/applications/*` routes require a Bearer token. Interactive docs at `http://localhost:8000/docs`.

---

## 📁 Project Structure

```
job_board/
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── agents/                 # 🤖 Google ADK agents (orchestrator + 4 sub-agents)
│   ├── api/routes/             # auth, profile, applications endpoints
│   ├── services/               # business logic + analysis pipeline entry
│   ├── tools/                  # pdf_parser, web_scraper (ADK tool)
│   ├── db/                     # async engine + ORM models
│   ├── schemas/                # Pydantic request/response models
│   ├── core/                   # config, JWT security, auth middleware
│   └── alembic/                # DB migrations
├── publish/                    # SvelteKit frontend (Svelte 5 + Tailwind v4)
│   └── src/
│       ├── routes/             # login, profile, applications board/detail
│       └── lib/                # api client, stores, components, types
├── docker-compose.yml          # self-hosted stack: PostgreSQL + app
├── Dockerfile                  # multi-stage app image (frontend + backend + Caddy)
├── Caddyfile                   # reverse proxy + static serving + scanner blocking
├── scripts/                    # SvelteKit frontend (Svelte 5 + Tailwind v4)
│   └── entrypoint.sh           # migrations → uvicorn → caddy
└── install.sh                  # self-hosting helper (up/down/start/stop/rebuild/logs/status)
```

---

## 🛠️ Development Workflow

```bash
pre-commit run --all-files      # ruff + prettier + eslint + svelte-check
cd publish && npm run check     # TypeScript type-checking
cd publish && npm run lint      # ESLint
python -m alembic revision --autogenerate -m "description"   # new migration
```

---

## 🤝 Contributing & Feedback

This is a personal portfolio project, but feedback and contributions are very welcome!

- **Want to suggest an edit?** Feel free to fork the repo and open a pull request — even small fixes (docs, typos, refactors) are welcome.
- **General feedback?** Thoughts on the agent design, code structure, or UX are always great to hear — don't hesitate to reach out or start a discussion.
