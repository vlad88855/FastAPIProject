from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class UserAchievementOut(BaseModel):
    id: int
    name: str
    description: str
    earned_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AchievementStatusOut(BaseModel):
    id: int
    name: str
    description: str
    earned: bool
    earned_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
