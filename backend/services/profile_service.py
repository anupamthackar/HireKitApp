from sqlmodel import Session, select
from ..database.engine import engine
from ..database.schema import Profile

class ProfileService:
    def get_profile(self) -> Profile:
        with Session(engine) as session:
            return session.exec(select(Profile)).first()

    def create_profile(self, profile_data: dict) -> Profile:
        with Session(engine) as session:
            profile = Profile(**profile_data)
            session.add(profile)
            session.commit()
            session.refresh(profile)
            return profile

    def update_profile(self, profile_data: dict) -> Profile:
        with Session(engine) as session:
            profile = session.exec(select(Profile)).first()
            if not profile:
                return self.create_profile(profile_data)
            
            for key, value in profile_data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            session.commit()
            session.refresh(profile)
            return profile

    def get_skills(self) -> dict:
        profile = self.get_profile()
        if not profile or not profile.metadata_json:
            return {}
        import json
        return json.loads(profile.metadata_json)