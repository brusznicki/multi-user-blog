from helpers import Handler, user_logged_in


class LogoutHandler(Handler):
    """Simple logout"""

    @user_logged_in
    def get(self, user):
        """Logout the user, erasing the user_id cookie"""
        self.response.set_cookie("user_id", "")
        return self.redirect("/")
