from webapp import views_auth
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^$', views_auth.webapp_login, name='login'),
                       url(r'^login/$', 'webapp.views_auth.webapp_login'),
                       url(r'^registration/new/$', views_auth.registration, name='registration'),
                       url(r'^logout/$', views_auth.webapp_logout, name='logout'),
                       url(r'^password_change/$', views_auth.password_change,
                           name='passwordChange'),
                       url(r'password_change_done/$', views_auth.password_change_done,
                           name="passwordChangeDone"),
                       )

