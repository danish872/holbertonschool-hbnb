from app import create_app
from app.models.user import User, create_first_admin
from config import config

app = create_app()

with app.app_context():
    # Création des tables si besoin
    from app.models import db
    db.create_all()

    # Création d'un admin par défaut s'il n'existe pas
    admin_email = config['admin'].DEFAULT_HBNB_ADMIN_EMAIL
    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin = User(
                first_name=config['admin'].DEFAULT_HBNB_ADMIN_FIRST_NAME,
                last_name=config['admin'].DEFAULT_HBNB_ADMIN_LAST_NAME,
                email=admin_email,
                is_admin=True
                )
        admin.hash_password(config['admin'].DEFAULT_HBNB_ADMIN_PASSWORD)
        from app import db
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created with email: {admin_email}")
    else:
        print(f"Admin user already exists with email: {admin_email}")

if __name__ == '__main__':
    app.run(debug=True)

