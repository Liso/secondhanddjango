from django.conf.urls import url
from customers import views

urlpatterns = [
    url(r'^register$', views.registerView, name='register'),
    url(r'^login$', views.loginView, name='login'),
]
