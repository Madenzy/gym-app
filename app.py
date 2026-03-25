from flask import Flask, render_template
from flask_login import LoginManager, login_required, current_user
from models import db, User
from config import get_config
from customers import customer_bp


# import your auth blueprint
from auth import auth_bp, login_manager

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


@app.route('/contact-us')
def contact_us():
    return render_template('contact_us.html')


# ------------------------
# DASHBOARD (PROTECTED)
# ------------------------

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

if __name__ == "__main__":
    app.run(debug=True)