from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.database import db
from backend.database.models.maintenance import MaintenanceModel, MaintenanceSchema
from flask_restplus import Resource

ns = api.namespace('maintenance/list', description='Operations related to blog posts')


@ns.route('/')
class MaintenanceResource(Resource):

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        maintenance_schema = MaintenanceSchema()
        maintenance = MaintenanceModel.query.all()

        maintenance_list = []
        for item in maintenance:
            maintenance_list.append(maintenance_schema.dump(item))

        response = jsonify(maintenance_list)
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
            date_last=inserted_data['date_last'],
            hours_last=inserted_data['hours_last'],
            hours_left=inserted_data['hours_left'],
            status=inserted_data['status']
        )
        db.session.add(new_maintenance)
        db.session.commit()

        return 201

    @api.response(201, 'Maintenance successfully added.')
    def put(self):

        inserted_data = request.get_json()

        update_maintenance = MaintenanceModel.filter_by(mtn_id=inserted_data['mtn_id']).first()

        update_maintenance.date_last=datetime.utcnow()
        update_maintenance.hours_last=inserted_data['hours_last']
        update_maintenance.hours_left=inserted_data['hours_left']
        update_maintenance.status=inserted_data['hours_left']/inserted_data['hours_interval']

        db.session.commit()

        return 201
