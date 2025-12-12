from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# ---------- AGSI ---------- #

class AgsiBase(BaseModel):
    date: datetime
    gas_in_storage_gwh: Optional[float] = None
    injection: Optional[float] = None
    withdrawal: Optional[float] = None
    working_gas_gwh: Optional[float] = None
    full_pct: Optional[float] = None
    trend: Optional[float] = None


class AgsiDB(AgsiBase):
    id: int
    version: int
    is_latest: bool
    created_date: datetime

    class Config:
        from_attributes = True   # pydantic v2: works with ORM objects


# ---------- ALSI ---------- #

class AlsiBase(BaseModel):
    date: datetime
    lng_storage_gwh: Optional[float] = None
    sendOut: Optional[float] = None
    dtmi_gwh: Optional[float] = None
    dtrs: Optional[float] = None
    contractedCapacity: Optional[float] = None
    availableCapacity: Optional[float] = None


class AlsiDB(AlsiBase):
    id: int
    version: int
    is_latest: bool
    created_date: datetime

    class Config:
        from_attributes = True
