from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity
import re

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
    })

facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    @api.response(403, 'Admin privileges required to create a user')
    @jwt_required()
    def post(self):
        """Register a new user (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Validate mandatory fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not user_data.get(field):
                return {'error': f"Missing required field: {field}"}, 400

        # Validate email format
        email = user_data['email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {'error': 'Invalid email format'}, 400

        # Check if email already exists
        existing_user = facade.get_user_by_email(email)
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Only admins can assign is_admin status
        if user_data.get("is_admin") and not current_user.get('is_admin'):
            return {'error': 'Only administrators can assign admin rights'}, 403

        try:
            new_user = facade.create_user(user_data)
            return {
                    'id': new_user.id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name,
                    'email': new_user.email,
                    'is_admin': new_user.is_admin,
                    'message': 'User successfully created'
                    }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, "List of users successfully retrieved")
    @jwt_required()
    def get(self):
        """Retrieve list of all users (admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_all_users()
        return [
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_admin': user.is_admin
                    } for user in users
                ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def get(self, user_id):
        """Get user details by ID"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        if not is_admin and str(current_user['id']) != str(user_id):
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin
                }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update a user's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_data = api.payload

        if not is_admin and str(current_user['id']) != str(user_id):
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Only admins can modify email and password
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'Only admins can modify email and password'}, 403

        # If email is changed, ensure it is valid and not already used
        if 'email' in user_data:
            email = user_data['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return {'error': 'Invalid email format'}, 400
            existing_user = facade.get_user_by_email(email)
            if existing_user and str(existing_user.id) != str(user_id):
                return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                    'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email,
                    'is_admin': updated_user.is_admin,
                    'message': 'User successfully updated'
                    }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

