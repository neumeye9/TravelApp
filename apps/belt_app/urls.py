from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^addtrip$', views.addtrip),
    url(r'^create$', views.create),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^join/(?P<trip_id>\d+)$', views.join)
]