# CleanTalk

> **Prosty blog z komentarzami i moderacją AI**  
> A simple blog with AI-powered comment moderation, built on a microservices architecture.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-38B2AC?logo=tailwind-css)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docs.docker.com/compose/)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running with Docker Compose](#running-with-docker-compose)
  - [Running Locally (Dev Mode)](#running-locally-dev-mode)
- [Services & API Reference](#services--api-reference)
  - [Auth Service](#auth-service)
  - [Post Service](#post-service)
  - [Comment Service](#comment-service)
- [AI Moderation](#ai-moderation)
- [Frontend](#frontend)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**CleanTalk** is a minimal blogging platform that demonstrates a **microservices** approach for a real-world use case: a blog where every comment is automatically reviewed by an AI model before being shown to other users.

The AI moderator classifies each comment into one of three categories:

| Decision | Meaning |
|----------|---------|
| ✅ `ok` | Comment is clean – shown immediately |
| 🙈 `hide` | Comment is suspicious – hidden pending review |
| 🚫 `spam` | Comment is spam – removed automatically |

Optionally, the AI can also suggest a concise title for a new article draft.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                          React Frontend                          │
│              (Vite + React 18 + Tailwind CSS)                    │
└───────────┬──────────────────┬──────────────────┬───────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
  │   Auth Service  │ │   Post Service  │ │ Comment Service │
  │  (FastAPI 0.111)│ │ (FastAPI 0.111) │ │ (FastAPI 0.111) │
  │   Port: 8001    │ │   Port: 8002    │ │   Port: 8003    │
  └────────┬────────┘ └────────┬────────┘ └────────┬────────┘
           │                   │                   │
           ▼                   ▼                   ▼
      PostgreSQL          PostgreSQL           PostgreSQL
       (auth_db)           (post_db)         (comment_db)
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │   AI Moderator  │
                                          │  (Hugging Face  │
                                          │   Transformers  │
                                          │   / OpenAI API) │
                                          └─────────────────┘
```

Each service owns its own database, communicates over HTTP, and can be deployed, scaled, and updated independently.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Backend framework | FastAPI 0.111 |
| Database | PostgreSQL 16 (per service) |
| ORM | SQLAlchemy 2 + Alembic |
| Authentication | JWT (python-jose) |
| Password hashing | bcrypt (passlib) |
| AI moderation | Hugging Face `transformers` / OpenAI API |
| Frontend framework | React 18 |
| Frontend build tool | Vite 5 |
| CSS framework | Tailwind CSS 3 |
| Containerisation | Docker + Docker Compose |
| HTTP client (FE) | Axios |
| State management | React Query (TanStack Query v5) |

---

## Features

### Backend
- **User registration & login** with hashed passwords and JWT access tokens.
- **CRUD for blog posts** (create, list, read, update, delete).
- **CRUD for comments** attached to posts.
- **AI moderation pipeline** that runs automatically on every new comment:
  - Returns `ok`, `hide`, or `spam`.
  - Hides or deletes the comment based on the decision.
- *(Optional)* **AI title suggestion** – given a post body, returns a short title proposal.

### Frontend
- **Post list page** – paginated list of all published posts.
- **Post detail page** – full article with visible approved comments.
- **Add comment form** – live feedback when a comment is submitted (shows moderation result).
- **Auth pages** – register and login forms with JWT stored in `localStorage`.
- Responsive design with **Tailwind CSS**.

---

## Project Structure

```
CleanTalk/
├── docker-compose.yml          # Orchestrates all services
├── .env.example                # Sample environment variables
│
├── auth-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/                # DB migrations
│   └── app/
│       ├── main.py             # FastAPI app entry point
│       ├── models.py           # SQLAlchemy models (User)
│       ├── schemas.py          # Pydantic schemas
│       ├── crud.py             # DB operations
│       ├── auth.py             # JWT helpers
│       └── routers/
│           └── users.py        # /register, /login, /me
│
├── post-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/
│   └── app/
│       ├── main.py
│       ├── models.py           # Post model
│       ├── schemas.py
│       ├── crud.py
│       └── routers/
│           └── posts.py        # /posts CRUD
│
├── comment-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/
│   └── app/
│       ├── main.py
│       ├── models.py           # Comment model
│       ├── schemas.py
│       ├── crud.py
│       ├── moderation.py       # AI moderation logic
│       └── routers/
│           └── comments.py     # /comments CRUD + moderation
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.ts
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── api/                # Axios API clients
        ├── components/         # Reusable UI components
        └── pages/
            ├── PostListPage.tsx
            ├── PostDetailPage.tsx
            ├── LoginPage.tsx
            └── RegisterPage.tsx
```

---

## Getting Started

### Prerequisites

| Tool | Minimum version |
|------|----------------|
| Docker | 24 |
| Docker Compose | v2 (plugin) |
| Node.js *(local dev only)* | 20 LTS |
| Python *(local dev only)* | 3.12 |

### Running with Docker Compose

```bash
# 1. Clone the repository
git clone https://github.com/soso4ok/CleanTalk.git
cd CleanTalk

# 2. Copy and edit environment variables
cp .env.example .env
# → Open .env and set your SECRET_KEY, database passwords,
#   and (optionally) OPENAI_API_KEY or HF_MODEL_NAME

# 3. Start all services
docker compose up --build

# 4. Open the app
#    Frontend  → http://localhost:5173
#    Auth API  → http://localhost:8001/docs
#    Post API  → http://localhost:8002/docs
#    Comment API → http://localhost:8003/docs
```

> **First run:** database migrations are applied automatically by each service on startup.

### Running Locally (Dev Mode)

<details>
<summary>Auth Service</summary>

```bash
cd auth-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```
</details>

<details>
<summary>Post Service</summary>

```bash
cd post-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8002
```
</details>

<details>
<summary>Comment Service</summary>

```bash
cd comment-service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8003
```
</details>

<details>
<summary>Frontend</summary>

```bash
cd frontend
npm install
npm run dev          # starts Vite dev server on http://localhost:5173
```
</details>

---

## Services & API Reference

All services expose interactive **Swagger UI** at `/docs`.

### Auth Service

Base URL: `http://localhost:8001`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/register` | ❌ | Create a new user account |
| `POST` | `/login` | ❌ | Obtain JWT access token |
| `GET` | `/me` | ✅ Bearer | Get current user profile |

### Post Service

Base URL: `http://localhost:8002`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/posts` | ❌ | List all posts (paginated) |
| `POST` | `/posts` | ✅ Bearer | Create a new post |
| `GET` | `/posts/{id}` | ❌ | Get post by ID |
| `PUT` | `/posts/{id}` | ✅ Bearer | Update a post (owner only) |
| `DELETE` | `/posts/{id}` | ✅ Bearer | Delete a post (owner only) |
| `POST` | `/posts/suggest-title` | ✅ Bearer | *(Optional)* AI title suggestion |

### Comment Service

Base URL: `http://localhost:8003`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/comments?post_id={id}` | ❌ | List approved comments for a post |
| `POST` | `/comments` | ✅ Bearer | Submit a new comment (triggers AI moderation) |
| `DELETE` | `/comments/{id}` | ✅ Bearer | Delete own comment |

---

## AI Moderation

The AI moderation pipeline lives in `comment-service/app/moderation.py`.

### How It Works

1. When a comment is submitted, the **Comment Service** passes the comment text to the moderation module.
2. The module sends the text to the configured AI backend (see `AI_BACKEND` env var).
3. The response is mapped to one of three verdicts: `ok`, `hide`, or `spam`.
4. The verdict is stored alongside the comment and the appropriate action is taken:
   - `ok` → comment is publicly visible.
   - `hide` → comment is stored but not shown to other users until an admin reviews it.
   - `spam` → comment is rejected immediately (HTTP 422 returned to the author).

### Supported Backends

| `AI_BACKEND` value | Description |
|--------------------|-------------|
| `openai` | Uses OpenAI Chat Completions API (requires `OPENAI_API_KEY`) |
| `huggingface` | Uses a local Hugging Face `text-classification` model (set `HF_MODEL_NAME`) |
| `mock` | Deterministic mock – returns `ok` for everything. Useful for tests. |

### Example Moderation Prompt (OpenAI)

```text
You are a content moderator for a public blog.
Classify the following comment as one of: ok, hide, spam.
Respond with only the single word.

Comment: "<user comment text>"
```

---

## Frontend

The React frontend is built with **Vite 5** and styled with **Tailwind CSS**.

### Pages

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | `PostListPage` | Paginated list of blog posts |
| `/posts/:id` | `PostDetailPage` | Full post + approved comments + comment form |
| `/login` | `LoginPage` | Login form |
| `/register` | `RegisterPage` | Registration form |

### Key Libraries

- **React Router v6** – client-side routing
- **TanStack Query v5** – server-state caching and mutation handling
- **Axios** – HTTP requests to the three backend services
- **Tailwind CSS** – utility-first styling

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```dotenv
# ── Shared ──────────────────────────────────────────────────────────
SECRET_KEY=change-me-in-production        # JWT signing secret

# ── Auth Service DB ─────────────────────────────────────────────────
AUTH_DATABASE_URL=postgresql://postgres:password@auth-db:5432/auth_db

# ── Post Service DB ─────────────────────────────────────────────────
POST_DATABASE_URL=postgresql://postgres:password@post-db:5432/post_db

# ── Comment Service DB ──────────────────────────────────────────────
COMMENT_DATABASE_URL=postgresql://postgres:password@comment-db:5432/comment_db

# ── AI Moderation ───────────────────────────────────────────────────
AI_BACKEND=mock                           # openai | huggingface | mock
OPENAI_API_KEY=sk-...                     # Required when AI_BACKEND=openai
HF_MODEL_NAME=martin-ha/toxic-comment-model  # Required when AI_BACKEND=huggingface
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -m "feat: add my feature"`.
4. Push to your fork: `git push origin feature/my-feature`.
5. Open a Pull Request and describe what you changed and why.

Please follow the existing code style (PEP 8 for Python, ESLint for TypeScript/React).

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
