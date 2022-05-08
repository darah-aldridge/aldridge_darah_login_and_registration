from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
        }
    user_id = User.save(data)
    print(user_id)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user = User.get_by_email(data)
    if not user:
        flash(u"Invalid Email/Password", 'login error')
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(u"Invalid Email/Password", 'login error')
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    return redirect('/dashboard')

@app.route('/dashboard')
def show():
    return render_template("dashboard.html")

@app.route('/log-out')
def clear():
    session.clear()
    return redirect('/')

