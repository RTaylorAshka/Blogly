
from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)
db.create_all()

@app.errorhandler(404)
def get_404_page(e):
    return render_template('error-404.html')

#
# USERS
#



@app.route('/')
def red_home():
    return redirect('/users')

# HOME
@app.route('/users')
def get_users():
    users = User.query.all()
    return render_template('user-list.html', users=users)

# USER PAGE
@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id).all()
    
    
    return render_template('user-page.html', user=user, posts=posts)

# USER NEW FORM
@app.route('/users/new')
def new_user_form():
    return render_template('user-form.html')

# POST NEW USER
@app.route('/users/new', methods=['POST'])
def save_new_user():
    fn = request.form["first_name"]
    ln = request.form["last_name"]
    img = request.form["image_url"]

    new_user = User(first_name=fn, last_name=ln, image_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

# USER EDIT FORM
@app.route('/users/<int:user_id>/edit')
def edit_user_interface(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)

# POST EDIT USER
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

# USER DELETE
@app.route('/users/<int:user_id>/delete')
def delete_user_action(user_id):
    

    User.query.filter_by(id=user_id).delete()
    
    db.session.commit()
    return redirect('/users')


# 
# POSTS
# 

# POST PAGE
@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post.html', post = post)

# POST NEW FORM
@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('post-form.html', user = user)

# POST NEW POST
@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def new_post_process(user_id):

    ti = request.form["title"]
    co = request.form["content"]
    

    post = Post(title = ti, content = co, user_id = user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

# POST EDIT FORM
@app.route('/posts/<int:post_id>/edit')
def post_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post-edit.html', post = post)

# POST POST EDIT
@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def update_post(post_id):
    ti = request.form["title"]
    co = request.form["content"]

    post = Post.query.get_or_404(post_id)
    post.title = ti
    post.content = co
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')

# DELETE POST
@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    user = post.user
    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    return redirect(f'/users/{user.id}')