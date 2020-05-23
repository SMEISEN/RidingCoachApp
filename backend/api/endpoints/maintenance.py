from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.maintenance import MaintenanceModel, MaintenanceSchema
from flask_restplus import Resource
from collections import defaultdict

ns = api.namespace('maintenance', description='Operations related to blog posts')


@ns.route('/')
class MaintenanceResource(Resource):

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        maintenance_schema = MaintenanceSchema()
        maintenance_all = MaintenanceModel.query.all()

        maintenance_list = []
        for maintenance in maintenance_all:
            maintenance_list.append(maintenance_schema.dump(maintenance))

        maintenance_categories_dict = defaultdict(list)
        for item in maintenance_list:
            category = item['category']
            item.pop('category')
            maintenance_categories_dict[category].append(item)

        response = jsonify(maintenance_categories_dict)
        response.status_code = 200

        return response

    @api.response(201, 'Maintenance work successfully added.')
    def post(self):

        inserted_data = request.get_json()

        new_maintenance = MaintenanceModel(
            mtn_id=inserted_data['mtn_id'],
            category=inserted_data['category'],
            name=inserted_data['name'],
            hours_interval=inserted_data['hours_interval'],
            hours_last=inserted_data['hours_last'],
            hours_left=inserted_data['hours_left'],
            status=inserted_data['status'],
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
            datetime_display=datetime.utcfromtimestamp(inserted_data['datetime_display']/1000)
        )
        db.session.add(new_maintenance)
        db.session.commit()

        return 201

    @api.response(201, 'Maintenance successfully added.')
    def put(self):

        inserted_data = request.get_json()

        update_maintenance = MaintenanceModel.filter_by(mtn_id=inserted_data['mtn_id']).first()

        update_maintenance.hours_last = inserted_data['hours_last']
        update_maintenance.hours_left = inserted_data['hours_left']
        update_maintenance.datetime_display = datetime.utcfromtimestamp(inserted_data['datetime_display']/1000)
        update_maintenance.datetime_last_modified = datetime.utcnow()

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
        maintenance_schema = MaintenanceSchema()
        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.mtn_id == id_).one()

        response = jsonify(maintenance_schema.dump(maintenance_work))
        response.status_code = 200

        return response

    @api.response(204, f"Maintenance work with requested id successfully updated.")
    def put(self, id_):
        """
        Updates a maintenance work.
        """
        inserted_data = request.get_json()

        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.mtn_id == id_).one()
        maintenance_work.hours_last = inserted_data['hours_last']

        maintenance_work.datetime_last_modified = datetime.utcnow()

        db.session.add(maintenance_work)
        db.session.commit()

        return None, 204

    @api.response(204, f"Maintenance work with requested id successfully deleted.")
    def delete(self, id_):
        """
        Deletes maintenance work.
        """
        maintenance_work = MaintenanceModel.query.filter(MaintenanceModel.mtn_id == id_).one()

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
        maintenance_categories = MaintenanceModel.query\
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
        maintenance_schema = MaintenanceSchema()
        maintenance_of_category = MaintenanceModel.query.filter(MaintenanceModel.category == category).all()

        maintenance_list = []
        for maintenance in maintenance_of_category:
            maintenance_list.append(maintenance_schema.dump(maintenance))

        response = jsonify(maintenance_list)
        response.status_code = 200

        return response
