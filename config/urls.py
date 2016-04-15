from django.conf.urls import patterns, include, url

from django.contrib import admin
from config import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.test),
]
