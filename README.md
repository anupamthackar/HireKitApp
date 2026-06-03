# HireKit - AI Job Hunting Agent

Multi-source job aggregator for iOS/Swift developers with visa sponsorship awareness.

## Features

- Scrapes 8+ job sources: LinkedIn, Indeed, Bayt, Himalayas, RemoteOK, Arbeitnow, Jooble, Adzuna
- AI-powered scoring using Ollama LLM (llama3.1:8b)
- Automatic outreach message generation for high-score jobs
- **Visa sponsorship detection** - flags jobs offering work visa/relocation assistance
- Email notifications for new job results

## Quick Start

```bash
cd /Users/apple/Documents/HireKit
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Run with Ollama

```bash
# Start Ollama (if not running)
ollama serve

# Run the agent
python job_agent_v3.py
```

## Configuration

### Environment Variables

```bash
# Required for scoring/outreach
OLLAMA_URL=http://127.0.0.1:11434/api/chat

# Optional API keys for extra sources
JOOBLE_API_KEY=your_key
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key

# Email notifications (optional)
EMAIL_USER=you@gmail.com
EMAIL_PASS=your_app_password
EMAIL_TO=notify@address.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Commands

```bash
# Run job hunt
python job_agent_v3.py

# View saved jobs
python check_jobs.py                # Show 10 latest jobs
python check_jobs.py -l 50         # Show 50 jobs
python check_jobs.py --stats        # Show database statistics
python check_jobs.py --sponsored    # Show only jobs with sponsorship
python check_jobs.py --csv export.csv # Export to CSV
```

## Output

- `digest.md` - Latest results (Markdown)
- `runs/digest_YYYYMMDD_HHMMSS.md` - Timestamped archives
- `jobs.db` - SQLite database with all saved jobs

Each job shows:
- **Sponsorship Status**: ✅ Sponsorship or ⚠️ Self-Funded
- **Score**: 0-100 with H/M/L match rating
- **Auto-Outreach**: Generated message for high-score jobs