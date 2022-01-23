from flask import Blueprint


note_bp = Blueprint('notes', __name__)

from assistent.notes import routes
