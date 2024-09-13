import logging
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from database.models import Device, DeviceGet, DeviceSend, Movement
from tools import get_department_name


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
        return f'Тип: {existing_device.category}\nФирма: {existing_device.firma}\nМодель: {existing_device.model}\nИнв.номер: {existing_device.number}\nОтделение: {existing_device.place}'
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
        logging.info('Добавлено новое устройство')
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


async def orm_send_device(session: AsyncSession, data: dict):
    stmt = select(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    )

    result = await session.execute(stmt)
    existing_device = result.scalar_one_or_none()
    device_get = DeviceSend(
        device_id=existing_device.id,
        comment=data['comment']
    )
    try:
        session.add(device_get)
        await session.commit()

        check_stmt = select(DeviceSend).where(DeviceSend.device_id == existing_device.id)
        result = await session.execute(check_stmt)
        added_record = result.scalar_one_or_none()

        if added_record:
            logging.info('Записи добавлена в БД')
        else:
            logging.error('Записи НЕ добавлена в БД')
    except Exception as e:
        await session.rollback()
        logging.info(f'Ошибка добавления записи в БД:\n{e}')


async def orm_update_device(session: AsyncSession, data: dict):
    # Добавление записи в таблицу перемещения
    stmt = select(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    )
    result = await session.execute(stmt)
    existing_device = result.scalar_one_or_none()
    move_log = Movement(
        device_id=existing_device.id,
        place_from=existing_device.place,
        place_to=data['place']
    )
    try:
        session.add(move_log)
        await session.commit()

        check_stmt = select(Movement).where(Movement.device_id == existing_device.id)
        result = await session.execute(check_stmt)
        added_record = result.scalar_one_or_none()

        if added_record:
            logging.info('Записи добавлена в БД')
        else:
            logging.error('Записи НЕ добавлена в БД')
    except Exception as e:
        await session.rollback()
        logging.info(f'Ошибка добавления записи в БД:\n{e}')

    # Обновление значения в устройстве
    stmt = update(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    ).values(
        place=get_department_name(int(data['place']))
    )
    result = await session.execute(stmt)
    await session.commit()
