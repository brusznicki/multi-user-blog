from helpers import Handler, post_exists


class PostShowHandler(Handler):
    """Get and show a specific post"""

    @post_exists
    def get(self, post_id, post):
        """Display the post show page."""
        params = dict(post=post)
        if self.user:
            params["user"] = self.user
            params["liked"] = post.likes.filter("user =", self.user).get()

        params["comments"] = post.comments.order("-created")
        return self.render("post-show.html", **params)
