from google.appengine.ext import db
from user import User
from post import Post

class Comment(db.Model):
    """Simple Comment Entity relating users, posts, and a comment"""
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True, required=True)
    author = db.ReferenceProperty(User, collection_name="comments")
    post = db.ReferenceProperty(Post, collection_name="comments")
