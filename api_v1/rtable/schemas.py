from typing import List, Optional

from pydantic import BaseModel, ConfigDict

class EquipItems(BaseModel):
    name: str
    cnt: int
    price_one: int

class LLMRespBase(BaseModel):
    smeta: int
    drone_model: List[EquipItems]
    additional: List[EquipItems]
    recommendation: str

class LLMReqBase(BaseModel):
    prompt: str


class RequestTableBase(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    dron_usage: Optional[str] = None
    dron_location: Optional[str] = None
    dron_realtime: Optional[str] = None
    dron_asset: Optional[str] = None
    file_name: Optional[list[str]] = None
    drag_file: Optional[list[str]] = None


class RequestTableCreate(RequestTableBase):
    pass


class RequestTable(RequestTableBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
