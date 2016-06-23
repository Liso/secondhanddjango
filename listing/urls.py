from django.conf.urls import url
from listing import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^fetchMoonbbs$', views.fetchMoonbbs, name='fetchMoonbbs'),
    url(r'^fetchChineseInSFBay$', views.fetchChineseInSFBay, name='fetchChineseInSFBay'),
]
