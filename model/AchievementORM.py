from sqlalchemy import Column, Integer, String, JSON, UniqueConstraint
from db import Base

class AchievementORM(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(1024), nullable=False)
    condition_type = Column(String(50), nullable=False)
    condition_params = Column(JSON, nullable=False)
    icon_url = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint("name", name="uq_achievements_name"),
    )
