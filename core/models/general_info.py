from sqlalchemy.orm import Mapped

from .base import Base


class RequestTable(Base):
    __tablename__ = 'RequestTable'

    name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    #4 fields Mapped[str]
    drag_file: Mapped[bytes]
