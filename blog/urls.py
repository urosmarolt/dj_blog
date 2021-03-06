from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed
from .views import RedirectPlay



urlpatterns = [
    url(r'^search/$', views.post_search, name='post_search'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
    url(r'^(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^$', views.review_list, name='review_list'),
    #url(r'^(?P<post>[-\w\d]+)', views.post_detail, name='post_detail'),

    url(r'^games/(?P<game>[-\w]+)/$', views.game_detail, name='game_detail'),
    url(r'^reviews/(?P<review>[-\w]+)/$', views.review_detail, name='review_detail'),
    url(r'^play/(?P<review>[-\w]+)/$', RedirectPlay.as_view(url=None), name='play_redirect'),
    #url(r'^$', views.post_detail, name='post_detail'),
]

