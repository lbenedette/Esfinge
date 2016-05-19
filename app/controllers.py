from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app import app
from app import db
from app import login_manager
from app.models import User, Question, Answer
import bcrypt


# support function
def database_add(data):
    db.session.add(data)
    db.session.commit()


def database_delete(data):
    db.session.delete(data)
    db.session.commit()


# user loader
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# controllers
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
                user.authenticated = True
                database_add(user)
                login_user(user, remember=True)
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
    user = current_user
    user.authenticated = False
    database_add(user)
    logout_user()
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
