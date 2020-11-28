from datetime import datetime
from flask import jsonify, request
from backend.api import api
from backend.api.authentication.validation import validate_api_key
from backend.database import db
from backend.database.models.sparepart import SparepartModel, SparepartSchema
from backend.database.models.sparepartitem import SparepartitemModel, SparepartitemSchema
from flask_restplus import Resource, fields

ns = api.namespace('sparepart', description='Operations related to spareparts.')
sparepart_schema = SparepartSchema()
sparepartitem_schema = SparepartitemSchema()


@ns.route('/')
class SparepartCollection(Resource):

    @api.doc(security='apikey')
    @api.response(200, 'Sparepart list successfully fetched.')
    def get(self):
        """
        Returns a list of all spareparts.
        """

        api_key = request.headers.get('apikey')
        if validate_api_key(api_key).status_code != 200:
            return validate_api_key(api_key)

        sparepart_all_entries = SparepartModel.query.order_by(SparepartModel.datetime_display.desc()).all()

        sparepart_entry_list = []
        for sparepart_entry in sparepart_all_entries:
            sparepartitem_data = sparepartitem_schema.dump(sparepart_entry.items, many=True)
            sparepart_data = sparepart_schema.dump(sparepart_entry)
            sparepart_data['stock'] = sparepart_entry.stock
            sparepart_data['items'] = sparepartitem_data
            sparepart_entry_list.append(sparepart_data)

        response = jsonify(sparepart_entry_list)
        response.status_code = 200

        return response
