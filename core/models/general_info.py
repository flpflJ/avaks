from sqlalchemy.orm import Mapped

from .base import Base


class RequestTable(Base):
    __tablename__ = 'RequestTable'

    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    field1: Mapped[str]
    field2: Mapped[str]
    field3: Mapped[str]
    field4: Mapped[str]
    drag_file: Mapped[bytes]
