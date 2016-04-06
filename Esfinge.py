import bcrypt
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
# if login_required: redirect to login
login_manager.login_view = 'login'
conn = SQLAlchemy(app)


# USER CLASS
class User(conn.Model):
    __tablename__ = 'user'

    email = conn.Column(conn.String(120), primary_key=True)
    pass_hash = conn.Column(conn.String(15))
    authenticated = conn.Column(conn.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


# USER LOADER
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# VIEWS
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = User.query.get(request.form['email'])
        if user is None:
            password = request.form['password'].encode('utf-8')
            user = User(email=request.form['email'],
                        pass_hash=bcrypt.hashpw(password, bcrypt.gensalt()))
            conn.session.add(user)
            conn.session.commit()
            flash('You were successfully registered!')
            return redirect(url_for('login'))
        else:
            flash('Email already registered!')
            return render_template('register.html', title='register')
    return render_template('register.html', title='register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.get(request.form['email'])
        if user:
            pass_byte = request.form['password'].encode('utf-8')
            if bcrypt.hashpw(pass_byte, user.pass_hash) == user.pass_hash:
                user.authenticated = True
                conn.session.add(user)
                conn.session.commit()
                login_user(user, remember=True)
                flash('Login realizado com sucesso!')
                return redirect(url_for('home'))
    return render_template('login.html', title='login')


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    conn.session.add(user)
    conn.session.commit()
    logout_user()
    flash('Logout realizado com sucesso!')
    return render_template('login.html', title='login')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
