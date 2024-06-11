from typing import List,Optional
from sqlalchemy import ForeignKey, String,create_engine,MetaData
from sqlalchemy.orm import DeclarativeBase,relationship,Mapped,mapped_column



engine = create_engine("postgresql+psycopg2://shio:root1121@78.36.44.30:5432/teatr",echo=False,
pool_size=5,
max_overflow=10,
)
metadata = MetaData()
class Base(DeclarativeBase):
    pass

class Speki(Base):
    __tablename__ = "Speki"

    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[Optional[str]]
    date:Mapped[Optional[str]]
    time:Mapped[Optional[str]]
    info:Mapped[Optional[str]]

    #addresses: Mapped[List["Address"]] = relationship(
    #    back_populates="Speki",cascade="all, delete-orphan"
    #)

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, name={self.name!r}, date={self.date!r}, time={self.time!r}, info={self.info!r})"
    

Base.metadata.create_all(engine)