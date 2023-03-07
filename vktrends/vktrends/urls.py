from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from trendsfinder.views import *
from vktrends import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trendsfinder.urls')),
]

handler404 = page_not_found


if not settings.DEBUG:
    urlpatterns.append(re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}))