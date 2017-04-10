import os
import hashlib
import hmac
import jinja2
import re
import random

import time
import webapp2

from google.appengine.ext import db
from models import Comment, Like, Post, User
from string import letters

# configure jinja2 template engine
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# User Controllers
SECRET = "jYXhfUnFGIR0ujKdWqm6"


def valid_username(username):
    """Confirm username is valid."""
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)


def valid_password(password):
    """Confirm password is valid."""
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    return PASSWORD_RE.match(password)


def valid_email(email):
    """Confirm email is valid or not present."""
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return not email or EMAIL_RE.match(email)


def make_salt(length=5):
    """Create a random salt."""
    return ''.join(random.choice(letters) for x in range(length))


def make_pw_hash(username, password, salt=None):
    """Hash password."""
    salt = salt or make_salt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (salt, h)


def make_secure_val(value):
    """Create a secure value"""
    return '%s|%s' % (value, hmac.new(SECRET, value).hexdigest())


def check_secure_val(secure_value):
    """Confirm the cookie value matches its hash, if so, return the value."""
    value = secure_value.split('|')[0]
    if secure_value == make_secure_val(value):
        return value


def fetch_post_from_path(post_id):
    key = db.Key.from_path('Post', int(post_id))
    post = db.get(key)
    return post


# Webapp2 Application Controller


class Handler(webapp2.RequestHandler):
    """ Main controller for drawing the application in the browser """
    def write(self, *a, **kw):
        """Write to the browser"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Get jinja template, invoke render"""
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        """Render the Jinja template"""
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, value):
        """Set a secure cookie given a name and value."""
        secure_val = make_secure_val(value)
        self.response.set_cookie(name, secure_val)

    def read_secure_cookie(self, cookie_name):
        """Decrypt secure cookie and return its value."""
        cookie_val = self.request.cookies.get(cookie_name)
        if cookie_val:
            return check_secure_val(cookie_val)

    def login(self, user):
        """Set a secure cookie with the user's id."""
        user_id = user.key().id()
        self.set_secure_cookie('user_id', str(user_id))

    def initialize(self, *a, **kw):
        """Invoked everytime app loads. If a user, assign to self.user"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.read_secure_cookie('user_id')
        self.user = user_id and User.get_by_id(int(user_id))

# Blog Post controllers


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


def users_key(group='default'):
    return db.Key.from_path('users', group)


class PostIndex(Handler):
    """Show Handler for posts"""
    def get(self):
        """Show 10 posts."""
        posts = Post.all().order('-created').run(limit=10)
        self.render('post-index.html',
                    posts=posts,
                    user=self.user)


class PostNew(Handler):
    """Create a new post via POST"""
    def get(self):
        """Gets and displays the create form"""
        if not self.user:
            return self.redirect('/login')

        self.render('post-new.html')

    def post(self):
        """Attempt to post the form data to server"""
        if not self.user:
            return self.redirect('/login')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(subject=subject,
                     content=content,
                     author=self.user)
            p.put()
            self.redirect("/%s" % p.key().id())
        else:

            error = "subject and content, please!"
            self.render("newpost.html",
                        subject=subject,
                        content=content,
                        error=error)


class PostShow(Handler):
    """Get and show a specific post"""
    def get(self, post_id):
        """Display the post show page."""
        post = fetch_post_from_path(post_id)
        like_count = 0
        comments = ""
        user_can_edit = user_can_delete = False
        user_can_like = True
        params = dict(comments=comments,
                      like_count=like_count,
                      post=post,
                      user=self.user,
                      user_can_delete=user_can_delete,
                      user_can_edit=user_can_edit,
                      user_can_like=user_can_like)
        if not post:
            self.error(404)
            self.redirect('/')
        author = post.author
        if author.key().id() == self.user.key().id():
            params['user_can_edit'] = True
            params['user_can_delete'] = True
            params['user_can_like'] = False
        if post.likes.filter('user =', self.user).count() > 0:
            params['already_liked_this'] = True
        params['like_count'] = post.likes.count()
        params['comments'] = post.comments.order('-created')
        self.render('post-show.html', **params)


class PostDelete(Handler):
    """Handles delete requests"""
    def post(self, post_id):
        """Check permissions and delete post."""
        if not self.user:
            return self.redirect('/login')
        post = fetch_post_from_path(post_id)
        if self.user.key() == post.author.key():
            post.delete()
            time.sleep(0.2)  # let Database do its thing
            self.redirect('/')
        else:
            self.redirect('/%s' % post.key().id())


class PostEdit(Handler):
    """Handles editing of a post"""
    def get(self, post_id):
        """Check permissions and display post edit form."""
        if not self.user:
            self.redirect('/login')
        # confirm that the user is the post author
        post = fetch_post_from_path(post_id)
        params = dict(subject=post.subject,
                      content=post.content,
                      post_id=post_id)

        if self.user.key() == post.author.key():
            self.render('post-edit.html', **params)
        else:
            self.redirect('%s' % post_id)

    def post(self, post_id):
        """Save the edited post."""
        have_error = False
        if not self.user:
            return self.redirect('/login')

        post = fetch_post_from_path(post_id)
        if not post:
            self.error(404)
            self.redirect("/")
        else:
            subject = self.request.get('subject')
            content = self.request.get('content')
            params = dict(subject=subject,
                          content=content,
                          post_id=post_id,
                          subject_error="",
                          content_error="",
                          error_msg="",
                          user=self.user)

            if not subject:
                have_error = True
                params['subject_error'] = "Subject is required"
            if not content:
                have_error = True
                params['content_error'] = "Subject is required"

            if have_error:
                params['error_msg'] = "Please correct the errors on this page"
                self.render("post-edit.html", **params)
            else:
                post.content = content
                post.subject = subject
                post.put()
                self.redirect('/%s' % post.key().id())


class PostLike(Handler):
    """Handles adding a like to a blog post"""
    def post(self, post_id):
        """Create like."""
        if not self.user:
            return self.redirect('/login')
        key = db.Key.from_path('Post', int(post_id))
        p = db.get(key)
        author = p.author
        remove = self.request.get("remove")
        if self.user.key() == author.key():
            self.write("you can't like your own post")
            self.redirect("/%s" % p.key().id())
        post_likes = p.likes
        post_likes_by_user = post_likes.filter('user =', self.user)
        if post_likes_by_user.count() > 0:
            if remove:
                for like in post_likes_by_user:
                    db.delete(like)
                time.sleep(0.2)

            self.redirect("/%s" % p.key().id())
        else:
            l = Like(post=p, user=self.user)
            l.put()
            time.sleep(0.2)
            self.redirect("/%s" % p.key().id())


class PostCommentNew(Handler):
    """Create a new comment for a blog post"""
    def get(self, post_id):
        # check if logged in and get username.

        if not self.user:
            self.redirect('/login')
        else:
            self.render('new-comment.html', post_id=post_id)

    def post(self, post_id):
        """Create a comment if the user is logged in."""
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if not post:
            self.error(404)
            return
        if not self.user:
            return self.redirect('/login')
        content = self.request.get('comment-content')
        if content:
            # create the comment
            c = Comment(author=self.user,
                        content=content,
                        post=post)
            c.put()
            time.sleep(0.2)  # rest for db job to finish
            return self.redirect('/%s' % post.key().id())


class CommentEdit(Handler):
    """Handles editing of a comment"""
    def get(self, comment_id):
        """Check permissions and display post edit form."""
        if not self.user:
            self.redirect('/login')
        # confirm that the user is the comment author
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)
        post = comment.post
        content = comment.content
        if comment.author.key() != self.user.key():
            self.redirect('/%s' % post.key().id())
        else:
            self.render("comment-edit.html",
                        content=content,
                        post=post)

    def post(self, comment_id):
        """Check permissions and display post edit form."""
        have_error = False
        if not self.user:
            self.redirect('/login')
        # confirm that the user is the comment author
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)

        if comment.author.key() != self.user.key():
            self.redirect('/%s' % comment.post.key().id())

        post = comment.post
        content = self.request.get('content')
        params = dict(content=content,
                      post=post,
                      user=self.user)

        if content and comment.content != content:
            comment.content = content
            comment.put()
            time.sleep(0.2)
            self.redirect('/%s' % post.key().id())
        else:
            have_error = True
            params['error'] = "Please update your comment or cancel"
        if not content:
            have_error = True
            params['error'] = "Comment can't be blank"
        if have_error:
            self.render("comment-edit.html", **params)


class CommentDelete(Handler):
    """Handles comment delete requests"""
    def post(self, comment_id):
        """Check permissions and delete post."""
        if not self.user:
            return self.redirect('/login')
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)
        post = comment.post
        if self.user.key() == comment.author.key():
            comment.delete()
            time.sleep(0.2)  # let Database do its thing
        self.redirect('/%s' % post.key().id())


class Signup(Handler):
    """Handles sign up flow for the user"""
    def get(self):
        """Display the signup form."""
        self.render('signup-form.html')

    def post(self):
        """Create the user if info is valid, then log them in."""
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username, email=email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That's not a valid password."
            have_error = True

        if verify != password:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        u = User.by_name(username)
        if u:
            params['error_username'] = 'That user already exists.'
            have_error = True

        if have_error:
            self.render('signup-form.html', **params)

        else:
            pw_hash = make_pw_hash(username, password)
            u = User(username=username,
                     pw_hash=pw_hash,
                     email=email)
            u.put()
            self.login(u)
            self.redirect('/')


class Login(Handler):
    """Authorizes and logs in the user"""
    def get(self):
        """Display the login form"""
        self.render('login-form.html')

    def post(self):
        """Login the user, setting a secure cookie 'user_id'."""
        username = self.request.get('username')
        password = self.request.get('password')
        u = User.login(username, password)

        if u:

            self.login(u)
            self.redirect('/')
        else:
            error = 'Invalid Credentials'
            self.render('login-form.html', error=error, username=username)


class Logout(Handler):
    """Simple logout"""
    def get(self):
        """Logout the user, erasing the user_id cookie"""
        self.response.set_cookie('user_id', '')
        self.redirect('/login')


# routes
routes = [
           ('/', PostIndex),
           ('/newpost', PostNew),
           ('/(\d+)', PostShow),
           ('/(\d+)/delete', PostDelete),
           ('/comment/(\d+)/delete', CommentDelete),
           ('/(\d+)/edit', PostEdit),
           ('/(\d+)/like?', PostLike),
           ('/(\d+)/comment', PostCommentNew),
           ('/comment/(\d+)', CommentEdit),
           ('/signup', Signup),
           ('/login', Login),
           ('/logout', Logout),
         ]

app = webapp2.WSGIApplication(routes=routes, debug=True)