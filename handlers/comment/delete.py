import time
from helpers import Handler, comment_exists, user_owns_comment


class CommentDeleteHandler(Handler):
    """Handles comment delete requests"""

    @comment_exists
    @user_owns_comment
    def post(self, comment_id, comment, user):
        """Check permissions and delete post."""
        post_id = comment.post.key().id()
        comment.delete()
        time.sleep(0.2)  # wait for db transaction
        return self.redirect('/%s' % post_id)
