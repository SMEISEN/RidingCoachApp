from backend.app import app, initialize_app
from backend.config import Config


if __name__ == '__main__':

    if Config.FLASK_ENV == 'development':
        initialize_app(app)
        app.run(host=Config.API_URL, port=Config.API_PORT, debug=True)

    else:
        initialize_app(app)
        app.run(host='0.0.0.0', debug=False)
