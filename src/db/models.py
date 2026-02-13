from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.db.database import Base 


class PlayersOrm(Base):
    __tablename__ = 'Players'
    ID: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str]



class MatchesOrm(Base):
    __tablename__ = 'Matches'
    ID: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    UUID: Mapped[str] = mapped_column(primary_key=True)
    Player1: Mapped[int] = mapped_column(ForeignKey('Players.ID'))
    Player2: Mapped[int] = mapped_column(ForeignKey('Players.ID'))
    Winner: Mapped[int|None] = mapped_column(ForeignKey('Players.ID'))
    Score: Mapped[str]
