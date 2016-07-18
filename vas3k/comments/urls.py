from django.conf.urls import patterns, url

urlpatterns = patterns("comments.views",
    url(r"^send/$", "send"),
    url(r"^ip/(?P<ip>.+?)/$", "ip")
)
