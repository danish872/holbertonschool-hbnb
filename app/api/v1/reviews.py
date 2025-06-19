from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'place_id': fields.String(required=True, description='Place ID'),
    'user_id': fields.String(required=True, description='User ID'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'comment': fields.String(required=True, description='Text of review')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        review_data = api.payload
        required_fields = {'place_id', 'user_id', 'rating', 'comment'}
        
        if not required_fields.issubset(review_data):
            return {'message': 'Missing required fields'}, 400
        
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return {'reviews': [review.to_dict() for review in reviews]}, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve review details by ID"""
        review = facade.get_review(review_id)
        return (review.to_dict(), 200) if review else ({'error': 'Review not found'}, 404)

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review information"""
        review_data = api.payload
        required_fields = {'user_id', 'place_id', 'rating', 'comment'}
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        if not required_fields.issubset(review_data):
            return {'message': 'Missing required fields'}, 400
        
        try:
            updated_review = facade.update_review(review_id, review_data)
            return updated_review.to_dict(), 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        place_reviews = facade.get_reviews_by_place(place_id)
        if not place_reviews:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place_reviews], 200
