import time
from helpers import Handler, post_exists
from models.comment import Comment


class CommentNewHandler(Handler):
    """Create a new comment for a blog post"""

    @post_exists
    def post(self, post_id, post):
        """Create a comment if the user is logged in."""
        if not self.user:
            return self.redirect('/login')
        content = self.request.get('comment-content')
        if content:
            c = Comment(author=self.user,
                        content=content,
                        post=post)
            c.put()
            time.sleep(0.2)  # wait for db transaction
        return self.redirect('/%s' % post.key().id())
