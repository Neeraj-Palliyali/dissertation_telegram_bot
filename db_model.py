from datetime import datetime

from sqlalchemy import DateTime, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class db_conn:

    def __init__(self) -> None:
        self.engine = create_engine("sqlite+pysqlite:///toxic.db", echo=False)
        Base.metadata.create_all(self.engine)

    async def add_row(self, vals):
        this_row = ToxicMessage(toxic_text=vals.get("toxic_text"),
                                neutered_text=vals.get("neutered_text"),
                                sender=vals.get("sender"),
                                incident_date=vals.get("incident_date"))
        with Session(self.engine) as session:
            session.add(this_row)
            session.commit()


class Base(DeclarativeBase):
    pass


class ToxicMessage(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    toxic_text: Mapped[str] = mapped_column(String, index=False,)
    neutered_text: Mapped[str] = mapped_column(
        String, index=True, nullable=True)
    sender: Mapped[str] = mapped_column(String)
    incident_date: Mapped[datetime] = mapped_column(DateTime)
