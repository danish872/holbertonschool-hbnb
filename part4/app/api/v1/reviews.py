from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
    })

facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        # Validation des champs requis
        required_fields = ['text', 'rating', 'user_id', 'place_id']
        if not all(field in review_data for field in required_fields):
            return {'message': 'Missing required fields'}, 400

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404

        # L'utilisateur ne peut pas noter son propre lieu sauf admin
        if not is_admin and place.owner_id == current_user['id']:
            return {'message': 'You cannot review your own place'}, 400

        # Vérifier que l'utilisateur n'a pas déjà laissé un avis sur ce lieu
        if not is_admin:
            existing_review = facade.get_review_by_user_and_place(current

