from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user

dashboard_bp = Blueprint('dashboard_route', __name__)


@dashboard_bp.route('/')
@login_required
def dashboard():
    current_business = current_user.current_business
    role = current_user.business_role
    return render_template('dashboard/dashboard.html',
                           current_user=current_user, business=current_business, role=role)