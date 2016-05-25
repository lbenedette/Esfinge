from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from app.models import User, Follow, Question, Answer
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
def index():
    return render_template('index.html')


# change flash message to error message?
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = User.query.get(request.form['email'])
        if user is None:
            password = request.form['password']
            re_password = request.form['re-password']
            if password == re_password:
                user = User(email=request.form['email'],
                            encrypt_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                            username=request.form['username'])
                database_add(user)
                flash('Você foi registrado com sucesso!')
                return redirect(url_for('login'))
            else:
                flash('As senhas são diferentes!')
        else:
            flash('Email já cadastrado!')
    return render_template('register.html')


# change flash message to error message?
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
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
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    database_add(user)
    logout_user()
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))


@app.route('/timeline', methods=['GET', 'POST'])
@login_required
def timeline():
    return render_template('timeline.html')


@app.route('/add_question', methods=['POST'])
@login_required
def add_question():
    if request.form['question']:
        question = Question(id=None, question=request.form['question'], user_id=current_user.id)
        database_add(question)
        flash('Questão adicionada com sucesso!')
    return redirect(url_for('timeline'))


@app.route('/delete_question/<int:question_id>')
@login_required
def delete_question(question_id):
    question = Question.query.get(question_id)
    database_delete(question)
    return redirect(url_for('timeline'))


@app.route('/<int:profile_id>')
@login_required
def user_timeline(profile_id):
    user_profile = User.query.get(profile_id)
    if user_profile is None:
        abort(404)
    followed = False
    follow = Follow.query.filter_by(user_id=current_user.id,follow_email=user_profile.email).first()
    if follow is not None:
        followed = True
    return render_template('timeline.html', user_profile=user_profile, followed=followed)


@app.route('/<int:profile_id>/follow')
@login_required
def follow_user(profile_id):
    user_profile = User.query.get(profile_id)
    if user_profile is None:
        abort(404)
    follow = Follow(follow_email=user_profile.email, user_id=current_user.id)
    database_add(follow)
    return redirect(url_for('user_timeline', profile_id=user_profile.id))


@app.route('/<int:profile_id>/unfollow')
@login_required
def unfollow_user(profile_id):
    user_profile = User.query.get(profile_id)
    if user_profile is None:
        abort(404)
    follow = Follow.query.filter_by(user_id=current_user.id,follow_email=user_profile.email).first()
    if follow is None:
        abort(404)
    database_delete(follow)
    return redirect(url_for('user_timeline', profile_id=user_profile.id))


@app.route('/<int:profile_id>/add_answer/<int:question_id>', methods=['POST'])
@login_required
def add_answer(profile_id, question_id):
    user_profile = User.query.get(profile_id)
    question = Question.query.get(question_id)
    if user_profile is None or question is None:
        abort(404)
    if request.form['answer']:
        answer = Answer(id=None, answer=request.form['answer'], user_id=current_user.id, question_id=question_id)
        database_add(answer)
    return redirect(url_for('user_timeline', profile_id=user_profile.id))
