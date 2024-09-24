import datetime

from sqlalchemy import String, Text, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Device(Base):
    __tablename__ = 'device'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    firma: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(Text)
    place: Mapped[str] = mapped_column(String(150), nullable=True, default='Undefined')
    last_status: Mapped[int] = mapped_column(nullable=True)
    date_update_status: Mapped[DateTime] = mapped_column(DateTime, nullable=False,
                                                         default=datetime.datetime(2024, 1, 1))

    device_gets = relationship("DeviceGet", back_populates="device")
    device_sends = relationship("DeviceSend", back_populates="device")
    device_movement = relationship("Movement", back_populates="device")


class DeviceGet(Base):
    __tablename__ = 'device_get'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id', ondelete='CASCADE'), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)

    device = relationship("Device", back_populates="device_gets")


class DeviceSend(Base):
    __tablename__ = 'device_send'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id', ondelete='CASCADE'), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)

    device = relationship("Device", back_populates="device_sends")


class Movement(Base):
    __tablename__ = 'movement'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('device.id', ondelete='CASCADE'), nullable=False)
    place_from: Mapped[int] = mapped_column(nullable=False)
    place_to: Mapped[int] = mapped_column(nullable=False)

    device = relationship("Device", back_populates="device_movement")
