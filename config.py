from flask import Flask
from models import db
import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = 'GLH_Task_2_Secret_Key'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///glh.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def get_config(app: Flask):
    app.secret_key = 'GLH_Task_2_Secret_Key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///glh.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB upload limit
    app.config['STRIPE_SECRET_KEY'] = os.environ.get("STRIPE_SECRET_KEY", "")
    app.config['STRIPE_PUBLIC_KEY'] = os.environ.get("STRIPE_PUBLIC_KEY", "")
    db.init_app(app)
