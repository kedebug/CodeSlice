#handlers.py
import tornado.web
from models import Post
from google.appengine.api import users
import forms

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = users.get_current_user()
        if user:
            user.is_admin = users.is_current_user_admin()
        return user

class NewPostHandler(BaseHandler):
    def get(self):
        if not (self.current_user and self.current_user.is_admin):
            return self.redirect(users.create_login_url(self.request.uri))
        form = forms.PostForm()
        self.render('new_post.html', form=form)
    
    def post(self):
        if not (self.current_user and self.current_user.is_admin):
            return self.redirect(users.create_login_url(self.request.uri))
        form = forms.PostForm(self)
        if form.validate():
            post = Post(title=form.title.data,
                        content=form.content.data,
                        author=self.current_user)
            post.put()
            return self.redirect('/')
        self.render('new_post.html', form=form)

class PostListHandler(tornado.web.RequestHandler):
    def get(self):
        posts = Post.all()
        self.render('list_posts.html', posts=posts)

