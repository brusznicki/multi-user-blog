import time
from helpers import Handler, comment_exists, user_owns_comment


class CommentEditHandler(Handler):
    """Handles editing of a comment"""

    @comment_exists
    @user_owns_comment
    def get(self, comment_id, comment, user):
        """Check permissions and display post edit form."""
        post = comment.post
        content = comment.content
        return self.render("comment-edit.html",
                           content=content,
                           post=post)

    @comment_exists
    @user_owns_comment
    def post(self, comment_id, comment, user):
        """Check permissions and display post edit form."""
        have_error = False
        post = comment.post
        content = self.request.get('content')
        params = dict(content=content,
                      post=post,
                      user=self.user)

        if content and comment.content != content:
            comment.content = content
            comment.put()
            time.sleep(0.2)  # wait for db transaction
            return self.redirect('/%s' % post.key().id())
        else:
            have_error = True
            params['error'] = "Please update your comment or cancel"
        if not content:
            have_error = True
            params['error'] = "Comment can't be blank"
        if have_error:
            return self.render("comment-edit.html", **params)
