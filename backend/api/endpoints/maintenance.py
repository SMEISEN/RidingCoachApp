from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.maintenance import MaintenanceModel, MaintenanceSchema
from backend.database.models.history import HistoryModel, HistorySchema
from flask_restplus import Resource, fields
from collections import defaultdict

ns = api.namespace('maintenance', description='Operations related to maintenance entries.')
history_schema = HistorySchema()
maintenance_schema = MaintenanceSchema()

query_parameters = api.model('MaintenanceQueryParameters', {
    "bike_id":
        fields.String(description="", required=False),
    "category":
        fields.String(description="", required=False),
    "name":
        fields.String(description="", required=False),
    "interval_amount":
        fields.Float(description="", required=False),
    "interval_unit":
        fields.String(description="", required=False),
    "interval_type":
        fields.String(description="", required=False)
})


def query_to_dict(maintenance_query: list, bike_id: str = None):
    """
    Reformats the query to a structured dictionary, which can be json serialized.
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

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns all maintenance work.
        """

        maintenance_all = MaintenanceModel.query.order_by(MaintenanceModel.category.asc()).all()

        maintenance_categories_dict = query_to_dict(maintenance_all)

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response

    @api.response(201, 'Maintenance work successfully added.')
    def post(self):
        """
        Creates a new maintenance work.
        """

        inserted_data = request.get_json()

        new_maintenance = MaintenanceModel(
            category=inserted_data.get('category'),
            name=inserted_data.get('name'),
            interval_amount=inserted_data.get('interval_amount'),
            interval_unit=inserted_data.get('interval_unit'),
            interval_latest=inserted_data.get('interval_latest'),
            interval_type=inserted_data.get('interval_type')
        )
        db.session.add(new_maintenance)
        db.session.commit()

        return 201


@ns.route('/<string:maintenance_id>')
@api.response(404, 'Maintenance work not found.')
class MaintenanceItem(Resource):

    @api.response(200, f"Maintenance work with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a maintenance work.
        """

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()

        response = jsonify(maintenance_schema.dump(maintenance_work))
        response.status_code = 200

        return response

    @api.response(204, f"Maintenance work with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a maintenance work.
        """

        inserted_data = request.get_json()

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()
        maintenance_work.interval_latest = inserted_data.get('interval_latest')
        maintenance_work.datetime_last_modified = datetime.utcfromtimestamp(inserted_data.get('datetime_display') / 1000)

        db.session.add(maintenance_work)
        db.session.commit()

        return None, 204

    @api.response(204, f"Maintenance work with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes maintenance work.
        """

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()

        db.session.delete(maintenance_work)
        db.session.commit()

        return None, 204


@ns.route('/query')
@api.response(404, 'Query parameters not found.')
class MaintenanceQuery(Resource):

    @api.expect(query_parameters)
    def post(self):
        """
        Creates a filtered query based on the input json file and returns the requested data.
        """

        requested = request.get_json()
        filter_data = {
            'category': requested.get('category'),
            'name': requested.get('name'),
            'interval_amount': requested.get('interval_amount'),
            'interval_unit': requested.get('interval_unit'),
            'interval_type': requested.get('interval_type'),
        }
        filter_data = {key: value for (key, value) in filter_data.items() if value}

        maintenance_query = MaintenanceModel.query.filter_by(**filter_data).all()

        maintenance_categories_dict = query_to_dict(maintenance_query, requested.get('bike_id'))

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response
