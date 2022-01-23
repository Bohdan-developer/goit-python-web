from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
from assistent.auth import routes
