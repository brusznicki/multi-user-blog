from helpers import Handler
from models import User


class LoginHandler(Handler):
    """Authorizes and logs in the user"""
    def get(self):
        """Display the login form"""
        if self.user:
            self.error(403)
            return self.redirect("/")
        return self.render("login-form.html")

    def post(self):
        """Login the user, setting a secure cookie "user_id"."""
        if self.user:
            self.error(403)
            return self.redirect("/")
        username = self.request.get("username")
        password = self.request.get("password")
        u = User.login(username, password)
        if u:
            self.login(u)
            return self.redirect("/")
        else:
            error = "Invalid Credentials"
            return self.render("login-form.html",
                               error=error,
                               username=username)
