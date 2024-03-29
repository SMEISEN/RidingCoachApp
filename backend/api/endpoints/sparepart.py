from flask import jsonify, request
from flask_restplus import Resource, fields
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.api.routines.common import query_intervals
from backend.database import db
from backend.database.models.sparepart import SparepartModel, SparepartSchema
from backend.database.models.sparepartitem import SparepartitemSchema

ns = api.namespace('sparepart', description='Operations related to spareparts.')
sparepart_schema = SparepartSchema()
sparepartitem_schema = SparepartitemSchema()

sparepart_input_parameters = api.model('SparepartInputParameters', {
    "name":
        fields.String(description="name of the spare part", required=True, example="spare part name"),
    "module":
        fields.String(description="bike module where the spare part belongs to", required=True, example="Engine"),
    "min_stock":
        fields.Integer(description="minimal stock of the spare part", required=True, example=2),
})
sparepart_query_parameters = api.model('SparepartQueryParameters', {
    "bike_id":
        fields.String(description="id of the bike where the spare part belongs to", required=False, example="UUID4"),
    "name":
        fields.String(description="name of the spare part", required=False, example="brake lever"),
    "module":
        fields.String(description="bike module where the spare part belongs to", required=False, example="Engine"),
    "min_stock":
        fields.Raw(description="minimal stock of the spare part", required=False, example={
            "values": [0, 2],
            "operators": ['>=', '<='],
        }),
})


@ns.route('/')
class SparepartCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Sparepart list successfully fetched.')
    def get(self):
        """
        Returns a list of all spare parts.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepart_all_entries = SparepartModel.query.order_by(SparepartModel.datetime_display.desc()).all()

        sparepart_entry_list = []
        for sparepart_entry in sparepart_all_entries:
            sparepartitem_data = sparepartitem_schema.dump(sparepart_entry.items, many=True)
            sparepart_data = sparepart_schema.dump(sparepart_entry)
            sparepart_data['current_stock'] = sparepart_entry.current_stock
            sparepart_data['items'] = sparepartitem_data
            sparepart_entry_list.append(sparepart_data)

        response = jsonify(sparepart_entry_list)
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(sparepart_input_parameters)
    @api.response(201, 'Spare part successfully added.')
    def post(self):
        """
        Creates a new spare part item parent.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        new_sparepart = SparepartModel(
            name=inserted_data.get('name'),
            module=inserted_data.get('module'),
            min_stock=inserted_data.get('min_stock'),
        )
        db.session.add(new_sparepart)
        db.session.commit()

        response = jsonify(new_sparepart.sparepart_id)
        response.status_code = 201

        return response


@ns.route('/<string:id_>')
@api.response(404, 'Spare part item not found.')
class SparepartItem(Resource):

    @api.doc(security='apikey')
    @api.response(200, f"Spare part with requested id successfully fetched.")
    def get(self, id_: str):
        """
        Returns a spare part item parent.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepart_item = SparepartModel.query.filter(SparepartModel.sparepart_id == id_).one()

        response = jsonify(sparepart_schema.dump(sparepart_item))
        response.status_code = 200

        return response

    @api.doc(security='apikey')
    @api.expect(sparepart_input_parameters)
    @api.response(204, f"Spare part with requested id successfully updated.")
    def put(self, id_: str):
        """
        Updates a spare part item parent.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        inserted_data = request.get_json()

        sparepart = SparepartModel.query.filter(SparepartModel.sparepart_id == id_).one()

        if inserted_data.get('name', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            sparepart.name = inserted_data.get('name')
        if inserted_data.get('module', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            sparepart.module = inserted_data.get('module')
        if inserted_data.get('min_stock', 'ParameterNotInPayload') != 'ParameterNotInPayload':
            sparepart.min_stock = inserted_data.get('min_stock')

        db.session.add(sparepart)
        db.session.commit()

        return None, 204

    @api.doc(security='apikey')
    @api.response(204, f"Spare part with requested id successfully deleted.")
    def delete(self, id_: str):
        """
        Deletes a spare part item parent.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepart = SparepartModel.query.filter(SparepartModel.sparepart_id == id_).one()

        db.session.delete(sparepart)
        db.session.commit()

        return None, 204


@ns.route('/query')
@api.response(404, 'Query parameters not found.')
class SparepartQuery(Resource):

    @api.doc(security='apikey')
    @api.expect(sparepart_query_parameters)
    def post(self):
        """
        Creates a filtered query based on the input json file and returns the requested data.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        requested = request.get_json()
        valid_keys = ["bike_id", "name", "module", "min_stock"]
        if not all(x in valid_keys for x in requested.keys()):
            response = jsonify([])
            response.status_code = 404

            return response

        filter_by_data = {
            'bike_id': requested.get('bike_id'),
            'name': requested.get('name'),
            'module': requested.get('module'),
        }
        filter_by_data = {key: value for (key, value) in filter_by_data.items() if value is not None}

        sparepart_query = SparepartModel.query.filter_by(**filter_by_data)

        sparepart_query = query_intervals(filter_keys=[
            "min_stock",
        ], query=sparepart_query, request=requested, model=SparepartModel)

        sparepart_query = sparepart_query \
            .order_by(SparepartModel.module.asc()) \
            .order_by(SparepartModel.name.asc()) \
            .order_by(SparepartModel.min_stock.asc()) \
            .all()

        sparepart_entry_list = []
        for sparepart_entry in sparepart_query:
            sparepartitem_data = sparepartitem_schema.dump(sparepart_entry.items, many=True)
            sparepart_data = sparepart_schema.dump(sparepart_entry)
            sparepart_data['current_stock'] = sparepart_entry.current_stock
            sparepart_data['items'] = sparepartitem_data
            sparepart_entry_list.append(sparepart_data)

        response = jsonify(sparepart_entry_list)
        response.status_code = 200

        return response


@ns.route('/warnings')
class SparepartWarning(Resource):

    @api.doc(security='apikey')
    @api.response(200, f"Spare part warnings successfully fetched.")
    def get(self):
        """
        Returns the number of spoare part warnings.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepart_all_entries = SparepartModel.query.order_by(SparepartModel.datetime_display.desc()).all()

        warnings = {
            'warnings': 0,
            'missing_spareparts': [],
        }
        for sparepart_entry in sparepart_all_entries:
            if sparepart_entry.current_stock is None or sparepart_entry.min_stock is None:
                continue
            if sparepart_entry.current_stock < sparepart_entry.min_stock:
                sparepartitem_data = sparepartitem_schema.dump(sparepart_entry.items, many=True)
                sparepart_data = sparepart_schema.dump(sparepart_entry)
                sparepart_data['current_stock'] = sparepart_entry.current_stock
                sparepart_data['items'] = sparepartitem_data

                warnings['warnings'] += 1
                warnings['missing_spareparts'].append(sparepart_data)

        response = jsonify(warnings)
        response.status_code = 200

        return response
