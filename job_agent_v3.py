#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║   AI Job Finder Agent  v5 (Multi-Source Global)              ║
║   Target: High-Profile iOS/Swift Roles (Anupam Thackar)      ║
║   Sources: LinkedIn, Indeed, Bayt, Himalayas, RemoteOK,      ║
║            Arbeitnow, Jooble, Adzuna                          ║
║   Countries: UAE(*), Qatar, India, Europe, Global Remote      ║
╚══════════════════════════════════════════════════════════════╝

Install:
    pip install -r requirements.txt
"""

import json
import os
import re
import smtplib
import sqlite3
import time
from datetime import datetime, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
DB_FILE     = BASE_DIR / "jobs.db"
DIGEST_FILE = BASE_DIR / "digest.md"
RUNS_DIR    = BASE_DIR / "runs"
RESUME_FILE = BASE_DIR / "Anupam_Thackar_Resume.md"
OLLAMA_URL  = "http://127.0.0.1:11434/api/chat"

RESUME_TEXT = ""
if RESUME_FILE.exists():
    with open(RESUME_FILE, "r", encoding="utf-8") as f:
        RESUME_TEXT = f.read()


# ── Country Priorities ────────────────────────────────────────────────────────
COUNTRY_PRIORITY = {
    "united arab emirates": 1, "uae": 1, "dubai": 1, "abu dhabi": 1,
    "qatar": 2, "doha": 2,
    "india": 3, "bangalore": 3, "bengaluru": 3, "mumbai": 3, "pune": 3,
    "gurugram": 3, "haryana": 3, "maharashtra": 3, "karnataka": 3,
    "tamil nadu": 3, "chennai": 3,
    "germany": 4, "berlin": 4, "munich": 4, "netherlands": 4, "amsterdam": 4,
    "uk": 4, "united kingdom": 4, "london": 4, "europe": 4,
    "remote": 5, "worldwide": 5, "anywhere": 5,
}

COUNTRY_NAMES = {
    1: "🇦🇪 UAE", 2: "🇶🇦 Qatar", 3: "🇮🇳 India",
    4: "🇪🇺 Europe", 5: "🌍 Remote/Global"
}

# ── Strict Profile & Constraints ─────────────────────────────────────────────
ANUPAM_PROFILE = """
Name: Anupam Thackar
Role: Senior iOS Developer (2+ yrs)
Skills: Swift 6, SwiftUI, MVVM, Clean Architecture, CoreML, RAG, SSE, SPM Libraries.
Targets (by priority):
1. UAE (Dubai/Abu Dhabi): AED 12K-22K/mo [TOP PRIORITY]
2. Qatar (Doha): QAR 10K-18K/mo
3. India (Bangalore/Pune/Mumbai): ₹14-30 LPA
4. Europe (Germany/Netherlands/UK): €50K-80K/yr
5. Remote (USD/EUR): $50K-90K/yr

STRICT RULES:
 ✅ MUST have iOS/Swift/Mobile as PRIMARY requirement in TITLE.
 ✅ Mid/Senior level preferred.
 ❌ NO: Android-only, Flutter, React Native, Junior, Intern.
"""

KEYWORD_ROTATION = {
    0: "iOS Developer SwiftUI AI",
    1: "Swift Engineer CoreML on-device",
    2: "Senior iOS SwiftUI MVVM product",
    3: "Mobile AI Engineer iOS Foundation Models",
    4: "iOS Developer RAG AI integration",
    5: "Swift Package Manager SDK iOS",
    6: "iOS Engineer AI startup remote",
}

def today_keyword() -> str:
    return KEYWORD_ROTATION[date.today().weekday()]

# ── Scoring Logic ─────────────────────────────────────────────────────────────
SCORE_SYSTEM = """You are a strict recruiter for an Indian iOS developer seeking jobs abroad. 
Score 0 if job title does NOT contain "ios", "swift", or "mobile developer".
Score 0 for: Android-only, Flutter, React Native, Junior, Intern.
Score 85-100 (H) for: Senior iOS/Swift + matches salary + mentions AI/CoreML + visa sponsorship/ relocation.
Score 70-84 (M) for: iOS/Swift focused, sponsorship mentioned, mostly matches targets.
Score 60-69 (L) for: Good iOS/Swift match but no sponsorship info & requires work permit.
Score <60 (Reject): Weak match.
Output JSON only: {"score":0-100,"match":"H/M/L","reason":"brief reason"}"""

def ollama_chat(system: str, user: str, model: str) -> str:
    payload = {"model": model, "stream": False, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        return r.json()["message"]["content"].strip()
    except:
        return '{"score":0,"match":"L","reason":"LLM error"}'

def score_job(title: str, company: str, description, location: str, model: str) -> dict:
    title_lower = (title or "").lower()
    if not any(x in title_lower for x in ["ios", "swift", "swiftui", "mobile developer", "mobile engineer"]):
        return {"score": 0, "match": "L", "reason": "Title missing iOS/Swift/Mobile"}
    if any(x in title_lower for x in ["android only", "flutter", "react native", "junior", "intern", "entry level"]):
        return {"score": 0, "match": "L", "reason": "Excluded role type"}
    desc_str = str(description)[:2000] if description else ""
    user_msg = f"TITLE: {title}\nCOMPANY: {company}\nLOCATION: {location}\nDESC: {desc_str}"
    raw = ollama_chat(SCORE_SYSTEM, user_msg, model)
    match = re.search(r'\{.*?\}', raw, re.DOTALL)
    if match:
        try: return json.loads(match.group())
        except: pass
    return {"score": 0, "match": "L", "reason": "parse error"}

OUTREACH_SYSTEM = """You are Anupam, an extraordinary Senior iOS Developer from India.
Write a highly targeted, 3-sentence outreach message (DM/Email) to the hiring manager or CTO.
Tone: Professional, yet startup-casual and "builder-focused".
Highlight matching skills (ApplePlatformToolkit, Swift 6, CoreML, AI/SSE) from the resume.
If visa sponsorship is mentioned in the job, emphasize that you're interested in relocating.
If sponsorship is NOT mentioned, ask directly if visa sponsorship is available for Indian candidates.
Do NOT use placeholders like [Hiring Manager Name] or [Company Name]. Start with "Hi Team," or "Hi,".
Output ONLY the message text. No pleasantries outside the message."""

def generate_outreach(title: str, company: str, description: str, model: str) -> str:
    if not RESUME_TEXT:
        return "Please place Anupam_Thackar_Resume.md in the directory."
    desc_str = str(description)[:2000] if description else ""
    user_msg = f"JOB TITLE: {title}\nCOMPANY: {company}\nJOB DESCRIPTION:\n{desc_str}\n\nMY RESUME:\n{RESUME_TEXT}"
    return ollama_chat(OUTREACH_SYSTEM, user_msg, model)

# ── Database ──────────────────────────────────────────────────────────────────
def init_db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_FILE)
    con.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY, title TEXT, company TEXT, location TEXT, 
        source TEXT, url TEXT, salary TEXT, score INTEGER, match TEXT, 
        found_at TEXT, reason TEXT, outreach_msg TEXT, sponsorship INTEGER, sp_status TEXT
    )""")
    try: con.execute("ALTER TABLE jobs ADD COLUMN reason TEXT")
    except sqlite3.OperationalError: pass
    try: con.execute("ALTER TABLE jobs ADD COLUMN outreach_msg TEXT")
    except sqlite3.OperationalError: pass
    try: con.execute("ALTER TABLE jobs ADD COLUMN sponsorship INTEGER")
    except sqlite3.OperationalError: pass
    try: con.execute("ALTER TABLE jobs ADD COLUMN sp_status TEXT")
    except sqlite3.OperationalError: pass
    con.commit()
    return con

def save_job(con, j):
    con.execute("INSERT OR REPLACE INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                (j["id"], j["title"], j["company"], j["location"], j["source"], 
                 j["url"], j.get("salary",""), j["score"], j["match"], 
                 datetime.now().isoformat(), j.get("reason",""), j.get("outreach_msg",""),
                 1 if j.get("sponsorship", False) else 0, j.get("sp_status", "")))
    con.commit()

# ── Helper Functions ──────────────────────────────────────────────────────────
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

def is_ios_job(title: str) -> bool:
    t = (title or "").lower()
    return any(x in t for x in ["ios", "swift", "swiftui", "mobile developer", "mobile engineer", "mobile app"])

def has_excluded_keywords(title: str) -> bool:
    t = (title or "").lower()
    return any(x in t for x in ["android only", "flutter", "react native", "junior", "intern", "entry level"])

def get_country_priority(location: str) -> int:
    loc_lower = (location or "").lower()
    for country, priority in COUNTRY_PRIORITY.items():
        if country in loc_lower:
            return priority
    return 99

def get_country_group(priority: int) -> str:
    return COUNTRY_NAMES.get(priority, "❓ Other")

SPONSORSHIP_KEYWORDS = [
    "visa sponsorship", "work visa", "relocation assistance", "spouse visa",
    "housing allowance", "tax equalization", "international candidates", "visa support",
    "work permit", "relocation package", "immigration support", "visa provided"
]

def check_sponsorship(description: str) -> bool:
    """Check if job description mentions visa/work sponsorship for international candidates."""
    if not description:
        return False
    desc_lower = description.lower()
    return any(kw in desc_lower for kw in SPONSORSHIP_KEYWORDS)

def get_sponsorship_status(description_str: str) -> str:
    """Return sponsorship status indicator: '✅ Sponsorship' or '⚠️ Self-Funded'."""
    if check_sponsorship(description_str):
        return "✅ Sponsorship"
    return "⚠️ Self-Funded"

def send_email_notification(subject: str, body: str, to_email: str = None):
    """Send email notification about job results using SMTP."""
    from_email = os.environ.get("EMAIL_USER", "")
    email_pass = os.environ.get("EMAIL_PASS", "")
    to_email = to_email or os.environ.get("EMAIL_TO", "")
    
    if not from_email or not email_pass or not to_email:
        print("  ⚠ Email notification skipped (set EMAIL_USER, EMAIL_PASS, EMAIL_TO env vars)")
        return False
    
    try:
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        server = smtplib.SMTP(os.environ.get("SMTP_SERVER", "smtp.gmail.com"), 
                              int(os.environ.get("SMTP_PORT", "587")))
        server.starttls()
        server.login(from_email, email_pass)
        server.send_message(msg)
        server.quit()
        print(f"  ✅ Email notification sent to {to_email}")
        return True
    except Exception as e:
        print(f"  ⚠ Email failed: {e}")
        return False

def process_batch(con, batch, all_found, stats, model, check_sponsorship_flag=True):
    """Process a batch of jobs: score, filter, save."""
    for j in batch:
        source = j.get("source", "unknown")
        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
        scored = score_job(j["title"], j["company"], j["description"], j["location"], model)
        j.update(scored)
        stats["scored"] += 1
        if j["score"] >= 65:
            if j["score"] >= 85:
                print(f"    ✨ Generating outreach for: {j['title']} @ {j['company']}")
                j["outreach_msg"] = generate_outreach(j["title"], j["company"], j["description"], model)
            else:
                j["outreach_msg"] = ""
            j["priority"] = get_country_priority(j["location"])
            if check_sponsorship_flag:
                j["sponsorship"] = check_sponsorship(j.get("description", ""))
                j["sp_status"] = get_sponsorship_status(j.get("description", ""))
            save_job(con, j)
            all_found.append(j)
            stats["passed"] += 1
    """Process a batch of jobs: score, filter, save."""
    for j in batch:
        source = j.get("source", "unknown")
        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
        scored = score_job(j["title"], j["company"], j["description"], j["location"], model)
        j.update(scored)
        stats["scored"] += 1
        if j["score"] >= 65:
            if j["score"] >= 85:
                print(f"    ✨ Generating outreach for: {j['title']} @ {j['company']}")
                j["outreach_msg"] = generate_outreach(j["title"], j["company"], j["description"], model)
            else:
                j["outreach_msg"] = ""
            j["priority"] = get_country_priority(j["location"])
            if check_sponsorship_flag:
                j["sponsorship"] = check_sponsorship(j.get("description", ""))
                j["sp_status"] = get_sponsorship_status(j.get("description", ""))
            save_job(con, j)
            all_found.append(j)
            stats["passed"] += 1

# ── Source 1: JobSpy (LinkedIn, Indeed, Bayt) ────────────────────────────────
def scrape_jobspy(term, location, sites, country_indeed="usa", results=30, hours=168):
    try:
        from jobspy import scrape_jobs
        df = scrape_jobs(site_name=sites, search_term=term, location=location, 
                        country_indeed=country_indeed, results_wanted=results, hours_old=hours)
        if df is None or df.empty: return []
        jobs = []
        for _, row in df.iterrows():
            title = row.get("title") or ""
            if not is_ios_job(title): continue
            if has_excluded_keywords(title): continue
            jobs.append({
                "id": f"spy_{hash(str(row.get('id',''))+title)}",
                "title": title,
                "company": row.get("company") or "Unknown",
                "location": row.get("location") or "",
                "source": row.get("site") or "linkedin",
                "url": row.get("job_url") or "",
                "salary": str(row.get("min_amount", "")),
                "description": row.get("description") or ""
            })
        return jobs
    except Exception as e:
        print(f"    ⚠ JobSpy: {e}")
        return []

def scrape_bayt_js(keyword, country="uae"):
    """Use jobspy's built-in Bayt scraper."""
    try:
        from jobspy import scrape_jobs
        df = scrape_jobs(site_name=["bayt"], search_term=keyword, location=country, results_wanted=30, hours_old=168)
        if df is None or df.empty: return []
        jobs = []
        for _, row in df.iterrows():
            title = row.get("title") or ""
            if not is_ios_job(title): continue
            if has_excluded_keywords(title): continue
            loc = "UAE" if country == "uae" else "Qatar"
            jobs.append({
                "id": f"bayt_{hash(str(row.get('id',''))+title)}",
                "title": title,
                "company": row.get("company") or "Unknown",
                "location": loc,
                "source": "bayt",
                "url": row.get("job_url") or "",
                "salary": str(row.get("min_amount", "")),
                "description": row.get("description") or ""
            })
        return jobs
    except Exception as e:
        print(f"    ⚠ Bayt: {e}")
        return []

# ── Source 1b: Bayt Custom Scraper ───────────────────────────────────────────
def scrape_bayt_custom(keyword, country="uae"):
    """Custom Bayt scraper for UAE/Qatar."""
    jobs = []
    url = f"https://www.bayt.com/en/{country}/jobs/{keyword.lower().replace(' ', '-')}-jobs/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "lxml")
        cards = soup.select("li[data-qa='job-card'], li[class*='has-pointer'], div[class*='jb-item']")
        if not cards:
            cards = soup.select("ul[class*='jobs'] > li, div[class*='job']")
        for card in cards:
            t_el = card.select_one("h2 a, h3 a, a[class*='title']")
            if not t_el: continue
            title = t_el.get_text(strip=True)
            if not is_ios_job(title): continue
            if has_excluded_keywords(title): continue
            c_el = card.select_one("[class*='jb-comp'], [class*='company'], [data-qa='company-name']")
            company = c_el.get_text(strip=True) if c_el else "Unknown"
            link = t_el.get("href", "")
            if not link.startswith("http"): link = "https://www.bayt.com" + link
            loc_text = "UAE" if country == "uae" else "Qatar"
            jobs.append({
                "id": f"bayt_{hash(title+company)}",
                "title": title,
                "company": company,
                "location": loc_text,
                "source": "bayt",
                "url": link,
                "salary": "",
                "description": title + " " + company
            })
    except: pass
    return jobs

# ── Source 2: Himalayas (Free, No Auth, Country Filtering) ───────────────────
def scrape_himalayas(query="iOS developer", country="AE", max_pages=2):
    jobs = []
    for page in range(1, max_pages + 1):
        try:
            url = "https://himalayas.app/jobs/api/search"
            params = {"q": query, "country": country, "page": page, "sort": "recent"}
            r = requests.get(url, params=params, timeout=15)
            data = r.json()
            for j in data.get("jobs", []):
                title = j.get("title") or ""
                if not is_ios_job(title): continue
                if has_excluded_keywords(title): continue
                locations = j.get("locationRestrictions", [])
                loc_str = ", ".join(locations) if locations else "Remote"
                salary_min = j.get("minSalary") or ""
                salary_max = j.get("maxSalary") or ""
                currency = j.get("currency") or ""
                salary = f"{salary_min}-{salary_max} {currency}" if salary_min else ""
                jobs.append({
                    "id": f"himalayas_{j.get('id')}",
                    "title": title,
                    "company": j.get("companyName") or "Unknown",
                    "location": loc_str,
                    "source": "himalayas",
                    "url": f"https://himalayas.app/jobs/{j.get('slug', '')}",
                    "salary": salary,
                    "description": j.get("description", "")[:2000]
                })
            time.sleep(1)
        except: pass
    return jobs

# ── Source 3: RemoteOK (Free, No Auth, Remote Jobs) ──────────────────────────
def scrape_remoteok(tag="ios"):
    jobs = []
    try:
        url = f"https://remoteok.com/api?tag={tag}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        data = r.json()
        for item in data[1:]:
            if not isinstance(item, dict): continue
            title = item.get("position") or ""
            if not is_ios_job(title): continue
            if has_excluded_keywords(title): continue
            jobs.append({
                "id": f"remoteok_{item.get('id')}",
                "title": title,
                "company": item.get("company") or "Unknown",
                "location": item.get("location") or "Remote",
                "source": "remoteok",
                "url": item.get("url") or f"https://remoteok.com/remote-jobs/{item.get('id')}",
                "salary": str(item.get("salary", "")),
                "description": item.get("description", "")[:2000]
            })
    except: pass
    return jobs

# ── Source 4: Arbeitnow (Free, No Auth, Europe Jobs) ─────────────────────────
def scrape_arbeitnow(keyword="iOS", country=None):
    jobs = []
    try:
        url = "https://www.arbeitnow.com/api/job-board-api"
        r = requests.get(url, timeout=15)
        data = r.json()
        for item in data.get("data", []):
            title = item.get("title") or ""
            location = item.get("location") or ""
            if not is_ios_job(title): continue
            if has_excluded_keywords(title): continue
            if country and country.lower() not in location.lower(): continue
            jobs.append({
                "id": f"arbeitnow_{item.get('id')}",
                "title": title,
                "company": item.get("company_name") or "Unknown",
                "location": location,
                "source": "arbeitnow",
                "url": item.get("url") or item.get("apply_url") or "",
                "salary": "",
                "description": item.get("description", "")[:2000]
            })
    except: pass
    return jobs

# ── Source 5: Jooble (Free API Key) ──────────────────────────────────────────
def scrape_jooble(query="iOS Developer", location="Germany", api_key=""):
    if not api_key: return []
    jobs = []
    try:
        url = f"https://jooble.org/api/{api_key}"
        payload = {"keywords": query, "location": location, "page": "1"}
        r = requests.post(url, json=payload, timeout=15)
        data = r.json()
        for item in data.get("jobs", []):
            title = item.get("title") or ""
            if not is_ios_job(title): continue
            if has_excluded_keywords(title): continue
            jobs.append({
                "id": f"jooble_{hash(item.get('link',''))}",
                "title": title,
                "company": item.get("company") or "Unknown",
                "location": item.get("location") or "",
                "source": "jooble",
                "url": item.get("link") or "",
                "salary": item.get("salary") or "",
                "description": item.get("snippet", "")[:2000]
            })
    except: pass
    return jobs

# ── Source 6: Adzuna (Free API Key) ──────────────────────────────────────────
def scrape_adzuna(keyword, country_code="in", page=1, results_per_page=20):
    app_id = os.environ.get("ADZUNA_APP_ID", "")
    app_key = os.environ.get("ADZUNA_APP_KEY", "")
    if not app_id or not app_key: return []
    jobs = []
    url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/{page}"
    params = {"app_id": app_id, "app_key": app_key, "what": keyword, "results_per_page": results_per_page, "sort_by": "date", "max_days_old": 7}
    try:
        r = requests.get(url, params=params, timeout=15)
        data = r.json()
        for item in data.get("results", []):
            title = item.get("title") or ""
            if not is_ios_job(title): continue
            if has_excluded_keywords(title): continue
            jobs.append({
                "id": f"adzuna_{item.get('id')}",
                "title": title,
                "company": item.get("company", {}).get("display_name", "Unknown"),
                "location": item.get("location", {}).get("display_name", ""),
                "source": "adzuna",
                "url": item.get("redirect_url"),
                "salary": str(item.get("salary_min", "")),
                "description": item.get("description", "")
            })
    except: pass
    return jobs

# ── Main Processing ───────────────────────────────────────────────────────────
def run_agent(model="llama3.1:8b"):
    print(f"🔄 Checking connection to Ollama at {OLLAMA_URL}...")
    try:
        requests.get("http://127.0.0.1:11434/", timeout=3)
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Ollama is not running. Please start the Ollama app or run 'ollama serve' in your terminal.")
        return
    
    con = init_db()
    all_found = []
    stats = {"total_scraped": 0, "scored": 0, "passed": 0, "by_source": {}, "sponsored": 0}
    kw = today_keyword()
    jooble_key = os.environ.get("JOOBLE_API_KEY", "")
    
    print(f"🚀 Starting Job Hunt. Today's Keyword: {kw}")
    print(f"📅 Date: {date.today()}")
    print(f"🇮🇳 Indian candidate - Sponsorship-aware search enabled")
    print(f"🌍 Priority: UAE(*) > Qatar > India > Europe > Global Remote")
    print(f"📡 Sources: LinkedIn, Indeed, Bayt, Himalayas, RemoteOK, Arbeitnow, Jooble, Adzuna\n")

    # ── JobSpy: LinkedIn + Indeed (with country_indeed fix) ────────────────────
    print("━━━ JobSpy (LinkedIn + Indeed) ━━━")
    targets = [
        (kw, "Dubai, UAE", ["linkedin", "indeed"], "united arab emirates"),
        (kw, "Abu Dhabi, UAE", ["linkedin", "indeed"], "united arab emirates"),
        (kw, "Doha, Qatar", ["linkedin", "indeed"], "qatar"),
        (kw, "Bangalore, India", ["linkedin", "indeed"], "india"),
        (kw, "Mumbai, India", ["linkedin", "indeed"], "india"),
        (kw, "Pune, India", ["linkedin", "indeed"], "india"),
        (kw, "Berlin, Germany", ["linkedin", "indeed"], "germany"),
        (kw, "Amsterdam, Netherlands", ["linkedin", "indeed"], "netherlands"),
        (kw, "London, UK", ["linkedin", "indeed"], "uk"),
        ("iOS Developer Remote", "Remote", ["linkedin", "indeed"], "usa"),
        ("Swift Engineer Remote", "Worldwide", ["linkedin", "indeed"], "usa"),
    ]
    for term, loc, sites, country in targets:
        batch = scrape_jobspy(term, loc, sites, country_indeed=country)
        stats["total_scraped"] += len(batch)
        print(f"  ✓ {loc}: {len(batch)} jobs [{', '.join(sites)}]")
        process_batch(con, batch, all_found, stats, model)

    # ── JobSpy: Bayt (UAE + Qatar) - Using custom scraper ──────────────────────
    print("\n━━━ Bayt (UAE + Qatar) ━━━")
    for country in ["uae", "qatar"]:
        for b_kw in ["ios developer", "swift engineer"]:
            batch = scrape_bayt_custom(b_kw, country=country)
            stats["total_scraped"] += len(batch)
            if batch: print(f"  ✓ Bayt {country.upper()}: {len(batch)} jobs")
            process_batch(con, batch, all_found, stats, model)

    # ── Himalayas (Free, Country Filtering) ────────────────────────────────────
    print("\n━━━ Himalayas API ━━━")
    for code, name in [("AE", "UAE"), ("QA", "Qatar"), ("IN", "India"), ("DE", "Germany"), ("GB", "UK"), ("NL", "Netherlands")]:
        batch = scrape_himalayas("iOS developer", country=code)
        stats["total_scraped"] += len(batch)
        if batch: print(f"  ✓ Himalayas {name}: {len(batch)} jobs")
        process_batch(con, batch, all_found, stats, model)
        time.sleep(1)

    # ── RemoteOK (Remote Jobs) ────────────────────────────────────────────────
    print("\n━━━ RemoteOK API ━━━")
    for tag in ["ios", "swift", "mobile"]:
        batch = scrape_remoteok(tag=tag)
        stats["total_scraped"] += len(batch)
        if batch: print(f"  ✓ RemoteOK #{tag}: {len(batch)} jobs")
        process_batch(con, batch, all_found, stats, model)

    # ── Arbeitnow (Europe Jobs) ────────────────────────────────────────────────
    print("\n━━━ Arbeitnow API ━━━")
    for country in ["Germany", "Netherlands", "Remote"]:
        batch = scrape_arbeitnow("iOS", country=country)
        stats["total_scraped"] += len(batch)
        if batch: print(f"  ✓ Arbeitnow {country}: {len(batch)} jobs")
        process_batch(con, batch, all_found, stats, model)

    # ── Jooble (Free API Key) ─────────────────────────────────────────────────
    if jooble_key:
        print("\n━━━ Jooble API ━━━")
        for country in ["United Arab Emirates", "India", "Germany", "United Kingdom"]:
            batch = scrape_jooble("iOS Developer", location=country, api_key=jooble_key)
            stats["total_scraped"] += len(batch)
            if batch: print(f"  ✓ Jooble {country}: {len(batch)} jobs")
            process_batch(con, batch, all_found, stats, model)
    else:
        print("\n━━━ Jooble: SKIPPED (set JOOBLE_API_KEY env var) ━━━")

    # ── Adzuna (Free API Key) ─────────────────────────────────────────────────
    adzuna_id = os.environ.get("ADZUNA_APP_ID", "")
    if adzuna_id:
        print("\n━━━ Adzuna API ━━━")
        for code, name in [("ae", "UAE"), ("qa", "Qatar"), ("in", "India"), ("gb", "UK"), ("de", "Germany")]:
            batch = scrape_adzuna(kw, country_code=code)
            stats["total_scraped"] += len(batch)
            if batch: print(f"  ✓ Adzuna {name}: {len(batch)} jobs")
            process_batch(con, batch, all_found, stats, model)
    else:
        print("\n━━━ Adzuna: SKIPPED (set ADZUNA_APP_ID/ADZUNA_APP_KEY env vars) ━━━")

    # ── Generate Country-Wise Output ──────────────────────────────────────────
    by_country = {1: [], 2: [], 3: [], 4: [], 5: [], 99: []}
    for j in all_found:
        p = j.get("priority", 99)
        by_country.setdefault(p, []).append(j)
    for p in by_country:
        by_country[p].sort(key=lambda x: -x.get("score", 0))

    sources_used = set(j.get("source", "") for j in all_found)
    output = [f"# 🎯 Job Hunt Results - {date.today()}", ""]
    output.append(f"**Keyword:** {kw}")
    output.append(f"**Priority:** UAE(*) > Qatar > India > Europe > Global Remote")
    output.append(f"**Sources:** {', '.join(sorted(sources_used))}")
    output.append(f"**Total Found:** {len(all_found)} qualified iOS/Swift jobs")
    sponsored_count = sum(1 for j in all_found if j.get("sponsorship", False))
    output.append(f"**Visa Sponsorship:** {sponsored_count} jobs offer sponsorship")
    output.append("")
    output.append("---")
    output.append("")
    
    job_num = 0
    for priority in [1, 2, 3, 4, 5, 99]:
        jobs = by_country.get(priority, [])
        if not jobs: continue
        country_label = get_country_group(priority)
        output.append(f"## {country_label} ({len(jobs)} jobs)")
        output.append("")
        for j in jobs[:15]:
            job_num += 1
            salary = j.get("salary") or "N/A"
            if salary in ("nan", "None", ""): salary = "N/A"
            location = j["location"] or "Location TBD"
            reason = (j.get("reason") or "")[:80]
            sp_status = j.get("sp_status", "❓ Unknown")
            output.append(f"**[{job_num:02d}]** {j['title']}")
            output.append(f"   📍 {j['company']} | {location} | via {j.get('source','')} | {sp_status}")
            output.append(f"   💰 {salary} | Score: {j['score']}/100 ({j['match']})")
            if reason: output.append(f"   📝 {reason}")
            output.append(f"   🔗 {j['url']}")
            
            outreach = j.get("outreach_msg")
            if outreach:
                formatted_outreach = outreach.replace('\\n', '\\n   > ').replace('\n', '\n   > ')
                output.append(f"   ✉️ **Auto-Outreach:**\n   > {formatted_outreach}")
            
            output.append("")
        output.append("---")
        output.append("")

    result_text = "\n".join(output)
    
    # Ensure runs directory exists
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create timestamped file for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_digest_file = RUNS_DIR / f"digest_{timestamp}.md"
    
    with open(run_digest_file, "w") as f:
        f.write(result_text)
        
    with open(DIGEST_FILE, "w") as f:
        f.write(result_text)
    
    print("\n" + "="*60)
    print("--- SUMMARY ---")
    print("="*60)
    for p in [1, 2, 3, 4, 5]:
        count = len(by_country.get(p, []))
        if count: print(f"  {get_country_group(p)}: {count} jobs")
    other = len(by_country.get(99, []))
    if other: print(f"  ❓ Other: {other} jobs")
    sponsored_total = sum(1 for j in all_found if j.get("sponsorship", False))
    print(f"\n📊 Total: {stats['total_scraped']} scraped | {stats['scored']} scored | {stats['passed']} passed")
    print(f"🏆 Sponsorship-friendly jobs: {sponsored_total}")
    print(f"📡 Sources: {json.dumps(stats['by_source'], indent=2)}")
    print(f"✅ Digest saved to:")
    print(f"   • {run_digest_file}")
    print(f"   • {DIGEST_FILE} (latest reference)")
    print("="*60)
    
    # Send email notification
    if all_found:
        email_subject = f"HireKit Job Hunt - {len(all_found)} iOS/Swift Jobs Found ({sponsored_total} sponsorship)"
        email_body = f"""Job Hunt Results - {date.today()}

Keyword: {kw}
Total Qualified Jobs: {len(all_found)}
Visa Sponsorship Available: {sponsored_total}

By Country:
"""
        for p in [1, 2, 3, 4, 5]:
            count = len(by_country.get(p, []))
            if count:
                email_body += f"  {get_country_group(p)}: {count} jobs\n"
        
        if sponsored_total > 0:
            email_body += "\n🎯 Sponsorship Jobs (High Priority):\n"
            for j in sorted(all_found, key=lambda x: -x.get("score", 0)):
                if j.get("sponsorship", False) and j["score"] >= 85:
                    email_body += f"• {j['title']} @ {j['company']} ({j['location']})\n"
                    email_body += f"  {j['url']}\n\n"
        
        send_email_notification(email_subject, email_body)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="HireKit Job Agent")
    parser.add_argument("--run", action="store_true", default=True, help="Run the job agent")
    parser.add_argument("--notify", action="store_true", help="Send email notification (requires SMTP env vars)")
    parser.add_argument("--model", default="llama3.1:8b", help="Ollama model to use")
    args = parser.parse_args()
    run_agent(model=args.model)

if __name__ == "__main__":
    main()
