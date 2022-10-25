from datetime import datetime
from flask import Flask
from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib.pymongo import ModelView
from flask_simplelogin import login_required
from wtforms import form, fields, validators
from blog.database import mongo
from blog.posts import slugify
from mistune import markdown


# decorate Flask-Admin view via Monkey Patching
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
ModelView._handle_view = login_required(ModelView._handle_view)


class PostsForm(form.Form):
    title = fields.StringField("Title", [validators.data_required()])
    slug = fields.HiddenField("Slug")
    content = fields.TextAreaField("Content")
    published = fields.BooleanField("Published", default=True)

class AdminPosts(ModelView):
    column_list = ("title", "slug", "content", "published")
    form = PostsForm

    def on_model_change(self, form, post, is_created):
        post["slug"] = slugify(post["title"])
        #TODO: verificar se um post com mesmo slug já existe
        post["content"] = markdown(post["content"])
        if is_created:
            post["date"] = datetime.now()
        


def configure(app: Flask):
    admin = Admin(
        app,
        name=app.config.get("TITLE"),
        template_mode="bootstrap4"
    )
    admin.add_view(AdminPosts(mongo.db.posts, "Post"))








