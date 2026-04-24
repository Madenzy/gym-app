from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Product, Order, Category, Enquiry, StockMovement, Loyalty
from datetime import datetime
from auth import NAV, nav_for
from auth import is_valid_password

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")





@admin_bp.route("/manage-accounts/<int:user_id>/toggle-active", methods=["POST"])
@admin_required
def toggle_active(user_id):
    target = db.session.get(User, user_id)
    if not target:
        flash("User not found.", "danger")
    elif target.id == current_user.id:
        flash("You cannot deactivate your own account.", "warning")
    else:
        target.is_active = not target.is_active
        db.session.commit()
        status = "activated" if target.is_active else "deactivated"
        flash(f"Account for {target.name} has been {status}.", "success")
    return redirect(url_for("admin.manage_accounts"))





# ─────────────────────────────────────────────────────────────────────────────
# MANAGE ORDERS
# ─────────────────────────────────────────────────────────────────────────────

@admin_bp.route("/orders")
@admin_required
def orders():
    status_filter = request.args.get("status", "")
    query = Order.query
    if status_filter:
        query = query.filter_by(order_status=status_filter)
    all_orders = query.order_by(Order.order_date.desc()).all()

    return render_template(
        "admin/orders.html",
        orders=all_orders,
        status_filter=status_filter,
        user=current_user,
        nav_links=nav_for(current_user),
    )


@admin_bp.route("/orders/<int:order_id>/update-status", methods=["POST"])
@admin_required
def update_order_status(order_id):
    order      = db.session.get(Order, order_id)
    new_status = request.form.get("status", "")
    valid_statuses = ("Pending", "Confirmed", "Processing", "Out for Delivery", "Delivered", "Cancelled")

    if not order:
        flash("Order not found.", "danger")
    elif new_status not in valid_statuses:
        flash("Invalid status.", "danger")
    else:
        order.order_status = new_status
        db.session.commit()
        flash(f"Order #GLH-{order.id:04d} updated to '{new_status}'.", "success")

    return redirect(url_for("admin.orders"))


# ─────────────────────────────────────────────────────────────────────────────
# ENQUIRIES
# ─────────────────────────────────────────────────────────────────────────────

@admin_bp.route("/producers")
@admin_required
def producers():
    all_producers = User.query.filter_by(role="producer").order_by(User.name).all()
    return render_template(
        "admin/producers.html",
        producers=all_producers,
        user=current_user,
        nav_links=nav_for(current_user),
    )


@admin_bp.route("/enquiries")
@admin_required
def enquiries():
    type_filter = request.args.get("type", "")
    query = Enquiry.query
    if type_filter:
        query = query.filter_by(subject=type_filter)
    all_enquiries = query.order_by(Enquiry.submitted_date.desc()).all()
    return render_template(
        "admin/enquiries.html",
        enquiries=all_enquiries,
        type_filter=type_filter,
        user=current_user,
        nav_links=nav_for(current_user),
    )
