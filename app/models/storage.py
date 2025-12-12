from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, DateTime
from app.database import Base


class AgsiTimeseries(Base):
    __tablename__ = "agsi_timeseries"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(DateTime, index=True, nullable=False)

    gas_in_storage_gwh = Column(Float, nullable=True)
    injection = Column(Float, nullable=True)
    withdrawal = Column(Float, nullable=True)
    working_gas_gwh = Column(Float, nullable=True)
    full_pct = Column(Float, nullable=True)
    trend = Column(Float, nullable=True)

    version = Column(Integer, nullable=False, default=1)
    is_latest = Column(Boolean, nullable=False, default=True)

    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)


class AlsiTimeseries(Base):
    __tablename__ = "alsi_timeseries"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)

    date = Column(DateTime, index=True, nullable=False)

    lng_storage_gwh = Column(Float, nullable=True)
    sendOut = Column(Float, nullable=True)
    dtmi_gwh = Column(Float, nullable=True)
    dtrs = Column(Float, nullable=True)
    contractedCapacity = Column(Float, nullable=True)
    availableCapacity = Column(Float, nullable=True)

    version = Column(Integer, nullable=False, default=1)
    is_latest = Column(Boolean, nullable=False, default=True)

    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
