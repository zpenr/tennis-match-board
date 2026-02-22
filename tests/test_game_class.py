from src.score_logic.match import Match
from src.score_logic.player import Player
import pytest

@pytest.mark.parametrize('player1_score, player1_last_balls, player2_score, player2_last_balls, result',
        [
            (40,1,30,0,True),
            (30,0,0,0,False),
            (40,1,40,0,False),
            (40,2,40,0,True)
        ])
def test_is_game_win(player1_score, player1_last_balls, player2_score, player2_last_balls, result):
    player1 = Player(player1_score, last_balls=player1_last_balls)
    player2 = Player(player2_score, last_balls=player2_last_balls)
    assert Match(player1,player2).is_game_win(player1,player2)==result

@pytest.mark.parametrize('player1_win_games, player2_win_games, result',
        [
            (6,4,True),
            (6,5,False),
            (7,5,True),
            (5,2,False)
        ])
def test_is_win_set(player1_win_games, player2_win_games, result):
    player1 = Player(win_games=player1_win_games)
    player2 = Player(win_games=player2_win_games)
    assert Match(player1,player2).is_win_set(player1) == result

@pytest.mark.parametrize('player_win_sets, result',
        [
            (1,False),
            (2,True)
        ])
def test_is_win_match(player_win_sets, result):
    player1 = Player(win_sets=player_win_sets)
    player2 = Player()
    assert Match(player1,player2).is_win_match(player1) == result
