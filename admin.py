from flask import Blueprint, render_template, redirect, url_for, flash, request
from __init__ import db,User
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def adminpage():
    result = db.session.execute("SELECT * FROM user")
    response = [dict(row.items()) for row in result]
    return render_template('admin.html', users=response)


@admin.route('/deleteuser/<int:id>')
@login_required
def deleteuser(id):
    task_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except:
        flash('There was an issue with deleting that task')
    return redirect(url_for('admin.adminpage'))

@admin.route('/resetpass/<int:id>', methods=['POST','GET'])
@login_required
def resetpassword(id):
    if request.method == 'GET':
        return render_template('reset-pass.html')
    else:
        pass_to_update = User.query.get_or_404(id)
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if password != password2:
            flash('Pasword is not match')
            return redirect(request.url)
        pass_to_update.password = password
        try:
            db.session.commit()
            flash('Password has been updated!')
            return redirect(url_for('admin.adminpage'))
        except:
            flash('There was an issue with resetting that password')
            return redirect(url_for('admin.adminpage'))

@admin.route('/adduser', methods=['POST'])
@login_required
def adduser():
     # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    
    #check if password is not match 
    if password != password2:
        flash('Pasword is not match')
        return redirect(url_for('admin.adminpage'))
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    uname = User.query.filter_by(name=name).first()
    if user or uname: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User already exists')
        return redirect(url_for('admin.adminpage'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    flash('User has been added')
    return redirect(url_for('admin.adminpage'))

@admin.route('/api/user')
@login_required
def getuser():
    return {'data': [user.to_dict() for user in User.query]}