from __future__ import annotations
from datetime import datetime
import unicodedata
import pymongo
from blog.database import mongo


# Fuções utiltárias
def slugify(title: str):
    slug = title.replace(" ", "-").replace("_", "-").lower()
    slug = unicodedata.normalize("NFD", slug)
    slug = slug.encode("ascii", "ignore")
    slug = slug.decode("utf-8")
    return slug
    


def get_all_posts(published: bool = True):
    posts = mongo.db.posts.find({"published": published})
    return posts.sort("date", pymongo.DESCENDING )

def get_post_by_slug(slug: str) -> dict:
    posts = mongo.db.posts.find_one({"slug": slug})
    return posts

def update_post_by_slug(slug: str, data: dict) -> dict:
    # TODO: Se o título mudar, atualizar o slug (falhar se já existir)
    return mongo.db.posts.find_one_and_update({"slug": slug}, {"$set": data})

def new_post(title: str, content: str, published: bool = True):
    slug = slugify(title)
    if list(mongo.db.posts.find({"title": title})) != []:
        return None
          
    new = mongo.db.posts.insert_one(
        {
            "title": title,
            "content": content,
            "published": published,
            "slug": slug,
            "date": datetime.now(),
            
        }
    )
    return slug
