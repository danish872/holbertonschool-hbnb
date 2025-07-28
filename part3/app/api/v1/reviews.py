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

        # Validate required fields
        for field in ('text', 'rating', 'user_id', 'place_id'):
            if field not in review_data:
                return {'message': f'Missing required field: {field}'}, 400

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404

        if not is_admin and place.owner_id == current_user['id']:
            return {'message': 'You cannot review your own place'}, 400

        if not is_admin:
            existing_review = facade.get_review_by_user_and_place(current_user['id'], review_data['place_id'])
            if existing_review:
                return {'message': 'You have already reviewed this place'}, 400

        review_data['user_id'] = current_user['id']
        try:
            new_review = facade.create_review(review_data)
            return {
                    'id': new_review.id,
                    'text': new_review.text,
                    'rating': new_review.rating,
                    'user_id': new_review.user_id,
                    'place_id': new_review.place_id,
                    'message': 'Review successfully created'
                    }, 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id
                    } for review in reviews
                ], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
                }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        if not is_admin and str(review.user_id) != str(current_user['id']):
            return {'error': 'Unauthorized action'}, 403

        updated_review = facade.update_review(review_id, review_data)
        return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'message': 'Review successfully updated'
                }, 200

    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        if not is_admin and str(review.user_id) != str(current_user['id']):
            return {'error': 'Unauthorized action'}, 403

        success = facade.delete_review(review_id)
        if success:
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Review not found'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place_reviews = facade.get_reviews_by_place(place_id)
        if place_reviews is None:
            return {'message': 'Place not found'}, 404
        return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id
                    } for review in place_reviews
                ], 200

