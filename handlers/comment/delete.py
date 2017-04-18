import time
from helpers import Handler, comment_exists, user_logged_in, user_owns_comment


class CommentDeleteHandler(Handler):
    """Handles comment delete requests"""

    @user_logged_in
    @comment_exists
    @user_owns_comment
    def post(self, comment_id, comment, user):
        """Check permissions and delete post."""
        post_id = comment.post.key().id()  # get post id for redirect
        comment.delete()
        time.sleep(0.2)  # wait for db transaction
        return self.redirect("/%s" % post_id)
