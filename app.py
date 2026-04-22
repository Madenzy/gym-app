from flask import Flask, render_template
from flask_login import LoginManager, login_required, current_user
from models import db, User
from config import get_config
from customers import customer_bp
<<<<<<< HEAD


# import your auth blueprint
from auth import auth_bp, login_manager
=======
from shop import shop_bp
>>>>>>> cc240c4 (update)

app = Flask(__name__)
get_config(app)



with app.app_context():
    db.create_all()

# --- setup login manager ---
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# --- register blueprint ---
app.register_blueprint(auth_bp)
app.register_blueprint(customer_bp)
<<<<<<< HEAD
=======
app.register_blueprint(shop_bp)
>>>>>>> cc240c4 (update)


# ------------------------
# BASIC ROUTES
# ------------------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


<<<<<<< HEAD
@app.route('/contact-us')
=======
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
>>>>>>> cc240c4 (update)
def contact_us():
    return render_template('contact_us.html')


# ------------------------
# DASHBOARD (PROTECTED)
# ------------------------

<<<<<<< HEAD
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        user=current_user
    )


# ------------------------
# ERROR PAGE
# ------------------------

@app.route('/failure')
def failure():
    return render_template('500.html')


# ------------------------
# RUN APP
# ------------------------
=======
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
>>>>>>> cc240c4 (update)

if __name__ == "__main__":
    app.run(debug=True)