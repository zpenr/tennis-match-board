from sqlalchemy import text, insert, update, delete,select
from src.db.database import engine,session_factory, Base
from src.db.models import PlayersOrm, MatchesOrm

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
        print(ans.first())

def insert_player(name: str):
    player = PlayersOrm(Name = name)
    with session_factory() as session:
        session.add(player)
        session.commit()

def insert_match(player_id1: int,  player_id2: int, UUID: str, score: int, winner: str = None):
    match = MatchesOrm( UUID = UUID, Player1 = player_id1, Player2 = player_id2, Winner = winner, Score = score)
    with session_factory() as session:
        session.add(match)
        session.commit()
        print(session.execute(select(MatchesOrm.ID)).first())

# create_tables()
# insert_match(1,2,'qwtery',"12")