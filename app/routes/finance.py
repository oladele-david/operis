from flask import Blueprint, render_template, redirect, url_for, flash, request

finance_bp = Blueprint('finance_route', __name__)


@finance_bp.route('/')
def finance():
    return "Finance"