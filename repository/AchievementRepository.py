import logging
from typing import List, Set
from sqlalchemy.orm import Session
from model.AchievementORM import AchievementORM
from model.UserAchievementORM import UserAchievementORM

class AchievementRepository:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def get_all_achievements(self) -> List[AchievementORM]:
        return self.db.query(AchievementORM).all()

    def get_user_achievements(self, user_id: int) -> List[UserAchievementORM]:
        return self.db.query(UserAchievementORM).filter(UserAchievementORM.user_id == user_id).all()

    def get_user_achievement_ids(self, user_id: int) -> Set[int]:
        return {
            ua.achievement_id 
            for ua in self.db.query(UserAchievementORM.achievement_id)
            .filter(UserAchievementORM.user_id == user_id)
            .all()
        }

    def add_user_achievement(self, user_id: int, achievement_id: int) -> UserAchievementORM:
        user_achievement = UserAchievementORM(
            user_id=user_id,
            achievement_id=achievement_id
        )
        self.db.add(user_achievement)
        self.db.commit()
        self.logger.info(f"User {user_id} earned achievement {achievement_id}")
        return user_achievement

    def get_user_achievements_with_details(self, user_id: int) -> List[tuple[UserAchievementORM, AchievementORM]]:
        return (
            self.db.query(UserAchievementORM, AchievementORM)
            .join(AchievementORM, UserAchievementORM.achievement_id == AchievementORM.id)
            .filter(UserAchievementORM.user_id == user_id)
            .all()
        )
