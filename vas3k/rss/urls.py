from django.conf.urls import patterns, url
from rss.feeds import FullFeed, BlogFeed, GalleryFeed, CommentFeed

urlpatterns = patterns('rss.views',
    url(r'^$', FullFeed(), name='rss.full'),
    url(r'^blog/$', BlogFeed(), name='rss.blog'),
    url(r'^gallery/$', GalleryFeed(), name='rss.gallery'),
    url(r'^comments/$', CommentFeed(), name='rss.comments'),
)
