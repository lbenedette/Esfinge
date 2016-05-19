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
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(50), primary_key=True)
    encrypt_password = db.Column(db.String(15))
    name = db.Column(db.String(20))
    authenticated = db.Column(db.Boolean, default=False)
    questions = db.relationship('Question', backref='user', lazy='dynamic')
    answers = db.relationship('Answer', backref='user', lazy='dynamic')

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


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    user_id = db.Column(db.String(50), db.ForeignKey('user.email'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text)
    user_id = db.Column(db.String(50), db.ForeignKey('user.email'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))


# support functions
def database_add(data):
    db.session.add(data)
    db.session.commit()


def database_delete(data):
    db.session.delete(data)
    db.session.commit()


def logger(user):
    user.authenticated = True
    database_add(user)
    login_user(user, remember=True)


def des_logger(user):
    user.authenticated = False
    database_add(user)
    logout_user()


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
                        encrypt_password=bcrypt.hashpw(password, bcrypt.gensalt()),
                        name=request.form['name'])
            database_add(user)
            flash('Você foi registrado com sucesso!')
            return redirect(url_for('login'))
        else:
            flash('Email já cadastrado!')
    return render_template('register.html', title='register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.get(request.form['email'])
        if user:
            password = request.form['password'].encode('utf-8')
            if bcrypt.hashpw(password, user.encrypt_password) == user.encrypt_password:
                logger(user)
                flash('Login realizado com sucesso!')
                return redirect(url_for('timeline'))
            else:
                flash('Senha incorreta!')
        else:
            flash('Email de usuário não cadastrado!')
    return render_template('login.html', title='login')


@app.route('/logout')
@login_required
def logout():
    des_logger(current_user)
    flash('Logout realizado com sucesso!')
    return render_template('login.html', title='login')


@app.route('/timeline', methods=['GET', 'POST'])
@login_required
def timeline():
    if request.method == 'POST':
        question = Question(id=None, question=request.form['question'], user_id=current_user.email)
        database_add(question)
    return render_template('timeline.html', user=current_user)


@app.route('/timeline/<int:question_id>')
@login_required
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        return redirect(url_for('timeline'))
    database_delete(question)
    return render_template('timeline.html', user=current_user)


@app.route('/timeline/<name>')
@login_required
def user_timeline(name):
    user = User.query.filter_by(name=name).first()
    if user != current_user:
        return render_template('user_timeline.html', user=user)
    else:
        return render_template('timeline.html', user=current_user)


@app.route('/timeline/<name>/<int:question_id>', methods=['POST'])
@login_required
def add_answer(name, question_id):
    user = User.query.filter_by(name=name).first()
    print(user.name)
    answer = Answer(id=None, answer=request.form['answer'], user_id=current_user.email, question_id=question_id)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('user_timeline', name=user.name))


if __name__ == '__main__':
    app.run(debug=True)
