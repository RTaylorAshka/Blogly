"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    
    
    db.app = app
    db.init_app(app)


class User(db.Model):
    
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User_id = {u.id}, first_name = {u.first_name}, last_name = {u.last_name}, img_url = {u.image_url}>"
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String,
                           nullable = False,
                           )
    last_name = db.Column(db.String,
                           nullable = False,
                           )
    image_url = db.Column(db.String,
                           default = 'https://picsum.photos/200'
    )
    
    
    posts = db.relationship('Post', backref = 'user', cascade="all, delete-orphan")

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):

    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"post_id = {p.id}, title = {p.title}, created_at = {p.created_at}"
    
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String,
                      nullable = False
                      )
    content = db.Column(db.String,
                        nullable = False)
    created_at = db.Column(db.String,
                           default = datetime.now().strftime("%-m/%-d/%Y at %-H:%M %p")
                           )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id')
                        )
    
    
   
    




class Tag(db.Model):

        __tablename__ = 'tags'

        id = db.Column(db.Integer,
                       primary_key = True,
                       autoincrement = True
                       )
        tag_name = db.Column(db.String,
                             nullable = False
                             )
        
        posts = db.relationship('Post', secondary = 'post_tags', backref = 'tags', cascade ='all, delete')
        
        
    
    
        

class PostTag(db.Model):

        __tablename__ = 'post_tags'
        
        tag_id = db.Column(db.Integer, 
                        db.ForeignKey('tags.id'),
                        primary_key = True
                        )
        
        post_id = db.Column(db.Integer, 
                        db.ForeignKey('posts.id'),
                        primary_key = True
                        )

        
    

def collapse_tags(tag):

    for post in tag.posts:
        PostTag.query.filter_by(tag_id = tag.id, post_id = post.id).delete()

    db.session.commit()

    Tag.query.filter_by(id=tag.id).delete()
    
    db.session.commit()



def collapse_post(post):
     
    for tag in post.tags:
        PostTag.query.filter_by(tag_id = tag.id, post_id = post.id).delete()

    Post.query.filter_by(id = post.id).delete()

    db.session.commit()


def collapse_user(user):
     
    for post in user.posts:
        collapse_post(post)

    
    User.query.filter_by(id=user.id).delete()

    db.session.commit()
     