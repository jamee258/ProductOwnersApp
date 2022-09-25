import os
import re
from flask import Flask, render_template, url_for, redirect, flash, request, current_app as app
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms import ApplicationForm, EditApplicationForm, LoginForm

from passlib.hash import sha256_crypt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

from models import User as UserTable, Application as ApplicationTable, db

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in before proceeding"

@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))

def create_app(config):
    app.config.from_object(config)
    return app

@app.route("/")
@login_required
def home():

    apps = ApplicationTable.query.all()

    isAdmin = False
    # For checking if current user is admin
    if current_user.is_admin == True:
        isAdmin = True

    user = UserTable.query.filter_by(id=current_user.id).first()
    if(user.comments == None):
        user.comments = ""

    allUsersWithComments = UserTable.query.filter(UserTable.comments!=None, UserTable.comments!="", UserTable.id!=user.id).all()

    return render_template("home.html", applications=apps, isAdmin=isAdmin, currentUser=user, allComments=allUsersWithComments)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = UserTable.query.filter_by(username=form.username.data).first()
        if user:
            # Check if details are valid
            password_input = form.password.data
            if sha256_crypt.verify(password_input, user.password):
                login_user(user)
                flash("You have successfully logged in")
                return redirect(url_for('home'))
            else:
                flash("Incorrect username and/or password combination")
        else:
            flash("Incorrect username and/or password combination")
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    print(current_user.is_authenticated)
    flash("You have successfully logged out")
    return redirect(url_for('login'))

@app.route('/createApp/', methods=('GET', 'POST'))
@login_required
def create():
    if current_user.is_admin == False:
        flash("You do not have the permissions to access this page")
        return redirect(url_for('home'))
    name = None
    form = ApplicationForm()
    users = UserTable.query.all()
    apps = ApplicationTable.query.filter(ApplicationTable.users == None).all()
    form.users.choices = users
    form.apps.choices = apps
    if form.validate_on_submit():

        selectedApplication = form.apps.data
        selectedUsers = form.users.data

        retrievedApplication = ApplicationTable.query.filter_by(name=selectedApplication).first()
        for user in selectedUsers:
            retrievedUser = UserTable.query.filter_by(first_name=user).first()
            retrievedApplication.users.append(retrievedUser)

        db.session.commit()

        return redirect(url_for('home'))
    return render_template('createApplication.html', form=form)

@app.route('/updateApp/<int:id>', methods = ['GET', 'POST'])
@login_required
def update(id):
    if current_user.is_admin == False:
        flash("You do not have the permissions to access this page")
        return redirect(url_for('home'))

    users = UserTable.query.all()
    selectedApp = ApplicationTable.query.filter_by(id=id).first()

    form = EditApplicationForm()

    form.users.choices = users
    form.app.data = selectedApp.name
    form.current_product_owners.data = selectedApp.users
    return render_template('editApplication.html', application=selectedApp, form=form)

@app.route('/editApp/', methods = ['POST'])
@login_required
def edit():
    if current_user.is_admin == False:
        flash("You do not have the permissions to perform this action")
        return redirect(url_for('home'))

    form = EditApplicationForm()
    selectedApp = ApplicationTable.query.filter_by(name=form.app.data).first()
    selectedApp.users = []
    db.session.commit()
    selectedUsers = form.users.data
    for user in selectedUsers:
        retrievedUser = UserTable.query.filter_by(first_name=user).first()
        selectedApp.users.append(retrievedUser)
    db.session.commit()

    flash("Product Owners updated successfully")

    return redirect(url_for('home'))

@app.route("/deleteApp/<int:id>")
@login_required
def delete(id):
    if current_user.is_admin == False:
        flash("You do not have the permissions to perform this action")
        return redirect(url_for('home'))

    selectedApp = ApplicationTable.query.filter_by(id=id).first()
    db.session.delete(selectedApp)
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/editComment", methods = ['POST'])
@login_required
def editComment():
    user = UserTable.query.filter_by(id=current_user.id).first()
    commentInput = request.form['userComments']
    regex = re.compile('[@_#$%^&*()<>?/\|}{~:]')
    if(regex.search(commentInput) != None):
        flash("Comment update was unsuccessful. Only alphanumeric and some special characters are allowed")
        return redirect(url_for('home'))
    else:
        user.comments = commentInput
        db.session.commit()
        flash("Your comments have been updated successfully")
        return redirect(url_for('home'))

@app.route("/deleteComment", methods = ['POST'])
@login_required
def deleteComment():
    userID = request.form['commentUserID']
    user = UserTable.query.filter_by(id=userID).first()
    user.comments = ""
    db.session.commit()

    flash("You have successfully deleted the comment")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
