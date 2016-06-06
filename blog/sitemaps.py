from django.contrib.sitemaps import Sitemap
from .models import Post, Review

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish

class ReviewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Review.published.all()

    def lastmod(self, obj):
        return obj.publish