# JOBAGENT 🚀

> **Autonomous AI-powered job hunting, resume optimization, and application engine.**

JOBAGENT is a production-grade multi-agent AI system that automates your entire job search pipeline — from profile analysis and resume generation to job scraping, ATS scoring, cover letter writing, and auto-apply.

---

## Architecture

Built on:
- **FastAPI** + **LangGraph** for agent orchestration
- **Next.js 14** (App Router) for the frontend dashboard
- **SQLite** (dev) / **PostgreSQL** (prod) for persistence
- **WebSockets** for real-time agent activity feeds

### Agent Pipeline

```
Profile Agent → Resume Agent → ATS Agent
                              ↓
                       Job Hunter Agent → Ranking Agent
                                          ↓
                                   Cover Letter Agent → Auto Apply Agent
                                                         ↓
                                                  Tracker Agent → Notifier Agent
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)

### 1. Clone & Setup

```bash
git clone <repo>
cd jobagent
cp .env.example .env
```

### 2. Backend

```bash
cd apps/api
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd apps/web
npm install
npm run dev
```

### 4. Docker (All-in-One)

```bash
docker-compose up --build
```

---

## Project Structure

```
jobagent/
├── apps/
│   ├── api/          # FastAPI backend + LangGraph agents
│   └── web/          # Next.js 14 frontend dashboard
├── packages/
│   └── types/        # Shared TypeScript types
├── docs/             # Architecture & demo scripts
├── docker-compose.yml
└── .env.example
```

---

## Key Features

| Feature | Description |
|---|---|
| 🤖 Multi-Agent Pipeline | 9 specialized AI agents orchestrated via LangGraph |
| 📄 ATS Resume Builder | Keyword-optimized resume generation with score feedback |
| 🔍 Job Hunter | Scrapes LinkedIn, Indeed, Naukri, Internshala, Glassdoor |
| 🎯 Smart Ranking | Embeddings-based cosine similarity job matching |
| ✉️ Cover Letter AI | Personalized cover letters per job application |
| ⚡ Real-Time Feed | WebSocket agent activity log on dashboard |
| 📊 Application Tracker | Full pipeline from apply → interview → offer |

---

## License

MIT
