#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 16:19:49 2022

@author: ben
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), unique=True)
    def __repr__(self):
        return '<User %r>' % self.email
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'pass': self.password,
            'name': self.name,
        }

class Contact(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True, unique=True)
    group_name = db.Column(db.String(1000))
    chat_id = db.Column(db.String(1000), unique=True)
    app_name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    label_id = db.Column(db.Integer)
    
class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer)
    label_id = db.Column(db.Integer)
    
class Labels(db.Model):
    label_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), unique=True)


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'what-do-you-want?'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # blueprint for admin parts of app
    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    db.create_all(app=create_app())
    app.run(host='0.0.0.0',port=5002, debug=True)