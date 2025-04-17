from pydantic import BaseModel, ConfigDict


class RequestTableBase(BaseModel):
    name: str
    phone: str
    email: str
    # 4 fields Mapped[str]
    drag_file: bytes


class RequestTableCreate(RequestTableBase):
    pass


class RequestTable(RequestTableBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
