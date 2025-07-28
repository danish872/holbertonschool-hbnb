from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
    })

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt_identity()

        if not current_user.get('is_admin', True):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        if not amenity_data:
            return {'message': 'Invalid input data'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {
                'id': new_amenity.id,
                'name': new_amenity.name
                }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
                {
                    'id': amenity.id,
                    'name': amenity.name
                    } for amenity in amenities
                ]

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenities_data = facade.get_amenity(amenity_id)

        if not amenities_data:
            return  {'message': 'Amenity not found'}, 404
        return {
                'id': amenities_data.id,
                'name': amenities_data.name
                }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        if not amenity_data:
            return {'message': 'Invalid input data'}, 400

        updated_amenities = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenities:
            return {'message': 'Amenity not found'}, 404
        return {
                'name': updated_amenities.name
                }

