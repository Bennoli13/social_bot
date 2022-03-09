from contextlib import redirect_stderr
from flask import Blueprint, render_template, request,redirect, url_for, flash
from __init__ import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

#This is to generate the admin user in the first time
@auth.route('/default')
def create_admin():
    user = User.query.filter_by(name="admin").first()
    if user: # check if admin already exist
        flash('admin already exist')
        return redirect(url_for('auth.login')) 
    #set default admin
    admin = User(email="admin@example.com", name="admin", password=generate_password_hash("admin", method='sha256'))
    flash('default admin has been created')
     # add the new user to the database
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('auth.login')) 
        
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(name=name).first()
    
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    
     # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


    