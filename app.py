"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)
db.create_all()


@app.route('/')
def red_home():
    return redirect('/users')


@app.route('/users')
def get_users():
    users = User.query.all()
    return render_template('user-list.html', users=users)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-page.html', user=user)


@app.route('/users/new')
def new_user_form():
    return render_template('user-form.html')


@app.route('/users/new', methods=['POST'])
def save_new_user():
    fn = request.form["first_name"]
    ln = request.form["last_name"]
    img = request.form["image_url"]

    new_user = User(first_name=fn, last_name=ln, image_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/edit')
def edit_user_interface(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_action(user_id):
    fn = request.form["first_name"]
    ln = request.form["last_name"]
    img = request.form["image_url"]

    user = User.query.get(user_id)
    user.first_name = fn
    user.last_name = ln
    user.image_url = img
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')


# with app.app_context():
#     db.create_all()
# with app.app_context():
#     db.session.add(timmy)
#     db.session.commit()
