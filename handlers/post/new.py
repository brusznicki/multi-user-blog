from models import Post
from helpers import Handler, user_logged_in


class PostNewHandler(Handler):
    """Create a new post via POST"""

    @user_logged_in
    def get(self):
        """Gets and displays the create form"""
        return self.render('post-new.html')

    @user_logged_in
    def post(self):
        """Attempt to post the form data to server"""
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(subject=subject,
                        content=content,
                        author=self.user)
            post.put()
            return self.redirect("/%s" % post.key().id())
        else:

            error = "subject and content, please!"
            return self.render("newpost.html",
                               subject=subject,
                               content=content,
                               error=error)
