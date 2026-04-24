from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import db, User, Category, Product, Loyalty
from config import get_config
from auth import auth_bp, login_manager

from customers import customer_bp
from shop import shop_bp

app = Flask(__name__)
get_config(app)

with app.app_context():
    db.create_all()

# --- setup login manager ---
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# --- register blueprints ---
app.register_blueprint(auth_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(shop_bp)


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC ROUTES
# ─────────────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    from auth import NAV, nav_for
    nav = nav_for(current_user) if current_user.is_authenticated else NAV["public"]
    categories = Category.query.order_by(Category.category_name).all()
    return render_template('index.html', nav_links=nav, categories=categories)


@app.route('/about')
def about():
    from auth import NAV, nav_for
    nav = nav_for(current_user) if current_user.is_authenticated else NAV["public"]
    return render_template('about.html', nav_links=nav)


@app.route('/privacy')
def privacy():
    from auth import NAV, nav_for
    nav = nav_for(current_user) if current_user.is_authenticated else NAV["public"]
    return render_template('privacy.html', nav_links=nav)


@app.route('/terms')
def terms():
    from auth import NAV, nav_for
    nav = nav_for(current_user) if current_user.is_authenticated else NAV["public"]
    return render_template('terms.html', nav_links=nav)


@app.route('/producers')
def producers():
    from auth import NAV, nav_for
    nav = nav_for(current_user) if current_user.is_authenticated else NAV["public"]
    producers = User.query.filter_by(role="producer", is_active=True).order_by(User.name).all()
    return render_template('producers.html', nav_links=nav, producers=producers)


@app.route('/contact-us', methods=["GET", "POST"])
def contact_us():
    from auth import NAV, nav_for
    from models import Enquiry
    nav = nav_for(current_user) if current_user.is_authenticated else NAV["public"]

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name  = request.form.get("last_name", "").strip()
        email      = request.form.get("email", "").strip()
        subject    = request.form.get("subject", "General Inquiry")
        message    = request.form.get("message", "").strip()

        if not first_name or not email or not message:
            flash("Please fill in all required fields.", "danger")
            return render_template("contact_us.html", nav_links=nav)

        enquiry = Enquiry(
            name    = f"{first_name} {last_name}".strip(),
            email   = email,
            subject = subject,
            message = message,
            user_id = current_user.id if current_user.is_authenticated else None,
        )
        db.session.add(enquiry)
        db.session.commit()
        flash("Thank you for your message! We'll be in touch soon.", "success")
        return redirect(url_for("contact_us"))

    return render_template('contact_us.html', nav_links=nav)


# ─────────────────────────────────────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# ─────────────────────────────────────────────────────────────────────────────
# SEED ROUTE — visit /seed in the browser to populate demo data
# ─────────────────────────────────────────────────────────────────────────────

def _get_or_create_user(email, **kwargs):
    """Return existing user by email, or create and return a new one."""
    user = User.query.filter_by(email=email).first()
    if user:
        return user, False
    password = kwargs.pop("password")
    user = User(email=email, **kwargs)
    user.set_password(password)
    db.session.add(user)
    return user, True



# RUN APP

if __name__ == "__main__":
    app.run(debug=True)
