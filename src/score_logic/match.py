import json
from src.score_logic.player import Player
class Match():

    IN_PROGRESS = 'in process'
    FINISHED = 'end'
    PLAYER1 = 'player1'
    PLAYER2 = 'player2'

    def __init__(self,player1 = None, player2 = None):
        self.player1 = player1
        self.player2 = player2
        self.match_status = Match.IN_PROGRESS

    def is_game_win(self,scorer, missed):
        return scorer.last_balls == 2 or (scorer.score == 40 and missed.score!=40)
            
    def is_win_set(self, player):
        return player.win_games >=6 and abs(self.player1.win_games - self.player2.win_games)>=2
 
    def is_win_match(self,player):
        return player.win_sets == 2
    
    @property
    def is_match_in_process(self):
        return self.match_status == Match.IN_PROGRESS

    def update_match_progress(self, scorer, missed):
        if self.is_game_win(scorer, missed):
            scorer.win_game()
            missed.lose_game()
            if self.is_win_set(scorer):
                scorer.win_set()
                missed.lose_set()
                if self.is_win_match(scorer):
                    scorer.win_match()
                    if scorer.is_match_win:
                        self.match_status = Match.FINISHED

    def serve(self,scorer_key: str):
        if self.is_match_in_process:
            if scorer_key == Match.PLAYER1:
                scorer = self.player1
                missed = self.player2
            elif scorer_key == Match.PLAYER2:
                scorer = self.player2
                missed = self.player1
            else:
                return
            
            scorer.add_point()
            missed.reset_last_balls()

            self.update_match_progress(scorer, missed)
    
    def to_json(self):
        template = {
            Match.PLAYER1:self.player1.to_dict(),
            Match.PLAYER2:self.player2.to_dict(),
            'match_status': self.match_status
        }
        return json.dumps(template)
    
    def load_from_dict(self, dict:dict):
        self.player1 = Player().load_from_dict(dict.get('player1'))
        self.player2 = Player().load_from_dict(dict.get('player2'))
        self.match_status = dict.get('match_status', Match.IN_PROGRESS)