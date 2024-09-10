from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Device


async def orm_add_device(session: AsyncSession, data: dict):
    obj = Device(
        number=float(data['number']),
        category=data['category'],
        firma=data['firma'],
        model=data['model']
    )
    session.add(obj)
    await session.commit()
