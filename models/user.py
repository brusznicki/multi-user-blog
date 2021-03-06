import hashlib
import random

from google.appengine.ext import db
from string import letters


def users_key(group='default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    """User Entity"""
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, username):
        u = User.all().filter('username =', username).get()
        return u

    @classmethod
    def register(cls, username, pw, email=None):
        pw_hash = make_pw_hash(username, pw)
        return User(parent=users_key(),
                    username=username,
                    pw_hash=pw_hash,
                    email=email)

    @classmethod
    def login(cls, username, pw):
        u = cls.by_name(username)
        if u and confirm_pw(username, pw, u.pw_hash):
            return u

# private


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def confirm_pw(username, pw, pw_hash):
    """Verify a password for a given user."""
    salt = pw_hash.split(',')[0]
    return make_pw_hash(username, pw, salt) == pw_hash


def make_pw_hash(username, password, salt=None):
    """Hash password."""
    salt = salt or make_salt()
    pw_hash = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (salt, pw_hash)


def make_salt(length=5):
    """Create a random salt."""
    return ''.join(random.choice(letters) for x in range(length))
