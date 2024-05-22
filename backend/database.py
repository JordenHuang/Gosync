from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config["SECRET_KEY"] = "iwonttellyou"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()

    from backend.views import views
    app.register_blueprint(views, url_prefix="/")

    return app
