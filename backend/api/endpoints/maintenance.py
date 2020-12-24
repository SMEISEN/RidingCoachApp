from datetime import datetime, timedelta
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.maintenance import MaintenanceModel, MaintenanceSchema
from backend.database.models.history import HistoryModel, HistorySchema
from backend.database.models.bike import BikeModel, BikeSchema
from flask_restplus import Resource, fields
from collections import defaultdict

ns = api.namespace('maintenance', description='Operations related to maintenance entries.')
history_schema = HistorySchema()
maintenance_schema = MaintenanceSchema()
bike_schema = BikeSchema()

maintenance_input_parameters = api.model('MaintenanceInputParameters', {
    "category":
        fields.String(description="maintenance work category according to bike module", required=True),
    "name":
        fields.String(description="maintenance work name", required=True),
    "interval_amount":
        fields.Float(description="interval of maintenance work", required=True),
    "interval_unit":
        fields.String(description="unit of maintenance interval", required=False),
    "interval_type":
        fields.String(description="type of maintenance interval", required=False),
    "tags_default":
        fields.Raw(description="default tags of maintenance work", required=False),
})
maintenance_query_parameters = api.model('MaintenanceQueryParameters', {
    "bike_id":
        fields.String(description="id of the bike where this maintenance belongs to", required=False),
    "category":
        fields.String(description="maintenance work category according to bike module", required=False),
    "name":
        fields.String(description="maintenance work name", required=False),
    "interval_amount":
        fields.Float(description="interval of maintenance work", required=False),
    "interval_unit":
        fields.String(description="unit of maintenance interval", required=False),
    "interval_type":
        fields.String(description="type of maintenance interval", required=False),
    "tags_default":
        fields.Raw(description="default tags of maintenance work", required=False),
})


def maintenance_state(maintenance_data, history_data, bike_operating_hours):

    interval_left = 0.0

    if maintenance_data['interval_unit'] == 'h':
        interval_left = history_data[0]['operating_hours'] - bike_operating_hours + maintenance_data['interval_amount']
        print(interval_left)

    elif maintenance_data['interval_unit'] == 'a':
        interval_left = (
            datetime.fromisoformat(history_data[0]['datetime_display']) -
            datetime.utcnow() +
            timedelta(days=365 * maintenance_data['interval_amount'])
        ).total_seconds()

    # interval "every x trainings" is omitted, could be integrated later
    # elif maintenance_data['interval_unit'] == 't':
    #     interval_left = (
    #         datetime.fromisoformat(history_data[0]['datetime_display']) -
    #         datetime.utcnow() +
    #         timedelta(days=1)
    #     ).total_seconds()

    state_left = interval_left / maintenance_data['interval_amount']

    return {
        'interval_left': interval_left,
        'state_left': state_left,
    }


def query_to_dict(maintenance_query: list, bike_id: str = None):
    """
    Re-formats the query to a structured dictionary, which can be json serialized.
    """

    maintenance_list = []
    for maintenance_entry in maintenance_query:

        maintenance_data = maintenance_schema.dump(maintenance_entry)

        if bike_id is None:
            maintenance_list.append(maintenance_data)

        else:
            history_data = history_schema.dump(maintenance_entry.history, many=True)
            history_data = list(filter(lambda d: d['bike_id'] in [bike_id], history_data))

            if len(history_data) > 0:
                maintenance_list.append({**maintenance_data, **history_data[0]})
            else:
                maintenance_list.append(maintenance_data)

    maintenance_categories_dict = defaultdict(lambda: defaultdict(dict))
    for item in maintenance_list:
        category = item['category']
        item.pop('category')
        name = item['name']
        item.pop('name')
        maintenance_categories_dict[category][name].update(item)

    return maintenance_categories_dict


@ns.route('/')
class MaintenanceCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns all maintenance work.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        maintenance_all = MaintenanceModel.query.order_by(MaintenanceModel.category.asc()).all()

        maintenance_categories_dict = query_to_dict(maintenance_all)

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(maintenance_input_parameters)
    @api.response(201, 'Maintenance work successfully added.')
    def post(self):
        """
        Creates a new maintenance work.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        new_maintenance = MaintenanceModel(
            category=inserted_data.get('category'),
            name=inserted_data.get('name'),
            interval_amount=inserted_data.get('interval_amount'),
            interval_unit=inserted_data.get('interval_unit'),
            interval_type=inserted_data.get('interval_type'),
            tags_default=inserted_data.get('tags_default'),
        )
        db.session.add(new_maintenance)
        db.session.commit()

        response = jsonify(new_maintenance.maintenance_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Maintenance work not found.')
class MaintenanceItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, f"Maintenance work with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a maintenance work.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()

        response = jsonify(maintenance_schema.dump(maintenance_work))
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(maintenance_input_parameters)
    @api.response(204, f"Maintenance work with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a maintenance work.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()

        if inserted_data.get('category') is not None:
            maintenance_work.category = inserted_data.get('category')
        if inserted_data.get('name') is not None:
            maintenance_work.name = inserted_data.get('name')
        if inserted_data.get('interval_amount') is not None:
            maintenance_work.interval_amount = inserted_data.get('interval_amount')
        if inserted_data.get('interval_unit') is not None:
            maintenance_work.interval_unit = inserted_data.get('interval_unit')
        if inserted_data.get('interval_type') is not None:
            maintenance_work.interval_type = inserted_data.get('interval_type')
        if inserted_data.get('tags_default') is not None:
            maintenance_work.interval_type = inserted_data.get('tags_default')
        if bool(inserted_data) is True:
            maintenance_work.datetime_last_modified = datetime.utcnow()

        db.session.add(maintenance_work)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, f"Maintenance work with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes maintenance work.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()

        db.session.delete(maintenance_work)
        db.session.commit()

        return None, 204


@ns.route('/query')
@api.response(404, 'Query parameters not found.')
class MaintenanceQuery(Resource):

    @api.doc(security='apikey')
    @api.expect(maintenance_query_parameters)
    def post(self):
        """
        Creates a filtered query based on the input json file and returns the requested data.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        requested = request.get_json()
        filter_by_data = {
            'bike_id': requested.get('bike_id'),
            'category': requested.get('category'),
            'name': requested.get('name'),
            'interval_unit': requested.get('interval_unit'),
            'interval_type': requested.get('interval_type'),
            'tags_default': requested.get('tags_default'),
        }
        filter_by_data = {key: value for (key, value) in filter_by_data.items() if value}

        maintenance_query = MaintenanceModel.query.filter_by(**filter_by_data)

        filter_data = {}
        if requested.get('interval_amount') is not None:
            filter_data['interval_amount'] = {
                'values': requested.get('interval_amount')['values'],
                'operators': requested.get('interval_amount')['operators'],
            }
        elif requested.get('tags_default') is not None:
            filter_data['tags_default'] = {
                'values': requested.get('tags_default')['values'],
                'operators': requested.get('tags_default')['operators'],
            }

        for attr, item in filter_data.items():
            for operator, value in zip(item['operators'], item['values']):
                if operator == '==':
                    maintenance_query = maintenance_query.filter(getattr(MaintenanceModel, attr) == value)
                elif operator == '<=':
                    maintenance_query = maintenance_query.filter(getattr(MaintenanceModel, attr) <= value)
                elif operator == '>=':
                    maintenance_query = maintenance_query.filter(getattr(MaintenanceModel, attr) >= value)
                elif operator == '<':
                    maintenance_query = maintenance_query.filter(getattr(MaintenanceModel, attr) < value)
                elif operator == '>':
                    maintenance_query = maintenance_query.filter(getattr(MaintenanceModel, attr) > value)
                elif operator == '!=':
                    maintenance_query = maintenance_query.filter(getattr(MaintenanceModel, attr) != value)
                else:
                    raise ValueError('Given operator does not match available operators!')

        maintenance_query = maintenance_query\
            .order_by(MaintenanceModel.category.asc()) \
            .order_by(MaintenanceModel.name.asc())\
            .order_by(MaintenanceModel.interval_type.asc())\
            .order_by(MaintenanceModel.interval_unit.asc())\
            .order_by(MaintenanceModel.interval_amount.asc())\
            .all()

        maintenance_categories_dict = query_to_dict(maintenance_query, requested.get('bike_id'))

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response


@ns.route('/warnings/<string:id_>')
class MaintenanceWarning(Resource):

    @api.doc(security='apikey')
    @api.response(200, f"Maintenance warnings successfully fetched.")
    def get(self, id_: str):
        """
        Returns the number of maintenance warnings.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        maintenance_query = MaintenanceModel.query.filter_by(**{'bike_id': id_}).all()
        bike_query = BikeModel.query.filter_by(**{'bike_id': id_}).all()

        bike_operating_hours = bike_schema.dump(bike_query, many=True)[0]['operating_hours']

        warning_count = {'warnings': 0}
        for maintenance_entry in maintenance_query:
            maintenance_data = maintenance_schema.dump(maintenance_entry)
            history_data = history_schema.dump(maintenance_entry.history, many=True)

            if len(history_data) > 0:
                state = maintenance_state(maintenance_data, history_data, bike_operating_hours)

                if state['interval_left'] <= 0:
                    warning_count['warnings'] += 1

        response = jsonify(warning_count)
        response.status_code = 200

        return response
