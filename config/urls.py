from django.conf.urls import patterns, include, url

from django.contrib import admin
from config import views
from chat.models import ChatRoom

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.test),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^chat/',include('chat.urls')),
    url(r'^chatInfo/',include('chat.staticUrls') ),
]
