from functools import wraps
from google.appengine.ext import db


def user_logged_in(function):
    """checks whether user is logged in"""
    @wraps(function)
    def wrapper(self):
        if not self.user:
            self.error(403)
            return self.redirect("/")
        else:
            return function(self)
    return wrapper


def user_owns_comment(function):
    """Check that user owns comment"""
    @wraps(function)
    def wrapper(self, comment_id, comment):
        if not comment:
            self.error(404)
            if self.request.referer:
                self.redirect(self.request.referer)
            else:
                self.redirect("/")
            return
        else:
            if self.user.key() == comment.author.key():
                return function(self,
                                comment_id=comment_id,
                                comment=comment,
                                user=self.user)
            else:
                self.error(403)
                return self.redirect("/%s" % comment.post.key().id())

    return wrapper


def user_owns_post(function):
    """Check that post exists and return error 403 if user owns post"""
    @wraps(function)
    def wrapper(self, post_id, post):
        if not post:
            self.error(404)
            if self.request.referer:
                self.redirect(self.request.referer)
            else:
                self.redirect("/")
            return
        else:
            if self.user.key() == post.author.key():
                return function(self,
                                post_id=post_id,
                                post=post,
                                user=self.user)
            else:
                self.error(403)
                return self.redirect("/%s" % post_id)

    return wrapper


def comment_exists(function):
    @wraps(function)
    def wrapper(self, comment_id):
        key = db.Key.from_path("Comment", int(comment_id))
        comment = db.get(key)
        if comment:
            return function(self,
                            comment_id=comment_id,
                            comment=comment)
        else:
            self.error(404)
            return
    return wrapper


def post_exists(function):
    @wraps(function)
    def wrapper(self, post_id):
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        if post:
            return function(self,
                            post_id=post_id,
                            post=post)
        else:
            self.error(404)
            return
    return wrapper
