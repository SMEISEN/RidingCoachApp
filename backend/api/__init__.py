from flask_restplus import Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'apikey'
    }
}

api = Api(version='1.0', title='Riding-Coach PostgreSQL APK',
          description='Flask RestPlus powered API', authorizations=authorizations)
