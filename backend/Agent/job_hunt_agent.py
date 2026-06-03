import asyncio
from typing import List, Dict
from ..llm.ollama_client import OllamaClient

class JobHuntAgent:
    SOURCES = {
        'linkedin': 'linkedin',
        'indeed': 'indeed',
        'bayt': 'bayt',
        'himalayas': 'himalayas',
        'remoteok': 'remoteok',
        'arbeitnow': 'arbeitnow',
    }

    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client
        self.COUNTRY_PRIORITY = {
            "united arab emirates": 1, "uae": 1, "dubai": 1,
            "india": 3, "bangalore": 3, "mumbai": 3,
            "germany": 4, "berlin": 4,
            "netherlands": 4, "amsterdam": 4,
            "remote": 5, "worldwide": 5,
        }

    async def execute(self, payload: dict) -> dict:
        """Execute job hunt with given parameters"""
        keywords = payload.get('keywords', [])
        locations = payload.get('locations', ['UAE', 'India', 'Germany', 'Netherlands'])
        model = payload.get('model', 'llama3.1:8b')

        all_jobs = []
        
        # Scrape each location
        for loc in locations:
            jobs = await self._scrape_location(keywords, loc)
            all_jobs.extend(jobs)

        # Deduplicate
        unique_jobs = self._deduplicate(all_jobs)

        return {
            "status": "completed",
            "jobs_found": len(unique_jobs),
            "jobs": unique_jobs[:50]  # Limit to 50
        }

    async def _scrape_location(self, keywords: List[str], location: str) -> List[Dict]:
        """Scrape jobs for a location using jobspy"""
        jobs = []
        
        try:
            from jobspy import scrape_jobs
            for kw in keywords:
                try:
                    df = scrape_jobs(
                        site_name=["linkedin", "indeed"],
                        search_term=kw,
                        location=location,
                        results_wanted=20,
                        hours_old=168
                    )
                    if df is not None and not df.empty:
                        for _, row in df.iterrows():
                            jobs.append({
                                "id": f"spy_{row.get('id','')}",
                                "title": row.get("title", ""),
                                "company": row.get("company", "Unknown"),
                                "location": row.get("location", location),
                                "source": "linkedin/indeed",
                                "url": row.get("job_url", ""),
                                "salary": str(row.get("min_amount", "")),
                                "description": row.get("description", "")[:2000]
                            })
                except Exception as e:
                    print(f"Error scraping {kw} in {location}: {e}")
        except ImportError:
            print("jobspy not installed")

        return jobs

    def _deduplicate(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on company+title+location"""
        seen = set()
        unique = []
        for job in jobs:
            key = f"{job['company']}_{job['title']}_{job['location']}"
            if key not in seen:
                seen.add(key)
                unique.append(job)
        return unique

    def get_priority(self, location: str) -> int:
        loc_lower = (location or "").lower()
        for country, priority in self.COUNTRY_PRIORITY.items():
            if country in loc_lower:
                return priority
        return 99