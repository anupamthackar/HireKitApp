# HireKit Quick Reference

## Branch Strategy
```
main        ← Production releases (protected)
develop     ← Integration branch
feature/*   ← Feature development
```

## Running Locally

### Start Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### Run Job Hunt Agent
```bash
ollama serve
cd /Users/apple/Documents/HireKit
.venv/bin/python3 job_agent_v3.py
```

## API Endpoints
- `GET /jobs` - List jobs (supports `?limit=50&match=H&sponsored=true`)
- `POST /chat` - Chat with AI
- `POST /agents/job-hunt` - Run job hunt agent

## Configuration Files
- `config/models.yaml` - LLM models
- `config/agents.yaml` - Agent settings
- `backend/database/engine.py` - Database config

## Docker
```bash
docker-compose up --build
```