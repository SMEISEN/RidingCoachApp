from datetime import datetime, timedelta, timezone
from flask import jsonify, request
from flask_restplus import Resource, fields
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.maintenance import MaintenanceModel, MaintenanceSchema
from backend.database.models.history import HistorySchema
from backend.database.models.bike import BikeModel, BikeSchema
from backend.api.routines.common import query_intervals
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import ARRAY
from collections import defaultdict

ns = api.namespace('maintenance', description='Operations related to maintenance entries.')
history_schema = HistorySchema()
maintenance_schema = MaintenanceSchema()
bike_schema = BikeSchema()

maintenance_input_parameters = api.model('MaintenanceInputParameters', {
    "category":
        fields.String(description="maintenance work category according to bike module",
                      required=True, example="maintenance category"),
    "name":
        fields.String(description="maintenance work name", required=True, example="maintenance name"),
    "interval_amount":
        fields.Float(description="interval of maintenance work", required=True, example=10.0),
    "interval_unit":
        fields.String(description="unit of maintenance interval", required=False, example="h"),
    "interval_type":
        fields.String(description="type of maintenance interval", required=False, example="planned maintenance"),
    "tags_default":
        fields.Raw(description="default tags of maintenance work", required=False, example=[
            "checked",
            "fixed",
            "replaced",
        ]),
})
maintenance_query_parameters = api.model('MaintenanceQueryParameters', {
    "bike_id":
        fields.String(description="id of the bike where this maintenance belongs to", required=False, example="UUID4"),
    "category":
        fields.String(description="maintenance work category according to bike module",
                      required=False, example="maintenance category"),
    "name":
        fields.String(description="maintenance work name", required=False, example="maintenance name"),
    "interval_amount":
        fields.Raw(description="interval of maintenance work", required=False, example={
            "values": [5, 10],
            "operators": ['>=', '<='],
        }),
    "interval_unit":
        fields.String(description="unit of maintenance interval", required=False, example="h"),
    "interval_type":
        fields.String(description="type of maintenance interval", required=False, example="planned maintenance"),
    "tags_default":
        fields.Raw(description="default tags of maintenance work", required=False, example=["checked", "fixed"]),
})


def maintenance_state(maintenance_data, history_data, bike_operating_hours):
    state_left = None
    interval_left = None

    if maintenance_data['interval_unit'] == 'h':
        interval_left = history_data[0]['operating_hours'] - bike_operating_hours + maintenance_data['interval_amount']
        state_left = interval_left / maintenance_data['interval_amount']

    elif maintenance_data['interval_unit'] == 'a':
        interval_left = (
                datetime.fromisoformat(history_data[0]['datetime_display']) -
                datetime.now(timezone.utc) +
                timedelta(days=365 * maintenance_data['interval_amount'])
        )
        state_left = interval_left / timedelta(days=365 * maintenance_data['interval_amount'])
        interval_left = interval_left.days

    # interval "every x trainings" is omitted, could be integrated later
    # elif maintenance_data['interval_unit'] == 't':
    #     interval_left = (
    #         datetime.fromisoformat(history_data[0]['datetime_display']) -
    #         datetime.now(timezone.utc) +
    #         timedelta(days=1)
    #     ).total_seconds()

    return {
        'absolute': interval_left,
        'relative': state_left,
    }


def query_to_dict(maintenance_query: list, bike_operating_hours: float = None, bike_id: str = None):
    """
    Re-formats the query to a structured dictionary, which can be json serialized.
    """

    maintenance_list = []
    for maintenance_entry in maintenance_query:

        maintenance_data = maintenance_schema.dump(maintenance_entry)
        interval_state = {
            'absolute': None,
            'relative': None,
        }

        if bike_id is None:
            maintenance_data['interval_state'] = interval_state
            maintenance_list.append(maintenance_data)

        else:
            history_data = history_schema.dump(maintenance_entry.history, many=True)
            history_data = list(filter(lambda d: d['bike_id'] in [bike_id], history_data))

            if len(history_data) > 0:
                if bike_operating_hours is not None:
                    interval_state = maintenance_state(
                        maintenance_data=maintenance_data,
                        history_data=history_data,
                        bike_operating_hours=bike_operating_hours)
                maintenance_data['interval_state'] = interval_state
                maintenance_list.append({**maintenance_data, **history_data[0]})
            else:
                maintenance_data['interval_state'] = interval_state
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

        maintenance_categories_dict = query_to_dict(maintenance_query=maintenance_all)

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
            bike_id=inserted_data.get('bike_id'),
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

        if inserted_data.get('bike_id', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_work.bike_id = inserted_data.get('bike_id')
        if inserted_data.get('category', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_work.category = inserted_data.get('category')
        if inserted_data.get('name', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_work.name = inserted_data.get('name')
        if inserted_data.get('interval_amount', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_work.interval_amount = inserted_data.get('interval_amount')
        if inserted_data.get('interval_unit', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_work.interval_unit = inserted_data.get('interval_unit')
        if inserted_data.get('interval_type', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_work.interval_type = inserted_data.get('interval_type')
        if inserted_data.get('tags_default', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_work.tags_default = inserted_data.get('tags_default')

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
        }
        filter_by_data = {key: value for (key, value) in filter_by_data.items() if value is not None}

        maintenance_query = MaintenanceModel.query.filter_by(**filter_by_data)

        maintenance_query, filter_data = query_intervals(filter_keys=[
            "interval_amount",
        ], query=maintenance_query, request=requested, model=MaintenanceModel)

        filtered_special = False
        bike_operating_hours = None
        if requested.get('bike_id', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            bike_query = BikeModel.query.filter_by(**{'bike_id': requested.get('bike_id')}).all()
            bike_operating_hours = bike_schema.dump(bike_query, many=True)[0]['operating_hours']
            filtered_special = True

        if requested.get('tags_default', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            maintenance_query = maintenance_query \
                .filter(MaintenanceModel.tags_default.contains(cast(requested.get('tags_default'), ARRAY(db.String))))
            filtered_special = True

        if bool(filter_data) is False and bool(filter_by_data) is False and filtered_special is False:
            response = jsonify([])
            response.status_code = 404

            return response

        maintenance_query = maintenance_query \
            .order_by(MaintenanceModel.category.asc()) \
            .order_by(MaintenanceModel.name.asc()) \
            .order_by(MaintenanceModel.interval_type.asc()) \
            .order_by(MaintenanceModel.interval_unit.asc()) \
            .order_by(MaintenanceModel.interval_amount.asc()) \
            .all()

        maintenance_categories_dict = query_to_dict(
            maintenance_query=maintenance_query,
            bike_operating_hours=bike_operating_hours,
            bike_id=requested.get('bike_id')
        )

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

        warnings = {
            'warnings': 0,
            'overdue_maintenance': [],
        }
        for maintenance_entry in maintenance_query:
            maintenance_data = maintenance_schema.dump(maintenance_entry)
            history_data = history_schema.dump(maintenance_entry.history, many=True)

            if len(history_data) > 0:
                state = maintenance_state(maintenance_data, history_data, bike_operating_hours)

                if state['absolute'] and state['absolute'] <= 0:
                    warnings['warnings'] += 1
                    warnings['overdue_maintenance'].append({**maintenance_data, **history_data[0]})

        response = jsonify(warnings)
        response.status_code = 200

        return response
