from flask import Flask
import pymysql
from flask_admin.contrib.sqla import ModelView

pymysql.install_as_MySQLdb()

from .extensions import db, migrate, login_manager
# from .routes import dashboard_bp
from app.routes import auth_bp, finance_bp, dashboard_bp
# from .admin.initialize_admin import initialize_admin
from .errors import errors_bp


def create_app():
    """Construct the core application."""

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models to register them with SQLAlchemy
    from app.models import user, business, finance, inventory, user_business_association

    # Initialize Flask-Admin
    # initialize_admin(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(finance_bp, url_prefix='/finance')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(errors_bp)

    return app
