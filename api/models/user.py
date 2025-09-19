from datetime import date
from enum import StrEnum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Enum


from api.core.database import Base


class ActivityEnum(StrEnum):
    sedentary = 'sedentary'
    normal = 'normal'
    sportive = 'sportive'


class GoalEnum(StrEnum):
    lose_weight = 'lose_weight'
    support_weight = 'support_weight'
    gain_weight = 'gain_weight'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True, nullable=False)

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    is_active: Mapped[bool] = mapped_column(default=False)


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)

    weight: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)

    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    activity_type: Mapped[ActivityEnum] = mapped_column(
        Enum(ActivityEnum, name="activity_enum"),
        default=ActivityEnum.normal, 
        nullable=False,
    )

    allergy: Mapped[str] = mapped_column(nullable=False)

    goal: Mapped[GoalEnum] = mapped_column(
        Enum(GoalEnum, name="goal_enum"),
        default=GoalEnum.support_weight, 
        nullable=False,
        
    )
    desired_weight: Mapped[int] = mapped_column()
