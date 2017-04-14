import time
from helpers import Handler, user_owns_post, post_exists


class PostDeleteHandler(Handler):
    """Handles delete requests"""

    @post_exists
    @user_owns_post
    def post(self, post_id, post=None, user=None):
        """Check permissions and delete post."""
        likes = post.likes
        for like in likes:
            like.delete()
        comments = post.comments
        for comment in comments:
            comment.delete()
        post.delete()
        time.sleep(0.2)  # wait for db transaction
        self.redirect('/')
