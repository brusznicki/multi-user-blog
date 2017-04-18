from functools import wraps
from google.appengine.ext import db


def user_logged_in(function):
    """checks whether user is logged in"""
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if not self.user:
            self.error(403)
            return self.redirect("/")
        else:
            kwargs["user"] = self.user
            return function(self, *args, **kwargs)
    return wrapper


def user_owns_comment(function):
    """Check that user owns comment"""
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        comment = kwargs["comment"]
        user = kwargs["user"]
        if not comment:
            self.error(404)
            if self.request.referer:
                self.redirect(self.request.referer)
            else:
                self.redirect("/")
            return
        else:
            if user.key() == comment.author.key():
                return function(self, *args, **kwargs)
            else:
                self.error(403)
                return self.redirect("/%s" % comment.post.key().id())

    return wrapper


def user_owns_post(function):
    """Check that post exists and return error 403 if user owns post"""
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        post = kwargs['post']
        post_id = post.key().id()
        if not post:
            self.error(404)
            if self.request.referer:
                self.redirect(self.request.referer)
            else:
                self.redirect("/")
            return
        else:
            if self.user.key() == post.author.key():
                kwargs["user"] = self.user
                return function(self, *args, **kwargs)
            else:
                self.error(403)
                return self.redirect("/%s" % post_id)

    return wrapper


def comment_exists(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        comment_id = args[0]
        key = db.Key.from_path("Comment", int(comment_id))
        comment = db.get(key)
        if comment:
            kwargs['comment'] = comment
            return function(self, *args, **kwargs)
        else:
            self.error(404)
            return
    return wrapper


def post_exists(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        post_id = args[0]
        key = db.Key.from_path("Post", int(post_id))
        post = db.get(key)
        if post:
            kwargs['post'] = post
            return function(self, *args, **kwargs)
        else:
            self.error(404)
            return
    return wrapper
