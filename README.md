# HireKit - AI Career Operating System

A local-first AI-powered career platform for iOS/Swift developers with visa sponsorship awareness.

## Architecture

```
frontend/          # React + TypeScript UI
  ├── src/
  │   ├── pages/   # Chat, Resume, Interview, Outreach, Jobs, Database, Profile
  │   ├── components/ # Sidebar, DataGrid, ChatWindow
  │   └── services/ # API client
  └── package.json

backend/           # FastAPI + Python agents
  ├── Agent/       # Multi-agent orchestrator
  │   ├── orchestrator/ # registry, coordinator, task_router
  │   ├── job_hunt_agent.py
  │   ├── resume_agent.py
  │   ├── interview_agent.py
  │   ├── outreach_agent.py
  │   └── profile_agent.py
  ├── api/         # FastAPI endpoints
  ├── database/    # SQLModel + SQLite
  ├── llm/         # Ollama client
  └── startup.py
```

## Features

- **Multi-agent orchestrator**: JobHunt, Resume, Interview, Outreach, Profile agents
- **Visa sponsorship detection**: Flags jobs offering work visa/relocation assistance
- **AI-powered scoring**: Uses Ollama LLM (llama3.1:8b)
- **Outreach automation**: Generates targeted messages for high-score jobs
- **Email notifications**: SMTP-based job alerts
- **Responsive UI**: Material UI with dark theme and futuristic design

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Run Job Hunt Agent
```bash
ollama serve
.venv/bin/python3 job_agent_v3.py
```

### Commands
- `python check_jobs.py --sponsored` - Show jobs with visa sponsorship
- `python check_jobs.py --stats` - Database statistics
- `python check_jobs.py --csv export.csv` - Export to CSV