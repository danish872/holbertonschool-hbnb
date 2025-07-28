import uuid
from datetime import datetime
import config
from extends import db, bcrypt, jwt
from flask_cors import CORS

# Import API namespaces
from app.api.v1.auth import api as auth_ns
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns


def create_default_admin():
    """
    Create a default admin user if it does not exist.
    """
    from app.models.user import User

    admin_exists = User.query.filter_by(is_admin=True).first()
    if not admin_exists:
        from config import DefaultAdmin
        admin = User(
                first_name=DefaultAdmin.DEFAULT_HBNB_ADMIN_FIRST_NAME,
                last_name=DefaultAdmin.DEFAULT_HBNB_ADMIN_LAST_NAME,
                password=DefaultAdmin.DEFAULT_HBNB_ADMIN_PASSWORD,
                email=DefaultAdmin.DEFAULT_HBNB_ADMIN_EMAIL,
                is_admin=True
                )
        db.session.add(admin)
        db.session.commit()


def create_app(config_class=config.DevelopmentConfig):
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_class)
    api = Api(
            app,
            version='1.0',
            title='HBnB API',
            description='HBnB Application API',
            contact_email='9798@holbertonstudents.com',
            authorizations={
                'BearerAuth': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Authorization',
                    'description': 'Bearer authentication token'
                    }
                },
            security='BearerAuth'
            )

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_default_admin()

    return app

