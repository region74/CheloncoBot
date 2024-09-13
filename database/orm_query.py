from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from database.models import Device


async def orm_add_device(session: AsyncSession, data: dict) -> Optional[str]:
    # Сначала проверяем, существует ли устройство с указанными полями
    stmt = select(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    )

    result = await session.execute(stmt)
    existing_device = result.scalar_one_or_none()  # Получаем один результат или None

    # Если устройство существует, выходим из функции
    if existing_device:
        return None
    else:
        # Если устройства нет в базе, добавляем новое
        obj = Device(
            number=data['number'],
            category=data['category'],
            firma=data['firma'],
            model=data['model']
        )
        session.add(obj)
        await session.commit()
        return 'Это новое устройство, оно было добавлено в БД'
