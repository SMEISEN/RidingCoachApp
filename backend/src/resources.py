from datetime import datetime
from flask import jsonify, request, redirect, url_for
from backend.src import db
from backend.src.models import MaintenanceModel, MaintenanceSchema, HistoryModel, HistorySchema, BikeModel
from flask_restplus import Resource


class MaintenanceResource(Resource):

    def get(self):
        maintenance_schema = MaintenanceSchema()
        maintenance = MaintenanceModel.query.all()

        maintenance_list = []
        for item in maintenance:
            maintenance_list.append(maintenance_schema.dump(item))

        return jsonify(maintenance_list)


class HistoryResource(Resource):

    def get(self):
        history_schema = HistorySchema()
        history = HistoryModel.query.all()

        history_list = []
        for item in history:
            history_list.append(history_schema.dump(item))

        return jsonify(history_list)

    def post(self):

        inserted_data = request.get_json()
        new_maintenance = MaintenanceModel(
            mtn_id=3,
            category=inserted_data['category'],
            name=inserted_data['name'],
            hours_interval=inserted_data['hours_interval'],
            date_last=datetime.utcnow(),
            hours_last=77.5,
            hours_left=5,
            status=80
        )
        db.session.add(new_maintenance)
        db.session.commit()
        return redirect(url_for('home'))


class BikeResource(Resource):

    def get(self):
        bike = BikeModel.query.all()
        pass

    def post(self):
        pass

# @app.route('/api/bike', methods=['GET'])
# def get_bike_data():
#     bike = Bike.query.all()
#     return jsonify(bike)
#
#
# @app.route('/api/history', methods=['GET'])
# def get_history_data():
#     history = History.query.all()
#     return jsonify(history)


# @app.route('/api/maintenance/<int:mtn_id>/update"', methods=['GET', 'POST'])
# def update_maintenance(mtn_id):
#     mtn = Maintenance.query.get_or_404(mtn_id)
#
#     mtn.date_last =
#     mtn.hours_last =
#     mtn.hours_left =
#     mtn.status = mtn.hours_left/mtn.hours_interval * 100.0
#
#     db.session.commit()
#     flash('Your post has been updated!', 'success')
#     return redirect(url_for('home'))


# @app.route('/api/maintenance/<int:mtn_id>/update"', methods=['GET', 'POST'])
# def update_maintenance(mtn_id):
#     mtn = Maintenance.query.get_or_404(mtn_id)
#
#     mtn.date_last =
#     mtn.hours_last =
#     mtn.hours_left =
#     mtn.status = mtn.hours_left/mtn.hours_interval * 100.0
#
#     db.session.commit()
#     flash('Your post has been updated!', 'success')
#     return redirect(url_for('home'))


# @app.route("/api/history/new", methods=['GET', 'POST'])
# def post_history():
#     new_hist = History(
#         hist_id = ,
#         category = ,
#         name = ,
#         date = ,
#         hours = ,
#         comment = ,
#     )
#     db.session.add(new_hist)
#     db.session.commit()
#     return redirect(url_for('home'))
