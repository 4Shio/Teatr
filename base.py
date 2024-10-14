from sqlalchemy.orm import Mapped,mapped_column
from config import Base
from datetime import datetime


class Speki(Base):
    __tablename__ = "Speki"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    date:Mapped[datetime]
    info:Mapped[str]
    weekday:Mapped[str]
    message_text:Mapped[str]
 

    def __repr__(self) -> str:
        return f"( {self.name!r} {self.date!r} {self.info!r}  {self.weekday!r})"
    
class user(Base):
    __tablename__ = 'User'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str]
    t_id:Mapped[float]
    role:Mapped[str]
    note:Mapped[bool]

    
