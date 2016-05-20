from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    meta_keywords = models.CharField(max_length=200)
    meta_description = models.TextField()
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

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
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

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
                                    processors=[ResizeToFill(100, 50)],
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

    def __str__(self):
        return self.title