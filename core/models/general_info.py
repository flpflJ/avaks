import array
from typing import List, Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RequestTable(Base):
    __tablename__ = 'RequestTable'

    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(nullable=True)
    email: Mapped[Optional[str]] = mapped_column(nullable=True)
    dron_usage: Mapped[Optional[str]] = mapped_column(nullable=True)
    dron_location: Mapped[Optional[str]] = mapped_column(nullable=True)
    dron_realtime: Mapped[Optional[str]] = mapped_column(nullable=True)
    dron_asset: Mapped[Optional[str]] = mapped_column(nullable=True)
    file_name: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    drag_file: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
