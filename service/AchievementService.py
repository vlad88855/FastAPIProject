import logging
from typing import List
from sqlalchemy.orm import Session
from model.AchievementORM import AchievementORM
from model.UserAchievementORM import UserAchievementORM
from model.DTOs.AchievementDTO import UserAchievementOut, AchievementStatusOut
from service.AchievementHandlers import HandlerRegistry

from repository.AchievementRepository import AchievementRepository

class AchievementService:
    def __init__(self, repo: AchievementRepository, db: Session):
        self.repo = repo
        self.db = db # Keeping db for handlers that might need it, or we should refactor handlers too?
        # Handlers currently take 'db' as argument. Ideally handlers should also use repositories or not access DB directly.
        # For now, let's keep db for handlers but use repo for service logic.
        self.logger = logging.getLogger(__name__)

    def check_new_achievements(self, user_id: int) -> List[AchievementORM]:
        all_achievements = self.repo.get_all_achievements()
        user_achievement_ids = self.repo.get_user_achievement_ids(user_id)

        newly_earned = []

        for achievement in all_achievements:
            if achievement.id in user_achievement_ids:
                continue

            handler = HandlerRegistry.get_handler(achievement.condition_type)
            if not handler:
                continue

            if handler.check(user_id, achievement.condition_params, self.db):
                self.repo.add_user_achievement(user_id, achievement.id)
                newly_earned.append(achievement)
                self.logger.info(f"User {user_id} earned new achievement: {achievement.name}")
        
        # Repo commits individually in add_user_achievement, so we might not need bulk commit here 
        # or we should change repo to not commit immediately if we want bulk.
        # For now, let's assume repo commits.
        
        return newly_earned
        
        if newly_earned:
            self.db.commit()
            
        return newly_earned

    def get_user_achievements(self, user_id: int) -> List[UserAchievementOut]:
        user_achievements = self.repo.get_user_achievements_with_details(user_id)
        
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
        all_achievements = self.repo.get_all_achievements()
        
        user_achievements = self.repo.get_user_achievements(user_id)
        user_achievements_map = {
            ua.achievement_id: ua.earned_at
            for ua in user_achievements
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
