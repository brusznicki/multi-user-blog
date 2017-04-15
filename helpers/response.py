import jinja2
import os
import webapp2
import auth

from models import User
template_dir = os.path.join(os.getcwd(), 'templates/')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


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
        secure_val = auth.make_secure_val(value)
        self.response.set_cookie(name, secure_val)

    def read_secure_cookie(self, cookie_name):
        """Decrypt secure cookie and return its value."""
        cookie_val = self.request.cookies.get(cookie_name)
        if cookie_val:
            return auth.check_secure_val(cookie_val)

    def login(self, user):
        """Set a secure cookie with the user's id."""
        user_id = user.key().id()
        self.set_secure_cookie('user_id', str(user_id))

    def initialize(self, *a, **kw):
        """Invoked everytime app loads. If a user, assign to self.user"""
        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.read_secure_cookie('user_id')
        self.user = user_id and User.get_by_id(int(user_id))
