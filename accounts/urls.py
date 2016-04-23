from django.conf.urls import url
from accounts import views

urlpatterns = [
        url(r'^signup/$', views.signup),
        url(r'^logout/$',views.logout),
        url(r'^login/$', views.test),
        url(r'^manage/$',views.manage),
]

