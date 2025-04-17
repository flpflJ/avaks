from typing import List

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
    name: str
    phone: str
    email: str
    field1: str
    field2: str
    field3: str
    field4: str
    file_name: str
    drag_file: bytes


class RequestTableCreate(RequestTableBase):
    pass


class RequestTable(RequestTableBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
