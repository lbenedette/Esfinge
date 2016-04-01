from flask import Flask, render_template, request, redirect, url_for
from app import app, db, models
import base64

user = {}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            user = models.User(email=email, hash_pass=password)
            db.session.add(user)
            db.session.commit()
            print('Registered')
            return redirect(url_for('login'))
        else:
            print('Email already registered!')
            return redirect(url_for('register'))
    return render_template('register.html', title='register')


@app.route('/login')
def login():
    return render_template('login.html', title='login')


@app.route('/home', methods=['POST'])
def home():
    email = request.form['email']
    password = request.form['password']
    if request.method == 'POST':
        user = models.User.query.filter_by(email=email).first()
        if user is None:
            print('Wrong email')
            return redirect(url_for('login'))
        else:
            if user.hash_pass == password:
                return render_template('home.html',title='home')
            else:
                print('Wrong password')
                return redirect(url_for('login'))