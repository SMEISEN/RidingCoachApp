import os
from datetime import datetime
from flask import jsonify, request, redirect, url_for, current_app, render_template
from backend.src import app, db
from backend.src.models import Maintenance, Bike, History, MaintenanceSchema


@app.route('/')
@app.route('/home')
def index_client():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return render_template(entry)


@app.route('/api/maintenance/list', methods=['GET'])
def get_maintenance_data():
    maintenance_schema = MaintenanceSchema()
    maintenance = Maintenance.query.all()

    maintenance_list = []
    for item in maintenance:
        maintenance_list.append(maintenance_schema.dump(item))

    print(jsonify(maintenance_list))
    return jsonify(maintenance_list)


@app.route('/api/bike', methods=['GET'])
def get_bike_data():
    bike = Bike.query.all()
    return jsonify(bike)


@app.route('/api/history', methods=['GET'])
def get_history_data():
    history = History.query.all()
    return jsonify(history)


@app.route("/api/maintenance/new", methods=['POST'])
def post_history():
    inserted_data = request.get_json()

    print(f"inserted data {inserted_data}")

    new_maintenance = Maintenance(
        mtn_id=3,
        category=inserted_data['category'],
        name=inserted_data['name'],
        hours_interval=inserted_data['hours_interval'],
        date_last=datetime.utcnow(),
        hours_last=77.5,
        hours_left=5,
        status=80
    )

    print(f"push data {new_maintenance}")

    db.session.add(new_maintenance)
    db.session.commit()
    return redirect(url_for('home'))

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
