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
    created_at = db.Column(db.DateTime,
                           default = datetime.now()
                           )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id')
                        )
    
    user = db.relationship('User', backref = 'posts')
    


