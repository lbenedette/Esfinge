from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect page
login_manager.login_message = 'Por favor entre para poder acessar a página!'    # login message


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app import controllers


db.create_all()
