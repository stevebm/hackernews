from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings

urlpatterns = patterns('',
    ('^$', 'articles.views.index'),
    (r'^new_articles/$', 'articles.views.new_articles'),
    (r'^page_articles/$', 'articles.views.page_articles'),
    (r'^scripts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
