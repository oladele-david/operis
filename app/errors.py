# app/errors.py
from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    """ Handle 404 errors """
    return render_template('404.html'), 404
