from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.maintenance import MaintenanceModel, MaintenanceSchema
from flask_restplus import Resource
from collections import defaultdict

ns = api.namespace('maintenance', description='Operations related to blog posts')
maintenance_schema = MaintenanceSchema()


@ns.route('/')
class MaintenanceResource(Resource):

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        maintenance_all = MaintenanceModel.query.order_by(MaintenanceModel.maintenance_id.asc()).all()

        maintenance_list = []
        for maintenance in maintenance_all:
            maintenance_list.append(maintenance_schema.dump(maintenance))

        maintenance_categories_dict = defaultdict(lambda: defaultdict(dict))
        for item in maintenance_list:
            category = item['category']
            item.pop('category')
            name = item['name']
            item.pop('name')
            maintenance_categories_dict[category][name].update(item)

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response

    @api.response(201, 'Maintenance work successfully added.')
    def post(self):

        inserted_data = request.get_json()

        new_maintenance = MaintenanceModel(
            maintenance_id=inserted_data['maintenance_id'],
            category=inserted_data['category'],
            name=inserted_data['name'],
            interval_amount=inserted_data['interval_amount'],
            interval_unit=inserted_data['interval_unit'],
            interval_latest=inserted_data['interval_latest'],
            interval_type=inserted_data['interval_type'],
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
            datetime_display=datetime.utcfromtimestamp(inserted_data['datetime_display'] / 1000)
        )
        db.session.add(new_maintenance)
        db.session.commit()

        return 201


@ns.route('/<int:id_>')
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


@ns.route('/category/list')
@api.response(404, 'Maintenance category list not found.')
class MaintenanceCategories(Resource):

    @api.response(200, f"Maintenance category list successfully fetched.")
    def get(self):
        """
        Returns a list of maintenance categories.
        """
        maintenance_categories = MaintenanceModel.query.with_entities(MaintenanceModel.category).distinct().all()
        maintenance_categories = list(zip(*maintenance_categories))

        response = jsonify(maintenance_categories)
        response.status_code = 200

        return response


@ns.route('/category/dict')
@api.response(404, 'Maintenance category dictionary not found.')
class MaintenanceCategories(Resource):

    @api.response(200, f"Maintenance category dictionary successfully fetched.")
    def get(self):
        """
        Returns a dicttionary of maintenance categories and their work names.
        """
        maintenance_categories = MaintenanceModel.query \
            .with_entities(MaintenanceModel.category, MaintenanceModel.name).all()

        maintenance_categories_dict = defaultdict(list)
        for key, value in sorted(maintenance_categories):
            maintenance_categories_dict[key].append(value)

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response


@ns.route('/category/<string:category>')
@api.response(404, 'Maintenance work not found.')
class MaintenanceCategoryItems(Resource):

    @api.response(200, f"Maintenance work with requested category successfully fetched.")
    def get(self, category):
        """
        Returns all maintenance work of a category.
        """
        maintenance_of_category = MaintenanceModel.query.filter(MaintenanceModel.category == category).all()

        maintenance_list = []
        for maintenance in maintenance_of_category:
            maintenance_list.append(maintenance_schema.dump(maintenance))

        response = jsonify(maintenance_list)
        response.status_code = 200

        return response
