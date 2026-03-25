from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "customer/dashboard.html",
        user=current_user,
        current_date=datetime.now()
    )