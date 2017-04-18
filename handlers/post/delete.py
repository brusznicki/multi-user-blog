import time
from helpers import Handler, post_exists, user_logged_in, user_owns_post


class PostDeleteHandler(Handler):
    """Handles delete requests"""

    @user_logged_in
    @post_exists
    @user_owns_post
    def post(self, post_id, post=None, user=None):
        """Check permissions and delete post."""
        likes = post.likes  # get likes associated with post
        comments = post.comments  # get comments associated with post
        for comment in comments:
            comment.delete()  # delete the comments
        for like in likes:
            like.delete()  # delete the likes
        post.delete()  # finally, delete the post
        time.sleep(0.2)  # wait for db transaction
        return self.redirect("/")
