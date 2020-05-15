from backend.src import app
from backend.config import Config


if __name__ == '__main__':

    if Config.FLASK_ENV == 'development':
        app.run(debug=True)

    else:
        app.run(host='0.0.0.0', debug=False)
