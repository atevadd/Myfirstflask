from flask import Flask, render_template, url_for, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, LoginManager, mixins, logout_user, login_required, login_user


app = Flask(__name__)


db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:atevadd@localhost:3306/niit"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "ynI\xcc\xdb\x03\xd6QR8X\x12\xff\xd3Wv\xf3\x14{Z\xc5\x08"
app.config['extend_existing'] = True
