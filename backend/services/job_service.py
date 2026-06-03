import sqlite3
from pathlib import Path
from typing import Optional, List

JOBS_DB = Path(__file__).parent.parent.parent / "jobs.db"

class JobService:
    def _get_conn(self):
        return sqlite3.connect(JOBS_DB)

    def list_jobs(self, limit: int = 50, match: str = None, sponsored: bool = False) -> List[dict]:
        conn = self._get_conn()
        cursor = conn.cursor()

        query = """
            SELECT id, title, company, location, source, url, salary, score, match, 
                   CASE WHEN sponsorship = 1 THEN 1 ELSE 0 END as sponsorship, 
                   sp_status
            FROM jobs
        """
        params = []

        if match or sponsored:
            conditions = []
            if match:
                conditions.append("match = ?")
                params.append(match)
            if sponsored:
                conditions.append("(sponsorship = 1 OR sponsorship IS NULL)")

            query += " WHERE " + " AND ".join(conditions)

        query += f" ORDER BY found_at DESC LIMIT {limit}"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0], "title": r[1], "company": r[2], "location": r[3],
                "source": r[4], "url": r[5], "salary": r[6], "score": r[7],
                "match": r[8], "sponsorship": bool(r[9]), "sp_status": r[10] or "⚠️ Self-Funded"
            }
            for r in rows
        ]

    def save_job(self, job_data: dict) -> dict:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO jobs 
            (id, title, company, location, source, url, salary, score, match, found_at, reason, outreach_msg, sponsorship, sp_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_data.get("id"), job_data.get("title"), job_data.get("company"),
            job_data.get("location"), job_data.get("source"), job_data.get("url"),
            job_data.get("salary"), job_data.get("score"), job_data.get("match"),
            job_data.get("found_at"), job_data.get("reason"), job_data.get("outreach_msg"),
            1 if job_data.get("sponsorship") else 0, job_data.get("sp_status")
        ))
        conn.commit()
        conn.close()
        return job_data