import os
import jinja2
import webapp2

from handlers.user import LoginHandler, LogoutHandler, RegisterHandler
from handlers.post import BlogIndexHandler, PostDeleteHandler, \
                          PostEditHandler, PostNewHandler, PostShowHandler
from handlers.like import PostLikeHandler
from handlers.comment import CommentDeleteHandler, CommentEditHandler, \
                             CommentNewHandler

# configure jinja2 template engine
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


routes = [
           ('/', BlogIndexHandler),
           ('/newpost', PostNewHandler),
           ('/(\d+)', PostShowHandler),
           ('/(\d+)/delete', PostDeleteHandler),
           ('/comment/(\d+)/delete', CommentDeleteHandler),
           ('/(\d+)/edit', PostEditHandler),
           ('/(\d+)/like', PostLikeHandler),
           ('/(\d+)/comment', CommentNewHandler),
           ('/comment/(\d+)', CommentEditHandler),
           ('/signup', RegisterHandler),
           ('/login', LoginHandler),
           ('/logout', LogoutHandler),
         ]

app = webapp2.WSGIApplication(routes=routes, debug=True)
