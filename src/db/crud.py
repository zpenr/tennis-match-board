from sqlalchemy import text, insert, update, delete,select, label, or_, func
from sqlalchemy.orm import aliased, joinedload
from src.db.database import engine,session_factory, Base
from src.db.models import PlayersOrm, MatchesOrm
from src.errors_types import *
from varibals import *


def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def select_player_by_name(name: str):
    with session_factory() as session:
        query = (
            select(PlayersOrm.ID,
                   PlayersOrm.Name)
            .select_from(PlayersOrm)
            .filter_by(Name = name)
            )
        ans = session.execute(query)
        return ans.first()

def player_name_by_id(id: int):
    with session_factory() as session:
        query = select(PlayersOrm.Name).where(PlayersOrm.ID == id)
        name = session.execute(query).scalar()
        return name
    
def insert_player(name: str):
    player = PlayersOrm(Name = name)
    with session_factory() as session:
        session.add(player)
        session.commit()

def insert_match(player_id1: int,  player_id2: int, UUID: str, score: str = BASE_SCORE, winner: int = None):
    match = MatchesOrm( UUID = UUID, Player1_id = player_id1, Player2_id = player_id2, Winner_id = winner, Score = score)
    with session_factory() as session:
        session.add(match)
        session.commit()

def select_match_by_uuid(uuid: str):
    with session_factory() as session:
        query = select(MatchesOrm).options(joinedload(MatchesOrm.Player1),joinedload(MatchesOrm.Player2)).where(MatchesOrm.UUID == uuid)
        match = session.execute(query).scalar()
        return match

def update_match_score(uuid: str, score: str):
    with session_factory() as session:
        query = update(MatchesOrm).where(MatchesOrm.UUID == uuid).values(Score = score)
        session.execute(query)
        session.commit()

def select_matches_with_names(start:int = 0):
    with session_factory() as session:
        query = select(MatchesOrm).options(joinedload(MatchesOrm.Player1),joinedload(MatchesOrm.Player2),joinedload(MatchesOrm.Winner)).offset(start).limit(WRITES_ON_PAGE)
        all_writes_number = int(session.scalar(select(func.count()).select_from(MatchesOrm)))
        return session.execute(query).scalars().all(), all_writes_number
    
def select_matches_by_name(name:str, start:int):
    with session_factory() as session:
        p1 = aliased(PlayersOrm)
        p2 = aliased(PlayersOrm)
        base_query = (
            select(MatchesOrm)
            .join(p1,p1.ID == MatchesOrm.Player1_id)
            .join(p2,p2.ID == MatchesOrm.Player2_id)
            .filter(or_(p1.Name == name, p2.Name == name))
            
            )
        range_query = (
            base_query
            .options(
                joinedload(MatchesOrm.Player1)
                ,joinedload(MatchesOrm.Player2)
                ,joinedload(MatchesOrm.Winner)
                )
            .limit(WRITES_ON_PAGE)
            .offset(start)
        )
        all_writes_number = session.scalar(select(func.count()).select_from(base_query.subquery()))
        return session.execute(range_query).scalars().all(), all_writes_number
    
def update_match_winner(uuid: str ,winner: str):
    with session_factory() as session:
        if winner == 'player1':
            query = update(MatchesOrm).where(MatchesOrm.UUID == uuid).values(Winner_id = MatchesOrm.Player1_id)
        elif winner == 'player2':
            query = update(MatchesOrm).where(MatchesOrm.UUID == uuid).values(Winner_id = MatchesOrm.Player2_id)
        else:
            raise DBErrors
        session.execute(query)
        session.commit()