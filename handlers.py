import tornado.web
from models import Post

class PostListHandler(tornado.web.RequestHandler):
    def get(self):
        posts = Post.all()
        self.render('list_posts.html', posts=posts)

