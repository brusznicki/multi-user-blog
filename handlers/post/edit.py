import time
from helpers import Handler, post_exists, user_owns_post


class PostEditHandler(Handler):
    """Handles editing of a post"""

    @post_exists
    @user_owns_post
    def get(self, post_id, post, user):
        """Check permissions and display post edit form."""
        params = dict(subject=post.subject,
                      content=post.content,
                      post_id=post_id)
        return self.render("post-edit.html", **params)

    @post_exists
    @user_owns_post
    def post(self, post_id, post, user):
        """Save the edited post."""
        have_error = False
        subject = self.request.get("subject")
        content = self.request.get("content")
        params = dict(subject=subject,
                      content=content,
                      post_id=post_id,
                      subject_error="",
                      content_error="",
                      error_msg="",
                      user=user)
        if not subject:
            have_error = True
            params["subject_error"] = "Subject is required"
        if not content:
            have_error = True
            params["content_error"] = "Subject is required"

        if have_error:
            params["error_msg"] = "Please correct the errors on this page"
            return self.render("post-edit.html", **params)
        else:
            post.content = content
            post.subject = subject
            post.put()
            time.sleep(0.2)
            return self.redirect("/%s" % post.key().id())
