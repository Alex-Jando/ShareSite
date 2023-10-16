from flask import Blueprint, redirect, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'GET':

        return render_template('login.html', current_user = current_user)
    
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()

        if not user:
            flash('Email does not exist!')
            return redirect(url_for('auth.login'))
        
        if not check_password_hash(user.password, password):
            flash('Incorrect password!')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember = True)

        return redirect(url_for('views.index'))

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():

    if request.method == 'GET':
        
        return render_template('signup.html', current_user = current_user)

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('confirm-password')

        if password != password_confirm:
            flash('Passwords do not match!')
            return redirect(url_for('auth.signup'))
        
        if '@' not in email or '.' not in email or len(email) < 6:
            flash('Invalid email!')
            return redirect(url_for('auth.signup'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters!')
            return redirect(url_for('auth.signup'))
        
        if User.query.filter_by(email = email).first():
            flash('Email already exists!')
            return redirect(url_for('auth.signup'))
        
        new_user = User(email = email, password = generate_password_hash(password, method = 'scrypt'))

        db.session.add(new_user)

        db.session.commit()

        login_user(new_user, remember = True)

        flash('Account created!')

        return redirect(url_for('views.index'))

@auth.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('auth.login'))