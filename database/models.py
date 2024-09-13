from sqlalchemy import String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Device(Base):
    __tablename__ = 'device'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(50), nullable=False)
    # number: Mapped[float] = mapped_column(Float(asdecimal=False), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    firma: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(Text)
