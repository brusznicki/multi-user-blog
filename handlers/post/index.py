from helpers import Handler
from models.post import Post


class BlogIndexHandler(Handler):
    """Show Handler for posts"""
    def get(self):
        """Show 10 posts."""
        posts = Post.all().order('-created').run(limit=10)
        return self.render('post-index.html',
                           posts=posts,
                           user=self.user)
