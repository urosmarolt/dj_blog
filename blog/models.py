from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from taggit.managers import TaggableManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from meta.models import ModelMeta


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(ModelMeta, models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
    )
    POST_TYPE = (
        ('post', 'Post'),
        ('page', 'Page'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    meta_keywords = models.TextField()
    meta_description = models.TextField()
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    post_type = models.CharField(max_length=10, choices=POST_TYPE, default='post')
    tags = TaggableManager()

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    _metadata = {
        'title': 'title',
        'description': 'meta_description',
        'keywords': 'get_meta_keywords',
        'author': 'author',
    }

    def get_meta_keywords(self):
        return self.meta_keywords.split(",")

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.slug])

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

class Review(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='review_posts')
    featured = models.BooleanField(default=False)
    slider = models.IntegerField()
    meta_keywords = models.CharField(max_length=200, default="Meta Keywords")
    meta_description = models.TextField(default="Meta Description")
    tracking_link = models.CharField(max_length=250)
    review_text = models.TextField(default="Review text")
    general_info = models.TextField(default="General info")
    ratings = models.IntegerField(default=10)
    payment_methods = models.TextField(default="Payment methods")
    image = models.ImageField(upload_to='blog/static/uploads', default='blog/static/uploads/douche1.jpg')
    review_banner = models.ImageField(upload_to='blog/static/uploads', default='blog/static/uploads/review_banner.jpg')
    thumbnail = ProcessedImageField(upload_to='static/thumbnails',
                                    processors=[ResizeToFill(50, 20)],
                                    format='JPEG',
                                    options={'quality': 60},
                                    default='blog/static/thumbnails/douche1.jpg'
                                    )
    exclusive_bonus = models.TextField(default="Exclusive bonus")
    match_bonus = models.TextField(default="Match bonus")
    freespins = models.TextField(default="Freespins")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    _metadata = {
        'title': 'title',
        'description': 'meta_description',
        'keywords': 'meta_keywords',
        'author': 'author',
    }

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:review_detail',
                       args=[self.slug])
    @classmethod
    def get_review(cls, review_page):
        object_list = cls.published.all()
        paginator = Paginator(object_list, 6)  #
        try:
            reviews = paginator.page(review_page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            reviews = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            reviews = paginator.page(paginator.num_pages)
        return reviews

    def __str__(self):
        return self.title

class Game(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='games_posts')
    meta_keywords = models.CharField(max_length=200, default="Meta Keywords")
    meta_description = models.TextField(default="Meta Description")
    games_link = models.TextField(default="Games URL")
    games_text = models.TextField(default="Games text")
    image = models.ImageField(upload_to='blog/static/uploads', default='blog/static/uploads/douche1.jpg')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    _metadata = {
        'title': 'title',
        'description': 'meta_description',
        'keywords': 'meta_keywords',
        'author': 'author',
    }

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:game_detail',
                       args=[self.slug])

    def __str__(self):
        return self.title
