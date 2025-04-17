from pydantic import BaseModel, ConfigDict


class RequestTableBase(BaseModel):
    name: str
    phone: str
    email: str
    field1: str
    field2: str
    field3: str
    field4: str
    drag_file: bytes


class RequestTableCreate(RequestTableBase):
    pass


class RequestTable(RequestTableBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
