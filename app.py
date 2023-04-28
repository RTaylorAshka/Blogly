
from flask import Flask, request, render_template, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, Tag, PostTag, collapse_tags, collapse_post, collapse_user

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
    users_list = User.query.order_by(User.first_name)
    new_posts = Post.query.order_by(Post.created_at).limit(5)
    


    return render_template('homepage.html', users=users_list, featured = new_posts)

# USER PAGE
@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user_id).all()
    bg = f"https://picsum.photos/id/{user_id + 10}/2000/300?blur=1"
    
    
    return render_template('user-page.html', user=user, posts=posts, bg = bg)

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
    
    user = User.query.get_or_404(user_id)

    collapse_user(user)

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
    tags = Tag.query.all()
    return render_template('post-form.html', user = user, tags = tags)

# POST NEW POST
@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def new_post_process(user_id):

    ti = request.form["title"]
    co = request.form["content"]
    

    post = Post(title = ti, content = co, user_id = user_id)
    db.session.add(post)

    tags = request.form.getlist("tag")
    for tag in tags:
        tag = Tag.query.get_or_404(int(tag))
        post.tags.append(tag)
    
    db.session.commit()
    return redirect(f'/users/{user_id}')

# POST EDIT FORM
@app.route('/posts/<int:post_id>/edit')
def post_edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post-edit.html', post = post, tags = tags)

# POST POST EDIT
@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def update_post(post_id):
    ti = request.form["title"]
    co = request.form["content"]

    post = Post.query.get_or_404(post_id)
    post.title = ti
    post.content = co

    db.session.add(post)

    tags = request.form.getlist("tag")
    for tag in tags:
        tag = Tag.query.get_or_404(int(tag))
        post.tags.append(tag)


    db.session.commit()

    return redirect(f'/posts/{post_id}')

# DELETE POST
@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    
    collapse_post(post)

    return redirect(f'/users/{user.id}')


#
# TAGS
#

# GET ALL TAGS
@app.route('/tags')
def get_all_tags():
    tags = Tag.query.all()

    return render_template('tags.html', tags = tags)

# TAG POSTS
@app.route('/tags/<int:tag_id>')
def get_tag_posts(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('tag-info.html', tag = tag)

# TAG FORM
@app.route('/tags/new')
def get_tag_form():
    return render_template('tags-new.html')

# POST TAG
@app.route('/tags/new', methods = ['POST'])
def post_new_tag():
    tag_name = request.form['tag_name']
    tag = Tag(tag_name = tag_name)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


# EDIT TAG
@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags-edit.html', tag = tag)



# POST EDIT TAG
@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def post_edit_tag(tag_id):
    new_name = request.form['tag_name']
    tag = Tag.query.get_or_404(tag_id)

    tag.tag_name = new_name
    db.session.commit()

    return redirect('/tags')

# DELETE TAG
@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    collapse_tags(tag)

    return redirect('/tags')
