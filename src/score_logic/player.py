class Player():
    def __init__(self, score = 0, win_games= 0, last_balls= 0, win_sets= 0, is_match_win = False):
        self.score: int = score
        self.win_games: int = win_games
        self.last_balls: int = last_balls
        self.win_sets: int = win_sets
        self.is_match_win: bool = is_match_win

    def add_point(self, is_tiebreak=False):
        if is_tiebreak:
            self.score += 1
            return
        
        if self.score < 30: 
            self.score += 15 
        elif self.score == 30:
            self.score = 40
        elif self.score == 40:
            self.last_balls += 1
    
    def reset_last_balls(self):
        self.last_balls = 0

    def win_game(self):
        self.score = 0
        self.last_balls = 0
        self.win_games +=1

    def lose_game(self):
        self.score = 0
        self.last_balls = 0

    def win_set(self):
        self.win_games = 0
        self.win_sets +=1

    def lose_set(self):
        self.win_games = 0

    def win_match(self):
        self.is_match_win = True

    def to_dict(self):
        template = {
            "score": self.score,
            "win_games": self.win_games,
            "last_balls": self.last_balls,
            "win_sets": self.win_sets,
            "is_match_win":self.is_match_win
        }
        return template
    
    def load_from_dict(self,dict: dict):
        self.score = dict.get('score',0)
        self.win_games = dict.get('win_games',0)
        self.last_balls = dict.get('last_balls',0)
        self.win_sets = dict.get('win_sets',0)
        self.is_match_win = dict.get('is_match_win',False)