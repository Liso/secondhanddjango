from django.conf.urls import url
from listing import views

urlpatterns = [
    url(r'^fetcher$', views.fetcher, name='fetcher'),
]
