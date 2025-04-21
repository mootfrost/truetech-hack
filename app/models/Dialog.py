from typing import Optional

from app.models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ARRAY, Text
from sqlalchemy.ext.mutable import MutableList



class Dialog(Base):
    __tablename__ = "dialogs"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(nullable=True)
    messages: Mapped[list] = mapped_column(MutableList.as_mutable(ARRAY(Text)))
