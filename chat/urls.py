from django.conf.urls import url
from chat import views

urlpatterns = [
        url(r'(?P<title>[-\w]+)',views.accessChat),
]
