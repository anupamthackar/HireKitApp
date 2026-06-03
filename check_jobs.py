#!/usr/bin/env python3
import sqlite3
import argparse
import sys
import json
import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "jobs.db"

def connect_db():
    if not DB_FILE.exists():
        print(f"❌ Database not found at {DB_FILE}")
        sys.exit(1)
    con = sqlite3.connect(DB_FILE)
    try:
        con.execute("ALTER TABLE jobs ADD COLUMN sponsorship INTEGER")
    except sqlite3.OperationalError: pass
    try:
        con.execute("ALTER TABLE jobs ADD COLUMN sp_status TEXT")
    except sqlite3.OperationalError: pass
    con.commit()
    return con

def show_stats(con):
    cursor = con.cursor()
    
    # Total count
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total = cursor.fetchone()[0]
    
    # Match breakdown
    cursor.execute("SELECT match, COUNT(*) FROM jobs GROUP BY match ORDER BY COUNT(*) DESC")
    match_breakdown = cursor.fetchall()
    
    # Source breakdown
    cursor.execute("SELECT source, COUNT(*) FROM jobs GROUP BY source ORDER BY COUNT(*) DESC")
    source_breakdown = cursor.fetchall()
    
    # Location breakdown (top 5)
    cursor.execute("SELECT location, COUNT(*) FROM jobs GROUP BY location ORDER BY COUNT(*) DESC LIMIT 5")
    loc_breakdown = cursor.fetchall()
    
    # Sponsorship breakdown
    cursor.execute("SELECT sponsorship, COUNT(*) FROM jobs GROUP BY sponsorship")
    sp_breakdown = cursor.fetchall()
    
    print("\n📊 Database Statistics")
    print("=" * 40)
    print(f"Total Saved Jobs: {total}")
    
    print("\nMatch Quality:")
    for match, count in match_breakdown:
        grade = {"H": "High 🔥", "M": "Medium ⚡", "L": "Low 🧊"}.get(match, match)
        print(f"  • {grade}: {count}")
    
    print("\nTop Sources:")
    for source, count in source_breakdown:
        print(f"  • {source.capitalize()}: {count}")
        
    print("\nTop Locations:")
    for loc, count in loc_breakdown:
        print(f"  • {loc or 'Unknown'}: {count}")
    
    print("\nVisa Sponsorship:")
    sp_total = sum(c for _, c in sp_breakdown)
    sp_yes = next((c for s, c in sp_breakdown if s == 1), 0)
    print(f"  • Sponsorship Available: {sp_yes}")
    print(f"  • Self-Funded/Unknown: {sp_total - sp_yes}")
    print("=" * 40 + "\n")

def list_jobs(args):
    con = connect_db()
    
    if args.stats:
        show_stats(con)
        con.close()
        return

    query = "SELECT title, company, location, source, url, salary, score, match, found_at, reason, sp_status, id FROM jobs WHERE 1=1"
    params = []
    
    if args.match:
        query += " AND match = ?"
        params.append(args.match.upper())
        
    if args.min_score:
        query += " AND score >= ?"
        params.append(args.min_score)
        
    if args.search:
        query += " AND (title LIKE ? OR company LIKE ? OR reason LIKE ? OR location LIKE ?)"
        search_wild = f"%{args.search}%"
        params.extend([search_wild, search_wild, search_wild, search_wild])
    
    if args.sponsored:
        query += " AND sponsorship = 1"
        
    # Sort options
    if args.sort == "date":
        query += " ORDER BY found_at DESC"
    elif args.sort == "score":
        query += " ORDER BY score DESC"
    else:
        query += " ORDER BY found_at DESC"
        
    query += " LIMIT ?"
    params.append(args.limit)
    
    cursor = con.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    if not rows:
        print("🔍 No saved jobs found matching your criteria.")
        con.close()
        return
        
    if args.json:
        jobs_list = []
        for r in rows:
            jobs_list.append({
                "title": r[0], "company": r[1], "location": r[2], "source": r[3],
                "url": r[4], "salary": r[5], "score": r[6], "match": r[7],
                "found_at": r[8], "reason": r[9], "sponsorship": r[10], "id": r[11]
            })
        print(json.dumps(jobs_list, indent=2))
        con.close()
        return
        
    if args.csv:
        csv_file = BASE_DIR / args.csv
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Company", "Location", "Source", "URL", "Salary", "Score", "Match", "Date Found", "Reason", "Sponsorship"])
            for r in rows:
                writer.writerow(r[:-2]) # exclude DB ID and sp_status
        print(f"💾 Exported {len(rows)} jobs to {csv_file}")
        con.close()
        return

    # Standard pretty console output
    print(f"\n📂 Showing {len(rows)} Saved Jobs:")
    print("=" * 80)
    for idx, r in enumerate(rows, 1):
        title, company, loc, source, url, salary, score, match, found_at, reason, sp_status, db_id = r
        
        # Color & emoji coding
        match_emoji = {"H": "🔥 [High]", "M": "⚡ [Medium]", "L": "🧊 [Low]"}.get(match, f"[{match}]")
        salary_str = salary if (salary and salary != "nan" and salary != "None") else "N/A"
        date_str = found_at.split("T")[0] if "T" in found_at else found_at
        sp_display = sp_status if sp_status else "❓ Unknown"
        
        print(f"[{idx:02d}] \033[1m{title}\033[0m")
        print(f"     Company:  {company} | Location: {loc} ({source.capitalize()})")
        print(f"     Score:    {score}/100 - {match_emoji} | Sponsorship: {sp_display} | Date Found: {date_str}")
        print(f"     Salary:   {salary_str}")
        if reason:
            print(f"     Reason:   \033[3m{reason}\033[0m")
        print(f"     URL:      \033[4m{url}\033[0m")
        print("-" * 80)
    
    con.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query and inspect saved jobs in the HireKit database.")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Number of jobs to list (default: 10)")
    parser.add_argument("-m", "--match", choices=["H", "M", "L"], help="Filter by match quality (H/M/L)")
    parser.add_argument("-s", "--min-score", type=int, help="Minimum score to filter by")
    parser.add_argument("-q", "--search", help="Search text in job titles, companies, locations, or match reasons")
    parser.add_argument("--sort", choices=["date", "score"], default="date", help="Sort by 'date' (default) or 'score'")
    parser.add_argument("--stats", action="store_true", help="Show total database statistics instead of listing jobs")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--csv", help="Export results to a CSV file (specify filename)")
    parser.add_argument("--sponsored", action="store_true", help="Show only jobs with visa sponsorship")
    
    args = parser.parse_args()
    list_jobs(args)
