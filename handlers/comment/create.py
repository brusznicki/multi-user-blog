import time
from helpers import Handler, post_exists, user_logged_in
from models.comment import Comment


class CommentNewHandler(Handler):
    """Create a new comment for a blog post"""

    @user_logged_in
    @post_exists
    def post(self, post_id, post, user):
        """Create a comment if the user is logged in."""
        content = self.request.get("comment-content")
        if content:
            c = Comment(author=self.user,
                        content=content,
                        post=post)
            c.put()
            time.sleep(0.2)  # wait for db transaction
        return self.redirect("/%s" % post.key().id())
