from flask import jsonify, current_app


def validate_api_key(apikey):
    if not apikey == current_app.config['FLASK_RESTPLUS_API_KEY']:
        response = jsonify({'message': 'Invalid or missing api key'})
        response.status_code = 401
        return response
    else:
        response = jsonify({'message': 'Valid api key'})
        response.status_code = 200
        return response
