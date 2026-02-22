import json
WRITES_ON_PAGE = 5
NO_WINNER = '$NO_WINNNER$'
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
            'in_process': True 
        })