from flask_restx import Namespace, Resource, fields
from app.services import facade
import re 

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
        except ValueError as e:
            return  {'error': str(e)}, 400

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

@api.route('/')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'No user found')
    def get(self):
        list_all = []
        user = facade.get_all_user()
        if not user:
            return {'error': 'No user found'}, 404
        for element in user:
            list_all.append({
                "id": element.id,
                "first_name": element.first_name,
                "last_name": element.last_name,
                "email": element.email
                })
        return list_all, 200

@api.route('/<user_id>')
class UserChange(Resource):
    @api.response(200, 'User details change successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Get user details by ID"""
        new_data = api.payload
        if facade.get_user_by_email(new_data['email']):
            return {'error': 'Email already registered'}, 400
        if not facade.get_user(user_id):
            return {'error': 'User not found'}, 404
        try:
            facade.update_user(user_id=user_id, data=new_data)
            return {'id': user_id, 'first_name': new_data["first_name"], 'last_name': new_data["last_name"], 'email': new_data["email"]}, 200
        except ValueError as e:
            return  {'error': str(e)}, 400
