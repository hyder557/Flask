# app/login/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from app import db
from .forms import LoginForm, RegistrationForm
from .models import User
from flask import session

main = Blueprint('main', __name__)

# 定义路由和视图函数
@main.route('/')
def index():
    form = LoginForm()
    return render_template('login.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect('http://localhost:4200/welcome')
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            new_user = User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('Username already exists', 'error')
    return render_template('register.html', form=form)