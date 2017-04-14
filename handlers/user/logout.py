from helpers import Handler


class LogoutHandler(Handler):
    """Simple logout"""
    def get(self):
        """Logout the user, erasing the user_id cookie"""
        self.response.set_cookie('user_id', '')
        return self.redirect('/')
