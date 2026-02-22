from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.db.database import Base 
from typing import Optional

class PlayersOrm(Base):
    __tablename__ = 'Players'
    ID: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str]= mapped_column(index=True, unique=True)

class MatchesOrm(Base):
    __tablename__ = 'Matches'
    ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    UUID: Mapped[str] = mapped_column(index=True, unique=True)

    Player1_id: Mapped[int] = mapped_column(ForeignKey("Players.ID"))
    Player2_id: Mapped[int] = mapped_column(ForeignKey("Players.ID"))
    Winner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("Players.ID"))

    Player1: Mapped[Optional["PlayersOrm"]] = relationship("PlayersOrm",foreign_keys=Player1_id)
    Player2: Mapped[Optional["PlayersOrm"]] = relationship("PlayersOrm",foreign_keys=Player2_id)
    Winner: Mapped[Optional["PlayersOrm"]] = relationship("PlayersOrm",foreign_keys=Winner_id)

    Score: Mapped[str]