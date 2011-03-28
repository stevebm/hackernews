from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<article_id>\d+)/$', 'articles.views.detail'),
    ('', 'articles.views.index'),
    # Example:
    # (r'^hackernews/', include('hackernews.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
