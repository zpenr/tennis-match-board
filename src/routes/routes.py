from src.wsgi.app import App, Redirect
from ..render_templates import render_template
from src.db.crud import insert_match, select_player_by_name, insert_player, select_match_by_uuid
import uuid
from src.score_logic.match import Match
from src.score_logic.player import Player

app = App()


@app.route('/')
def post():
    return render_template('main.html')

@app.route('/match-score')
def test(uuid):
    print(uuid.strip())
    match = select_match_by_uuid(uuid)
    return render_template('match-score.html', name1 = match.Player1, name2 = match.Player2, score = match.Score)

@app.route('/new-match')
def create_match(): 
    return render_template('create-match.html')

@app.route('/new-match', request_method='POST')
def create_match(name1,name2):

    if not(select_player_by_name(name1)):insert_player(name1)
    if not(select_player_by_name(name2)):insert_player(name2)

    player_id1 = select_player_by_name(name1)[0]
    player_id2 = select_player_by_name(name2)[0]

    match_id = uuid.uuid4()
    insert_match(player_id1,player_id2,match_id)
    
    return Redirect(f'/match-score?uuid={match_id}')


@app.route('/static/main.css')
def style():
    with open('src/static/main.css') as f:
        return f.read()