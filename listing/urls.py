from django.conf.urls import url
from listing import views

urlpatterns = [
    url(r'^$', views.index, name='listing'),
    url(r'^home$', views.home, name='home'),
    url(r'^fetchHourly$', views.fetchHourly, name='fetchHourly'),
    url(r'^fetchMoonbbs$', views.fetchMoonbbs, name='fetchMoonbbs'),
    url(r'^fetchChineseInSFBay$', views.fetchChineseInSFBay, name='fetchChineseInSFBay'),
]
