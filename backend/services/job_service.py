from sqlmodel import Session, select
from ..database.engine import engine
from ..database.schema import Job, Profile, Application, Outreach

class JobService:
    def list_jobs(self, limit: int = 50, match: str = None, sponsored: bool = False):
        with Session(engine) as session:
            query = select(Job)
            if match:
                query = query.where(Job.match == match)
            if sponsored:
                query = query.where(Job.sponsorship == 1)
            return session.exec(query.limit(limit)).all()
    
    def save_job(self, job_data: dict) -> Job:
        with Session(engine) as session:
            job = Job(**job_data)
            session.add(job)
            session.commit()
            session.refresh(job)
            return job

class ProfileService:
    def get_profile(self) -> Profile:
        with Session(engine) as session:
            return session.exec(select(Profile)).first()
    
    def update_profile(self, profile_data: dict) -> Profile:
        with Session(engine) as session:
            profile = session.exec(select(Profile)).first()
            if not profile:
                profile = Profile(**profile_data)
                session.add(profile)
            else:
                for key, value in profile_data.items():
                    setattr(profile, key, value)
            session.commit()
            return profile

class OutreachService:
    def create_outreach(self, job_id: int, message: str) -> Outreach:
        with Session(engine) as session:
            outreach = Outreach(job_id=job_id, message=message)
            session.add(outreach)
            session.commit()
            return outreach