from sqlalchemy import text, insert, update, delete,select
from src.db.database import engine,session_factory, Base
from src.db.models import PlayersOrm, MatchesOrm
import json 
BASE_SCORE = json.dumps({
            'player1':{
                "score": 0,
                "win_games": 0,
                "last_balls": 0,
                "win_sets": 0,
                "is_match_win":False
            },
            'player2':{
                "score": 0,
                "win_games": 0,
                "last_balls": 0,
                "win_sets": 0,
                "is_match_win":False
            },
            'match_status': 'in process'
        })
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

def insert_player(name: str):
    player = PlayersOrm(Name = name)
    with session_factory() as session:
        session.add(player)
        session.commit()

def insert_match(player_id1: int,  player_id2: int, UUID: str, score: str = BASE_SCORE, winner: str = None):
    match = MatchesOrm( UUID = UUID, Player1 = player_id1, Player2 = player_id2, Winner = winner, Score = score)
    with session_factory() as session:
        session.add(match)
        session.commit()
        print(session.execute(select(MatchesOrm.ID)).first())

def select_match_by_uuid(uuid: str):
    with session_factory() as session:
        query = select(MatchesOrm).where(MatchesOrm.UUID == uuid)
        match = session.execute(query).scalar()
        return match