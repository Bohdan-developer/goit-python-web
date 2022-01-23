from flask import Blueprint

contact_bp = Blueprint('contacts', __name__)

from assistent.contacts import routes
