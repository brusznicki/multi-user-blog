from google.appengine.ext import db
from user import User

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    """Blog Post entity"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    modified = db.DateTimeProperty(auto_now_add=True, required=True)
    author = db.ReferenceProperty(User, collection_name="posts")