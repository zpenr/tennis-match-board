from waitress import serve
from src.routes.routes import app
from src.db.crud import create_tables


if __name__=='__main__':    
    # create_tables()
    serve(app, host = 'localhost', port = '8000')