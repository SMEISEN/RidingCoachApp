import email
import requests
from io import BytesIO
from flask import jsonify, request, current_app
from backend.api import api
from backend.database import db
from flask_restplus import Resource
from backend.api.routines.laptime import read_laptimesheet, validate_laptimes

ns = api.namespace('email', description='Operations related to received emails.')


@ns.route('/')
class EmailCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Email successfully received.')
    def post(self):
        """
        Receives emails containing training sessions.
        """

        header = bytes(str(request.headers).encode("utf-8"))
        body = request.get_data()

        msg = email.message_from_bytes(header + body)

        response = None
        for part in msg.walk():

            if part.get_content_maintype() == 'multipart':
                continue

            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            filetype = part.get_content_type()

            if filename is not None and \
                filetype == 'application/vnd.oasis.opendocument.spreadsheet':

                session_start_dt, \
                location_str, \
                application_str, \
                laptime_data = read_laptimesheet(BytesIO(part.get_payload(decode=True)))

                laptime_data = validate_laptimes(laptime_data)

                current_training_id, \
                current_bike_id, \
                current_setup_id = self.post_training(session_start_dt, location_str)

                current_session_id = self.post_session(current_training_id,
                                                       current_bike_id,
                                                       current_setup_id,
                                                       application_str,
                                                       session_start_dt)

                laptime_ids = self.post_laptimes(laptime_data, current_session_id)

                response = {
                    'session_id': current_session_id,
                    'bike_id': current_bike_id,
                    'setup_id': current_setup_id,
                    'laptime_ids': laptime_ids,
                }

        return response


    @staticmethod
    def post_training(session_start_dt, location_str):

        training_query = {
            'datetime_display': {
                'values': [
                    session_start_dt.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
                    ],
                'operators': ['>='],
            }
        }

        current_training = requests.post(
            url=f"http://{current_app.config['FLASK_BASE_URL']}/api/training/query",
            json=training_query,
            headers={'apikey': current_app.config['FLASK_RESTPLUS_API_KEY']},
            allow_redirects=True
        ).json()

        if len(current_training) > 0:
            current_training_id = current_training[0]['training_id']
            current_bike_id = current_training[0]['setups'][-1]['bike_id']
            current_setup_id = current_training[0]['setups'][-1]['setup_id']
        else:
            training_payload = {
                'location': location_str,
                'datetime_display': session_start_dt.timestamp(),
            }

            current_training_id = requests.post(
                url=f"http://{current_app.config['FLASK_BASE_URL']}/api/training",
                json=training_payload,
                headers={'apikey': current_app.config['FLASK_RESTPLUS_API_KEY']},
                allow_redirects=True,
            ).json()
            current_bike_id = None
            current_setup_id = None

        return current_training_id, current_bike_id, current_setup_id


    @staticmethod
    def post_session(
        current_training_id,
        current_bike_id,
        current_setup_id,
        application_str,
        session_start_dt):

        session_payload = {
            'training_id': current_training_id,
            'bike_id': current_bike_id,
            'setup_id': current_setup_id,
            'application': application_str,
            'datetime_display': session_start_dt.timestamp(),
        }

        current_session_id = requests.post(
            url=f"http://{current_app.config['FLASK_BASE_URL']}/api/session",
            json=session_payload,
            headers={'apikey': current_app.config['FLASK_RESTPLUS_API_KEY']},
            allow_redirects=True,
        ).json()

        return current_session_id


    @staticmethod
    def post_laptimes(laptime_data, current_session_id):

        laptime_ids = []
        for i, (lap_no, valid, track_layout, laptime_second, datetime_display) in\
            enumerate(zip(
                laptime_data.index.to_list(),
                laptime_data['valid'].to_list(),
                laptime_data['track_layout'].to_list(),
                laptime_data['laptime_seconds'].to_list(),
                laptime_data['datetime_display'].to_list())):

            sectors = {}
            for j, key in enumerate(laptime_data.iloc[:,5:].columns.to_list()):
                sectors[key] = laptime_data.iloc[i,5+j]

            laptime_payload = {
                'session_id': current_session_id,
                'lap_no': lap_no,
                'valid': valid,
                'track_layout': track_layout,
                'laptime_seconds': laptime_second,
                'sectors': sectors,
                'datetime_display': datetime_display.timestamp(),
            }

            current_laptime_id = requests.post(
                url=f"http://{current_app.config['FLASK_BASE_URL']}/api/laptime",
                json=laptime_payload,
                headers={'apikey': current_app.config['FLASK_RESTPLUS_API_KEY']},
                allow_redirects=True,
            ).json()
            laptime_ids.append(current_laptime_id)

        return laptime_ids
