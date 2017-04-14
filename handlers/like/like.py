import time
from helpers import Handler, user_owns_post, post_exists
from google.appengine.ext import db
from models.like import Like


class PostLikeHandler(Handler):
    """Handles adding / removing a like to a blog post"""
    @post_exists
    def post(self, post_id, post):
        """Create a post like assocation in db"""

        if post.author.key() == self.user.key():
            self.error(403)
            return self.redirect('/%s' % post_id)
        else:
            remove = self.request.get("remove")
            if remove:
                for like in post.likes.filter('user =', self.user):
                    db.delete(like)
                    time.sleep(0.2)  # wait for db transaction
            else:
                like = Like(post=post, user=self.user)
                like.put()
                time.sleep(0.2)  # wait for db transaction to finish
            return self.redirect("/%s" % post_id)
