from flask import Flask
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore  # Import Flask-Security components
from datetime import timedelta
from application.models1 import db, User, Role  # Import db and models from models.py

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=10)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SECURITY_PASSWORD_SALT'] = 'your_password_salt'  # Required for password hashing

app.config['SECURITY_REGISTERABLE'] = False  # Disable default registration view
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False  # Disable registration emails
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'auth/login.html'  # Use your custom login template

# Initialize SQLAlchemy with the app
db.init_app(app)

# Initialize Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register Blueprints
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.user import user_bp

app.register_blueprint(auth_bp )
app.register_blueprint(admin_bp )
app.register_blueprint(user_bp )

# Create database tables
with app.app_context():
    db.create_all()

# Run the application
if __name__ == "__main__":
    app.run()