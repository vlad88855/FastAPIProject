from typing import List
from sqlalchemy.orm import Session
from model.AchievementORM import AchievementORM
from model.UserAchievementORM import UserAchievementORM
from model.DTOs.AchievementDTO import UserAchievementOut, AchievementStatusOut
from service.AchievementHandlers import HandlerRegistry

class AchievementService:
    def __init__(self, db: Session):
        self.db = db

    def check_new_achievements(self, user_id: int) -> List[AchievementORM]:
        all_achievements = self.db.query(AchievementORM).all()
        
        user_achievement_ids = {
            ua.achievement_id 
            for ua in self.db.query(UserAchievementORM.achievement_id)
            .filter(UserAchievementORM.user_id == user_id)
            .all()
        }

        newly_earned = []

        for achievement in all_achievements:
            if achievement.id in user_achievement_ids:
                continue

            handler = HandlerRegistry.get_handler(achievement.condition_type)
            if not handler:
                continue

            if handler.check(user_id, achievement.condition_params, self.db):
                user_achievement = UserAchievementORM(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                self.db.add(user_achievement)
                newly_earned.append(achievement)
        
        if newly_earned:
            self.db.commit()
            
        return newly_earned

    def get_user_achievements(self, user_id: int) -> List[UserAchievementOut]:
        user_achievements = (
            self.db.query(UserAchievementORM, AchievementORM)
            .join(AchievementORM, UserAchievementORM.achievement_id == AchievementORM.id)
            .filter(UserAchievementORM.user_id == user_id)
            .all()
        )
        
        return [
            UserAchievementOut(
                id=ach.id,
                name=ach.name,
                description=ach.description,
                earned_at=ua.earned_at
            )
            for ua, ach in user_achievements
        ]

    def get_achievements_status(self, user_id: int) -> List[AchievementStatusOut]:
        all_achievements = self.db.query(AchievementORM).all()
        
        user_achievements_map = {
            ua.achievement_id: ua.earned_at
            for ua in self.db.query(UserAchievementORM)
            .filter(UserAchievementORM.user_id == user_id)
            .all()
        }
        
        result = []
        for ach in all_achievements:
            earned_at = user_achievements_map.get(ach.id)
            result.append(AchievementStatusOut(
                id=ach.id,
                name=ach.name,
                description=ach.description,
                earned=earned_at is not None,
                earned_at=earned_at
            ))
            
        return result
