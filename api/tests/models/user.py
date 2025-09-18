import pytest
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import Profile
from api.tests.conftest import db_session

@pytest.mark.asyncio
async def test_profile(db_session: AsyncSession) -> None:
    profile = Profile(
        weight=63,
        height=183,
        birth_date=date(2009, 10, 19),
        activity_type='normal',
        allergy='Аллергея на котов',
        goal='gain_weight',
        desired_weight=65,
    )
    async with db_session.begin():
        db_session.add(profile)
    result = await db_session.get(Profile, 1)
    assert profile == result
