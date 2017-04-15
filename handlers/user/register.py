from helpers import Handler
from helpers import auth

from models import User


class RegisterHandler(Handler):
    """Handles sign up flow for the user"""
    def get(self):
        """Display the signup form."""
        if self.user:
            self.error(403)  # they already have an account.
            return self.redirect("/")
        return self.render("signup-form.html")

    def post(self):
        """Create the user if info is valid, then log them in."""
        if self.user:
            self.error(403)  # they already have an account.
            return self.redirect("/")
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username, email=email)

        if not auth.valid_username(username):
            params["error_username"] = "That's not a valid username."
            have_error = True

        if not auth.valid_password(password):
            params["error_password"] = "That's not a valid password."
            have_error = True

        if verify != password:
            params["error_verify"] = "Your passwords didn't match."
            have_error = True

        if not auth.valid_email(email):
            params["error_email"] = "That's not a valid email."
            have_error = True

        u = User.by_name(username)
        if u:
            params["error_username"] = "That user already exists."
            have_error = True

        if have_error:
            return self.render("signup-form.html", **params)

        else:
            pw_hash = auth.make_pw_hash(username, password)
            u = User(username=username,
                     pw_hash=pw_hash,
                     email=email)
            u.put()
            self.login(u)
            return self.redirect("/")
