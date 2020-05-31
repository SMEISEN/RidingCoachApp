from datetime import datetime
from flask import jsonify, request
from flask_filter.query_filter import query_with_filters
from backend.api import api
from backend.database import db
from backend.database.models.maintenance import MaintenanceModel, MaintenanceSchema
from backend.database.models.history import HistoryModel, HistorySchema
from flask_restplus import Resource, fields
from collections import defaultdict

ns = api.namespace('maintenance', description='Operations related to blog posts')
history_schema = HistorySchema()
maintenance_schema = MaintenanceSchema()

search_parameters = api.model('Resource',
                              {
                                  "field": fields.String(description="cust ID", required=True),
                                  "op": fields.String(description="cust ID", required=True),
                                  "value": fields.String(description="cust ID", required=True)
                              })


def query_to_dict(maintenance_query):
    """
    Reformats the query to a structured dictonary, which can be json serialized.
    """

    maintenance_list = []
    for maintenance_entry in maintenance_query:
        history_data = history_schema.dump(
            maintenance_entry.history, many=True)
        maintenance_data = maintenance_schema.dump(maintenance_entry)
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
class MaintenanceResource(Resource):

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
            category=inserted_data['category'],
            name=inserted_data['name'],
            interval_amount=inserted_data['interval_amount'],
            interval_unit=inserted_data['interval_unit'],
            interval_latest=inserted_data['interval_latest'],
            interval_type=inserted_data['interval_type']
        )
        db.session.add(new_maintenance)
        db.session.commit()

        return 201


@ns.route('/<string:id_>')
@api.response(404, 'Maintenance work not found.')
class MaintenanceItem(Resource):

    @api.response(200, f"Maintenance work with requested id successfully fetched.")
    def get(self, id_):
        """
        Returns a maintenance work.
        """

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()

        response = jsonify(maintenance_schema.dump(maintenance_work))
        response.status_code = 200

        return response

    @api.response(204, f"Maintenance work with requested id successfully updated.")
    def put(self, id_):
        """
        Updates a maintenance work.
        """

        inserted_data = request.get_json()

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()
        maintenance_work.interval_latest = inserted_data['interval_latest']
        maintenance_work.datetime_last_modified = datetime.utcfromtimestamp(inserted_data['datetime_display'] / 1000)

        db.session.add(maintenance_work)
        db.session.commit()

        return None, 204

    @api.response(204, f"Maintenance work with requested id successfully deleted.")
    def delete(self, id_):
        """
        Deletes maintenance work.
        """

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.maintenance_id == id_).one()

        db.session.delete(maintenance_work)
        db.session.commit()

        return None, 204


@ns.route('/search')
@api.response(404, 'Searched entries not found.')
class MaintenanceSearch(Resource):

    @api.expect(search_parameters)
    def post(self):
        """
        Creates a filtered query based on the input json file and returns the requested data.
        """

        search = [request.get_json()]

        maintenance_searched = query_with_filters(MaintenanceModel, search, MaintenanceSchema)

        maintenance_categories_dict = query_to_dict(maintenance_searched)

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response
