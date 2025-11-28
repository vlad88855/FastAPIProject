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
                condition_params={"genre": "horror", "threshold": 5}
            ),
            AchievementORM(
                name="The Critic",
                description="Leave 5 comments",
                condition_type="COMMENT_COUNT",
                condition_params={"threshold": 5}
            ),
            AchievementORM(
                name="Genre Explorer",
                description="Rate movies from 3 different genres",
                condition_type="DISTINCT_GENRE",
                condition_params={"threshold": 3}
            ),
            AchievementORM(
                name="The Contrarian",
                description="Rate a movie 10 stars when its average is below 5",
                condition_type="CONTRARIAN",
                condition_params={"min_user_rating": 10, "max_movie_avg": 5.0, "threshold": 1}
            )
        ]

        for achievement in achievements:
            existing = db.query(AchievementORM).filter(AchievementORM.name == achievement.name).first()
            if not existing:
                db.add(achievement)
                print(f"Added achievement: {achievement.name}")
            else:
                existing.condition_params = achievement.condition_params
                existing.description = achievement.description
                existing.condition_type = achievement.condition_type
                print(f"Updated achievement: {achievement.name}")
        
        db.commit()
    except Exception as e:
        print(f"Error seeding achievements: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_achievements()
