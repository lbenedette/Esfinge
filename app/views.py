from flask import Flask, render_template, request, redirect, url_for
from app import app

user = {}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        print(data)
        if data['email'] in user.keys():
            print('Email already registered!')
            return redirect(url_for('index'))
        else:
            user[data['email']] = data['password']
            print(user)
            return redirect(url_for('login'))
    return render_template('register.html', title='register')


@app.route('/login')
def login():
    return render_template('login.html', title='login')


@app.route('/home', methods=['POST'])
def home():
    email = request.form['email']
    password = request.form['password']
    print(user)
    if request.method == 'POST':
        try:
            if user[email] == password:
                return render_template('home.html', title='home')
            else:
                print('Wrong password')
                return redirect(url_for('index'))
        except KeyError:
            print("Email don't exist")
            return redirect(url_for('index'))
