from backend.app import create_app
from backend.config import Config


if __name__ == '__main__':

    app = create_app(Config)

    if Config.FLASK_ENV == 'development':
        app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=True)

    else:
        app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=False)
