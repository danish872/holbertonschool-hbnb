from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True),
    'name': fields.String(required=True, description='Name of the amenity'),
    'created_at': fields.String(readOnly=True),
    'updated_at': fields.String(readOnly=True),
})

@api.route('/')
class AmenityList(Resource):
    @api.marshal_list_with(amenity_model)
    def get(self):
        return [a.__dict__ for a in facade.get_all_amenities()]

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        data = api.payload
        amenity = facade.create_amenity(data['name'])
        return amenity.__dict__, 201

@api.route('/<string:amenity_id>')
class AmenityDetail(Resource):
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.__dict__

    @api.expect(amenity_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        data = api.payload
        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            api.abort(404, "Amenity not found")
        return amenity.__dict__
