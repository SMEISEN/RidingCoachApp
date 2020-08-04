from datetime import datetime
from flask import jsonify, request
from backend.database.models.bike import BikeModel, BikeSchema
from flask_restplus import Resource, fields
from backend.api import api
from backend.database import db

ns = api.namespace('bike', description='Operations related to bike entries.')
bike_schema = BikeSchema()

bike_input_parameters = api.model('BikeInputParameters', {
    "operating_hours":
        fields.Float(description="operating hours", required=True),
    "manufacturer":
        fields.String(description="bike manufacturer", required=True),
    "model":
        fields.String(description="bike model", required=True),
    "year":
        fields.Integer(description="bike year", required=True),
    "ccm":
        fields.Float(description="engine size", required=False),
    "stroke":
        fields.Float(description="engine stroke", required=False),
    "piston":
        fields.Float(description="engine piston", required=False),
    "slick_front_name":
        fields.String(description="name of front slick tire", required=False),
    "slick_front_notes":
        fields.String(description="front slick tire application notes", required=False),
    "slick_front_pressure":
        fields.Float(description="recommended pressure of front slick tire", required=False),
    "slick_rear_name":
        fields.String(description="name of rear slick tire", required=False),
    "slick_rear_notes":
        fields.String(description="rear slick tire application notes", required=False),
    "slick_rear_pressure":
        fields.Float(description="recommended pressure of rear slick tire", required=False),
    "rain_front_name":
        fields.String(description="name of front rain tire", required=False),
    "rain_front_notes":
        fields.String(description="front rain tire application notes", required=False),
    "rain_front_pressure":
        fields.Float(description="recommended pressure of front rain tire", required=False),
    "rain_rear_name":
        fields.String(description="name of rear rain tire", required=False),
    "rain_rear_notes":
        fields.String(description="rear rain tire application notes", required=False),
    "rain_rear_pressure":
        fields.Float(description="recommended pressure of rear rain tire", required=False),
    "setup":
        fields.Raw(description="bike suspension and engine setup", required=False),
})


@ns.route('/')
class BikeCollection(Resource):

    @api.response(200, 'Maintenance work list successfully fetched.')
    def get(self):
        """
        Returns a list the bike characteristics.
        """

        bike_all_entries = BikeModel.query.all()

        bike_list = []
        for bike_entry in bike_all_entries:
            bike_list.append(bike_schema.dump(bike_entry))

        response = jsonify(bike_list)
        response.status_code = 200

        return response

    @api.expect(bike_input_parameters)
    @api.response(201, 'Bike successfully added.')
    def post(self):
        """
        Adds a bike entry.
        """

        inserted_data = request.get_json()

        new_bike = BikeModel(
            operating_hours=inserted_data.get('operating_hours'),
            manufacturer=inserted_data.get('manufacturer'),
            model=inserted_data.get('model'),
            year=inserted_data.get('year'),
            ccm=inserted_data.get('ccm'),
            stroke=inserted_data.get('stroke'),
            piston=inserted_data.get('piston'),
            slick_front_name=inserted_data.get('slick_front_name'),
            slick_front_notes=inserted_data.get('slick_front_pressure_notes'),
            slick_front_pressure=inserted_data.get('slick_front_pressure'),
            slick_rear_name=inserted_data.get('slick_rear_name'),
            slick_rear_notes=inserted_data.get('slick_rear_notes'),
            slick_rear_pressure=inserted_data.get('slick_rear_pressure'),
            rain_front_name=inserted_data.get('rain_front_name'),
            rain_front_notes=inserted_data.get('rain_front_notes'),
            rain_front_pressure=inserted_data.get('rain_front_pressure'),
            rain_rear_name=inserted_data.get('rain_rear_name'),
            rain_rear_notes=inserted_data.get('rain_rear_notes'),
            rain_rear_pressure=inserted_data.get('rain_rear_pressure'),
            setup=inserted_data.get('setup'),
            datetime_created=datetime.utcnow(),
            datetime_last_modified=datetime.utcnow(),
        )

        db.session.add(new_bike)
        db.session.commit()

        response = jsonify(new_bike.bike_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Bike not found.')
class BikeItem(Resource):

    @api.response(200, "Bike with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a bike.
        """

        bike_entry = BikeModel.query.filter(BikeModel.bike_id == id_).one()

        bike_data = bike_schema.dump(bike_entry)

        response = jsonify(bike_data)
        response.status_code = 200

        return response

    @api.expect(bike_input_parameters)
    @api.response(204, "Bike with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a bike.
        """

        inserted_data = request.get_json()

        bike_entry = BikeModel.query.filter(BikeModel.bike_id == id_).one()

        if inserted_data.get('operating_hours') is not None:
            bike_entry.operating_hours = inserted_data.get('operating_hours')
        if inserted_data.get('manufacturer') is not None:
            bike_entry.manufacturer = inserted_data.get('manufacturer')
        if inserted_data.get('model') is not None:
            bike_entry.model = inserted_data.get('model')
        if inserted_data.get('year') is not None:
            bike_entry.year = inserted_data.get('year')
        if inserted_data.get('ccm') is not None:
            bike_entry.ccm = inserted_data.get('ccm')
        if inserted_data.get('stroke') is not None:
            bike_entry.stroke = inserted_data.get('stroke')
        if inserted_data.get('piston') is not None:
            bike_entry.piston = inserted_data.get('piston')
        if inserted_data.get('slick_front_name') is not None:
            bike_entry.slick_front_name = inserted_data.get('slick_front_name')
        if inserted_data.get('slick_front_notes') is not None:
            bike_entry.slick_front_notes = inserted_data.get('slick_front_notes')
        if inserted_data.get('slick_front_pressure') is not None:
            bike_entry.slick_front_pressure = inserted_data.get('slick_front_pressure')
        if inserted_data.get('slick_rear_name') is not None:
            bike_entry.slick_rear_name = inserted_data.get('slick_rear_name')
        if inserted_data.get('slick_rear_notes') is not None:
            bike_entry.slick_rear_notes = inserted_data.get('slick_rear_notes')
        if inserted_data.get('slick_rear_pressure') is not None:
            bike_entry.slick_rear_pressure = inserted_data.get('slick_rear_pressure')
        if inserted_data.get('rain_front_name') is not None:
            bike_entry.rain_front_name = inserted_data.get('rain_front_name')
        if inserted_data.get('rain_front_notes') is not None:
            bike_entry.rain_front_notes = inserted_data.get('rain_front_notes')
        if inserted_data.get('rain_front_pressure') is not None:
            bike_entry.rain_front_pressure = inserted_data.get('rain_front_pressure')
        if inserted_data.get('rain_rear_name') is not None:
            bike_entry.rain_rear_name = inserted_data.get('rain_rear_name')
        if inserted_data.get('rain_rear_notes') is not None:
            bike_entry.rain_rear_notes = inserted_data.get('rain_rear_notes')
        if inserted_data.get('rain_rear_pressure') is not None:
            bike_entry.rain_rear_pressure = inserted_data.get('rain_rear_pressure')
        if inserted_data.get('setup') is not None:
            bike_entry.setup = inserted_data.get('setup')
        if bool(inserted_data) is True:
            bike_entry.datetime_last_modified = datetime.utcnow()

        db.session.add(bike_entry)
        db.session.commit()

        return None, 204

    @api.response(204, "History entry with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a bike.
        """

        bike_entry = BikeModel.query.filter(BikeModel.bike_id == id_).one()

        db.session.delete(bike_entry)
        db.session.commit()

        return None, 204
