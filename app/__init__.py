from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
db = SQLAlchemy(app)


from app import views, models
