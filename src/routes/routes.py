from src.wsgi.app import App, Redirect
from ..render_templates import render_template
import src.service.service as service

app = App()


@app.route('/')
def post():
    return render_template('main.html')

@app.route('/match-score')
def match_score_get(uuid):

    data_player1, data_player2, mutable = service.get_match(uuid)

    return render_template('match-score.html', name1 = data_player1[0], name2 = data_player2[0], player1 = data_player1[1], player2 = data_player2[1] , mutable = mutable)

@app.route('/match-score', request_method='POST')
def match_score_post(uuid, scorer):

    service.proccess_match(uuid, scorer)

    return Redirect(f'/match-score?uuid={uuid}')

@app.route('/new-match')
def create_match_get(): 
    return render_template('create-match.html')

@app.route('/new-match', request_method='POST')
def create_match_post(name1,name2):
    
    match_id = service.create_match(name1,name2)

    return Redirect(f'/match-score?uuid={match_id}')

@app.route('/matches')
def all_matches(page = 1, filter_by_player_name = None):
    
    player1_names, player2_names, winners, pages_num, is_found = service.get_matches(page,filter_by_player_name)

    return render_template('all-matches.html', player1_names = player1_names, player2_names = player2_names, winners = winners, page = int(page), pages_num = pages_num, filter_by_player_name = filter_by_player_name, is_found = is_found)

@app.route('/static/main.css')
def style():
    with open('src/static/main.css') as f:
        return f.read()