from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from app.models import User, Follow, Question, Answer
from sqlalchemy import or_
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
                            password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
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
            if bcrypt.hashpw(password, user.password) == user.password:
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


@app.route('/timeline', methods=['GET'])
@login_required
def timeline():
    user = current_user
    # TODO: add order_by (without internet :c )
    # BUG: if user don't have follows
    # .all() get all question from all users
    follows = Follow.query.filter_by(follower_id=user.id).first()
    if follows is not None: # test
        questions = Question.query.filter(or_(Question.user_id == f.follow_id for f in user.follows)).all()
    else:
        questions = []
    return render_template('timeline.html', questions=questions)

@app.route('/profile/<int:profile_id>')
@login_required
def profile_page(profile_id):
    profile = User.query.get(profile_id)
    user = current_user
    if profile is None:
        abort(404)
    followed = False # you don't follow this user
    follow = Follow.query.filter_by(follower_id=user.id, follow_id=profile.id).first()
    if follow is not None:
        followed = True
    elif profile.id == user.id:
        followed = None # your profile
    questions = Question.query.filter_by(user_id=profile.id)
    return render_template('profile.html', profile=profile, questions=questions, followed=followed)


@app.route('/add_question', methods=['POST'])
@login_required
def add_question():
    if request.form['question']:
        question = Question(id=None, question=request.form['question'], user_id=current_user.id)
        database_add(question)
        flash('Questão adicionada com sucesso!')
    return redirect(url_for('timeline'))


@app.route('/delete_question/<int:question_id>', methods=['GET'])
@login_required
def delete_question(question_id):
    question = Question.query.get(question_id)
    database_delete(question)
    return redirect(url_for('profile_page', profile_id=current_user.id))


@app.route('/profile/<int:profile_id>/follow')
@login_required
def follow_user(profile_id):
    profile = User.query.get(profile_id)
    user = current_user
    if profile is None:
        abort(404)
    follow = Follow(follower_id=user.id, follow_id=profile.id)
    database_add(follow)
    return redirect(url_for('profile_page', profile_id=profile.id))


@app.route('/profile/<int:profile_id>/unfollow')
@login_required
def unfollow_user(profile_id):
    profile = User.query.get(profile_id)
    user = current_user
    if profile is None:
        abort(404)
    follow = Follow.query.filter_by(follower_id=user.id, follow_id=profile.id).first()
    if follow is None:
        abort(404)
    database_delete(follow)
    return redirect(url_for('profile_page', profile_id=profile.id))


@app.route('/add_answer/<int:question_id>', methods=['POST'])
@login_required
def add_answer(question_id):
    user = current_user
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    if request.form['answer']:
        answer = Answer(id=None, answer=request.form['answer'], user_id=user.id, question_id=question.id)
        database_add(answer)
    # TODO: add redirect to last page
    return redirect(url_for('timeline'))


@app.route('/delete_answer/<int:answer_id>', methods=['GET'])
@login_required
def delete_answer(answer_id):
    answer = Answer.query.get(answer_id)
    if answer is None:
        abort(404)
    database_delete(answer)
    # TODO: add redirect to last page
    return redirect(url_for('timeline'))