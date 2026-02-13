from src.wsgi.app import App
from ..render_templates import render_template
from src.db.crud import insert_match, select_player_by_name, insert_player
import uuid
app = App()


@app.route('/')
def post():
    return render_template('main.html')

@app.route('/match-score')
def test():
    return 'da'

@app.route('/new-match')
def create_match():
    return render_template('create-match.html')

@app.route('/new-match', request_method='POST')
def create_match(data):
    player_name1 = data['name1'][0]
    player_name2 = data['name2'][0]

    if not(select_player_by_name(player_name1)):insert_player(player_name1)
    if not(select_player_by_name(player_name2)):insert_player(player_name2)

    player_id1 = select_player_by_name(player_name1)[0]
    player_id2 = select_player_by_name(player_name2)[0]

    insert_match(player_id1,player_id2,uuid.uuid4())

    return render_template('create-match.html')


@app.route('/static/main.css')
def style():
    with open('src/static/main.css') as f:
        return f.read()