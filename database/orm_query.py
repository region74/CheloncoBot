import logging
import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from database.models import Device, DeviceGet, DeviceSend, Movement
from tools import get_department_name, get_department_id, get_last_status


async def orm_add_device(session: AsyncSession, data: dict) -> Optional[str]:
    """
    Метод добавления устройства в БД
    :param session:
    :param data:
    :return:
    """
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
        return f'Тип: {existing_device.category}\nФирма: {existing_device.firma}\nМодель: {existing_device.model}\nИнв.номер: {existing_device.number}\nОтделение: {existing_device.place}\nПоследний статус: {get_last_status(int(existing_device.last_status))}'
    else:
        # Если устройства нет в базе, добавляем новое
        obj = Device(
            number=data['number'],
            category=data['category'],
            firma=data['firma'],
            model=data['model'],
            last_status=0
        )
        session.add(obj)
        await session.commit()
        logging.info('Добавлено новое устройство')
        return 'Это новое устройство, оно было добавлено в БД'


async def orm_get_device(session: AsyncSession, data: dict) -> Optional[str]:
    """
    Метод приемки устройства с ремонта
    :param session:
    :param data:
    :return:
    """
    stmt = select(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    )

    result = await session.execute(stmt)
    existing_device = result.scalar_one_or_none()
    if existing_device.last_status == 2:
        return ("Устройство уже принималось с ремонта, отправки в ремонт не было!\nСделайте отправку в ремонт, "
                "а затем приемку с ремонта.")
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

    stmt = update(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    ).values(
        last_status=2
    )
    await session.execute(stmt)
    await session.commit()


async def orm_send_device(session: AsyncSession, data: dict) -> Optional[str]:
    """
    Метод отправки устройства в ремонт
    :param session:
    :param data:
    :return:
    """
    stmt = select(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    )

    result = await session.execute(stmt)
    existing_device = result.scalar_one_or_none()

    # Проверка гарантийной даты 3 мес
    current_time = datetime.datetime.now()
    three_months_ago = current_time - datetime.timedelta(days=90)
    if existing_device.updated > three_months_ago:
        return 'Не прошло 3 месяцев с последнего ремонта! Отмена отправки в ремонт...'
    if existing_device.last_status == 1:
        return 'Устройство уже в ремонте! Проведите приемку и повторите отправку в ремонт.'

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

    stmt = update(Device).where(
        Device.number == data['number'],
        Device.category == data['category'],
        Device.firma == data['firma'],
        Device.model == data['model']
    ).values(
        last_status=1
    )
    await session.execute(stmt)
    await session.commit()


async def orm_update_device(session: AsyncSession, data: dict):
    """
    Изменение места устройства и запись перемещения в БД
    :param session:
    :param data:
    :return:
    """
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
        place_from=get_department_id(existing_device.place),
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
