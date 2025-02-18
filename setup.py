from app1 import app, db
from application.models1 import User, Role
from flask_security import SQLAlchemyUserDatastore

# Initialize Flask-Security user datastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Run the setup within the application context
with app.app_context():
    # Create roles
    admin_role = Role(name='admin', description='Administrator')
    user_role = Role(name='user', description='Regular User')
    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.commit()

    # Create a user
    user = user_datastore.create_user(email='admin@example.com', password='admin')
    db.session.commit()

    # Assign roles to the user
    user_datastore.add_role_to_user(user, admin_role)
    db.session.commit()

    print("Database initialized with roles and an admin user.")