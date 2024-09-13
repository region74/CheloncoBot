import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from database.models import Device, DeviceGet


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


async def orm_get_device(session: AsyncSession, data: dict):
    stmt = select(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    )

    result = await session.execute(stmt)
    existing_device = result.scalar_one_or_none()
    device_get = DeviceGet(
        device_id=existing_device.id,  # Устанавливаем внешний ключ
        comment=data['comment']  # Пример поля, необходимого для DeviceGet
    )
    try:
        session.add(device_get)
        await session.commit()

        check_stmt = select(DeviceGet).where(DeviceGet.device_id == existing_device.id)
        result = await session.execute(check_stmt)
        added_record = result.scalar_one_or_none()

        if added_record:
            logging.info('Записи добавлена в БД')
        else:
            logging.error('Записи НЕ добавлена в БД')
    except Exception as e:
        await session.rollback()
        logging.info(f'Ошибка добавления записи в БД:\n{e}')
