from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'stories.views.index', name='index'),
    url(r'^rss/', include("rss.urls")),
    url(r'^comments/', include("comments.urls")),
    url(r'^(?P<story_type>.+?)/(?P<story_slug>.+?)/', "stories.views.story_show", name="story_show"),
    url(r'^(?P<story_type>.+?)/', "stories.views.story_list", name="story_list"),
)
