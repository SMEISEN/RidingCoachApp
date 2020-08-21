from datetime import datetime
import email
from io import BytesIO
import ezodf
import requests
from flask import jsonify, request, current_app
from backend.api import api
from backend.database import db
from flask_restplus import Resource

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

        for part in msg.walk():

            if part.get_content_maintype() == 'multipart':
                continue

            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            filetype = part.get_content_type()

            if filename is not None and filetype == 'application/vnd.oasis.opendocument.spreadsheet':
                doc = ezodf.opendoc(BytesIO(part.get_payload(decode=True)))
                sheet_sectors = doc.sheets[0]
                sheet_channels = doc.sheets[2]
                channels_dict = {}
                channels_col_index = {}
                sectors_dict = {}
                sectors_col_index = {}
                session_start_str = 'undefined'
                session_start_dt = None
                location_str = 'undefined'
                application_str = 'undefined'
                for i, (row_sectors, row_channels) in enumerate(zip(sheet_sectors.rows(), sheet_channels.rows())):
                    if i == 2:
                        location_str = row_sectors[1].value
                        continue
                    if i == 4:
                        application_str = row_sectors[1].value
                        continue
                    if i == 6:
                        sectors_dict = {cell.value: [] for m, cell in enumerate(row_sectors) if m >= 3}
                        sectors_col_index = {n: cell.value for n, cell in enumerate(row_sectors) if n >= 3}
                        channels_dict = {cell.value: [] for k, cell in enumerate(row_channels) if k <= 3}
                        channels_col_index = {l: cell.value for l, cell in enumerate(row_channels) if l <= 3}
                        continue
                    if i == 10:
                        session_start_str = row_sectors[1].value
                        session_start_dt = datetime.strptime(session_start_str, '%d/%m/%Y %H:%M')
                    if i < 11:
                        continue
                    for j, (cell_channels, cell_sectors) in enumerate(zip(row_channels, row_sectors)):
                        if j <= 3:
                            cell_value = cell_channels.value
                            if j == 0:
                                cell_value = int(cell_value)
                            elif j == 1:
                                if ':' in cell_value:
                                    cell_value = cell_value.replace(',', '.')
                                    cell_value = (datetime.strptime(cell_value, '%M:%S.%f') -
                                                  datetime.strptime('00:00.0', '%M:%S.%f')).total_seconds()
                                else:
                                    cell_value = cell_value.replace(',', '.')
                                    cell_value = (datetime.strptime(cell_value, '%S.%f') -
                                                  datetime.strptime('00.0', '%S.%f')).total_seconds()
                            elif j == 2:
                                if ':' in cell_value:
                                    cell_value = cell_value.replace(',', '.').replace('+', '')
                                    cell_value = (datetime.strptime(cell_value, '%M:%S.%f') -
                                                  datetime.strptime('00:00.0', '%M:%S.%f')).total_seconds()
                                else:
                                    cell_value = cell_value.replace(',', '.').replace('+', '')
                                    cell_value = (datetime.strptime(cell_value, '%S.%f') -
                                                  datetime.strptime('00.0', '%S.%f')).total_seconds()
                            elif j == 3:
                                cell_value = datetime\
                                    .strptime(f"{session_start_str[0:10]} {cell_value}", '%d/%m/%Y %H:%M')
                            else:
                                cell_value = cell_channels.value
                            channels_dict[channels_col_index[j]].append(cell_value)
                        if j >= 3:
                            cell_value = cell_sectors.value
                            if not cell_value.strip():
                                cell_value = float(0)
                            else:
                                if ':' in cell_value:
                                    cell_value = cell_value.replace(',', '.')
                                    cell_value = (datetime.strptime(cell_value, '%M:%S.%f') -
                                                  datetime.strptime('00:00.0', '%M:%S.%f')).total_seconds()
                                else:
                                    cell_value = cell_value.replace(',', '.')
                                    cell_value = (datetime.strptime(cell_value, '%S.%f') -
                                                  datetime.strptime('00.0', '%S.%f')).total_seconds()
                            sectors_dict[sectors_col_index[j]].append(cell_value)
                lap_numbers = channels_dict.get('Lap')
                laptime_seconds = channels_dict.get('Full')
                datetimes_display = channels_dict.get('Start')

                training_query = {
                    'datetime_display': {
                        'values': [session_start_dt.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()],
                        'operators': ['>='],
                    }
                }
                current_training = requests.post(
                    url=f"http://{current_app.config['FLASK_BASE_URL']}/api/training/query",
                    json=training_query,
                    headers={'apikey': current_app.config['FLASK_RESTPLUS_API_KEY']},
                    allow_redirects=True
                ).json()
                if len(current_training) < 0:
                    current_training_id = current_training[0]['training_id']
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
                session_payload = {
                    'training_id': current_training_id,
                    'application': application_str,
                    'datetime_display': session_start_dt.timestamp(),
                }
                current_session_id = requests.post(
                    url=f"http://{current_app.config['FLASK_BASE_URL']}/api/session",
                    json=session_payload,
                    headers={'apikey': current_app.config['FLASK_RESTPLUS_API_KEY']},
                    allow_redirects=True,
                ).json()

                for i, (lap_no, laptime_second, datetime_display)\
                        in enumerate(zip(lap_numbers, laptime_seconds, datetimes_display)):
                    sectors = {}
                    for key, value in sectors_dict.items():
                        sectors[key] = value[i]
                    laptime_payload = {
                        'session_id': current_session_id,
                        'lap_no': lap_no,
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
