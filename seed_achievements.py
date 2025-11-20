from db import SessionLocal
from model.AchievementORM import AchievementORM

def seed_achievements():
    db = SessionLocal()
    try:
        achievements = [
            AchievementORM(
                name="Movie Buff",
                description="Rate 5 movies",
                condition_type="COUNT_REVIEWS",
                condition_params={"threshold": 5}
            ),
            AchievementORM(
                name="Cinema Addict",
                description="Rate 20 movies",
                condition_type="COUNT_REVIEWS",
                condition_params={"threshold": 20}
            ),
            AchievementORM(
                name="Horror Fan",
                description="Rate 5 Horror movies",
                condition_type="GENRE_MASTER",
                condition_params={"genre": "Horror", "threshold": 5}
            )
        ]

        for achievement in achievements:
            existing = db.query(AchievementORM).filter(AchievementORM.name == achievement.name).first()
            if not existing:
                db.add(achievement)
                print(f"Added achievement: {achievement.name}")
            else:
                print(f"Achievement already exists: {achievement.name}")
        
        db.commit()
    except Exception as e:
        print(f"Error seeding achievements: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_achievements()
