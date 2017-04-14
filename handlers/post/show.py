from helpers import Handler, post_exists


class PostShowHandler(Handler):
    """Get and show a specific post"""

    @post_exists
    def get(self, post_id, post):
        """Display the post show page."""
        # if self.user:
        #     self.write('user is %s' % self.user.key().id())
        # self.write('post_id is %s' % post_id)
        # self.write('post key is %s' % post.key().id())
        # comments = post.comments
        # for comment in comments:
        #     self.write("%s" % comment.content)
        if not post:
            self.error(404)
            return self.redirect("/")
        params = dict(post=post)
        if self.user:
            params['user'] = self.user
            params['liked'] = post.likes.filter('user =', self.user).get()

        params['comments'] = post.comments.order('-created')
        return self.render('post-show.html', **params)
