from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from assistent.config import Config
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
mail = Mail(app)


from assistent.models import User, Note
from assistent.auth.routes import auth_bp
from assistent.contacts.routes import contact_bp
from assistent.notes.routes import note_bp


app.register_blueprint(auth_bp)
app.register_blueprint(note_bp)
app.register_blueprint(contact_bp)
db.create_all()