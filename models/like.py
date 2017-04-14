from google.appengine.ext import db
from user import User
from post import Post

class Like(db.Model):
    """Simple Like Entity relating users and posts"""
    post = db.ReferenceProperty(Post, collection_name="likes")
    user = db.ReferenceProperty(User, collection_name="likes")
