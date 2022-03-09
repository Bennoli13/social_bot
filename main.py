from flask import Blueprint, render_template, redirect, url_for, flash, request
from __init__ import db,User,Contact
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return redirect(url_for('admin.adminpage'))

@main.route('/contactlist')
@login_required
def contactlist():
    result = db.session.execute("SELECT * FROM contact")
    response = [dict(row.items()) for row in result]
    return render_template('contactlist.html', contacts=response)

@main.route('/contactlist', methods=['POST'])
@login_required
def add_contactlist():
    cust_id = request.form.get('cust_id')
    group_name = request.form.get('group_name')
    chat_id = request.form.get('chat_id')
    app_name = request.form.get('app_name')
    email = request.form.get('email')
    
    check_cust_id = Contact.query.filter_by(cust_id=cust_id).first() 
    check_chat_id = Contact.query.filter_by(chat_id=chat_id).first() 
    
    if check_chat_id or check_cust_id:
        flash('Contact already exists')
        return redirect(url_for('main.contactlist'))
    
    new_contact = Contact(cust_id=cust_id, group_name=group_name, chat_id=chat_id,app_name=app_name,email=email )
    db.session.add(new_contact)
    db.session.commit()
    
    flash('Contact has been added')
    return redirect(url_for('main.contactlist'))


@main.route('/deletecontact/<int:id>')
@login_required
def del_contactlist(id):
    task_to_delete = Contact.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
    except:
        flash('There was an issue with deleting that task')
    return redirect(url_for('main.contactlist'))