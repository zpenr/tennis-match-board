from src.wsgi.app import App
from ..render_templates import render_template

app = App()


@app.route('/')
def post():
    return render_template('main.html')

@app.route('/match-score')
def test():
    return 'da'

@app.route('/static/main.css')
def style():
    with open('src/static/main.css') as f:
        return f.read()