from django.conf.urls import patterns, url
from webapp import views_user

urlpatterns = patterns('',
                       url(r'^index/$', views_user.user_home, name='user_home')
                       )