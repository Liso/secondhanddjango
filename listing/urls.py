from django.conf.urls import url
from listing import views

urlpatterns = [
    url(r'^fetchMoonbbs$', views.fetcher, name='fetchMoonbbs'),
    url(r'^fetchChineseInSFBay$', views.fetcher, name='fetchChineseInSFBay'),
]
