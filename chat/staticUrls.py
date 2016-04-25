from django.conf.urls import url
from chat import views

urlpatterns = [
        url(r'^update/$', views.updateChat),
        url(r'^sendMessage/$', views.sendMessage),
        url(r'^sendUser/$', views.sendUser),
]
