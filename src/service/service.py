from src.db.crud import *
import uuid, json, math
from src.score_logic.match import Match
from varibals import *

def create_player(name:str):
    if select_player_by_name(name) is None:insert_player(name)
    
def create_match(player1_name:str, player2_name:str):
    create_player(player1_name)
    create_player(player2_name)
    player1_id = select_player_by_name(player1_name)[0]
    player2_id = select_player_by_name(player2_name)[0]
    match_id = uuid.uuid4()
    insert_match(player1_id,player2_id,match_id)
    return match_id

def get_match_info_player(match,player:int):
    score = json.loads(match.Score)
    player_name = player_name_by_id(getattr(match,f'Player{player}_id'))
    player_score = score.get(f'player{player}')
    data_player = [player_name, player_score]
    return data_player

def is_match_end(match):
    if match.Winner_id is None:
        return False
    return True

def get_match(uuid:str):
    match = select_match_by_uuid(uuid)

    data_player1 = get_match_info_player(match,player=1)
    data_player2 = get_match_info_player(match,player=2)
    if is_match_end(match):
        mutable = False
    else:
        mutable = True
    return data_player1, data_player2, mutable

def proccess_match(uuid, scorer):
    match = select_match_by_uuid(uuid)
    score = json.loads(match.Score)
    game = Match()
    game.load_from_dict(score)
    game.serve(scorer)
    new_score = game.to_json()
    update_match_score(uuid=uuid, score=new_score)
    if not game.in_process:
        if game.player1.is_match_win:
            update_match_winner(uuid=uuid, winner='player1')
        elif game.player2.is_match_win:
            update_match_winner(uuid=uuid, winner='player2')

def get_matches(page = 1, filter_by_player_name = None):
    page = int(page)
    if filter_by_player_name is None:
        table,all_writes_number = select_matches_with_names(start=(page-1)*WRITES_ON_PAGE)
    else: 
        table,all_writes_number = select_matches_by_name(filter_by_player_name,start=(page-1)*WRITES_ON_PAGE)

    pages_num = math.ceil(all_writes_number/WRITES_ON_PAGE)

    player1_names = list()
    player2_names = list()
    winners = list()

    for match in table:
        player1_names.append(match.Player1.Name)
        player2_names.append(match.Player2.Name)
        if match.Winner_id is None:
            winners.append('match in process')

        else:
            winners.append(match.Winner.Name)
    if len(table)>0:
        is_found = True
    else:
        is_found = False
    return player1_names, player2_names, winners, pages_num, is_found